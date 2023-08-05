"""Tests for the authentication mechanism."""
from datetime import datetime, timezone
import functools
import json
from pathlib import Path
import re
from typing import Callable, Dict, Literal, Optional, Union, cast
from unittest.mock import Mock, PropertyMock, call

from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from dateutil.relativedelta import relativedelta
import jwt
import pytest
from pytest import fixture, raises
from pytest_lazyfixture import lazy_fixture
from pytest_mock import MockerFixture
import responses

from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _PRODUCTION_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
)
from bitfount.hub.authentication_flow import (
    _AUTHORIZATION_PENDING_ERROR,
    _DEFAULT_USERNAME,
    _DEVELOPMENT_AUTH_DOMAIN,
    _DEVELOPMENT_CLIENT_ID,
    _DEVICE_CODE_GRANT_TYPE,
    _PRODUCTION_AUTH_DOMAIN,
    _PRODUCTION_CLIENT_ID,
    _SLOW_DOWN_ERROR,
    _STAGING_AUTH_DOMAIN,
    _STAGING_CLIENT_ID,
    _USERNAME_KEY,
    BitfountSession,
    _AuthEnv,
    _get_auth_environment,
)
from bitfount.hub.exceptions import AuthenticatedUserError
from bitfount.hub.types import (
    APIKeys,
    _DeviceAccessTokenRequestDict,
    _DeviceAccessTokenResponseJSON,
    _DeviceCodeRequestDict,
    _DeviceCodeResponseJSON,
    _TokenRefreshRequestDict,
)
from bitfount.utils import web_utils
from tests.utils.helper import get_warning_logs, unit_test


@fixture
def username() -> str:
    """Username."""
    return "someUsername"


@fixture
def auth_domain() -> str:
    """Authentication domain as fixture."""
    return "some.auth.domain.com"


@fixture
def client_id() -> str:
    """Auth token client ID fixture."""
    return "oljorknkjnio"


@fixture
def scopes() -> str:
    """Auth token scopes fixture."""
    return "spaced out list of scopes"


@fixture
def audience() -> str:
    """Auth token audience fixture."""
    return "some.api.domain.com"


@fixture
def user_storage_path(tmp_path: Path, username: str) -> Path:
    """Temporary directory to act as user's .bitfount directory."""
    user_storage_path = tmp_path / username
    user_storage_path.mkdir()
    return user_storage_path


@fixture
def token_file(user_storage_path: Path) -> Path:
    """Path to save/load tokens from."""
    return user_storage_path / ".token"


@fixture
def bitfount_session_factory(
    audience: str,
    auth_domain: str,
    client_id: str,
    scopes: str,
    user_storage_path: Path,
    username: str,
) -> Callable[[], BitfountSession]:
    """Factory to create and setup BitfountSession instance for tests."""

    def _factory() -> BitfountSession:
        session = BitfountSession(auth_domain, client_id, username, scopes, audience)
        session.user_storage_path = user_storage_path
        session.token_file = user_storage_path / ".token"
        return session

    return _factory


@fixture
def bitfount_session(
    bitfount_session_factory: Callable[[], BitfountSession]
) -> BitfountSession:
    """Bitfount session instance as fixture."""
    return bitfount_session_factory()


@fixture
def mock_webbrowser(mocker: MockerFixture) -> Mock:
    """Mock webbrowser import."""
    mock_webbrowser: Mock = mocker.patch(
        "bitfount.hub.authentication_flow.webbrowser", autospec=True
    )
    return mock_webbrowser


@fixture
def mock_time(mocker: MockerFixture) -> Mock:
    """Mock time import."""
    mock_time: Mock = mocker.patch(
        "bitfount.hub.authentication_flow.time", autospec=True
    )
    return mock_time


@fixture
def mock_datetime(mocker: MockerFixture) -> Mock:
    """Mock datetime import."""
    mock_datetime: Mock = mocker.patch(
        "bitfount.hub.authentication_flow.datetime", autospec=True
    )
    return mock_datetime


@unit_test
class TestBitfountSession:
    """Tests for the custom BitfountSession."""

    @fixture
    def device_code_request(
        self, audience: str, client_id: str, scopes: str
    ) -> _DeviceCodeRequestDict:
        """Expected request data for /oauth/device/code."""
        return {"audience": audience, "scope": scopes, "client_id": client_id}

    @fixture
    def device_code_response(self) -> _DeviceCodeResponseJSON:
        """Expected response from /oauth/device/code."""
        return {
            "device_code": "Ag_EE...ko1p",
            "user_code": "QTZL-MCBW",
            "verification_uri": "https://accounts.acmetest.org/activate",
            "verification_uri_complete": "https://accounts.acmetest.org"
            "/activate?user_code=QTZL-MCBW",
            "expires_in": 900,
            "interval": 5,
        }

    @fixture
    def device_code(self) -> str:
        """Device code."""
        return "someDeviceCode"

    @fixture
    def access_token(self) -> str:
        """Access token."""
        return "someAccessToken"

    @fixture
    def token_request(
        self, client_id: str, device_code: str
    ) -> _DeviceAccessTokenRequestDict:
        """Expected request data for /oauth/token."""
        return {
            "client_id": client_id,
            "grant_type": _DEVICE_CODE_GRANT_TYPE,
            "device_code": device_code,
        }

    @fixture
    def token_response(self) -> _DeviceAccessTokenResponseJSON:
        """Expected response data from /oauth/token."""
        return {
            "access_token": "eyJz93a...k4laUWw",
            "id_token": "eyJ...0NE",
            "refresh_token": "eyJ...MoQ",
            "scope": "...",
            "expires_in": 86400,
            "token_type": "Bearer",
        }

    @fixture
    def refresh_token(self) -> str:
        """Refresh token."""
        return "someRefreshToken"

    @fixture
    def token_refresh_request(
        self, client_id: str, refresh_token: str
    ) -> _TokenRefreshRequestDict:
        """Expected request data for refresh request to /oauth/token."""
        return {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

    @fixture
    def id_token_for_username(self, username: str) -> str:
        """The JWT ID token for username."""
        return jwt.encode({_USERNAME_KEY: username}, "Secret key", algorithm="HS256")

    @fixture
    def wrong_username(self) -> str:
        """An incorrect username to test validation logic with."""
        return "wrong_username"

    @fixture
    def id_token_for_wrong_username(self, wrong_username: str) -> str:
        """The JWT ID token for the wrong username."""
        return jwt.encode(
            {_USERNAME_KEY: wrong_username}, "Secret key", algorithm="HS256"
        )

    def test_api_keys_are_read_from_environment_variables(
        self,
        bitfount_session_factory: Callable[[], BitfountSession],
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Tests that the API keys are read from environment variables."""
        monkeypatch.setenv("BITFOUNT_API_KEY_ID", "someApiKeyId")
        monkeypatch.setenv("BITFOUNT_API_KEY", "someApiKey")
        # Ensure session creation is done post-envvar setting
        bitfount_session = bitfount_session_factory()
        api_keys = bitfount_session.api_keys
        assert isinstance(api_keys, APIKeys)
        assert api_keys.access_key_id == "someApiKeyId"
        assert api_keys.access_key == "someApiKey"

    def test_api_keys_are_cached(
        self,
        bitfount_session_factory: Callable[[], BitfountSession],
        monkeypatch: MonkeyPatch,
    ) -> None:
        """Tests that the API keys are cached."""
        monkeypatch.setenv("BITFOUNT_API_KEY_ID", "someApiKeyId")
        monkeypatch.setenv("BITFOUNT_API_KEY", "someApiKey")
        # Ensure session creation is done post-envvar setting
        bitfount_session = bitfount_session_factory()
        api_keys = bitfount_session.api_keys
        assert isinstance(api_keys, APIKeys)
        assert api_keys.access_key_id == "someApiKeyId"
        assert api_keys.access_key == "someApiKey"

        # Reset the API keys
        monkeypatch.setenv("BITFOUNT_API_KEY_ID", "someApiKeyId2")
        monkeypatch.setenv("BITFOUNT_API_KEY", "someApiKey2")

        # The API keys should be cached (i.e. same as they were before)
        assert api_keys.access_key_id == "someApiKeyId"
        assert api_keys.access_key == "someApiKey"

    def test_both_api_key_environment_variables_are_required(
        self, bitfount_session: BitfountSession, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests that both API key environment variables are required."""
        # We only set the `BITFOUNT_API_KEY_ID` environment variable.
        monkeypatch.setenv("BITFOUNT_API_KEY_ID", "someApiKeyId")
        assert bitfount_session.api_keys is None

    def test_api_keys_property_without_api_key_environment_variables(
        self, bitfount_session: BitfountSession
    ) -> None:
        """Tests that the API keys are None if no environment variables are set."""
        assert bitfount_session.api_keys is None

    def test_api_keys_and_default_username_raises_error(
        self,
        audience: str,
        auth_domain: str,
        client_id: str,
        monkeypatch: MonkeyPatch,
        scopes: str,
        user_storage_path: Path,
    ) -> None:
        """Tests that if using API keys username cannot be the default."""
        monkeypatch.setenv("BITFOUNT_API_KEY_ID", "someApiKeyId")
        monkeypatch.setenv("BITFOUNT_API_KEY", "someApiKey")
        # Ensure session creation is done post-envvar setting
        with pytest.raises(
            AuthenticatedUserError, match="Must specify a username when using API Keys."
        ):
            BitfountSession(
                auth_domain=auth_domain,
                client_id=client_id,
                scopes=scopes,
                audience=audience,
            )

    @pytest.mark.parametrize(
        argnames=("error_expected", "id_token"),
        argvalues=(
            pytest.param(
                True,
                lazy_fixture("id_token_for_wrong_username"),
                id="wrong_user_authenticated",
            ),
            pytest.param(
                False,
                lazy_fixture("id_token_for_username"),
                id="correct_user_authenticated",
            ),
        ),
    )
    def test_username_property_validates_username(
        self,
        bitfount_session: BitfountSession,
        error_expected: bool,
        id_token: str,
        username: str,
    ) -> None:
        """Test that authenticated user is validated when retrieving username."""
        bitfount_session._username = username
        bitfount_session.id_token = id_token

        if error_expected:
            with pytest.raises(AuthenticatedUserError):
                bitfount_session.username
        else:
            assert bitfount_session.username == username

    @pytest.mark.parametrize(
        "url, expected_output",
        [
            ("https://hub.bitfount.com", True),
            ("https://hub.bitfount.com/api/blah", True),
            ("https://hub.staging.bitfount.com", True),
            ("https://am.hub.bitfount.com", False),
            ("http://hub.bitfount.com", False),  # HTTP is not allowed
        ],
    )
    def test_is_hub_url(
        self, bitfount_session: BitfountSession, expected_output: bool, url: str
    ) -> None:
        """Tests that the is_hub_url method returns the expected output."""
        assert bitfount_session._is_hub_url(url) == expected_output

    @pytest.mark.parametrize(
        "url, expected_output",
        [
            ("https://am.hub.bitfount.com", True),
            ("https://am.hub.bitfount.com/api/blah", True),
            ("https://am.hub.staging.bitfount.com", True),
            ("https://hub.bitfount.com", False),
            ("http://am.hub.bitfount.com", False),  # HTTP is not allowed
        ],
    )
    def test_is_am_url(
        self, bitfount_session: BitfountSession, expected_output: bool, url: str
    ) -> None:
        """Tests that the is_am_url method returns the expected output."""
        assert bitfount_session._is_am_url(url) == expected_output

    def test_token_file_path(
        self,
        audience: str,
        auth_domain: str,
        client_id: str,
        scopes: str,
        username: str,
    ) -> None:
        """Tests that token file is in provided path."""
        session = BitfountSession(auth_domain, client_id, username, scopes, audience)
        # Token file is the path provided with the token file specified
        assert session.token_file == session.user_storage_path / ".token"

    def test_authenticate_with_api_keys(
        self, bitfount_session: BitfountSession, mocker: MockerFixture
    ) -> None:
        """Tests that the authenticate method simply returns if API Keys are present."""
        mock_api_keys = mocker.patch.object(
            BitfountSession,
            "api_keys",
            PropertyMock(return_value=APIKeys("keyID", "key")),
        )
        mock_load_token_from_file = mocker.patch.object(
            bitfount_session, "_load_token_from_file"
        )
        bitfount_session.authenticate()
        mock_api_keys.assert_called_once()
        # The method returns before it gets to the step of loading the token from file
        mock_load_token_from_file.assert_not_called()

    @responses.activate
    def test_fetch_device_code_stores_and_returns_required_values(
        self,
        auth_domain: str,
        bitfount_session: BitfountSession,
        device_code_request: _DeviceCodeRequestDict,
        device_code_response: _DeviceCodeResponseJSON,
    ) -> None:
        """Checks that the needed attributes are stored from device code."""
        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/device/code",
            json=device_code_response,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], device_code_request)
                )
            ],
        )

        user_code, verification_uri = bitfount_session._fetch_device_code()

        assert bitfount_session.device_code == device_code_response.get("device_code")
        assert bitfount_session.device_code_arrival_time is not None
        assert bitfount_session.device_code_expires_in == device_code_response.get(
            "expires_in"
        )
        assert bitfount_session.token_request_interval == device_code_response.get(
            "interval"
        )
        assert user_code == device_code_response["user_code"]
        assert verification_uri == device_code_response["verification_uri_complete"]

    def test_do_verification_opens_browser_correctly(
        self,
        bitfount_session: BitfountSession,
        mock_webbrowser: Mock,
    ) -> None:
        """Checks that request to open browser works."""
        bitfount_session._do_verification("hello", "world")
        mock_webbrowser.open.assert_called_once_with("world")

    @responses.activate
    def test_exchange_device_code_for_token_eventually_receives_tokens(
        self,
        auth_domain: str,
        bitfount_session: BitfountSession,
        device_code: str,
        mock_time: Mock,
        token_request: _DeviceAccessTokenRequestDict,
        token_response: _DeviceAccessTokenResponseJSON,
    ) -> None:
        """Checks that device code successfully exchanged for token."""
        bitfount_session.device_code = device_code
        bitfount_session.device_code_arrival_time = datetime.now(timezone.utc)
        bitfount_session.device_code_expires_in = 2
        bitfount_session.token_request_interval = 1

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json={"error": _AUTHORIZATION_PENDING_ERROR},
            status=400,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )
        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=token_response,
            status=200,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        bitfount_session._exchange_device_code_for_token()

        assert len(responses.calls) == 2
        assert bitfount_session._access_token == token_response["access_token"]
        assert bitfount_session.refresh_token == token_response["refresh_token"]
        assert bitfount_session.id_token == token_response["id_token"]

        assert bitfount_session.access_token_expires_at is not None
        assert bitfount_session.access_token_expires_at > datetime.now(timezone.utc)
        mock_time.sleep.assert_called_once_with(1)

    @responses.activate
    def test_exchange_device_code_for_token_eventually_receives_error(
        self,
        auth_domain: str,
        bitfount_session: BitfountSession,
        device_code: str,
        mock_time: Mock,
        token_request: _DeviceAccessTokenRequestDict,
    ) -> None:
        """The token endpoint here eventually informs us that the user denied access."""
        bitfount_session.device_code = device_code
        bitfount_session.device_code_arrival_time = datetime.now(timezone.utc)
        bitfount_session.device_code_expires_in = 2
        bitfount_session.token_request_interval = 1

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json={"error": _AUTHORIZATION_PENDING_ERROR},
            status=400,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )
        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json={"error": "access_denied"},
            status=400,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        with raises(ConnectionError):
            bitfount_session._exchange_device_code_for_token()

        assert len(responses.calls) == 2
        assert bitfount_session._access_token is None
        assert bitfount_session.refresh_token is None
        assert bitfount_session.id_token is None
        assert bitfount_session.access_token_expires_at is None
        assert all(map(lambda x: x == call(1), mock_time.sleep.call_args_list))

    @responses.activate
    def test_exchange_device_code_for_token_never_receives_tokens(
        self,
        auth_domain: str,
        bitfount_session: BitfountSession,
        device_code: str,
        mock_datetime: Mock,
        mock_time: Mock,
        token_request: _DeviceAccessTokenRequestDict,
    ) -> None:
        """The token endpoint here never issues tokens, so the device code expires."""
        bitfount_session.device_code = device_code
        bitfount_session.device_code_arrival_time = datetime(
            2020, 1, 14, tzinfo=timezone.utc
        )
        bitfount_session.device_code_expires_in = 300
        bitfount_session.token_request_interval = 1

        mock_datetime.now.side_effect = [
            datetime(2020, 1, 14, minute=x, tzinfo=timezone.utc)
            for x in range(0, 60, 2)
        ]

        auth_server_response = {"error": _AUTHORIZATION_PENDING_ERROR}

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=auth_server_response,
            status=400,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        with raises(ConnectionError):
            bitfount_session._exchange_device_code_for_token()

        assert len(responses.calls) == 3

        assert all(map(lambda x: x == call(1), mock_time.sleep.call_args_list))
        assert len(mock_time.sleep.call_args_list) == 3

        assert bitfount_session._access_token is None
        assert bitfount_session.refresh_token is None
        assert bitfount_session.id_token is None
        assert bitfount_session.access_token_expires_at is None

    @responses.activate
    def test_exchange_device_code_for_token_receives_slow_down(
        self,
        auth_domain: str,
        bitfount_session: BitfountSession,
        caplog: LogCaptureFixture,
        capsys: CaptureFixture,
        device_code: str,
        mock_time: Mock,
        token_request: _DeviceAccessTokenRequestDict,
        token_response: _DeviceAccessTokenResponseJSON,
    ) -> None:
        """Test interval increased if receive slow down response."""
        # Set relevant attributes on session
        bitfount_session.device_code = device_code
        bitfount_session.device_code_arrival_time = datetime.now(timezone.utc)
        bitfount_session.device_code_expires_in = 300
        bitfount_session.token_request_interval = 1

        # First and second responses are "slow down"
        for _ in range(2):
            responses.add(
                responses.POST,
                f"https://{auth_domain}/oauth/token",
                json={"error": _SLOW_DOWN_ERROR},
                status=400,
                match=[
                    responses.matchers.urlencoded_params_matcher(
                        cast(Dict[str, str], token_request)
                    )
                ],
            )
        # Final response is correct response
        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=token_response,
            status=200,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        bitfount_session._exchange_device_code_for_token()

        # Check warning logs for interval notes
        warning_logs = get_warning_logs(caplog)
        assert (
            "Polling too quickly; increasing interval from 1 to 2 seconds"
            in warning_logs
        )
        assert (
            "Polling too quickly; increasing interval from 2 to 3 seconds"
            in warning_logs
        )
        # Check stdout for increased interval waits
        stdout = capsys.readouterr().out
        assert (
            "Awaiting authentication in browser. Will check again in 1 seconds."
            not in stdout
        )
        assert (
            "Awaiting authentication in browser. Will check again in 2 seconds."
            in stdout
        )
        assert (
            "Awaiting authentication in browser. Will check again in 3 seconds."
            in stdout
        )

        # Check correct number of requests made
        assert len(responses.calls) == 3

        # Check sleep called with updated intervals
        assert mock_time.sleep.call_args_list == [call(2), call(3)]

    @pytest.mark.parametrize(
        argnames=("content_type", "content_value", "expected_error_msg", "in_stdout"),
        argvalues=(
            pytest.param(
                "json",
                {},
                'An unexpected error occurred: status code: 404; "{}"',
                True,
                id="incorrect json",
            ),
            pytest.param(
                "body",
                "error but not necessarily json",
                (
                    "Received 404 status response, but JSON is invalid: "
                    '"error but not necessarily json"'
                ),
                False,
                id="non-json response",
            ),
        ),
    )
    @responses.activate
    def test_exchange_device_code_for_token_receives_non_400_error(
        self,
        auth_domain: str,
        bitfount_session: BitfountSession,
        caplog: LogCaptureFixture,
        capsys: CaptureFixture,
        content_type: Literal["json", "body"],
        content_value: Union[dict, str],
        device_code: str,
        expected_error_msg: str,
        in_stdout: bool,
        mock_time: Mock,
        remove_web_retry_backoff_sleep: Optional[Mock],
        token_request: _DeviceAccessTokenRequestDict,
        token_response: _DeviceAccessTokenResponseJSON,
    ) -> None:
        """Test error raised if receive non-400 error response."""
        # Check retry backoff is patched
        assert remove_web_retry_backoff_sleep is not None

        # Set relevant attributes on session
        bitfount_session.device_code = device_code
        bitfount_session.device_code_arrival_time = datetime.now(timezone.utc)
        bitfount_session.device_code_expires_in = 300
        bitfount_session.token_request_interval = 1

        partial_response_add = functools.partial(
            responses.add,
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            status=404,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )
        if content_type == "json":
            partial_response_add(json=content_value)
        else:
            partial_response_add(body=content_value)

        with pytest.raises(
            ConnectionError,
            match="Failed to retrieve a device code from the authentication server",
        ):
            bitfount_session._exchange_device_code_for_token()

        # Check logger/stdout for errors
        assert expected_error_msg in caplog.text
        if in_stdout:
            assert expected_error_msg in capsys.readouterr().out

        # Check retries occurred
        assert (
            remove_web_retry_backoff_sleep.call_count == web_utils._DEFAULT_MAX_RETRIES
        )

    @responses.activate
    def test_bitfount_session_request_provides_token(
        self,
        access_token: str,
        bitfount_session: BitfountSession,
        device_code: str,
    ) -> None:
        """Checks that `request()` call provides token."""
        bitfount_session._access_token = access_token
        bitfount_session.device_code = device_code
        # Expires 1 month in future
        bitfount_session.access_token_expires_at = datetime.now(
            timezone.utc
        ) + relativedelta(months=1)

        api_url = "https://some.api.url/goes/here"

        responses.add(
            responses.POST,
            api_url,
        )

        # Send request
        bitfount_session.request("POST", api_url)

        # Check request had access token
        first_call: responses.Call = cast(responses.Call, responses.calls[0])
        assert first_call.request.headers["authorization"] == f"Bearer {access_token}"

    @responses.activate
    def test_bitfount_session_request_refreshes_expired_then_provides_token(
        self,
        access_token: str,
        auth_domain: str,
        bitfount_session: BitfountSession,
        device_code: str,
        id_token_for_username: str,
        mock_time: Mock,
        refresh_token: str,
        token_file: Path,
        token_refresh_request: _TokenRefreshRequestDict,
        token_response: _DeviceAccessTokenResponseJSON,
    ) -> None:
        """Checks that if token expired new one is provided and saved."""
        bitfount_session._access_token = access_token
        bitfount_session.device_code = device_code
        bitfount_session.refresh_token = refresh_token
        bitfount_session.id_token = id_token_for_username

        # Expire token
        bitfount_session.access_token_expires_at = datetime(
            2000, 1, 14, tzinfo=timezone.utc
        )
        bitfount_session.token_request_interval = 1

        api_url = "https://some.api.url/goes/here"

        # Set expected ID Token on response
        token_response["id_token"] = id_token_for_username

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            # Token refresh has same form as initial token response so we just reuse it
            json=token_response,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_refresh_request)
                )
            ],
        )

        responses.add(
            responses.POST,
            api_url,
        )

        # Send request
        bitfount_session.request("POST", api_url)

        # Check request had refreshed access token
        second_call: responses.Call = cast(responses.Call, responses.calls[1])
        assert (
            second_call.request.headers["authorization"]
            == f"Bearer {token_response['access_token']}"
        )

        # Check refreshed token was saved
        saved_token = json.load(token_file.open())
        assert saved_token["access_token"] == token_response["access_token"]
        assert saved_token["refresh_token"] == token_response["refresh_token"]
        assert saved_token["id_token"] == token_response["id_token"]
        assert datetime.fromtimestamp(
            saved_token["access_token_expires_at"], tz=timezone.utc
        ) > datetime.now(timezone.utc)

        # Check session metadata was saved
        assert saved_token["auth_domain"] == bitfount_session._auth_domain
        assert saved_token["client_id"] == bitfount_session._client_id
        assert saved_token["scopes"] == bitfount_session._scopes
        assert saved_token["audience"] == bitfount_session._audience

        mock_time.sleep.assert_not_called()

    @responses.activate
    def test_bitfount_session_request_forces_manual_login_when_refresh_fails(
        self,
        access_token: str,
        auth_domain: str,
        bitfount_session: BitfountSession,
        device_code: str,
        device_code_request: _DeviceCodeRequestDict,
        device_code_response: _DeviceCodeResponseJSON,
        id_token_for_username: str,
        mock_time: Mock,
        mock_webbrowser: Mock,
        refresh_token: str,
        scopes: str,
        token_refresh_request: _TokenRefreshRequestDict,
        token_request: _DeviceAccessTokenRequestDict,
        token_response: _DeviceAccessTokenResponseJSON,
    ) -> None:
        """Checks that the user is made to log in if the token refresh fails.

        Once they have logged in the web request is completed
        """
        bitfount_session._access_token = access_token
        bitfount_session.device_code = device_code
        bitfount_session.refresh_token = refresh_token
        bitfount_session.id_token = id_token_for_username

        # Expire token
        bitfount_session.access_token_expires_at = datetime(
            2000, 1, 14, tzinfo=timezone.utc
        )
        bitfount_session.token_request_interval = 1

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json={"error": "some error"},
            status=401,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_refresh_request)
                )
            ],
        )

        # Set new device code on /oauth/device/code response and expected request
        # against /oauth/token
        new_device_code = "newDeviceCode"
        device_code_response["device_code"] = new_device_code
        token_request["device_code"] = new_device_code

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/device/code",
            json=device_code_response,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], device_code_request)
                )
            ],
        )

        # Set ID Token on token response
        token_response["id_token"] = id_token_for_username

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=token_response,
            status=200,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        expected_json = {"request": "success"}
        api_url = "https://some.api.url/goes/here"
        responses.add(responses.POST, api_url, json=expected_json)

        # Send request
        response = bitfount_session.request("POST", api_url)

        assert response.json() == expected_json
        mock_time.sleep.assert_called_once()
        mock_webbrowser.open.assert_called_once()

    def test_bitfount_session_authenticates_when_no_token_loaded(
        self,
        bitfount_session: BitfountSession,
        mocker: MockerFixture,
        username: str,
    ) -> None:
        """Checks that token requested and saved when none exists to load."""
        mock_fetch_device_code = mocker.patch.object(
            bitfount_session, "_fetch_device_code", return_value=(1, 2)
        )
        mock_do_verification = mocker.patch.object(bitfount_session, "_do_verification")
        mock_exchange_device_code = mocker.patch.object(
            bitfount_session, "_exchange_device_code_for_token"
        )
        mock_save_token = mocker.patch.object(bitfount_session, "_save_token_to_file")
        mocker.patch.object(
            bitfount_session, "_get_username_from_id_token", return_value=username
        )

        bitfount_session.authenticate()

        mock_fetch_device_code.assert_called_once()
        mock_do_verification.assert_called_once_with(1, 2)
        mock_exchange_device_code.assert_called_once()
        mock_save_token.assert_called_once_with(bitfount_session.token_file)

    def test_authenticate_validates_username(
        self,
        bitfount_session: BitfountSession,
        id_token_for_wrong_username: str,
        mocker: MockerFixture,
        username: str,
        wrong_username: str,
    ) -> None:
        """Test that authenticate() validates username against authenticated user."""
        mock_fetch_device_code = mocker.patch.object(
            bitfount_session, "_fetch_device_code", autospec=True, return_value=(1, 2)
        )
        mock_do_verification = mocker.patch.object(
            bitfount_session, "_do_verification", autospec=True
        )

        # Make it so the call to _exchange_device_code_for_token()
        # sets the _wrong_ id token
        def _set_id_token() -> None:
            bitfount_session.id_token = id_token_for_wrong_username

        mock_exchange_device_code = mocker.patch.object(
            bitfount_session,
            "_exchange_device_code_for_token",
            autospec=True,
            side_effect=lambda: _set_id_token(),
        )

        with pytest.raises(
            AuthenticatedUserError,
            match=(
                f"BitfountSession object was created for {username}"
                f" but authentication was done against {wrong_username}"
            ),
        ):
            bitfount_session.authenticate()

        mock_fetch_device_code.assert_called_once()
        mock_do_verification.assert_called_once_with(1, 2)
        mock_exchange_device_code.assert_called_once()

    @pytest.mark.parametrize(
        "url",
        [
            "hub",  # Hub URL
            "am",  # AM URL
            "other",  # Other URL
        ],
    )
    @responses.activate
    def test_bitfount_session_request_with_api_keys(
        self,
        access_token: str,
        bitfount_session: BitfountSession,
        device_code: str,
        mocker: MockerFixture,
        url: str,
    ) -> None:
        """Checks that `request()` call adds api keys only to Hub and AM calls."""
        # Set API keys and token
        bitfount_session.api_keys = APIKeys(
            "accessKeyID1:accessKeyID2", "accessKey1:accessKey2"
        )
        bitfount_session._access_token = access_token
        bitfount_session.device_code = device_code
        # Expires 1 month in future
        bitfount_session.access_token_expires_at = datetime.now(
            timezone.utc
        ) + relativedelta(months=1)

        # Mock `_is_hub_url` and `_is_am_url` methods
        if url == "hub":
            mocker.patch.object(bitfount_session, "_is_hub_url", return_value=True)
            api_url = "https://this.is.a.hub.url"
        elif url == "am":
            mocker.patch.object(bitfount_session, "_is_am_url", return_value=True)
            api_url = "https://this.is.an.am.url"
        else:
            api_url = "https://this.is.a.different.url"

        # Set up response
        responses.add(
            responses.POST,
            api_url,
        )

        # Send request
        bitfount_session.request("POST", api_url)

        # Check request had appropriate headers
        first_call: responses.Call = cast(responses.Call, responses.calls[0])
        if url == "hub":
            assert "authorization" not in first_call.request.headers
            # Check that the request only included the first part of the api keys
            assert first_call.request.headers["x-api-key-id"] == "accessKeyID1"
            assert first_call.request.headers["x-api-key"] == "accessKey1"
        elif url == "am":
            assert "authorization" not in first_call.request.headers
            # Check that the request included the full api keys
            assert (
                first_call.request.headers["x-api-key-id"]
                == "accessKeyID1:accessKeyID2"
            )
            assert first_call.request.headers["x-api-key"] == "accessKey1:accessKey2"
        else:
            # Confirm that API keys are not used if the URL is not a Hub or AM URL
            assert "x-api-key-id" not in first_call.request.headers
            assert "x-api-key" not in first_call.request.headers
            assert (
                first_call.request.headers["authorization"] == f"Bearer {access_token}"
            )

    def test_bitfount_session_authenticates_when_token_loaded_but_expired(
        self,
        access_token: str,
        bitfount_session: BitfountSession,
        id_token_for_username: str,
        mocker: MockerFixture,
        refresh_token: str,
        token_file: Path,
    ) -> None:
        """Checks that a new token is fetched via the login flow.

        This is the case where the loaded token has expired completely.
        """
        # Create saved token
        bitfount_session._access_token = access_token
        bitfount_session.access_token_expires_at = datetime(
            year=2000, month=6, day=13, tzinfo=timezone.utc
        )
        bitfount_session.id_token = id_token_for_username
        bitfount_session.refresh_token = refresh_token
        bitfount_session._save_token_to_file(token_file)

        # Reset session to initial state
        bitfount_session._access_token = None
        bitfount_session.access_token_expires_at = None
        bitfount_session.id_token = None
        bitfount_session.refresh_token = None

        mocker.patch.object(
            bitfount_session, "_refresh_access_token", return_value=False
        )
        mock_fetch_device_code = mocker.patch.object(
            bitfount_session, "_fetch_device_code", return_value=(1, 2)
        )
        mock_do_verification = mocker.patch.object(bitfount_session, "_do_verification")
        mock_exchange_device_code = mocker.patch.object(
            bitfount_session, "_exchange_device_code_for_token"
        )

        bitfount_session.authenticate()

        mock_fetch_device_code.assert_called_once()
        mock_do_verification.assert_called_once_with(1, 2)
        mock_exchange_device_code.assert_called_once()

    def test_bitfount_session_refreshes_when_token_loaded_but_expired(
        self,
        access_token: str,
        bitfount_session: BitfountSession,
        id_token_for_username: str,
        mocker: MockerFixture,
        refresh_token: str,
        token_file: Path,
    ) -> None:
        """Checks that a new token is fetched using the refresh mechanism.

        This is for when the loaded token has expired,
        but the refresh token is still valid
        """
        # Create saved token
        bitfount_session._access_token = access_token
        bitfount_session.access_token_expires_at = datetime(
            year=2000, month=6, day=13, tzinfo=timezone.utc
        )
        bitfount_session.id_token = id_token_for_username
        bitfount_session.refresh_token = refresh_token
        bitfount_session._save_token_to_file(token_file)

        # Reset session to initial state
        bitfount_session._access_token = None
        bitfount_session.access_token_expires_at = None
        bitfount_session.id_token = None
        bitfount_session.refresh_token = None

        mock_refresh_access_token = mocker.patch.object(
            bitfount_session, "_refresh_access_token"
        )
        mock_fetch_device_code = mocker.patch.object(
            bitfount_session, "_fetch_device_code"
        )
        mock_do_verification = mocker.patch.object(bitfount_session, "_do_verification")
        mock_exchange_device_code = mocker.patch.object(
            bitfount_session, "_exchange_device_code_for_token"
        )

        bitfount_session.authenticate()

        # Ensure refresh was called
        mock_refresh_access_token.assert_called_once()
        # Ensure manual login flow is not run
        mock_fetch_device_code.assert_not_called()
        mock_do_verification.assert_not_called()
        mock_exchange_device_code.assert_not_called()

    def test_bitfount_session_authenticated_when_valid_token_loaded(
        self,
        access_token: str,
        bitfount_session: BitfountSession,
        id_token_for_username: str,
        mocker: MockerFixture,
        refresh_token: str,
        token_file: Path,
    ) -> None:
        """Checks that authentication is successful when token loaded from file."""
        # Create saved token
        bitfount_session._access_token = access_token
        # Timestamp for 1 month from now
        bitfount_session.access_token_expires_at = datetime.now(
            timezone.utc
        ) + relativedelta(months=1)
        bitfount_session.id_token = id_token_for_username
        bitfount_session.refresh_token = refresh_token
        bitfount_session._save_token_to_file(token_file)

        # Reset session to initial state
        bitfount_session._access_token = None
        bitfount_session.access_token_expires_at = None
        bitfount_session.id_token = None
        bitfount_session.refresh_token = None

        mock_fetch_device_code = mocker.patch.object(
            bitfount_session, "_fetch_device_code"
        )
        mock_exchange_device_code = mocker.patch.object(
            bitfount_session, "_exchange_device_code_for_token"
        )

        bitfount_session.authenticate()

        mock_fetch_device_code.assert_not_called()
        mock_exchange_device_code.assert_not_called()

    def test_bitfount_session_doesnt_use_loaded_token_when_metadata_differs(
        self,
        access_token: str,
        bitfount_session: BitfountSession,
        id_token_for_username: str,
        mocker: MockerFixture,
        refresh_token: str,
        token_file: Path,
        user_storage_path: Path,
    ) -> None:
        """Test bitfount session will create & save a new token when different."""
        # Create saved token
        old_session_configuration = BitfountSession(
            "someOtherDomain.com",
            "not our client id",
            "someUsername",
            "not our scopes",
            "someOtherAudience",
        )
        old_session_configuration.user_storage_path = user_storage_path
        old_session_configuration._access_token = access_token
        # Timestamp for 1 month from now
        old_session_configuration.access_token_expires_at = datetime.now(
            timezone.utc
        ) + relativedelta(months=1)
        bitfount_session.id_token = id_token_for_username
        old_session_configuration.refresh_token = refresh_token
        old_session_configuration._save_token_to_file(token_file)

        mock_fetch_device_code = mocker.patch.object(
            bitfount_session, "_fetch_device_code", return_value=(1, 2)
        )
        mock_do_verification = mocker.patch.object(bitfount_session, "_do_verification")
        mock_exchange_device_code = mocker.patch.object(
            bitfount_session, "_exchange_device_code_for_token"
        )
        mock_save_token = mocker.patch.object(bitfount_session, "_save_token_to_file")

        bitfount_session.authenticate()

        mock_fetch_device_code.assert_called_once()
        mock_do_verification.assert_called_once_with(1, 2)
        mock_exchange_device_code.assert_called_once()
        mock_save_token.assert_called_once_with(token_file)

    @responses.activate
    def test_send_token_request_to_refresh_expired_token(
        self,
        auth_domain: str,
        bitfount_session: BitfountSession,
        refresh_token: str,
        token_refresh_request: _TokenRefreshRequestDict,
    ) -> None:
        """Checks _send_token_request works with refresh=True."""
        bitfount_session.refresh_token = refresh_token

        auth_server_response = {"some": "response"}

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=auth_server_response,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_refresh_request)
                )
            ],
        )

        response = bitfount_session._send_token_request(refresh=True)

        assert response.json() == auth_server_response

    @responses.activate
    def test_send_token_request_as_device_code(
        self,
        auth_domain: str,
        bitfount_session: BitfountSession,
        client_id: str,
        device_code: str,
        token_request: _DeviceAccessTokenRequestDict,
    ) -> None:
        """Checks that _send_token_request works correctly."""
        bitfount_session.device_code = device_code

        auth_server_response = {"some": "response"}

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=auth_server_response,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        response = bitfount_session._send_token_request()

        assert response.json() == auth_server_response

    def test_get_username_from_id_token(
        self,
        bitfount_session: BitfountSession,
        id_token_for_username: str,
        username: str,
    ) -> None:
        """Tests username can be extracted from ID Token."""
        bitfount_session.id_token = id_token_for_username

        assert bitfount_session._get_username_from_id_token() == username

    def test_get_username_from_id_token_raises_error_if_no_id_token(
        self,
        bitfount_session: BitfountSession,
    ) -> None:
        """Tests error raised if no id token when trying to extract username."""
        with pytest.raises(
            AuthenticatedUserError,
            match=re.escape(
                "User not authenticated yet,"
                " call authenticate() before accessing the ID token"
            ),
        ):
            bitfount_session._get_username_from_id_token()

    @pytest.mark.parametrize(
        "_username, assertion_error",
        [(lazy_fixture("username"), False), ("not-real-username", True)],
    )
    def test__verify_user_storage_path(
        self,
        _username: str,
        assertion_error: bool,
        bitfount_session: BitfountSession,
        mocker: MockerFixture,
    ) -> None:
        """Tests that token won't be saved in a directory with a different username."""
        mocker.patch.object(
            BitfountSession, "username", PropertyMock(return_value=_username)
        )

        if assertion_error:
            with pytest.raises(AuthenticatedUserError):
                bitfount_session._verify_user_storage_path()
        else:
            bitfount_session._verify_user_storage_path()

    @pytest.mark.parametrize(
        argnames=("error_expected", "username_"),
        argvalues=(
            pytest.param(False, _DEFAULT_USERNAME, id="default_username"),
            pytest.param(True, lazy_fixture("username"), id="nondefault_username"),
        ),
    )
    def test__validate_authenticated_user_when_authenticated_with_wrong_user(
        self,
        bitfount_session: BitfountSession,
        error_expected: bool,
        id_token_for_wrong_username: str,
        username_: str,
        wrong_username: str,
    ) -> None:
        """Test _validate_authenticated_user() when wrong user authenticated."""
        bitfount_session._username = username_
        bitfount_session.id_token = id_token_for_wrong_username

        if error_expected:
            with pytest.raises(
                AuthenticatedUserError,
                match=(
                    f"BitfountSession object was created for {username_}"
                    f" but authentication was done against {wrong_username}"
                ),
            ):
                bitfount_session._validate_authenticated_user()
        else:
            # Otherwise should run without issue
            bitfount_session._validate_authenticated_user()

    @pytest.mark.parametrize(
        argnames=("error_expected", "username_"),
        argvalues=(
            pytest.param(True, _DEFAULT_USERNAME, id="api_keys_and_default_username"),
            pytest.param(
                False, lazy_fixture("username"), id="api_keys_and_nondefault_username"
            ),
        ),
    )
    def test__validate_authenticated_user_when_using_api_keys(
        self,
        bitfount_session: BitfountSession,
        error_expected: bool,
        id_token_for_username: str,
        mocker: MockerFixture,
        username_: str,
    ) -> None:
        """Test _validate_authenticated_user() when using API keys."""
        bitfount_session._username = username_
        bitfount_session.id_token = id_token_for_username

        # Make it look like we're using API keys
        mocker.patch.object(
            type(bitfount_session), "api_keys", PropertyMock(return_value=True)
        )

        if error_expected:
            with pytest.raises(
                AuthenticatedUserError,
                match="Must specify a username when using API Keys.",
            ):
                bitfount_session._validate_authenticated_user()
        else:
            # Otherwise should run without issue
            bitfount_session._validate_authenticated_user()


@unit_test
@pytest.mark.parametrize(
    argnames=(
        "environment",
        "expected_name",
        "expected_auth_domain",
        "expected_client_id",
    ),
    argvalues=(
        pytest.param(
            _STAGING_ENVIRONMENT,
            "staging",
            _STAGING_AUTH_DOMAIN,
            _STAGING_CLIENT_ID,
            id="staging",
        ),
        pytest.param(
            _DEVELOPMENT_ENVIRONMENT,
            "development",
            _DEVELOPMENT_AUTH_DOMAIN,
            _DEVELOPMENT_CLIENT_ID,
            id="development",
        ),
        pytest.param(
            _PRODUCTION_ENVIRONMENT,
            "production",
            _PRODUCTION_AUTH_DOMAIN,
            _PRODUCTION_CLIENT_ID,
            id="production",
        ),
    ),
)
def test_get_auth_environment(
    environment: str,
    expected_auth_domain: str,
    expected_client_id: str,
    expected_name: str,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests _get_auth_environment with various envvar values."""
    # Patch out environment variable
    monkeypatch.setenv("BITFOUNT_ENVIRONMENT", environment)

    # Check return
    assert _get_auth_environment() == _AuthEnv(
        expected_name, expected_auth_domain, expected_client_id
    )
