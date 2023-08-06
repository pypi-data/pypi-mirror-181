"""
Rest adapter for the Metabase API
"""
from __future__ import annotations

from json import JSONDecodeError
from logging import getLogger
from pathlib import Path
from typing import Any, Literal, Optional

from packaging.version import Version
from requests import Response, Session
from requests.exceptions import RequestException

from metabase_tools.endpoints.activity_endpoint import Activity
from metabase_tools.endpoints.dashboard_endpoint import Dashboards
from metabase_tools.endpoints.alerts_endpoint import Alerts
from metabase_tools.endpoints.cards_endpoint import Cards
from metabase_tools.endpoints.collections_endpoint import Collections
from metabase_tools.endpoints.databases_endpoint import Databases
from metabase_tools.endpoints.users_endpoint import Users
from metabase_tools.exceptions import MetabaseApiException
from metabase_tools.models.server_settings import ServerSettings, Setting
from metabase_tools.tools.tools import MetabaseTools

logger = getLogger(__name__)


class MetabaseApi:
    """Metabase API adapter"""

    server_version: Version

    activity: Activity
    alerts: Alerts
    cards: Cards
    collections: Collections
    dashboards: Dashboards
    databases: Databases
    settings: ServerSettings
    tools: MetabaseTools
    users: Users

    def __init__(
        self,
        metabase_url: str,
        credentials: Optional[dict[str, str]] = None,
        cache_token: bool = False,
        token_path: Optional[Path | str] = None,
        session: Optional[Session] = None,
    ):
        if not credentials and not token_path:
            raise MetabaseApiException("No authentication method provided")
        credentials = credentials or {}
        token_path = Path(token_path) if token_path else None

        # Validate Metabase URL
        self.metabase_url = self._validate_base_url(url=metabase_url)

        # Starts session to be reused by the adapter so that the auth token is cached
        self._session = session or Session()

        # Authenticate
        self._authenticate(token_path=token_path, credentials=credentials)

        # Cache token, if set during init
        if cache_token:
            save_path = Path(token_path or "metabase.token")
            self._save_token(save_path=save_path)

        # Set server version for compatability checks
        self._set_server_version()

        # Create endpoints
        self.activity = Activity(self)
        self.alerts = Alerts(self)
        self.cards = Cards(self)
        self.collections = Collections(self)
        self.dashboards = Dashboards(self)
        self.databases = Databases(self)
        self.settings = self._fetch_settings()
        self.tools = MetabaseTools(self)
        self.users = Users(self)

    def _validate_base_url(self, url: str) -> str:
        if url[-1] == "/":
            url = url[:-1]
        if url[-4:] == "/api":
            url = url[:-4]
        if url[:4] != "http":
            url = f"http://{url}"
        return f"{url}/api"

    def _authenticate(
        self, token_path: Optional[Path], credentials: dict[str, str]
    ) -> None:
        authed = False
        # Try cached token first
        if token_path and token_path.exists():
            authed = self._auth_with_cached_token(token_path=token_path)
            if not authed:
                self._delete_cached_token(token_path=token_path)
        # Try token passed as credentials next
        if not authed and "token" in credentials:
            authed = self._auth_with_passed_token(credentials=credentials)
        # Finally try username and password
        if not authed and "username" in credentials and "password" in credentials:
            authed = self._auth_with_login(credentials=credentials)
        # Raise error if still not authenticated
        if not authed:
            logger.error("Failed to authenticate")
            raise MetabaseApiException(
                "Failed to authenticate with credentials provided"
            )

    def _add_token_to_header(self, token: str) -> None:
        headers = {
            "Content-Type": "application/json",
            "X-Metabase-Session": token,
        }
        self._session.headers.update(headers)

    def _delete_cached_token(self, token_path: Path) -> None:
        if token_path.exists():
            logger.warning("Deleting token file")
            token_path.unlink()

    def _auth_with_cached_token(self, token_path: Path) -> bool:
        with open(token_path, "r", encoding="utf-8") as file:
            token = file.read()
        logger.info("Attempting authentication with token file")
        self._add_token_to_header(token=token)
        authed = self.test_for_auth()
        logger.info(
            "Authenticated with token file"
            if authed
            else "Failed to authenticate with token file"
        )
        return authed

    def _auth_with_passed_token(self, credentials: dict[str, str]) -> bool:
        logger.info("Attempting authentication with token passed")
        self._add_token_to_header(token=credentials["token"])
        authed = self.test_for_auth()
        logger.info(
            "Authenticated with token passed"
            if authed
            else "Failed to authenticate with token passed"
        )
        return authed

    def _auth_with_login(self, credentials: dict[str, str]) -> bool:
        """Private method for authenticating a session with the API

        Args:
            credentials (dict): Username and password
        """
        try:
            logger.info("Attempting authentication with username and password")
            response = self._session.post(
                f"{self.metabase_url}/session", json=credentials
            )
            self._add_token_to_header(token=response.json()["id"])
            authed = self.test_for_auth()
            logger.info(
                "Authenticated with login"
                if authed
                else "Failed to authenticate with login"
            )
            return authed
        except KeyError as error_raised:
            logger.warning(
                "Exception encountered during attempt to authenticate with login \
                    passed: %s",
                error_raised,
            )
        return False

    def test_for_auth(self) -> bool:
        """Validates successful authentication by attempting to retrieve data about \
            the current user

        Returns:
            bool: Authentication success status
        """
        return (
            200
            <= self._session.get(f"{self.metabase_url}/user/current").status_code
            <= 299
        )

    def _save_token(self, save_path: Path | str) -> None:
        """Writes active token to the specified file

        Args:
            save_path (Path | str): Name of file to write
        """
        logger.debug("Saving token to %s", save_path)
        token = str(self._session.headers.get("X-Metabase-Session"))
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(token)

    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Response:
        """Perform an HTTP request, catching and re-raising any exceptions

        Args:
            method (str): GET or POST or DELETE or PUT
            url (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Raises:
            RequestFailure: Request failed

        Returns:
            Response: Response from the API
        """
        try:
            logger.info("Making HTTP request: %s:%s:%s", method, url, params)
            return self._session.request(
                method=method, url=url, params=params, json=json, timeout=30
            )
        except RequestException as error_raised:
            logger.error(str(error_raised))
            raise MetabaseApiException from error_raised

    def generic_request(
        self,
        http_verb: Literal["GET", "POST", "PUT", "DELETE"],
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Method for dispatching HTTP requests

        Args:
            http_method (str): GET or POST or PUT or DELETE
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Raises:
            InvalidDataReceived: Unable to decode response from API
            AuthenticationFailure: Auth failure received from API
            RequestFailure: Other failure during request

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        log_line_post = "Request result: success=%s, status_code=%s, message=%s"
        response = self._make_request(
            method=http_verb,
            url=self.metabase_url + endpoint,
            params=params,
            json=json,
        )

        # If status_code in 200-299 range, return Result, else raise exception
        if 299 >= response.status_code >= 200:
            logger.info(log_line_post, True, response.status_code, response.reason)
            try:
                data = response.json()
                if isinstance(data, dict) and all(
                    key in data for key in ["data", "total"]
                ):
                    data = data["data"]
                if isinstance(data, (list, dict)):
                    return data
            except JSONDecodeError:
                if response.status_code == 204:
                    return {"success": True}
                logger.error(log_line_post, False, response.status_code, response.text)
                raise
        elif response.status_code == 401:
            logger.error(log_line_post, False, response.status_code, response.text)
            raise MetabaseApiException(
                f"Failed to authenticate: {response.status_code} - {response.reason}"
            )

        error_line = f"{response.status_code} - {response.reason} - {response.text}"
        logger.error(log_line_post, False, response.status_code, response.text)
        raise MetabaseApiException(error_line)

    def get(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """HTTP GET request

        Args:
            endpoint (str): URL endpoint
            ep_params (dict, optional): Endpoint parameters

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        return self.generic_request(http_verb="GET", endpoint=endpoint, params=params)

    def post(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """HTTP POST request

        Args:
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        return self.generic_request(
            http_verb="POST", endpoint=endpoint, params=params, json=json
        )

    def delete(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """HTTP DELETE request

        Args:
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        return self.generic_request(
            http_verb="DELETE", endpoint=endpoint, params=params
        )

    def put(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """HTTP PUT request

        Args:
            endpoint (str): URL endpoint
            ep_params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        return self.generic_request(
            http_verb="PUT", endpoint=endpoint, params=params, json=json
        )

    def _set_server_version(self) -> None:
        """Get the Metabase version running on the server

        Returns:
            str: version string
        """
        properties = self.get("/session/properties")
        if isinstance(properties, dict):
            self.server_version = Version(properties["version"]["tag"])
            logger.info("Server version: %s", self.server_version)
        else:
            logger.error("Unable to fetch server version")
            raise MetabaseApiException("Unable to fetch server version")

    def _fetch_settings(self) -> ServerSettings:
        """Retrieves settings from Metabase server"""
        settings = self.get("/setting")
        if isinstance(settings, list):
            settings = {setting["key"]: Setting(**setting) for setting in settings}
            server_settings = ServerSettings(**settings)
            server_settings.set_adapter(self)
            return server_settings
        logger.error("Unable to fetch settings")
        raise MetabaseApiException("Unable to fetch settings")
