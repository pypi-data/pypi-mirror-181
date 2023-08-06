from __future__ import annotations
import datetime
import json
import logging
import requests
from pprint import pprint
from typing import Any, Literal, Mapping, Union, List, Optional, Set
from uuid import uuid4
from urllib.parse import urlencode
import asyncio
import aiohttp
import httpx
from dateutil.parser import parse

from .client import AsyncClient
from .resource import Resource


def format_date(date_str: str) -> Any:
    """Auxiliar function to parse a date with timezone offset"""
    # tz = time.tzname[0]
    return parse(date_str)


class QueueItem(Resource):
    """Class to handle a QueueItem type Resource"""
    _type = "queue_item"
    _def_endpoint = "/odata/QueueItems({id})"

    # pylint: disable=redefined-builtin, broad-except
    def __init__(self, id: int, name: str, client: AsyncClient, queue: Queue, item_data: dict[str, Any]):
        super().__init__(id, name, self._type)
        self.client = client
        self.queue = queue
        self.item_data = item_data
        self.reference = item_data["Reference"]
        try:
            self.creation_date = format_date(item_data["CreationTime"])
        except Exception:
            self.creation_date = item_data["CreationTime"]
        self.status = item_data["Status"]

    def __hash__(self):
        return hash((self.reference, self.id))

    def info(self):
        return self.item_data

    def key(self):
        return self.item_data["Key"]

    async def refresh(self):
        endpoint = self._def_endpoint.format(id=self.id)
        data = await self.client.get(endpoint=endpoint)
        self.item_data = data
        self.status = data["Status"]

    def _prepare_body_edit_item(self, priority, content: Mapping[str, Any], ref, prog: str = ""):
        body = {
            "Name": self.queue.name,
            "Priority": priority,
            "SpecificContent": content,
            "Reference": ref,
            "Progress": prog
        }
        return body

    def edit(self, content: Mapping[str, Any], priority: str = "", progress: str = "", reference: str = "") -> QueueItem:
        """Edits the QueueItem.
        :param content: the SpecificContent of the QueueItem
        :type content: Mapping[str, Any]
        :param priority: optional new Priority attribute
        :type priority: str
        :param progress: optional new Progress attribute
        :type progress: str
        :param reference: optional new Reference attribute
        :type reference: str
        """
        if self.status not in ("New", "Failed", "Abandoned"):
            raise TypeError("Only New, Failed and Abandoned queue items are editable.")
        if not priority:
            priority = self.item_data["Priority"]
        if not progress:
            progress = self.item_data["Progress"]
        if not reference:
            reference = self.item_data["Reference"]
        body = self._prepare_body_edit_item(
            priority,
            content,
            reference,
            progress
        )
        self.client.put(endpoint=self._def_endpoint.format(id=self.id), body=body)
        self.item_data["SpecificContent"] = content
        self.item_data["Priority"] = priority
        self.reference = reference
        return self

    async def delete(self):
        await self.client.delete(endpoint=self._def_endpoint.format(id=self.id))

    @staticmethod
    async def _prepare_result_body_success() -> dict[str, Any]:
        success_body = {
            "transactionResult": {
                "IsSuccessful": True,
            }
        }
        return success_body

    @staticmethod
    async def _prepare_result_body_failure(reason: str, details: str, exc: str, fail: str):
        failure_body = {
            "transactionResult": {
                "IsSuccessful": False,
                "ProcessingException": {
                    "Reason": reason,
                    "Details": details,
                    "Type": exc,

                },
                "Output": {
                    "fail_reason": fail
                }

            }
        }
        return failure_body

    async def set_transaction_result(self, success: bool, reason: str = "", details: str = "", exception_type: str = "BusinessRuleException", failure: str = ""):

        queue_item_endpoint = f"/odata/Queues({self.id})"
        uipath_svc = "/UiPathODataSvc.SetTransactionResult"
        endpoint = queue_item_endpoint + uipath_svc
        if success:
            body = await self._prepare_result_body_success()
            self.status = "Successful"
            # add to the queue items pool if successful
            self.queue.items.append(
                QueueItem(
                    id=self.id,
                    name=self.name,
                    client=self.client,
                    queue=self.queue,
                    item_data=self.item_data)
            )
        else:
            body = await self._prepare_result_body_failure(reason, details, exception_type, failure)
            self.status = "Failed"
        data = await self.client.post(endpoint=endpoint, body=body)
        return data


class Queue(Resource):
    """Class to manage a Queue type Resource"""
    _MAX_ITEMS = 1000
    _type = "queue_definition"
    _def_endpoint = "/odata/QueueDefinitions({id})"

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, name: str, client: AsyncClient):
        super().__init__(id, name, self._type)
        self.client = client
        self.items = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *details):
        # await self.client._session.close()
        return self
    def info(self):
        return self.queue_data

    def key(self):
        return self.queue_data["Key"]

    async def refresh(self):
        endpoint = self._def_endpoint.format(id=self.id)
        async with self.client.get(endpoint=endpoint) as resp:
            data = await resp.json()
        data = self.client.get(
            self._def_endpoint.format(id=self.id)
        )
        self.queue_data = data
        if self.name != data["Name"]:
            logging.warning(f"User tried to overwrite Queue name <{data['Name']}> with <{self.name}>.")
        self.name = data["Name"]

    async def add(self, content: Mapping[str, Union[str, int]], priority: str = "Normal", references: Optional[List[str]] = None, batch_id: str = "", separator: str = "-") -> QueueItem:

        if not batch_id:
            batch_id = str(uuid4())
        body = self._format_new_queue_item_body(
            content=content,
            priority=priority,
            refs=references,
            batch_id=batch_id,
            separator=separator
        )
        endpoint = "/odata/Queues/UiPathODataSvc.AddQueueItem"
        data = self.client.post(
            endpoint,
            body=body
        )
        queue_item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            queue=self,
            item_data=data
        )
        return queue_item

    def _format_new_queue_item_body(self, content, priority: Optional[str] = None, refs: Optional[List[str]] = None, batch_id: str = "", separator: str = "-"):
        ref_id = str(uuid4())
        body_add = {
            "itemData": {
                "Priority": priority,
                "Name": self.name,
                "SpecificContent": content,
            }
        }
        if refs:
            reference = ""
            for ref in refs:
                try:
                    ref_value = body_add["itemData"]["SpecificContent"][ref]
                except KeyError as exc:
                    raise ValueError(f"Invalid reference: {ref} not found as attribute in SpecificContent") from exc
                reference += str(ref_value) + separator
                body_add["itemData"]["Reference"] = f"{reference[:-1]}#{batch_id}"
                body_add["itemData"]["SpecificContent"]["ItemID"] = reference[:-1]
                body_add["itemData"]["SpecificContent"]["ReferenceID"] = ref_id
                body_add["itemData"]["SpecificContent"]["BatchID"] = batch_id
        return body_add

    def filter(self, df, reference):
        """TODO: filter a dataframe with reference with item pool to 
        avoid checking for duplicate"""
        if not self.items:
            processed_items = self.sync_item_pool()

        

    @staticmethod
    def _validate_status(status):
        STATUS = ["In Progress", "New", "Abandoned", "Deleted", "Retried", "Successful"]
        for s in status:
            if s not in STATUS:
                raise ValueError(f"Invalid status: '{s}")


    async def _format_transaction_body(self, machine_identifier, content, batch_id, refs: Optional[List[str]] = None, separator: Optional[str] = "-") -> dict[str, Any]:
        ref_id = str(uuid4())
        body_start = {
            "transactionData": {
                "Name": self.name,
                "RobotIdentifier": machine_identifier,
                "SpecificContent": content
            }
        }
        if refs:
            reference = ""
            for ref in refs:
                try:
                    ref_value = body_start["transactionData"]["SpecificContent"][ref]
                except KeyError as exc:
                    raise ValueError(f"Invalid reference: {ref} not found as attribute in SpecificContent") from exc
                reference += f"{str(ref_value)}{separator}"
            body_start["transactionData"]["Reference"] = f"{reference[:-1]}#{batch_id}"
            body_start["transactionData"]["SpecificContent"]["ItemID"] = reference[:-1]
            body_start["transactionData"]["SpecificContent"]["ReferenceID"] = ref_id
            body_start["transactionData"]["SpecificContent"]["BatchID"] = batch_id
        return body_start

    async def start(self, machine_identifier: str, content: Mapping[str, Union[str, int]], batch_id: str = "", references: Optional[List[str]] = None, separator="-") -> QueueItem:
        """Starts a new transaction and sends back the item to be processed. 
        **Note:** If the parameter references is empty it will not have :code:`ItemID`, :code:`ReferenceID` and :code:`BatchID`.
        :param machine_identifier: the unique identifier of your machine. 
        :param content: the SpecificContent attrubitue of you transaction.
        :param batch_id: an optional unique id for batch transactions.
        :param references: an optional list of references to be hashed. 
        :param separator: an optional character to hash the references.
        :type machine_identifier: str. 
        :type content: Mapping[str, Union[str, int]].
        :type batch_id: str.
        :type references: Optional[List[str]]. 
        :type separator: str.
        :rtype: QueueItem
        """
        if not batch_id:
            batch_id = str(uuid4())
        endpoint = "/odata/Queues/UiPathODataSvc.StartTransaction"
        body = await self._format_transaction_body(  # type: ignore
            machine_identifier=machine_identifier,
            content=content,
            batch_id=batch_id,
            refs=references,
            separator=separator
        )
        data = await self.client.post(
            endpoint,
            body=body
        )
        # pprint(data)
        queue_item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            queue=self,
            item_data=data
        )
        return queue_item

    def _process_queue_item_params(self, options: Optional[dict[str, str]] = None):
        filter_params = {
            "$filter": f"QueueDefinitionId eq {self.id}"
        }
        mod_filter_params = filter_params.copy()
        if options and ("$filter" in options):
            # if a filter flag is passed we need to modify it to only get
            # the elements of the Queue and delete it afterwards to prevent
            # getting all queue items for all queues (default by API).
            filter_params["$filter"] += f" and {options['$filter']}"
            del options["$filter"]  # type: ignore
            try:
                mod_filter_params = filter_params | options
            except TypeError:
                mod_filter_params = {**filter_params, **options}
        if options and ("$select" in options):
            del options["$select"]
            logging.warning("'$select' in options detected. Ignoring the parameter.")
            try:
                mod_filter_params = filter_params | options
            except TypeError:
                mod_filter_params = {**filter_params, **options}
        return mod_filter_params

    async def _get_queue_items_content(self, options: Optional[dict[str, Any]] = None):
        params = self._process_queue_item_params(options=options)
        endpoint = "/odata/QueueItems"
        data = await self.client.get(
            endpoint,
            params=params
        )
        queue_items = list(QueueItem(id=item["Id"], name=self.name, client=self.client, queue=self, item_data=item) for item in data["value"])
        count = data["@odata.count"]
        if count < self._MAX_ITEMS:
            return [], queue_items
        pages = count // self._MAX_ITEMS if count > self._MAX_ITEMS else 0
        offset = 0
        async with httpx.AsyncClient() as client:
            urls = []
            for _ in range(pages):
                try:
                    new_params = params | {"$skip": self._MAX_ITEMS + offset}
                except TypeError:
                    new_params = {**params, "$skip": self._MAX_ITEMS + offset}
                new_url = self.client.prepare_url(endpoint, new_params)
                urls.append(new_url)
                offset += self._MAX_ITEMS

            headers = self.client.prepare_headers()
            tasks = [await client.get(url, headers=headers) for url in urls]
            json_strings = [json.loads(task.text) for task in tasks]
        return json_strings, queue_items

    def sync_item_pool(self, days_from: int = 2) -> List[QueueItem]:
        options = {
            "$filter": "Status in ('New', 'Abandoned', 'Retried', 'InProgress', 'Deleted', 'Successful')",
            "$orderby": "CreationTime"
        }
        params = self._process_queue_item_params(options=options)
        endpoint = "/odata/QueueItems"
        data = self.client.sync_get(
            endpoint,
            params=params
        )
        queue_items = list(QueueItem(id=item["Id"], name=self.name, client=self.client, queue=self, item_data=item) for item in data["value"])
        count = data["@odata.count"]
        if count < self._MAX_ITEMS:
            return [], queue_items
        pages = count // self._MAX_ITEMS if count > self._MAX_ITEMS else 0
        offset = 0 
        urls = []
        for _ in range(pages):
            try:
                new_params = params | {"$skip": self._MAX_ITEMS + offset}
            except TypeError:
                new_params = {**params, "$skip": self._MAX_ITEMS + offset}
            new_url = f"{endpoint}?{urlencode(new_params)}"
            urls.append(new_url)
            offset += self._MAX_ITEMS

        resps = [self.client.sync_get(url) for url in urls]
        for resp in resps:
            for elem in resp["value"]:
                item = QueueItem(id=elem["Id"], name=self.name, client=self.client, queue=self, item_data=elem)
                queue_items.append(item)
        filtered = [elem for elem in queue_items if (datetime.datetime.now(self.client.tz) - elem.creation_date).days <= days_from]
        self.items = filtered
        return filtered            

    async def item_pool(self, days_from: int = 2) -> Set[QueueItem]:
        """Asynchronously retrieves the QueueItem resiyrces if the queue. 
        Default behaviour is to retrieve all of them using :code:`@odata.count` as a pagination parameter.
        Retrieves those items with status New, Abandoned, Retried, InProgress, Deleted and Successful

        :param days_from: optional parameter to indicate how many days ago to query from (default = 2)
        :type days_from: int 
        :rtype: Set[QueueItem]
        """
        options = {
            "$filter": "Status in ('New', 'Abandoned', 'Retried', 'InProgress', 'Deleted', 'Successful')",
            "$orderby": "CreationTime"
        }
        data, queue_items = await self._get_queue_items_content(options=options)
        for page in data:
            for elem in page["value"]:
                item = QueueItem(id=elem["Id"], name=self.name, client=self.client, queue=self, item_data=elem)
                queue_items.append(item)
        filtered = [elem for elem in queue_items if (datetime.datetime.now(self.client.tz) - elem.creation_date).days <= days_from]
        self.items = filtered
        return filtered

    async def get_item(self, id: int, options: Optional[Mapping[str, str]] = None) -> QueueItem:
        """Retrieves a single QueueItem resource given its id.

        :param id: the item id.
        :type id: int
        :param options: and optional dictionary of odata query options.
        :type options: Optional[Mapping[str, str]]
        :rtype: QueueItem
        """
        endpoint = f"/odata/QueueItems({id})"
        data = await self.client.get(endpoint=endpoint, params=options)
        item = QueueItem(id=data["Id"], name=self.name, client=self.client, queue=self, item_data=data)
        return item

    def check_duplicate(self, reference):
        """Checks whether an element has appeared in the Queue with status
        Successful, New, Abandoned, In Progress or Retried. If it has been found, it returns it

        :param reference: the reference value of the item to compare to the pool.
        :type reference: str
        """
        for item in set(self.items):
            if item.reference and (reference in item.reference):
                return item
        return False

    def edit(self, content):
        """Edits a Queue"""
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class Folder(Resource):
    """Class to handle a Folder type Resource"""
    _type = "folder"
    def_endpoint = "/odata/Folders({id})"

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, name: str, client: AsyncClient, folder_data: dict[str, str]):
        super().__init__(id, name, self._type)
        self.client = client
        self.folder_data = folder_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, *details):
        # await self.client._session.close()
        return self

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.folder_data

    def key(self):
        return self.folder_data["Key"]

    async def refresh(self):
        endpoint = self.def_endpoint.format(id=self.id)
        data = await self.client.get(endpoint=endpoint)
        self.folder_data = data
        self.name = data["DisplayName"]

    def set_queue(self, id: int) -> Queue:
        endpoint = f"/odata/QueueDefinitions({id})"
        data = self.client.sync_get(endpoint)
        return Queue(id=data["Id"], name=data["Name"], client=self.client)

    async def get_queue(self, id: int, options: Optional[Mapping[str, str]] = None) -> Queue:
        endpoint = f"/odata/QueueDefinitions({id})"
        data = await self.client.get(endpoint=endpoint, params=options)
        queue = Queue(id=data["Id"], name=data["Name"], client=self.client)
        return queue

    async def get_asset(self, id: int, options: Optional[Mapping[str, str]] = None) -> Asset:
        endpoint = f"/odata/Assets({id})"
        data = await self.client.get(endpoint=endpoint, params=options)
        return Asset(id=data["Id"], name=data["Name"], client=self.client, asset_data=data)

    def set_asset(self, id: int, options: Optional[Mapping[str, str]] = None) -> Asset:
        endpoint = f"/odata/Assets({id})"
        headers = self.client.prepare_headers()
        url = self.client.prepare_url(endpoint, params=options)
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return Asset(id=data["id"], name=data["Name"], client=self.client, asset_data=data)

    def _create_body(self, name, value, value_type, description):
        attr_value = value_type
        if value_type == "Text":
            attr_value = "String"
        elif value_type == "Integer":
            attr_value = "Int"
        body = {
            "Name": name,
            "ValueScope": "Global",
            "ValueType": value_type,
            f"{attr_value}Value": value,
            "Description": description
        }
        return body

    # def create_asset(self, name: str, value: Union[str, bool, int], value_type: Literal["Text", "Integer", "Bool"], description: str = "") -> Asset:
        # assert value_type in ("Text", "Integer", "Bool")
        # body = self._create_body(name, value, value_type, description)
        # data = self.client.post(
        #     endpoint="/odata/Assets",
        #     body=body
        # )
        # asset = Asset(id=data["Id"], name=data["Name"], client=self.client, asset_data=data)
        # return asset

    def edit(self, content):
        """Edits an Folder"""
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class Asset(Resource):
    """Class to handle an Asset type Resource"""
    _type = "asset"
    _def_endpoint = "/odata/Assets({id})"

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, name: str, client: AsyncClient, asset_data: dict[str, str]):
        super().__init__(id, name, self._type)
        self.client = client
        self.asset_data = asset_data
        self.value = asset_data["Value"]
        self.value_type = asset_data["ValueType"]

    def info(self):
        return self.asset_data

    def key(self):
        return self.asset_data["Key"]

    def refresh(self):
        data = self.client.get(
            self._def_endpoint.format(id=self.id)
        )
        self.asset_data = data
        self.value = data["Value"]

    def _prepare_edit_body(self, value, name, description):
        formatted_body = self.asset_data.copy()
        formatted_body["Description"] = description if description else formatted_body["Description"]
        if self.value_type == "Credential":
            raise ValueError("Attempted to edit Asset resource with ValueType='Credential'.")
        if self.value_type == "Integer":
            assert isinstance(value, int)
            formatted_body["IntValue"] = str(value)
            formatted_body["Value"] = str(value) if value else formatted_body["Value"]
            formatted_body["Name"] = name if name else formatted_body["Name"]
        elif self.value_type == "Bool":
            assert isinstance(value, bool)
            formatted_body["BoolValue"] = str(value)
            formatted_body["Value"] = str(value) if value else formatted_body["Value"]
            formatted_body["Name"] = name if name else formatted_body["Name"]
        elif self.value_type == "Text":
            formatted_body["StringValue"] = value
            formatted_body["Value"] = value if value else formatted_body["Value"]
            formatted_body["Name"] = name if name else formatted_body["Name"]
        else:
            raise Exception("Unrecognized value_type.")
        return formatted_body

    def edit(self, value: Optional[Union[str, int, bool]] = "", name: Optional[str] = None, description: Optional[str] = None):  # type: ignore
        """Edits a Resource of type Asset.

        :param value: optional value (str, int, bool) to edit the Asset.
        :param name: optional name to edit the Asset.
        :param description: optional description to edit the Asset.
        """
        body = self._prepare_edit_body(value=value, name=name, description=description)
        self.client.put(
            self._def_endpoint.format(id=self.id),
            body=body
        )
        self.refresh()

    def delete(self):
        self.client.delete(
            self._def_endpoint.format(id=self.id)
        )


class Orchestrator:
    """Creates an Orchestrator object. 
    If no parameters are passed, it forces authentication via one of the credential methods. 
    Otherwise, you need to provide together with the `auth` parameter, the necessary keyword
    arguments to authentication depending on the value of `auth` you provided.
    Check the documentation for the different types of authentication flows (`CloudFlow` 
    and `CustomFlow`)
    Optional parameters:

    :param auth: authentication type ('cloud', 'custom', 'premise').
    :param client_id: client id for oauth authentication type.
    :param refresh_token: refresh token for cloud authentication type.
    :param tenant_name: orchestrator tenant name
    :param organization: your organization name
    :param username: username for on-premise authentication type
    :param password: password for on-premise authentication type
    :param base_url: base url for custom or premise authentication type
    """
    client: Client = None  # type: ignore
    _auth_methods = ("cloud", "premise", "custom")

    def __init__(self, **kwargs):
        if not kwargs:
            return
        self.client = AsyncClient(**kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *details):
        # await self.client._session.close()
        return self
    def from_oauth_credentials(self, tenant_name: str, client_id: str, refresh_token: str, organization: str):
        """Authenticates a client using default cloud base_url.
        :param tenant_name: orchestrator tenant name.
        :param client_id: client id for oauth authentication type.
        :param refresh_token: refresh token for cloud authentication type.
        :param organization: your organization name.
        """
        if self.client:
            return self
        self.client = AsyncClient(tenant_name=tenant_name, client_id=client_id, refresh_token=refresh_token, organization=organization)
        self.client.flow.authenticated = True
        return self

    def auth(self):
        if not self.client: 
            raise ValueError("You are no authenticated yet")
        self.client.flow.auth()
        return self

    def from_custom_credentials(self, tenant_name: str, client_id: str, refresh_token: str, base_url: str, organization: str):
        """Authenticates a client using custom base_url

        :param tenant_name: orchestrator tenant name.
        :param client_id: client id for oauth authentication type.
        :param refresh_token: refresh token for cloud authentication type.
        :param organization: your organization name.
        :param base_url: a custom base_url for your orchestrator.
        """
        raise NotImplementedError

    async def from_on_premise_credentials(self):
        """Authenticates a client using on-premise credentials"""
        raise NotImplementedError

    # @raise_no_client
    async def get_folders(self, options: Optional[Mapping[str, str]] = None):
        """Returns a set of Folders resources

        :param options: an optional dictionary of odata query options.
        """
        if self.client is None:
            raise ValueError("You need to authenticate yourself first!")
        endpoint = "/odata/Folders"
        data = await self.client.get(endpoint, options)
        try:
            return [Folder(id=folder["Id"], name=folder["DisplayName"], folder_data=folder, client=self.client) for folder in data["value"]]
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either field in the '$select' parameter."
            raise ValueError(msg) from err

    def set_folder(self, folder_id) -> Folder:
        endpoint = f"/odata/Folders({folder_id})"
        data = self.client.sync_get(endpoint)
        self.client.folder_id = data["Id"]
        return Folder(id=data["Id"], name=data["DisplayName"], client=self.client, folder_data=data)

    async def get_folder(self, id: int, options: Optional[Mapping[str, str]] = None):
        """Returns a Folder resource based on its id

        :param id: the folder id.
        :param options: optional dictionary of odata query options.
        """
        if self.client is None:
            raise ValueError("You need to authenticate yourself first!")
        # pylint: disable=redefined-builtin
        endpoint = f"/odata/Folders({id})"
        data = await self.client.get(endpoint, options)
        self.client.folder_id = id
        return Folder(id=data["Id"], name=data["DisplayName"], client=self.client, folder_data=data)
        # try:
        #     return Folder(id=data["Id"], name=data["DisplayName"], folder_data=data, client=self.client)
        # except KeyError as err:
        #     msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either field in the '$select' parameter."
        #     raise ValueError(msg) from err
