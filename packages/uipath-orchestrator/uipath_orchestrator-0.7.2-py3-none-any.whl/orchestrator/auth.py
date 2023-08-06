"""Module to perform authentication to Orchestrator's API"""
# pylint: disable=locally-disabled, line-too-long, invalid-name, too-many-instance-attributes
from __future__ import annotations
from typing import Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod
import datetime
import json
import requests


class Flow(ABC):
    """Base class for different authentication flows"""

    @abstractmethod
    def content_header(self) -> Dict[str, str]:
        """Creates the content header"""

    @abstractmethod
    def prepare_body(self) -> Dict[str, str]:
        """Prepares the body for authentication"""

    @abstractmethod
    def auth_headers(self) -> Dict[str, str]:
        """Prepares the auth header"""

    @abstractmethod
    def _get_token(self) -> None:
        """Abstract method for retrieven the access token"""

    @abstractmethod
    def token_expires(self) -> bool:
        """Abstract method for checking whether an access token has expired"""

    @abstractmethod
    def auth(self) -> None:
        """Abstract class method for authenticating"""


@dataclass
class CloudFlow(Flow):
    """Base class to parse and manage attributes for cloud type
    authentication"""

    client_id: str
    refresh_token: str
    tenant_name: str
    organization: str
    base_url = "https://cloud.uipath.com"
    token_url = "https://account.uipath.com"
    _token_endpoint = "/oauth/token"
    expires = datetime.datetime.now()
    authenticated: bool = False
    _access_token = ""

    def __post_init__(self):
        self.base_url = f"{self.base_url}/{self.tenant_name}/{self.organization}"
        self.token_url = f"{self.token_url}{self._token_endpoint}"

    def content_header(self):
        return {"Content-Type": "application/json"}

    def prepare_body(self) -> dict[str, str]:
        return {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
        }

    def auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._access_token}"}

    def _get_token(self) -> None:
        body = self.prepare_body()
        headers = self.content_header()
        url = self.token_url
        r = requests.post(url=url, data=json.dumps(body), headers=headers, timeout=10)
        r.raise_for_status()
        token_data = r.json()
        token = token_data["access_token"]
        expiracy = token_data["expires_in"]
        self._access_token = token
        self.authenticated = True
        self.expires = self.expires + datetime.timedelta(seconds=expiracy)

    def token_expires(self) -> bool:
        """Checks whether the access_token has expired already"""
        now = datetime.datetime.now()
        if now > self.expires:
            return True
        return False

    def auth(self):
        self._get_token()


@dataclass
class CustomFlow:
    """Base class to parse and manage attributes for custom type
    authentication"""

    client_id: str
    refresh_token: str
    tenant_name: str
    organization: str
    base_url: str
    token_url = "https://account.uipath.com"
    _token_endpoint = "/oauth/token"
    expires = datetime.datetime.now()
    authenticated = False
    _access_token = ""

    def __post_init__(self):
        self.base_url = f"{self.base_url}/{self.tenant_name}/{self.organization}"
        self.token_url = f"{self.token_url}{self._token_endpoint}"

    @staticmethod
    def content_header() -> dict[str, str]:
        """Prepares the Content-Type header for the requests (application/json)"""
        return {"Content-Type": "application/json"}

    def prepare_body(self) -> dict[str, str]:
        """Prepares the body to perform the authentication request."""
        return {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
        }

    def auth_headers(self) -> dict[str, str]:
        """Prepares the Authorization header for subsequent requests"""
        return {"Authorization": f"Bearer {self._access_token}"}

    def _get_token(self) -> None:
        body = self.prepare_body()
        headers = self.content_header()
        url = self.token_url
        r = requests.post(url=url, data=json.dumps(body), headers=headers, timeout=10)
        if r.status_code != 200:
            token_data = r.json()
            raise Exception("Something went wrong")
        token_data = r.json()
        token = token_data["access_token"]
        expiracy = token_data["expires_in"]
        self._access_token = token
        self.authenticated = True
        self.expires = self.expires + datetime.timedelta(seconds=expiracy)

    def token_expires(self) -> bool:
        """Checks the expiracy time of the current access_token"""
        now = datetime.datetime.now()
        if now > self.expires:
            return True
        return False

    def auth(self):
        """Performs CustomFlow authentication."""
        self._get_token()


@dataclass
class OnPremiseFlow:
    """Base class to parse and manage attributes for on-premise type authentication"""

    _TIMEOUT = 30 * 60  # 30 minutes
    username: str
    password: str
    tenant_name: str
    orchestrator_url: str
    auth_endpoint = "/api/Account/Authenticate"
    expires = datetime.datetime.now()
    authenticated: bool = False
    _access_token: str = ""

    def __post_init__(self):
        self.token_url = f"{self.orchestrator_url}{self.auth_endpoint}"
        self.base_url = f"{self.orchestrator_url}{self.tenant_name}"

    @staticmethod
    def content_header() -> dict[str, str]:
        """Prepares the Content-Type header for the requests (application/json)"""
        return {"Content-Type": "application/json"}

    def prepare_body(self) -> dict[str, str]:
        """Prepares the body to perform the OnPremise authentication request."""
        return {
            "tenancyName": self.tenant_name,
            "usernameOrEmailAddress": self.username,
            "password": self.password,
        }

    def auth_headers(self) -> dict[str, str]:
        """Prepares the Authorization header for subsequent requests"""
        return {"Authorization": f"Bearer {self._access_token}"}

    def _get_token(self):
        body = self.prepare_body()
        headers = self.content_header()
        r = requests.post(url=self.token_url, headers=headers, json=body, timeout=10)
        r.raise_for_status()
        token_data = r.json()
        self._access_token = token_data["result"]
        self.authenticated = True
        self.expires = self.expires + datetime.timedelta(
            seconds=self._TIMEOUT
        )

    def auth(self):
        """Performs OnPremise authentication"""
        self._get_token()

    def token_expires(self) -> bool:
        """Checks whether the access_token has expired already"""
        now = datetime.datetime.now()
        if now > self.expires:
            return True
        return False