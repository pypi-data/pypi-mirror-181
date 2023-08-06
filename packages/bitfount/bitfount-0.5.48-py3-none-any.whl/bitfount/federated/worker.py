"""Workers for handling task running on pods."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from sqlite3 import Connection
from typing import Any, List, Optional, Sequence, cast

import numpy as np
import pandas as pd
import sqlvalidator

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.exceptions import DataStructureError
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithm,
    _BaseModelAlgorithmFactory,
)
from bitfount.federated.authorisation_checkers import _AuthorisationChecker
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.monitoring.monitor import task_config_update
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseProtocolFactory,
)
from bitfount.federated.protocols.model_protocols.federated_averaging import (
    FederatedAveraging,
)
from bitfount.federated.transport.message_service import _BitfountMessageType
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import (
    SerializedAlgorithm,
    SerializedProtocol,
    _DataLessAlgorithm,
)
from bitfount.federated.utils import _PROTOCOLS
from bitfount.hub.api import BitfountHub
from bitfount.schemas.utils import bf_load
from bitfount.types import _JSONDict

logger = _get_federated_logger(__name__)


class _Worker:
    """Client worker which runs a protocol locally.

    Args:
        datasource: BaseSource object.
        mailbox: Relevant mailbox.
        bitfounthub: BitfountHub object.
        authorisation: AuthorisationChecker object.
        pod_identifier: Identifier of the pod the Worker is running in.
        serialized_protocol: SerializedProtocol dictionary that the Pod has received
            from the Modeller.
        pod_vitals: PodVitals object.
        pod_dp: DPPodConfig object.
    """

    def __init__(
        self,
        datasource: BaseSource,
        mailbox: _WorkerMailbox,
        bitfounthub: BitfountHub,
        authorisation: _AuthorisationChecker,
        pod_identifier: str,
        serialized_protocol: SerializedProtocol,
        pod_vitals: Optional[_PodVitals] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_db: bool = False,
        show_datapoints_in_results_db: bool = True,
        **_kwargs: Any,
    ):
        self.datasource = datasource
        self.mailbox = mailbox
        self.hub = bitfounthub
        self.authorisation = authorisation
        self.pod_identifier = pod_identifier
        self.serialized_protocol = serialized_protocol
        self.pod_vitals = pod_vitals
        self._pod_dp = pod_dp
        self._pod_db = pod_db
        self._show_datapoints_in_results_db = show_datapoints_in_results_db
        # Compute task hash on ordered json dictionary
        self._task_hash = (
            hashlib.sha256(
                json.dumps(serialized_protocol, sort_keys=True).encode("utf-8")
            ).hexdigest()
            if self._pod_db
            else None
        )

    async def run(self) -> None:
        """Calls relevant training procedure and sends back weights/results."""
        # Send task to Monitor service. This is done regardless of whether or not
        # the task is accepted. This method is being run in a task monitor context
        # manager so no need to set the task monitor prior to sending.
        task_config_update(dict(self.serialized_protocol))

        # Check authorisation with access manager
        authorisation_errors = await self.authorisation.check_authorisation()

        if authorisation_errors.messages:
            # Reject task, as there were errors
            await self.mailbox.reject_task(
                authorisation_errors.messages,
            )
            return

        # Accept task and inform modeller
        logger.info("Task accepted, informing modeller.")
        await self.mailbox.accept_task()
        # Wait for Modeller to give the green light to start the task
        await self.mailbox.get_task_start_update()

        # Update hub instance if BitfountModelReference
        algorithm = self.serialized_protocol["algorithm"]
        if not isinstance(self.serialized_protocol["algorithm"], list):
            algorithm = [cast(SerializedAlgorithm, algorithm)]

        algorithm = cast(List[SerializedAlgorithm], algorithm)
        for algo in algorithm:
            if model := algo.get("model"):
                if model["class_name"] == "BitfountModelReference":
                    logger.debug("Patching model reference hub.")
                    model["hub"] = self.hub

        # Deserialize protocol only after task has been accepted just to be safe
        protocol = cast(
            BaseProtocolFactory,
            bf_load(cast(_JSONDict, self.serialized_protocol), _PROTOCOLS),
        )
        # For FederatedAveraging, we return a dictionary of
        # validation metrics, which is incompatible with the database.
        if isinstance(protocol, FederatedAveraging):
            self._pod_db = False
        # Load data according to model datastructure if one exists.
        # For multi-algorithm protocols, we assume that all algorithm models have the
        # same datastructure.
        datastructure: Optional[DataStructure] = None
        algorithm_ = protocol.algorithm
        if not isinstance(algorithm_, Sequence):
            algorithm_ = [algorithm_]

        algorithm_ = cast(List[BaseCompatibleAlgoFactory], algorithm_)
        for algo_ in algorithm_:
            if isinstance(algo_, _BaseModelAlgorithmFactory):
                datastructure = algo_.model.datastructure

            if not isinstance(algo_, _DataLessAlgorithm):
                if self._pod_db:
                    # For now, use pod name.
                    # TODO: [BIT-2486] Update this to reflect the project id.
                    con = sqlite3.connect(
                        f'{self.mailbox.pod_identifier.split("/")[-1]}.db'
                    )
                    cur = con.cursor()
                    cur.execute(
                        f"""CREATE TABLE IF NOT EXISTS "{self._task_hash}" (rowID INTEGER PRIMARY KEY, 'datapoint_hash' VARCHAR, 'results' VARCHAR)"""  # noqa: B950
                    )
                    self._load_data_for_worker(datastructure=datastructure, con=con)
                    self._map_task_to_hash_add_to_db(con)
                else:
                    # We execute the query directly on the db connection,
                    # or load the data at runtime for a csv.
                    # TODO: [NO_TICKET: Reason] No ticket created yet. Add the private sql query algorithm here as well. # noqa: B950
                    self._load_data_for_worker(datastructure=datastructure)

        # Calling the `worker` method on the protocol also calls the `worker` method on
        # underlying objects such as the algorithm and aggregator. The algorithm
        # `worker` method will also download the model from the Hub if it is a
        # `BitfountModelReference`
        worker_protocol = protocol.worker(mailbox=self.mailbox, hub=self.hub)

        # If the algorithm is a model algorithm, then we need to pass the pod identifier
        # to the model so that it can extract the relevant information from the
        # datastructure the Modeller has sent. This must be done after the worker
        # protocol has been created, so that any model references have been converted
        # to models.
        for worker_algo in worker_protocol.algorithms:
            if isinstance(worker_algo, _BaseModelAlgorithm):
                worker_algo.model.set_pod_identifier(self.pod_identifier)
        # TODO: [BIT-2486] check if projectid is given and only pass
        #  connection in that case
        results = await worker_protocol.run(
            datasource=self.datasource,
            pod_dp=self._pod_dp,
            pod_vitals=self.pod_vitals,
            pod_identifier=self.mailbox.pod_identifier,
        )
        if self._pod_db:
            if isinstance(results, list):
                self._save_results_to_db(results, con)
                con.close()
            else:
                logger.info(
                    "Results cannot be saved to pod database."
                    "Results can be only saved to database if "
                    "they are returned from the algorithm as a list, "
                    f"whereas the chosen protocol returns {type(results)}."
                )

        logger.info("Task complete.")
        self.mailbox.delete_all_handlers(_BitfountMessageType.LOG_MESSAGE)

    def _load_data_for_worker(
        self,
        datastructure: Optional[DataStructure] = None,
        con: Optional[Connection] = None,
    ) -> None:
        """Load the data for the worker."""
        sql_query: Optional[str] = None
        table: Optional[str] = None
        kwargs = {}

        if datastructure:
            if datastructure.table:
                if isinstance(datastructure.table, dict):
                    if not (table := datastructure.table.get(self.pod_identifier)):
                        raise DataStructureError(
                            f"Table definition not found for {self.pod_identifier}. "
                            f"Table definitions provided in this DataStructure: "
                            f"{str(datastructure.table)}"
                        )
                    kwargs["table_name"] = table
                elif isinstance(datastructure.table, str):
                    kwargs["table_name"] = datastructure.table
            elif datastructure.query:
                if isinstance(datastructure.query, dict):
                    if not (sql_query := datastructure.query.get(self.pod_identifier)):
                        raise DataStructureError(
                            f"Query definition not found for {self.pod_identifier}. "
                            f"Query definitions provided in this DataStructure: "
                            f"{str(datastructure.query)}"
                        )
                elif isinstance(datastructure.query, str):
                    sql_query = datastructure.query
                if sql_query and sqlvalidator.parse(sql_query).is_valid():
                    if not isinstance(self.datasource, DatabaseSource):
                        raise ValueError(
                            "Incompatible DataStructure, data source pair. "
                            "DataStructure is expecting the data source to "
                            "be a DatabaseSource."
                        )
                    kwargs["sql_query"] = sql_query
        # This call loads the data for a multi-table BaseSource as specified by the
        # Modeller/DataStructure.
        self.datasource.load_data(**kwargs)
        if self._pod_db:
            self.load_new_records_only_for_task(cast(Connection, con))

    def load_new_records_only_for_task(self, con: Connection) -> None:
        # Ignoring the security warning because the sql query is trusted and
        # the task_hash is calculated at __init__.
        task_data = pd.read_sql(
            f'SELECT "datapoint_hash" FROM "{self._task_hash}"', con  # nosec
        )
        # check hash in from static datasource table -
        # - needs new sql connection(TODO: [BIT-2486])
        data = pd.read_sql('SELECT * FROM "datasource"', con)
        # set datasource_data for specific task to only run on new records.
        new_records = data[~data["datapoint_hash"].isin(task_data["datapoint_hash"])]
        self.datasource._ignore_cols.append("datapoint_hash")
        self.datasource._data = new_records

    def _map_task_to_hash_add_to_db(self, con: Connection) -> None:
        algorithm_ = self.serialized_protocol["algorithm"]
        if not isinstance(algorithm_, Sequence):
            algorithm_ = [algorithm_]
        for algorithm in algorithm_:
            if "model" in algorithm:
                algorithm["model"].pop("schema")
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS "task_definitions" ('index' INTEGER  PRIMARY KEY AUTOINCREMENT  NOT NULL, 'taskhash' TEXT,'protocol' TEXT,'algorithm' TEXT)"""  # noqa: B950
        )
        data = pd.read_sql("SELECT * FROM 'task_definitions' ", con)
        if self._task_hash not in data["taskhash"].unique():
            cur.execute(
                """INSERT INTO "task_definitions" ('taskhash',  'protocol', 'algorithm' ) VALUES (?,?,?);""",  # noqa: B950
                (
                    self._task_hash,
                    self.serialized_protocol["class_name"],
                    str(algorithm_),
                ),
            )
        con.commit()

    def _save_results_to_db(self, results: List[np.ndarray], con: Connection) -> None:
        # TODO: [BIT-2486] change this to read from static pod
        #  database instead of the one with the project
        pod_data = pd.read_sql('SELECT * FROM "datasource"', con)
        # We only care about the test data since we don't log
        # anything in the database for validation or training data
        run_data = self.datasource.data.iloc[self.datasource._test_idxs]
        # convert results to string
        results_as_str = [str(item) for item in results]
        run_data["results"] = results_as_str
        columns = list(pod_data.columns)
        columns.remove("rowID")
        columns.remove("datapoint_hash")
        # get the datapoint hashes from the pod db
        data_w_hash = pd.merge(
            pod_data,
            run_data,
            how="outer",
            left_on=columns,
            right_on=columns,
            indicator=True,
        ).loc[lambda x: x["_merge"] == "both"]
        # drop the indicator and index columns
        data_w_hash.drop("_merge", inplace=True, axis=1)
        if "rowID" in data_w_hash.columns:
            data_w_hash.drop("rowID", inplace=True, axis=1)
        data_w_hash.drop_duplicates(inplace=True, keep="last")
        cur = con.cursor()
        # Ignoring the security warning because the sql query is trusted and
        # the task_hash is calculated at __init__.
        task_data = pd.read_sql(
            f'SELECT "datapoint_hash" FROM "{self._task_hash}"', con  # nosec
        )
        # If this is the first time the task is run, it will not
        # have all the columns, so we need to make sure they are
        # added. Otherwise, we don't need to worry about the columns
        # as any alterations to them will be classified as a new task
        if task_data.shape[0] == 0 and self._show_datapoints_in_results_db:
            for col in columns:
                cur.execute(
                    f"ALTER TABLE '{self._task_hash}' ADD COLUMN '{col}' {data_w_hash[col].dtype}"  # noqa: B950
                )

        # do merge and get new datapoints only
        new_task_datapoint = pd.merge(
            data_w_hash,
            task_data,
            how="left",
            indicator=True,
        ).loc[lambda x: x["_merge"] == "left_only"]
        if "rowId" in new_task_datapoint.columns:
            new_task_datapoint.drop("rowID", inplace=True, axis=1)
        # drop the indicator and index columns
        new_task_datapoint.drop("_merge", inplace=True, axis=1)
        logger.info(
            f"The task was run on {new_task_datapoint.shape[0]} "
            f"records from the datasource."
        )
        if self._show_datapoints_in_results_db:
            new_task_datapoint.to_sql(
                f"{self._task_hash}", con=con, if_exists="append", index=False
            )
        else:
            new_task_datapoint[["datapoint_hash", "results"]].to_sql(
                f"{self._task_hash}", con=con, if_exists="append", index=False
            )
