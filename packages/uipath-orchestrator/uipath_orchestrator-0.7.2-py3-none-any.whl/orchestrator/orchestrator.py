# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, invalid-name, too-many-arguments, trailing-whitespace
"""Orchestrator Module: A client to interact with Orchestrator's API. This module contains different
Resources to interact at different levels.
To start it is recommended that you instantiate an :code:`Orchestrator` object, and from it instantiate other
Resources you may need along the way. For example, to get to a specific :code:`QueueItem` object, we need first to naviage to the folder where this
:code:`QueueItem` is located; then we need to the the :code:`Queue` it belongs, to finally access it.
"""

from __future__ import annotations
import os
from pprint import pprint
import datetime
import json
import logging
from typing import Any, Literal, Mapping, Union, List, Optional, Set, Dict
from uuid import uuid4
import asyncio
import httpx
from dateutil.parser import parse
# from cron_descriptor import get_description

from .client import Client
from .orchestrator_resource import Resource


def format_date(date_str: str) -> Any:
    """Auxiliar function to parse a date with timezone offset"""
    # tz = time.tzname[0]
    return parse(date_str)


class QueueItem(Resource):
    """Class to handle a QueueItem type Resource"""

    _type = "queue_item"
    _def_endpoint = "/odata/QueueItems({id})"

    # pylint: disable=redefined-builtin, broad-except
    def __init__(
        self,
        id: Union[int, str],
        name: str,
        client: Client,
        queue: Queue,
        item_data: dict[str, Any],
    ):
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

    def refresh(self):
        data = self.client.get(self._def_endpoint.format(id=self.id))
        self.item_data = data
        self.status = data["Status"]

    def _prepare_body_edit_item(
        self, priority, content: Mapping[str, Any], ref, prog: str = ""
    ):
        body = {
            "Name": self.queue.name,
            "Priority": priority,
            "SpecificContent": content,
            "Reference": ref,
            "Progress": prog,
        }
        return body

    def edit(
        self,
        content: Mapping[str, Any],
        priority: str = "",
        progress: str = "",
        reference: str = "",
    ) -> QueueItem:
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
        body = self._prepare_body_edit_item(priority, content, reference, progress)
        self.client.put(endpoint=self._def_endpoint.format(id=self.id), body=body)
        self.item_data["SpecificContent"] = content
        self.item_data["Priority"] = priority
        self.reference = reference
        return self

    def delete(self):
        self.client.delete(endpoint=self._def_endpoint.format(id=self.id))

    @staticmethod
    def _prepare_result_body_success() -> dict[str, Any]:
        success_body = {
            "transactionResult": {
                "IsSuccessful": True,
            }
        }
        return success_body

    @staticmethod
    def _prepare_result_body_failure(reason: str, details: str, exc: str, fail: str):
        failure_body = {
            "transactionResult": {
                "IsSuccessful": False,
                "ProcessingException": {
                    "Reason": reason,
                    "Details": details,
                    "Type": exc,
                },
                "Output": {"fail_reason": fail},
            }
        }
        return failure_body

    def set_transaction_result(
        self,
        success: bool,
        reason: str = "",
        details: str = "",
        exception_type: str = "BusinessRuleException",
        failure: str = "",
    ):
        """Sets the transaction result of a QueueItem resource. If Successful, it adds the item to the QueueItem pool so continuos duplication checks will work regardless.
        :param success: indicates whether the transaction has been a success. If :code:`True` then no more arguments are needed.
        :type success: bool
        :param reason: (optional) reason why the transaction failed
        :type reason: str
        :param details: (optionl) more details on why the transaction failed
        :type details: str
        :param exception_type: (optional) exception type
        :type exception_type: str
        """
        queue_item_endpoint = f"/odata/Queues({self.id})"
        uipath_svc = "/UiPathODataSvc.SetTransactionResult"
        endpoint = queue_item_endpoint + uipath_svc
        if success:
            body = self._prepare_result_body_success()
            self.status = "Successful"
            # add to the queue items pool if successful
            self.queue.items.append(
                QueueItem(
                    id=self.id,
                    name=self.name,
                    client=self.client,
                    queue=self.queue,
                    item_data=self.item_data,
                )
            )
        else:
            body = self._prepare_result_body_failure(
                reason, details, exception_type, failure
            )
            self.status = "Failed"
        data = self.client.post(endpoint=endpoint, body=body)
        return data


def raise_no_pool(f):
    """Raises an AttributeError if a process which calls Queue.items
    has been called without setting the QueueItem pool."""

    def wrapper(self, *args, **kwargs):
        assert isinstance(self, Queue)
        if not self.items:
            raise AttributeError(
                f"item_pool has been set to False but method '{f.__name__}' of '{type(self).__name__}' requires a QueueItems pool."
            )
        return f(self, *args, **kwargs)

    return wrapper


class Queue(Resource):
    """Class to manage a Queue type Resource"""

    _MAX_ITEMS = 1000
    _type = "queue_definition"
    _def_endpoint = "/odata/QueueDefinitions({id})"

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, name: str, client: Client, item_pool: bool = True):
        super().__init__(id, name, self._type)
        self.client = client
        self.refresh()
        if item_pool:
            # to lookup which ones have already been processed
            self.items = list(asyncio.run(self.get_queue_items_async()))
        self.items = []

    def info(self):
        return self.queue_data

    def key(self):
        return self.queue_data["Key"]

    def refresh(self):
        data = self.client.get(self._def_endpoint.format(id=self.id))
        self.queue_data = data
        if self.name != data["Name"]:
            logging.warning(
                f"User tried to overwrite Queue name <{data['Name']}> with <{self.name}>."
            )
        self.name = data["Name"]

    def add(
        self,
        content: Mapping[str, Union[str, int]],
        priority: str = "Normal",
        references: Optional[List[str]] = None,
        batch_id: str = "",
        separator: str = "-",
    ) -> QueueItem:
        """Adds a new QueueItem resource to the queue with status 'New' and returns it to be processed.
        If references is empty it will not have ItemID, ReferenceID and BatchID
        :param content: the SpecificContent of the item.
        :type content: Mapping[str, Union[str, int]]
        :param priority: optional Priority attribute (default = 'Normal')
        :type priority: str
        :param references: optional list of references.
        :type references: Optional[List[str]]
        :param batch_id: a unique batch identificator.
        :type batch_id: str
        :param separator: optional character to separate the references if any (default = '-').
        :type separator: str
        :rtype: QueueItem
        """
        if not batch_id:
            batch_id = str(uuid4())
        body = self._format_new_queue_item_body(
            content=content,
            priority=priority,
            refs=references,
            batch_id=batch_id,
            separator=separator,
        )
        endpoint = "/odata/Queues/UiPathODataSvc.AddQueueItem"
        data = self.client.post(endpoint, body=body)
        queue_item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            queue=self,
            item_data=data,
        )
        return queue_item

    def _format_new_queue_item_body(
        self,
        content,
        priority: Optional[str] = None,
        refs: Optional[List[str]] = None,
        batch_id: str = "",
        separator: str = "-",
    ):
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
                    raise ValueError(
                        f"Invalid reference: {ref} not found as attribute in SpecificContent"
                    ) from exc
                reference += str(ref_value) + separator
                body_add["itemData"]["Reference"] = f"{reference[:-1]}#{batch_id}"
                body_add["itemData"]["SpecificContent"]["ItemID"] = reference[:-1]
                body_add["itemData"]["SpecificContent"]["ReferenceID"] = ref_id
                body_add["itemData"]["SpecificContent"]["BatchID"] = batch_id
        return body_add

    def _format_transaction_body(
        self,
        machine_identifier,
        content,
        batch_id,
        refs: Optional[List[str]] = None,
        separator: Optional[str] = "-",
    ) -> dict[str, Any]:
        ref_id = str(uuid4())
        body_start = {
            "transactionData": {
                "Name": self.name,
                "RobotIdentifier": machine_identifier,
                "SpecificContent": content,
            }
        }
        if refs:
            reference = ""
            for ref in refs:
                try:
                    ref_value = body_start["transactionData"]["SpecificContent"][ref]
                except KeyError as exc:
                    raise ValueError(
                        f"Invalid reference: {ref} not found as attribute in SpecificContent"
                    ) from exc
                reference += f"{str(ref_value)}{separator}"
            body_start["transactionData"]["Reference"] = f"{reference[:-1]}#{batch_id}"
            body_start["transactionData"]["SpecificContent"]["ItemID"] = reference[:-1]
            body_start["transactionData"]["SpecificContent"]["ReferenceID"] = ref_id
            body_start["transactionData"]["SpecificContent"]["BatchID"] = batch_id
        return body_start

    def start(
        self,
        machine_identifier: str,
        content: Mapping[str, Union[str, int]],
        batch_id: str = "",
        references: Optional[List[str]] = None,
        separator="-",
    ) -> QueueItem:
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
        body = self._format_transaction_body(  # type: ignore
            machine_identifier=machine_identifier,
            content=content,
            batch_id=batch_id,
            refs=references,
            separator=separator,
        )
        data = self.client.post(endpoint, body=body)
        queue_item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            queue=self,
            item_data=data,
        )
        return queue_item

    def _process_queue_item_params(self, options: Optional[dict[str, str]] = None):
        filter_params = {"$filter": f"QueueDefinitionId eq {self.id}"}
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
        data = self.client.get(endpoint, params=params)
        queue_items = set(
            QueueItem(
                id=item["Id"],
                name=self.name,
                client=self.client,
                queue=self,
                item_data=item,
            )
            for item in data["value"]
        )
        count = data["@odata.count"]
        pages = count // self._MAX_ITEMS if count > self._MAX_ITEMS else 0
        offset = 0
        async with httpx.AsyncClient() as client:
            urls = []
            for _ in range(pages):
                try:
                    new_params = params | {"$skip": self._MAX_ITEMS + offset}
                except TypeError:
                    new_params = {**params, "$skip": self._MAX_ITEMS + offset}
                urls.append(self.client.prepare_url(endpoint, new_params))
                offset += self._MAX_ITEMS
            headers = self.client.prepare_headers()
            tasks = (client.get(url, headers=headers) for url in urls)
            resps = await asyncio.gather(*tasks)
        return [json.loads(resp.text) for resp in resps], queue_items

    async def get_queue_items_async(self, days_from: int = 2) -> Set[QueueItem]:
        """Asynchronously retrieves the QueueItem resiyrces if the queue.
        Default behaviour is to retrieve all of them using :code:`@odata.count` as a pagination parameter.

        :param days_from: optional parameter to indicate how many days ago to query from (default = 2)
        :type days_from: int
        :rtype: Set[QueueItem]
        """
        options = {
            "$filter": "Status in ('New', 'Abandoned', 'Retried', 'InProgress', 'Deleted', 'Successful')",
            "$orderby": "CreationTime",
        }
        data, queue_items = await self._get_queue_items_content(options=options)
        for page in data:
            for item in page["value"]:
                item = QueueItem(
                    id=item["Id"],
                    name=self.name,
                    client=self.client,
                    queue=self,
                    item_data=item,
                )
                queue_items.add(item)
        filtered = {
            elem
            for elem in queue_items
            if (datetime.datetime.now(self.client.tz) - elem.creation_date).days
            <= days_from
        }
        return filtered

    def get_queue_items(
        self, options: Optional[dict[str, Any]] = None, days_from=2
    ) -> List[QueueItem]:
        """Synchronously retrieves the QueueItem resource of the queue.
        Default behaviour is to retrieve all of them using @odata.count as a pagination parameter.

        :param options: optional parameter of odata query options. Note: if :code:`$select`
         appears as a key in the :code:`options` parameter, it will get ignored.
        :type options: Optional[dict[str, Any]]
        :param days_from: optional parameter to indicate how many days ago to query from (default = 2)
        :type days_from: int
        :rtype: List[QueueItem]
        """
        params = self._process_queue_item_params(options=options)
        endpoint = "/odata/QueueItems"
        data = self.client.get(endpoint, params=params)
        count = data["@odata.count"]
        # set number of pages to run through all results
        pages = count // self._MAX_ITEMS if count > self._MAX_ITEMS else 0
        init_set = set(
            QueueItem(
                id=item["Id"],
                name=self.name,
                client=self.client,
                queue=self,
                item_data=item,
            )
            for item in data["value"]
        )
        offset = 0
        for _ in range(pages):
            try:
                new_options = params | {"$skip": self._MAX_ITEMS + offset}
            except TypeError:
                new_options = {**params, "$skip": self._MAX_ITEMS + offset}
            data = self.client.get(
                endpoint, self._process_queue_item_params(options=new_options)
            )
            aux_set = set(
                QueueItem(
                    id=item["Id"],
                    name=self.name,
                    client=self.client,
                    queue=self,
                    item_data=item,
                )
                for item in data["value"]
            )
            try:
                init_set = init_set | aux_set
            except TypeError:
                init_set = {**init_set, **aux_set}  # type: ignore
            offset += 1000
        # filter by days_from
        filtered = [
            elem
            for elem in init_set
            if (datetime.datetime.now(self.client.tz) - elem.creation_date).days
            <= days_from
        ]
        return filtered

    def get_item(
        self, id: int, options: Optional[Mapping[str, str]] = None
    ) -> QueueItem:
        """Retrieves a single QueueItem resource given its id.

        :param id: the item id.
        :type id: int
        :param options: and optional dictionary of odata query options.
        :type options: Optional[Mapping[str, str]]
        :rtype: QueueItem
        """
        endpoint = f"/odata/QueueItems({id})"
        data = self.client.get(endpoint, params=options)
        item = QueueItem(
            id=data["Id"],
            name=self.name,
            client=self.client,
            queue=self,
            item_data=data,
        )
        return item

    @raise_no_pool
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


class Asset(Resource):
    """Class to handle an Asset type Resource"""

    _type = "asset"
    _def_endpoint = "/odata/Assets({id})"

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, name: str, client: Client, asset_data: dict[str, str]):
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
        data = self.client.get(self._def_endpoint.format(id=self.id))
        self.asset_data = data
        self.value = data["Value"]

    def _prepare_edit_body(self, value, name, description):
        formatted_body = self.asset_data.copy()
        formatted_body["Description"] = (
            description if description else formatted_body["Description"]
        )
        if self.value_type == "Credential":
            raise ValueError(
                "Attempted to edit Asset resource with ValueType='Credential'."
            )
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
        self.client.put(self._def_endpoint.format(id=self.id), body=body)
        self.refresh()

    def delete(self):
        self.client.delete(self._def_endpoint.format(id=self.id))


class Machine(Resource):
    _type = "machine"
    def_endpoint = "/odata/Machines({key})"

    def __init__(
        self, id: int, name: str, client: Client, machine_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.machine_data = machine_data
        self.machine_key = machine_data["Key"]

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.machine_data

    def key(self):
        return self.machine_data["Key"]

    def refresh(self):
        data = self.client.get(self.def_endpoint.format(id=self.machine_key))
        self.machine_data = data
        self.name = data["Name"]
        self.machine_key = data["Key"]

    def edit(self, content):
        """Edits an Machine"""
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class Folder(Resource):
    """Class to handle a Folder type Resource"""

    _type = "folder"
    def_endpoint = "/odata/Folders({id})"

    # pylint: disable=redefined-builtin
    def __init__(self, id: int, name: str, client: Client, folder_data: dict[str, str]):
        super().__init__(id, name, self._type)
        self.client = client
        self.folder_data = folder_data

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.folder_data

    def key(self):
        return self.folder_data["Key"]

    def refresh(self):
        data = self.client.get(self.def_endpoint.format(id=self.id))
        self.folder_data = data
        self.name = data["DisplayName"]

    def get_queue(
        self,
        id: int,
        options: Optional[Mapping[str, str]] = None,
        item_pool: bool = True,
    ) -> Queue:
        """Retreives a Queue resource based on its id.

        :param id: the queue id
        :param options: an optional dicitonary of odata query options.
        :rtype: Queue
        :type id: int
        :type options: dict[str, str]
        """
        data = self.client.get(f"/odata/QueueDefinitions({id})", params=options)
        return Queue(
            id=data["Id"], name=data["Name"], client=self.client, item_pool=item_pool
        )

    def get_asset(self, id: int, options: Optional[Mapping[str, str]] = None) -> Asset:
        """Retrives an Asset resource based on its id.

        :param id: the asset id
        :param options: an optional dictionary of odata query options.
        :rtype: Asset
        :type id: int
        :type options: dict[str, str]
        """
        data = self.client.get(f"/odata/Assets({id})", params=options)
        return Asset(
            id=data["Id"], name=data["Name"], client=self.client, asset_data=data
        )

    def get_logs(self, options : Optional[Mapping[str, str]] = None):
        endpoint = "/odata/RobotLogs"
        data = self.client.get(endpoint, options)
        return data

    def get_jobs(self, options: Optional[Mapping[str, str]] = None):
        endpoint = "/odata/Jobs"
        data = self.client.get(endpoint, options)
        return data

    def get_job(self, job_id):
        endpoint = f"/odata/Jobs({job_id})"
        data = self.client.get(endpoint)
        return data

    def get_processes(
        self, options: Optional[Mapping[str, str]] = None
    ) -> List[Process]:
        """Returns a list of Process resources.

        :param options: an optional dictionary of odata query options
        :type options: dict[str, str]
        :rtype: List[Process]
        """
        endpoint = "/odata/Processes"
        data = self.client.get(endpoint, options)
        if not data["value"]:
            raise ValueError("No processes were found")
        try:
            return [
                Process(
                    id=val["Key"],
                    name=val["Title"],
                    client=self.client,
                    process_data=val,
                )
                for val in data["value"]
            ]
        except KeyError as err:
            msg = "Cannot get process without 'Key' and 'Title'. Please do not include either fields in the '$select' parameter."
            raise ValueError(msg) from err

    def get_schedules(
        self, options: Optional[Mapping[str, Any]] = None
    ) -> List[Schedule]:
        endpoint = "/odata/ProcessSchedules"
        data = self.client.get(endpoint, options)
        if not data["value"]:
            raise ValueError("No processes were found")
        schedules = [
            Schedule(
                id=sch["Id"], name=sch["Name"], client=self.client, schedule_data=sch
            )
            for sch in data["value"]
        ]
        return schedules

    def get_schedule(self, id: Optional[int] = None, name: Optional[str] = None):
        if id:
            return self._get_schedule_by_id(id)
        if name:
            return self._get_schedule_by_name(name)
        raise ValueError("At least one of 'id' or 'name' must not be 'None")

    def _get_schedule_by_name(self, name: str) -> Schedule:
        schedules = self.get_schedules(options={"$filter": f"Name eq '{name}'"})
        return schedules[0]  # return the first match

    def _get_schedule_by_id(self, id: int) -> Schedule:
        endpoint = f"/odata/ProcessSchedules({id})"
        data = self.client.get(endpoint)
        return Schedule(
            id=data["Id"], name=data["Name"], client=self.client, schedule_data=data
        )

    def get_release_ids(self) -> Dict[str, int]:
        r"""Retrieves a dictionary where the keys correspond to the release names (i.e) without the version,
        and the values are the ids of those releases, so they can be used to access a single Release

        :rtype: Dict[str, int]
        """
        endpoint = "/odata/Releases"
        data = self.client.get(endpoint)
        ids = {}
        for release in data["value"]:
            ids.update({release["Name"]: release["Id"]})
        return ids

    def get_release(self, release_id: int) -> Release:
        """Gets a single release based on its release id

        :param release_id: the id of the release to be queried
        :type release_id: int
        :rtype: Release
        """
        endpoint = f"/odata/Releases({release_id})"
        data = self.client.get(endpoint)
        return Release(
            id=data["Id"], name=data["Name"], client=self.client, release_data=data
        )

    def get_releases(
        self, options: Optional[Mapping[str, str]] = None
    ) -> List[Release]:
        """Retries a list of releases

        :param options: an optional fictionary of odata query options
        :type options: Optional[Mapping[str, str]]
        :rtype: List[Release]
        """
        endpoint = "/odata/Releases"
        data = self.client.get(endpoint, options)
        return [
            Release(
                id=release["Id"],
                name=release["Name"],
                client=self.client,
                release_data=release,
            )
            for release in data["value"]
        ]

    def upload_package(self, nuget_file: str):
        """Uploads a .nuget file to the Orchestrator tenant

        :param nuget_file: the location of the .nupkg file containing the process to be uploaded to your Orchestrator tenant

        """
        endpoint = "/odata/Processes/UiPath.Server.Configuration.OData.UploadPackage"
        files = {
            "file": (nuget_file, open(nuget_file, "rb")),
        }
        data = self.client.post(endpoint=endpoint, files=files)
        return data

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
            "Description": description,
        }
        return body

    def create_asset(
        self,
        name: str,
        value: Union[str, bool, int],
        value_type: Literal["Text", "Integer", "Bool"],
        description: str = "",
    ) -> Asset:
        """Creates a Resource of type Asset

        :param name: the name of the Asset.
        :param value: the value of the Asset.
        :param value_type: the value type of the Asset ('Test', 'Integer', 'Bool').
        :param description: an optional description of the Asset.
        :rtype: Asset
        :type name: str
        :type value: Union[str, bool, int]
        :type value_type: str
        :type description: str
        """
        assert value_type in ("Text", "Integer", "Bool")
        body = self._create_body(name, value, value_type, description)
        data = self.client.post(endpoint="/odata/Assets", body=body)
        asset = Asset(
            id=data["Id"], name=data["Name"], client=self.client, asset_data=data
        )
        return asset

    def edit(self, content):
        """Edits an Folder"""
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


def raise_no_client(f):
    """Raises a ValueError if the credentials flow has not been
    initialized first to prevent user from calling other methods first."""

    def wrapper(self, *args, **kwargs):
        if self.client is None:
            raise ValueError("You need to authenticate yourself first!")
        return f(self, *args, **kwargs)

    return wrapper


class Schedule(Resource):

    _def_endpoint = f"/odata/ProcessSchedules('{id}')"
    _type = "process_schedule"

    def __init__(
        self, id: int, name: str, client: Client, schedule_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.schedule_data = schedule_data

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.schedule_data

    def key(self):
        return self.schedule_data["Key"]

    def refresh(self) -> None:
        endpoint = self._def_endpoint.format(id=self.id)
        self.schedule_data = self.client.get(endpoint)

    def get_cron(self) -> str:
        cron_summary = (
            self.schedule_data["StartProcessCronSummary"]
            if self.schedule_data["StartProcessCronSummary"]
            # else get_description(self.schedule_data["StartProcessCron"])
            else self.schedule_data["StartProcessCron"]
        )
        return cron_summary

    def edit(self):
        pass

    def delete(self):
        pass


class Process(Resource):
    """Class to handle a Process type Resource"""

    _type = "process"
    def_endpoint = "/odata/Processes({id})"

    # pylint: disable=redefined-builtin
    def __init__(
        self, id: str, name: str, client: Client, process_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.process_data = process_data
        self.process_id = id.split(":")[0]

    def __hash__(self):
        return hash(self.id)

    def info(self):
        return self.process_data

    def key(self):
        return self.process_data["Key"]

    def refresh(self):
        raise NotImplementedError

    def download_package(self, dir_name: str):
        """Downloads a .nupkg containing the process in the specified route

        :param dir_name: string representing the directory name to download the package into
        :rtype dir_name: str
        """
        endpoint = f"/odata/Processes/UiPath.Server.Configuration.OData.DownloadPackage(key='{self.id}')"
        data = self.client.get(endpoint)
        with open(os.path.join(dir_name, f"{self.id}.nupkg"), "wb") as f:
            f.write(data)
        # return data

    def get_available_versions(self):
        """Retries all the available versions of the process"""
        endpoint = f"/odata/Processes/UiPath.Server.Configuration.OData.GetProcessVersions(processId='{self.process_id}')"
        data = self.client.get(endpoint)
        return data

    def get_arguments(self) -> Mapping[str, Any]:
        """Retrieves the input and ouput arguments of a process and returns their names and types"""
        endpoint = f"/odata/Processes/UiPath.Server.Configuration.ODATA.GetArguments(key = '{self.id}')"
        data = self.client.get(endpoint)
        parsed_arguments = self._parse_arguments(args=data)
        return parsed_arguments

    def _parse_arguments(self, args: Mapping[str, Any]) -> Mapping[str, Any]:
        input_args = json.loads(args["Input"]) if args["Input"] else None
        output_args = json.loads(args["Output"]) if args["Output"] else None
        fmt_input_args = []
        fmt_output_args = []
        if input_args:
            for arg in input_args:
                fmt_input_args.append(
                    {"name": arg["name"], "type": arg["type"].split(",")[0]}
                )
        if output_args:
            for arg in output_args:
                fmt_output_args.append(
                    {"name": arg["name"], "type": arg["type"].split(",")[0]}
                )
        return {"input_args": fmt_input_args, "output_args": fmt_output_args}

    def edit(self):
        pass

    def delete(self):
        pass


class Release(Resource):
    """Class to handle a Release type Resource"""

    _def_endpoint = f"/odata/Releases/({id})"
    _type = "process"

    # pylint: disable=redefined-builtin
    def __init__(
        self, id: int, name: str, client: Client, release_data: dict[str, str]
    ):
        super().__init__(id, name, self._type)
        self.client = client
        self.release_data = release_data

    def __hash__(self):
        return hash(self.id)

    def update_to_latest_version(self):
        endpoint = f"​/odata​/Releases({self.id})​/UiPath.Server.Configuration.OData.UpdateToLatestPackageVersion"
        data = self.client.post(endpoint=endpoint, body={"mergePackageTags": True})
        return data

    def rollback(self):
        endpoint = f"/odata/Releases({self.id})/UiPath.Server.Configuration.OData.RollbackToPreviousReleaseVersion"
        data = self.client.post(endpoint=endpoint)
        return data

    def update(self, version: str):
        """Updates the process to the given version

        :param version: string with a version for the process (e.g. 1.8.9)
        :type version: str
        """
        endpoint = f"/odata/Releases({self.id})/UiPath.Server.Configuration.OData.UpdateToSpecificPackageVersion"
        data = self.client.post(endpoint=endpoint, body={"packageVersion": version})
        return data

    def info(self):
        return self.release_data

    def key(self):
        return self.release_data["Key"]

    def refresh(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass


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

    def __init__(self, auth=None, **kwargs):

        if not kwargs:
            return
        self.client = Client(auth, **kwargs)

    def from_oauth_credentials(
        self, tenant_name: str, client_id: str, refresh_token: str, organization: str
    ):
        """Authenticates a client using default cloud base_url.
        :param tenant_name: orchestrator tenant name.
        :param client_id: client id for oauth authentication type.
        :param refresh_token: refresh token for cloud authentication type.
        :param organization: your organization name.
        """
        if self.client:
            return self
        self.client = Client(
            auth="cloud",
            tenant_name=tenant_name,
            client_id=client_id,
            refresh_token=refresh_token,
            organization=organization,
        )
        return self

    def from_custom_credentials(
        self,
        tenant_name: str,
        client_id: str,
        refresh_token: str,
        base_url: str,
        organization: str,
    ):
        """Authenticates a client using custom base_url

        :param tenant_name: orchestrator tenant name.
        :param client_id: client id for oauth authentication type.
        :param refresh_token: refresh token for cloud authentication type.
        :param organization: your organization name.
        :param base_url: a custom base_url for your orchestrator.
        """
        self.client = Client(
            auth="custom",
            tenant_name=tenant_name,
            refresh_token=refresh_token,
            client_id=client_id,
            base_url=base_url,
            organization=organization,
        )
        return self

    def from_on_premise_credentials(
        self, tenant_name: str, username: str, password: str, orchestrator_url: str
    ):
        """Authenticates a client using on-premise credentials"""
        if self.client:
            return self
        self.client = Client(
            auth="on-premise",
            tenant_name=tenant_name,
            username=username,
            password=password,
            orchestrator_url=orchestrator_url,
        )
        return self

    @raise_no_client
    def get_folders(self, options: Optional[Mapping[str, str]] = None) -> List[Folder]:
        """Returns a set of Folders resources

        :param options: an optional dictionary of odata query options.
        """
        if self.client is None:
            raise ValueError("You need to authenticate yourself first!")
        endpoint = "/odata/Folders"
        data = self.client.get(endpoint, options)
        try:
            return [
                Folder(
                    id=folder["Id"],
                    name=folder["DisplayName"],
                    folder_data=folder,
                    client=self.client,
                )
                for folder in data["value"]
            ]
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either field in the '$select' parameter."
            raise ValueError(msg) from err

    @raise_no_client
    def get_folder(
        self, id: int, options: Optional[Mapping[str, str]] = None
    ) -> Folder:
        """Returns a Folder resource based on its id

        :param id: the folder id.
        :param options: optional dictionary of odata query options.
        """
        # pylint: disable=redefined-builtin
        endpoint = f"/odata/Folders({id})"
        data = self.client.get(endpoint, options)
        self.client.folder_id = id
        try:
            return Folder(
                id=data["Id"],
                name=data["DisplayName"],
                folder_data=data,
                client=self.client,
            )
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either field in the '$select' parameter."
            raise ValueError(msg) from err

    def get_machine(
        self, machine_key: str, options: Optional[Mapping[str, str]] = None
    ) -> Machine:
        """Returns a Machine resource based on its key

        :param machine_key: the key of the machine
        :param options: optional dictionary of odata query options
        """
        endpoint = f"/odata/Machines({machine_key})"
        data = self.client.get(endpoint, options)
        try:
            return Machine(
                id=data["Id"], name=data["Name"], client=self.client, machine_data=data
            )
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either fields in the '$select' parameter."
            raise ValueError(msg) from err

    def get_machines(
        self, options: Optional[Mapping[str, str]] = None
    ) -> List[Machine]:
        """Returns a list of Machine resources"""

        endpoint = "/odata/Machines"
        data = self.client.get(endpoint, options)
        try:
            return [
                Machine(
                    id=val["Id"], name=val["Name"], client=self.client, machine_data=val
                )
                for val in data["value"]
            ]
        except KeyError as err:
            msg = "Cannot get folder without 'Id' and 'DisplayName'. Please do not include either fields in the '$select' parameter."
            raise ValueError(msg) from err
