# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, invalid-name
from abc import ABC, abstractmethod
from typing import Any, Optional, Mapping, Dict
from urllib.parse import urlencode
import datetime
import requests
import aiohttp
from aiohttp.client_exceptions import ContentTypeError, ClientOSError
from requests.exceptions import JSONDecodeError
from .auth import CloudFlow


def _build_service(**kwargs):
    return CloudFlow(**kwargs)


class HTTPClient(ABC):
    """Abstract Base Class for performing HTTP requests"""

    @abstractmethod
    async def get(self, endpoint: str, params: Optional[Mapping[str, str]] = None):
        """Abstract method for GET requests"""

    @abstractmethod
    async def post(
        self, endpoint: str, body: Optional[Mapping[str, Any]] = None
    ) -> Dict[str, Any]:
        """Abstract method for POST requests"""

    @abstractmethod
    async def put(
        self, endpoint: str, body: Optional[Mapping[str, Any]] = None
    ) -> Dict[str, Any]:
        """Abstract method for PUT requests"""

    @abstractmethod
    async def delete(self, endpoint: str):
        """Abstract method for DELETE requests"""


class AsyncClient(HTTPClient):
    def __init__(self, **kwargs):
        self.flow = _build_service(**kwargs)
        # self._session = aiohttp.ClientSession()
        self._sync_session = requests.Session()
        self.folder_id: int = None  # type: ignore
        self.tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    def _folder_header(self) -> Dict[str, str]:
        if not self.folder_id:
            raise AttributeError(
                "A folder id is needed to perform this operation. 'client.folder_id' attribute is set to None."
            )
        return {"X-UIPATH-OrganizationUnitId": f"{self.folder_id}"}

    def prepare_headers(self) -> Dict[str, str]:
        content_header = self.flow.content_header()
        auth_header = self.flow.auth_headers()
        folder_header = self._folder_header() if self.folder_id else {}
        try:
            headers = content_header | auth_header | folder_header
        except TypeError:  # different python version
            headers = {**content_header, **auth_header, **folder_header}
        return headers

    def prepare_url(
        self, endpoint: str, params: Optional[Mapping[str, str]] = None
    ) -> str:
        """Preparse the url depending on the base_url"""
        if params:
            encoded_params = urlencode(params)
            return f"{self.flow._base_url}{endpoint}?{encoded_params}"
        return f"{self.flow._base_url}{endpoint}"

    async def _internall_call(
        self, method: str, url: str, body: Optional[Mapping[str, Any]] = None
    ) -> Dict[str, Any]:
        if self.flow.token_expires() or not self.flow.authenticated:
            self.flow.auth()
        headers = self.prepare_headers()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method, url=url, json=body, headers=headers
                ) as resp:
                    resp.raise_for_status()
                    print(f"The request return with status {resp.status}")
                    try:
                        json_string = await resp.json()
                        return json_string

                    except ContentTypeError as err:
                        text = await resp.text()
                        if text == "":
                            return {}
                        raise err
        except ClientOSError as err:
            print(err)

    def _sync_internall_call(
        self, method: str, url: str, body: Optional[Mapping[str, Any]] = None
    ):
        if self.flow.token_expires() or not self.flow.authenticated:
            self.flow.auth()
        headers = self.prepare_headers()
        print(f"Synchronous url: {url}")
        resp = self._sync_session.request(
            method=method, url=url, json=body, headers=headers
        )
        resp.raise_for_status()
        try:
            data = resp.json()
            return data
        except JSONDecodeError as err:
            if resp.text:
                return {}
            raise err

    def sync_get(self, endpoint: str, params: Optional[Mapping[str, str]] = None):
        url = self.prepare_url(endpoint, params=params)
        json_string = self._sync_internall_call("GET", url)
        return json_string

    async def get(self, endpoint: str, params: Optional[Mapping[str, str]] = None):
        url = self.prepare_url(endpoint, params=params)
        json_string = await self._internall_call("GET", url)
        return json_string

    async def post(self, endpoint: str, body: Optional[Mapping[str, str]] = None):
        url = self.prepare_url(endpoint)
        json_string = await self._internall_call("POST", url, body=body)
        return json_string

    async def delete(self, endpoint: str):
        url = self.prepare_url(endpoint)
        json_string = await self._internall_call("DELETE", url)
        return json_string

    async def put(self, endpoint: str, body: Optional[Mapping[str, str]] = None):
        url = self.prepare_url(endpoint)
        json_string = await self._internall_call("PUT", url, body)
        return json_string
