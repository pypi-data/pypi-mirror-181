"""Module to perform requests to Orchestrator's API"""
# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, invalid-name
from abc import ABC, abstractmethod
from typing import Any, Optional, Mapping, Union, Dict
from urllib.parse import urlencode
import datetime
import logging
import re
import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import JSONDecodeError
from .auth import CloudFlow, CustomFlow, OnPremiseFlow

_AUTHS = ("cloud", "custom", "on-premise")


# type: ignore
def _auth_handler(auth: str, **kwargs) -> Union[CustomFlow, CloudFlow, OnPremiseFlow]:
    """Performs authentication"""
    if auth not in _AUTHS:
        raise ValueError(f"[{auth}] type not supported")
    if not kwargs:
        raise Exception("Parameters must be passed")
    try:
        if auth == "cloud":
            return CloudFlow(**kwargs)
        if auth == "custom":
            return CustomFlow(**kwargs)
        if auth == "on-premise":
            return OnPremiseFlow(**kwargs)
    except TypeError as err:
        p = re.compile("missing.*")
        msg = re.findall(p, str(err))[0]
        raise ValueError(str(msg)) from err
    raise Exception("Something went wrong.")


class _CustomAdapter(HTTPAdapter):
    _RETRY_STATUS = [
        500,
        501,
        502,
        504,
        504,
        429,
    ]
    _BACKOFF_FACTOR = 0.1
    _TOTAL_RETRIES = 3

    def __init__(self):
        super().__init__()
        self.max_retries = Retry(
            total=self._TOTAL_RETRIES,
            backoff_factor=self._BACKOFF_FACTOR,
            status_forcelist=self._RETRY_STATUS,
        )


class HTTPClient(ABC):
    """Abstract Base Class for performing HTTP requests"""

    @abstractmethod
    def get(self, endpoint: str, params: Optional[Mapping[str, str]] = None):
        """Abstract method for GET requests"""

    @abstractmethod
    def post(
        self,
        endpoint: str,
        body: Optional[Mapping[str, Any]] = None,
        files: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Abstract method for POST requests"""

    @abstractmethod
    def put(
        self, endpoint: str, body: Optional[Mapping[str, Any]] = None
    ) -> Dict[str, Any]:
        """Abstract method for PUT requests"""

    @abstractmethod
    def delete(self, endpoint: str):
        """Abstract method for DELETE requests"""


class Client(HTTPClient):
    """
    Client class to perform requests to Orchestrator's API

    :param auth: the authentication system of your choice
    :param tenant_name: your account's logical name

    :param client_id: you client id
    :param refresh_token: a refresh token
    :param base_url: a custom url

    """

    __slots__ = (
        "_client_id",
        "tenant_name",
        "refresh_token",
        "auth",
        "flow",
        "base_url",
        "_access_token",
        "token_expires",
        "_session",
        "folder_id",
    )

    def __init__(self, auth: str, **kwargs):

        self.flow = _auth_handler(auth=auth, **kwargs)
        self._session = requests.Session()
        self._session.mount("https://", _CustomAdapter())
        self.folder_id: int = None  # type: ignore
        self.tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    def _folder_header(self) -> Dict[str, str]:
        if not self.folder_id:
            raise AttributeError(
                "A folder id is needed to perform this operation. 'client.folder_id' attribute is set to None."
            )
        return {"X-UIPATH-OrganizationUnitId": f"{self.folder_id}"}

    def prepare_headers(self) -> Dict[str, str]:
        """Prepares the headers for the subsequent requests"""
        content_header = self.flow.content_header()
        auth_header = self.flow.auth_headers()
        folder_header = self._folder_header() if self.folder_id else {}
        try:
            headers = content_header | auth_header | folder_header
        except TypeError:
            headers = {**content_header, **auth_header, **folder_header}
        return headers

    def prepare_url(
        self, endpoint: str, params: Optional[Mapping[str, str]] = None
    ) -> str:
        """Preparse the url depending on the base_url"""
        if params:
            encoded_params = urlencode(params)
            return f"{self.flow.base_url}{endpoint}?{encoded_params}"
        return f"{self.flow.base_url}{endpoint}"

    def _internall_call(
        self,
        method: str,
        url: str,
        body: Optional[Mapping[str, Any]] = None,
        files: Optional[Mapping[str, Any]] = None,
    ) -> Union[Dict[str, Any], bytes]:
        # check if auth flow has been run or token has expired
        if self.flow.token_expires() or not self.flow.authenticated:
            # perform auth
            self.flow.auth()
        headers = self.prepare_headers()
        # headers.update({"Content-Type" : "application/octet-stream", "Content-Disposition" : "attachment"})
        # if files:
        #     headers.update({"Content-Type" : "undefined"})
        del headers["Content-Type"]
        # pprint(headers)
        res = self._session.request(
            method=method, url=url, json=body, headers=headers, files=files # type: ignore
        )
        print(res.url)
        print(res.status_code)
        if res.status_code == 503:
            # in case something went wrong with the expiracy clock
            print("Something wrong with the clock")
            self.flow.auth()
        # print(res.text)
        res.raise_for_status()
        try:
            json_string = res.json()
            return json_string
        except JSONDecodeError as err:
            if res.text == "":
                return {}
            else:
                if res.content:
                    return res.content
            logging.error("Something went wront during the authentication process.")
            raise ValueError(
                "Please check your 'tenant_name' and 'organization' credential values."
            ) from err

    def get(self, endpoint: str, params: Optional[Mapping[str, str]] = None):
        url = self.prepare_url(endpoint, params=params)
        json_string = self._internall_call("GET", url, params)
        return json_string

    def post(
        self,
        endpoint: str,
        body: Optional[Mapping[str, Any]] = None,
        files: Optional[Mapping[str, Any]] = None,
    ):
        url = self.prepare_url(endpoint)
        json_string = self._internall_call("POST", url, body=body, files=files)
        return json_string

    def delete(self, endpoint: str):
        url = self.prepare_url(endpoint)
        self._internall_call("DELETE", url)

    def put(self, endpoint: str, body: Optional[Mapping[str, Any]] = None):
        url = self.prepare_url(endpoint)
        json_string = self._internall_call("PUT", url, body=body)
        return json_string
