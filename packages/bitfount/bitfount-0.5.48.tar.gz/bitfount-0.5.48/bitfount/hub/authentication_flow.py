"""Authentication flow and session management."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import cached_property
import json
import logging
import os
from pathlib import Path
import threading
import time
from typing import TYPE_CHECKING, Dict, Final, List, Optional, Tuple, Union, cast
import webbrowser

import jwt
import requests
from requests.exceptions import InvalidJSONError

from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
    BITFOUNT_STORAGE_PATH,
    _get_environment,
)
from bitfount.exceptions import BitfountError
from bitfount.hub.exceptions import AuthenticatedUserError
from bitfount.hub.types import (
    _DEV_AM_URL,
    _DEV_HUB_URL,
    _STAGING_AM_URL,
    _STAGING_HUB_URL,
    PRODUCTION_AM_URL,
    PRODUCTION_HUB_URL,
    APIKeys,
    _DeviceAccessTokenFailResponseJSON,
    _DeviceAccessTokenRequestDict,
    _DeviceAccessTokenResponseJSON,
    _DeviceCodeRequestDict,
    _DeviceCodeResponseJSON,
    _TokenRefreshRequestDict,
    _TokenRefreshResponseJSON,
)
from bitfount.utils import delegates, web_utils
from bitfount.utils.web_utils import _auto_retry_request

if TYPE_CHECKING:
    from requests import Response

logger = logging.getLogger(__name__)

# This forces `requests` to make IPv4 connections
# TODO: [BIT-1443] Remove this once Hub/AM support IPv6
requests.packages.urllib3.util.connection.HAS_IPV6 = False  # type: ignore[attr-defined] # Reason: see above # noqa: B950

_HUB_URLS: List[str] = [PRODUCTION_HUB_URL, _STAGING_HUB_URL, _DEV_HUB_URL]
_AM_URLS: List[str] = [PRODUCTION_AM_URL, _STAGING_AM_URL, _DEV_AM_URL]


_PRODUCTION_AUTH_DOMAIN: Final = "auth.bitfount.com"
_STAGING_AUTH_DOMAIN: Final = "auth.staging.bitfount.com"
_DEVELOPMENT_AUTH_DOMAIN: Final = (
    "auth.staging.bitfount.com"  # this is part of the staging tenant on auth0
)

# TODO: [BIT-356] potentially remove these client ids from the codebase
_PRODUCTION_CLIENT_ID: Final = "8iCJ33Kp6hc9ofrXTzr5GLxMRHWrlzZO"
_STAGING_CLIENT_ID: Final = "Wk4XZHDKfY8F3OYcKdagIHETt6JYwX08"
_DEVELOPMENT_CLIENT_ID: Final = "MP8oao6gcJd4jARwzJiJlEiK59ZeLCt3"

_SCOPES: Final = "profile openid offline_access"
_HUB_API_IDENTIFIER: Final = (
    "https://hub.bitfount.com/api"  # this is the same for staging and production
)
_DEVICE_CODE_GRANT_TYPE: Final = "urn:ietf:params:oauth:grant-type:device_code"
_AUTHORIZATION_PENDING_ERROR: Final = "authorization_pending"
_SLOW_DOWN_ERROR: Final = "slow_down"

_DEFAULT_USERNAME: Final[str] = "_default"
_USERNAME_KEY: Final = "https://www.bitfount.com/username"


@dataclass
class _AuthEnv:
    """Captures the combined authorisation information."""

    name: str
    auth_domain: str
    client_id: str


def _get_auth_environment() -> _AuthEnv:
    """Determines the auth settings based on environment variables.

    Returns:
        A tuple containing the auth domain and client ID for the given environment.
    """
    environment = _get_environment()
    if environment == _STAGING_ENVIRONMENT:
        return _AuthEnv("staging", _STAGING_AUTH_DOMAIN, _STAGING_CLIENT_ID)
    if environment == _DEVELOPMENT_ENVIRONMENT:
        return _AuthEnv("development", _DEVELOPMENT_AUTH_DOMAIN, _DEVELOPMENT_CLIENT_ID)
    return _AuthEnv("production", _PRODUCTION_AUTH_DOMAIN, _PRODUCTION_CLIENT_ID)


class AuthEnvironmentError(BitfountError):
    """Exception related to the authorization and authentication environment."""

    pass


@delegates()
class BitfountSession(requests.Session):
    """Manages session-based interactions with Bitfount.

    Extends requests.Session, appending an access token to the
    authorization of any requests made if an access token is present

    When the token expires it will request a new token prior to
    sending the web request.

    Usage:
        `session = BitfountSession(...)`
        # When you want the user to interact to start the session:
        `session.authenticate()`
        # The session can then be used as a normal requests.Session


    Attributes:
        access_token_expires_at: The time at which the access token expires.
        device_code: The device code returned by the Bitfount API.
        device_code_arrival_time: The time at which the device code was issued.
        device_code_expires_at: The time at which the device code expires.
        id_token: The ID token returned by the Bitfount API.
        refresh_token: The refresh token returned by the Bitfount API.
        token_file: The path to the file where the token is stored.
        token_request_interval: The time between token requests.
        user_storage_path: The path to the file where the user is stored.
    """

    def __init__(
        self,
        auth_domain: str = _PRODUCTION_AUTH_DOMAIN,
        client_id: str = _PRODUCTION_CLIENT_ID,
        username: str = _DEFAULT_USERNAME,
        scopes: str = _SCOPES,
        audience: str = _HUB_API_IDENTIFIER,
    ):
        super().__init__()

        self._auth_domain = auth_domain
        self._client_id = client_id
        self._username = username
        self._scopes: str = scopes
        self._audience: str = audience
        self._device_code_endpoint: str = (
            f"https://{self._auth_domain}/oauth/device/code"
        )
        self._token_endpoint: str = f"https://{self._auth_domain}/oauth/token"
        self._access_token: Optional[str] = None
        self._reauthentication_lock = threading.Lock()

        self.access_token_expires_at: Optional[datetime] = None
        self.device_code: Optional[str] = None
        self.device_code_arrival_time: Optional[datetime] = None
        self.device_code_expires_in: Optional[int] = None
        self.id_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_storage_path: Path = BITFOUNT_STORAGE_PATH / username
        self.token_file: Path = self.user_storage_path / ".token"
        self.token_request_interval: Optional[int] = None

        # If using API keys verify that username has been set to non-default
        if self.api_keys and username == _DEFAULT_USERNAME:
            raise AuthenticatedUserError("Must specify a username when using API Keys.")

    @cached_property
    def api_keys(self) -> Optional[APIKeys]:
        """Returns API keys to be used for the current session if they exist.

        These are cached so they don't need to be retrieved every time.
        """
        if (access_key_id := os.environ.get("BITFOUNT_API_KEY_ID")) and (
            access_key := os.environ.get("BITFOUNT_API_KEY")
        ):
            logger.info("Using API keys for authentication.")
            return APIKeys(access_key_id=access_key_id, access_key=access_key)

        return None

    @property
    def username(self) -> str:
        """Returns the username of the authenticated user."""
        if self._username != _DEFAULT_USERNAME:
            # If non-default username specified check that the authenticated user
            # matches
            self._validate_authenticated_user()
            return self._username

        # If default username specified, get the _actual_ username from the token
        return self._get_username_from_id_token()

    @property
    def access_token(self) -> Optional[str]:
        """Returns the access token. Tries to refresh it if needed."""
        with self._reauthentication_lock:
            if not self.authenticated:
                self.authenticate()

            return self._access_token

    @property
    def authenticated(self) -> bool:
        """Returns true if we have an unexpired access token or API Keys."""
        return bool(self.api_keys) or bool(self._access_token and not self.expired)

    @property
    def expired(self) -> bool:
        """Whether or not the access token has expired.

        Returns: True if the token has expired
        """
        # Either both attributes will be present or neither will be
        if self._access_token and self.access_token_expires_at:
            # If the token expires in the next 10 minutes, refresh
            return (
                self.access_token_expires_at - timedelta(minutes=10)
            ) <= datetime.now(timezone.utc)
        else:
            return False

    @staticmethod
    def _is_url_in_urls(url: str, urls: List[str]) -> bool:
        """Returns true if the given `url` is in the list of `urls`.

        This includes if `url` points to a particular resource/page/endpoint etc. for
        a url present in `urls`.
        """
        for _url in urls:
            if url.startswith(_url):
                return True

        return False

    @classmethod
    def _is_hub_url(cls, url: str) -> bool:
        """Returns whether the provided url is a Bitfount Hub URL."""
        return cls._is_url_in_urls(url, _HUB_URLS)

    @classmethod
    def _is_am_url(cls, url: str) -> bool:
        """Returns whether the provided url is a Bitfount AM URL."""
        return cls._is_url_in_urls(url, _AM_URLS)

    def _validate_authenticated_user(self) -> None:
        """Check that authenticated user matches initialised username.

        If using API keys just validate that username was specified.
        """
        if self.api_keys:
            if self._username == _DEFAULT_USERNAME:
                # No token will be present, and username must be explicitly set in
                # __init__ to use API keys
                raise AuthenticatedUserError(
                    "Must specify a username when using API Keys."
                )
            else:
                return None
        elif self._username != _DEFAULT_USERNAME and self._username != (
            authenticated_user := self._get_username_from_id_token()
        ):
            raise AuthenticatedUserError(
                f"BitfountSession object was created for {self._username} but"
                f" authentication was done against {authenticated_user}"
            )
        else:
            return None

    def _verify_user_storage_path(self) -> None:
        """Verifies that user storage path corresponds to username.

        Raises:
            AssertionError: if user storage path corresponds to a different username
                from the BitfountSession.
        """
        # User storage should either be for the default username or the
        # authenticated user
        if not str(self.user_storage_path).endswith((_DEFAULT_USERNAME, self.username)):
            provided_user = self.user_storage_path.stem
            raise AuthenticatedUserError(
                f"BitfountSession connected to {self.username}. "
                f"This does not match the provided user storage path: {provided_user}"
            )

    def authenticate(self) -> None:
        """Authenticates user to allow protected requests.

        Prompts the user to login/authenticate and stores the tokens to use them
        in future requests.

        Raises:
            AssertionError: If user storage path corresponds to a different username
                from the BitfountSession.
            ConnectionError: If a token cannot be retrieved.
        """
        if self.api_keys:
            logger.debug("Using API keys, no need to authenticate.")
            return

        self._load_token_from_file(self.token_file)

        # Refresh the loaded token if it has expired
        refreshed = False
        if self.expired:
            refreshed = self._refresh_access_token()

        # Force user to go through login flow if we didn't refresh the token
        # Or if we haven't loaded an authenticated token
        if not self.authenticated and not refreshed:
            user_code, verification_uri = self._fetch_device_code()
            self._do_verification(user_code, verification_uri)
            self._exchange_device_code_for_token()

        # Check that logged-in user matches expected user
        self._validate_authenticated_user()

        # Verify that user storage path corresponds to username before saving the token
        self._verify_user_storage_path()

        # Ensure directory path exists
        self.user_storage_path.mkdir(parents=True, exist_ok=True)
        self._save_token_to_file(self.token_file)
        logger.info(f'Logged into Bitfount as "{self.username}"')

    def _fetch_device_code(self) -> Tuple[str, str]:
        """Fetches device code."""
        # See: https://auth0.com/docs/api/authentication?http#device-authorization-flow
        request_data: _DeviceCodeRequestDict = {
            "client_id": self._client_id,
            "scope": self._scopes,
            "audience": self._audience,
        }
        device_code_response: Response = web_utils.post(
            self._device_code_endpoint,
            data=request_data,
        )
        device_code_response.raise_for_status()

        response_json: _DeviceCodeResponseJSON = device_code_response.json()
        verification_uri: str = response_json["verification_uri_complete"]
        user_code: str = response_json["user_code"]

        self.device_code = response_json["device_code"]
        self.token_request_interval = response_json["interval"]
        self.device_code_expires_in = response_json["expires_in"]

        # This doesn't need to be exact, network latency affects this anyway
        self.device_code_arrival_time = datetime.now(timezone.utc)

        return user_code, verification_uri

    def _do_verification(self, user_code: str, verification_uri: str) -> None:
        """Opens web browser for verification."""
        print(f"Your confirmation code is: {user_code}")
        time.sleep(1)  # Give the user a second to see the code before opening browser
        webbrowser.open(verification_uri)
        print(
            "A browser window has been opened, "
            "please log in to confirm your identity."
        )
        print("If no browser window has opened, then please visit the following URL:")
        print(verification_uri)

    def _exchange_device_code_for_token(self) -> None:
        """Exchanges device code for token."""
        token_response: Optional[
            Union[_DeviceAccessTokenResponseJSON, _DeviceAccessTokenFailResponseJSON]
        ] = None

        # This method should only be called after a call to _fetch_device_code
        # so these will be set. Asserts to reassure mypy.
        assert self.device_code_arrival_time is not None  # nosec[assert_used]
        assert self.device_code_expires_in is not None  # nosec[assert_used]
        assert self.token_request_interval is not None  # nosec[assert_used]

        interval = self.token_request_interval

        while not self._device_code_expired(
            self.device_code_arrival_time, self.device_code_expires_in
        ):
            response: Response = self._send_token_request()

            # Break out of loop as we have our tokens!
            if (status_code := response.status_code) == 200:
                try:
                    token_response = cast(
                        _DeviceAccessTokenResponseJSON, response.json()
                    )
                except InvalidJSONError:
                    logger.error(
                        f"Received 200 status response, but JSON is invalid: "
                        f'"{response.text}"'
                    )
                    pass
                # Break because we have token or because we're unable to decode it
                break

            # Treat it as an expected "failure" response until we know otherwise;
            # status code could be any 4XX value, so we instead just check for the
            # right format and error values.
            try:
                token_response = cast(
                    _DeviceAccessTokenFailResponseJSON, response.json()
                )
            except InvalidJSONError:
                logger.error(
                    f"Received {status_code} status response, but JSON is invalid: "
                    f'"{response.text}"'
                )
                break

            # Break out of loop unless the flow is still in progress
            if (error := token_response.get("error")) not in (
                _AUTHORIZATION_PENDING_ERROR,
                _SLOW_DOWN_ERROR,
            ):
                # Not a retry-able response; fail out
                error_msg = (
                    f"An unexpected error occurred: status code: {status_code}; "
                    f'"{response.text}"'
                )
                logger.error(error_msg)
                print(error_msg)
                break
            elif error == _SLOW_DOWN_ERROR:
                # Somehow polling too fast (though should be using the interval
                # they specified); increase interval
                logger.warning(
                    f"Polling too quickly; increasing interval from {interval} "
                    f"to {interval+1} seconds"
                )
                interval += 1
            else:  # error == _AUTHORIZATION_PENDING_ERROR
                # Fine and expected, just keep trying
                pass

            print(
                f"Awaiting authentication in browser. "
                f"Will check again in {interval} seconds."
            )
            time.sleep(interval)

        if token_response and "access_token" in token_response:
            # Have our response now
            token_response = cast(_DeviceAccessTokenResponseJSON, token_response)
            self._access_token = token_response["access_token"]
            self.refresh_token = token_response["refresh_token"]
            self.id_token = token_response["id_token"]
            self.access_token_expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=token_response["expires_in"],
            )
        else:
            raise ConnectionError(
                "Failed to retrieve a device code from the authentication server"
            )

    def _send_token_request(self, refresh: bool = False) -> Response:
        """Sends a request to the Auth Server token endpoint to get a new token."""
        if refresh:
            # See: https://auth0.com/docs/api/authentication?http#refresh-token
            # If refreshing, must have refresh_token. Reassure mypy.
            assert self.refresh_token is not None  # nosec[assert_used]
            refresh_request_data: _TokenRefreshRequestDict = {
                "client_id": self._client_id,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            }
            return web_utils.post(self._token_endpoint, data=refresh_request_data)
        else:
            # See: https://auth0.com/docs/api/authentication?http#device-authorization-flow48  # noqa: B950
            # device_code must already be set by the time we are calling this.
            # Reassure mypy.
            assert self.device_code is not None  # nosec[assert_used]
            request_data: _DeviceAccessTokenRequestDict = {
                "client_id": self._client_id,
                "grant_type": _DEVICE_CODE_GRANT_TYPE,
                "device_code": self.device_code,
            }
            return web_utils.post(self._token_endpoint, data=request_data)

    # We only wrap this method in _auto_retry_request as any calls to the others
    # (post, get, etc) will make use of this. Wrapping them all would result in
    # a double retry loop, but we can't _not_ wrap request as it is often used
    # directly.
    @_auto_retry_request
    def request(  # type: ignore[no-untyped-def,override]
        self, method, url, params=None, data=None, headers=None, **kwargs
    ) -> Response:
        """Performs an HTTP request.

        Overrides requests.session.request, appending our access token
        to the request headers or API keys if present.
        """
        # Create headers if they don't exist already
        if not headers:
            headers = {}

        is_am_url = self._is_am_url(url)
        is_hub_url = self._is_hub_url(url)

        if self.api_keys and (is_am_url or is_hub_url):
            logger.debug(f"Adding API key to request headers for {url}")

            if is_hub_url:
                # If the URL is a hub URL, only the first half of the API keys are used
                # which corresponds to the portion required for the Hub
                headers["x-api-key-id"] = self.api_keys.access_key_id.split(":")[0]
                headers["x-api-key"] = self.api_keys.access_key.split(":")[0]

            elif is_am_url:
                # If the URL is an AM URL, the entire API key is used because the AM
                # also calls the Hub under the hood and therefore needs both portions
                headers["x-api-key-id"] = self.api_keys.access_key_id
                headers["x-api-key"] = self.api_keys.access_key

        elif self.access_token:
            logger.debug(f"Adding token to request headers for {url}")
            headers["authorization"] = f"Bearer {self._access_token}"

        return super().request(
            method, url, params=params, data=data, headers=headers, **kwargs
        )

    def _refresh_access_token(self) -> bool:
        """Attempts to refresh the access token.

        Returns: True if the token was refreshed, false otherwise

        """
        token_response = self._send_token_request(refresh=True)

        if token_response.status_code == 200:
            token_response_json: _TokenRefreshResponseJSON = token_response.json()
            self._access_token = token_response_json["access_token"]
            self.refresh_token = token_response_json["refresh_token"]
            self.id_token = token_response_json["id_token"]
            self.access_token_expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=token_response_json["expires_in"]
            )
            return True
        logger.warning(
            f"Failed to refresh access token, response was: {token_response.text}"
        )
        return False

    @staticmethod
    def _device_code_expired(arrival_time: datetime, expires_in_seconds: int) -> bool:
        """Checks if authorization code has expired.

        Checks if too much time has passed between the device code
        being issued by the Auth Server and the user approving access
        using that device code.
        """
        return datetime.now(timezone.utc) >= arrival_time + timedelta(
            seconds=expires_in_seconds
        )

    def _save_token_to_file(self, token_file: Path) -> None:
        """Saves authentication token to file.

        Saves all fields that are necessary to reproduce this object to a file.
        """
        # This will be set by the time this is called. Reassure mypy.
        assert self.access_token_expires_at is not None  # nosec[assert_used]
        json.dump(
            {
                "access_token": self._access_token,
                "refresh_token": self.refresh_token,
                "id_token": self.id_token,
                "access_token_expires_at": self.access_token_expires_at.timestamp(),
                "auth_domain": self._auth_domain,
                "client_id": self._client_id,
                "scopes": self._scopes,
                "audience": self._audience,
            },
            token_file.open("w"),
        )

    def _load_token_from_file(self, token_file: Path) -> None:
        """Loads authentication token from file.

        Attempts to load the data needed for authentication, when loaded it updates
        the fields on the instance.

        If the data is found but the metadata differs then it will not update
        the fields.

        If no data, or no file is found it will just return without error.
        """
        if token_file.exists():
            serialized_tokens = json.load(token_file.open())

            auth_domain = serialized_tokens["auth_domain"]
            client_id = serialized_tokens["client_id"]
            scopes = serialized_tokens["scopes"]
            audience = serialized_tokens["audience"]

            if (
                self._auth_domain != auth_domain
                or self._client_id != client_id
                or self._scopes != scopes
                or self._audience != audience
            ):
                print(
                    "Stored tokens are no longer valid, "
                    "fresh authentication is necessary"
                )
                return

            self._access_token = serialized_tokens["access_token"]
            self.refresh_token = serialized_tokens["refresh_token"]
            self.id_token = serialized_tokens["id_token"]
            self.access_token_expires_at = datetime.fromtimestamp(
                serialized_tokens["access_token_expires_at"], tz=timezone.utc
            )

    def _get_username_from_id_token(self) -> str:
        """Extracts the Bitfount username from the token.

        Note: This function performs no verification of the id_token signature
        and should only be used in situations where the username in the token
        is not used to make decisions. As this is not backend code (i.e.
        anyone can edit this) we aren't very concerned about the fact it is
        not verified.
        """
        if self.id_token is None:
            raise AuthenticatedUserError(
                "User not authenticated yet, call authenticate() before accessing"
                " the ID token"
            )

        # Decode the ID token without verification
        id_token_decode: Dict[str, str] = jwt.decode(
            self.id_token, options={"verify_signature": False}
        )
        return id_token_decode[_USERNAME_KEY]
