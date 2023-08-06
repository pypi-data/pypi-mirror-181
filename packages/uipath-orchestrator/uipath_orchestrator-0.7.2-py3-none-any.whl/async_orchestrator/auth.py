from __future__ import annotations
from typing import Dict
from dataclasses import dataclass

from abc import ABC, abstractmethod
import datetime 
import json 
import requests
import aiohttp


class Flow(ABC):

    @abstractmethod 
    def content_header(self) -> Dict[str, str]:
        """Creates content header"""

    @abstractmethod
    def prepare_body(self) -> Dict[str, str]:
        """Prepares the body for authentication"""

    @abstractmethod
    def auth_headers(self) -> Dict[str, str]:
        """Prepares the auth header"""
    @abstractmethod
    async def _get_token(self) -> None:
        """Abstract method for retrieven the access token"""
    @abstractmethod
    def token_expires(self) -> bool:
        """Abstract method for checking whether an access token has expired"""
    @abstractmethod
    async def auth(self) -> None:
        """Abstract class method for authenticating"""


@dataclass
class CloudFlow(Flow):
    client_id: str 
    refresh_token: str 
    tenant_name: str 
    organization: str 
    _base_url = "https://cloud.uipath.com"
    _token_url = "https://account.uipath.com"
    _token_endpoint = "/oauth/token"
    _access_token = ""
    expires = datetime.datetime.now()
    authenticated: bool = False

    def __post_init__(self):
        self._base_url = f"{self._base_url}/{self.tenant_name}/{self.organization}"
        self._token_url = f"{self._token_url}{self._token_endpoint}"

    @staticmethod
    def content_header():
        return {"Content-Type": "application/json"}

    def prepare_body(self) -> Dict[str, str]:
        return {"grant_type": "refresh_token", "client_id": self.client_id, "refresh_token": self.refresh_token}

    def auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._access_token}"}

    def _get_token(self):
        body = self.prepare_body()
        headers = self.content_header()
        url = self._token_url
        print(url)
        resp = requests.post(url=url, headers=headers, json=body)
        resp.raise_for_status()
        json_string = resp.json()
        self._access_token = json_string["access_token"]
        self.authenticated = True 
        self.expires = self.expires + datetime.timedelta(seconds=json_string["expires_in"])

    def token_expires(self) -> bool:
        now = datetime.datetime.now()
        if now > self.expires:
            return True 
        return False

    def auth(self):
        self._get_token()
