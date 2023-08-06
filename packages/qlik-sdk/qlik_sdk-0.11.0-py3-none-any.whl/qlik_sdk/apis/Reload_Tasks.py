# This is spectacularly generated code by spectacular v0.8.0 based on
# Qlik Cloud Services 0.529.8

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Task:
    """

    Attributes
    ----------
    appId: str
      The ID of the app.
    autoReload: bool
      A flag that indicates whether a reload is triggered when data of the app is changed
    autoReloadPartial: bool
      A flag that indicates whether it is a partial reload or not for the auto reload
    endDateTime: str
      The time that the task will stop recurring. If the time zone is missing, this is a combined date-time value expressing a time with a fixed UTC offset (formatted according to RFC3339). If a time zone is given, the zone offset must be omitted.
    partial: bool
      The task is partial reload or not
    recurrence: list[str]
      List of RECUR lines for a recurring event, as specified in RFC5545. Note that DTSTART and DTEND lines are not allowed in this field; event start and end times are specified in the start and end fields. This field is omitted for single events or instances of recurring events
    startDateTime: str
      The time that the task execution start recurring. If the time zone is missing, this is a combined date-time value expressing a time with a fixed UTC offset (formatted according to RFC3339). If a time zone is given, the zone offset must be omitted. Field startDateTime should not be before the Unix epoch 00:00:00 UTC on 1 January 1970. Note that the empty string value with the empty recurrence array indicates the scheduled job is not set.
    timeZone: str
      The time zone in which the time is specified. (Formatted as an IANA Time Zone Database name, e.g. Europe/Zurich.) This field specifies the time zone in which the event start/end are expanded. If missing the start/end fields must specify a UTC offset in RFC3339 format.
    fortressId: str
      The fortress ID of the application
    id: str
      The ID of the task.
    lastExecutionTime: str
      The last time the task executed.
    links: SelfLink
    log: str
      The reason why the task was disabled.
    nextExecutionTime: str
      The next time the task will execute.
    spaceId: str
      The space ID of the application
    state: str
      Toggle for enabling and disabling the reload task
    tenantId: str
      The ID of the tenant who owns the task.
    userId: str
      The ID of the user who owns the task.
    """

    appId: str = None
    autoReload: bool = None
    autoReloadPartial: bool = None
    endDateTime: str = None
    partial: bool = None
    recurrence: list[str] = None
    startDateTime: str = None
    timeZone: str = None
    fortressId: str = None
    id: str = None
    lastExecutionTime: str = None
    links: SelfLink = None
    log: str = None
    nextExecutionTime: str = None
    spaceId: str = None
    state: str = None
    tenantId: str = None
    userId: str = None

    def __init__(self_, **kvargs):

        if "appId" in kvargs and kvargs["appId"] is not None:
            if type(kvargs["appId"]).__name__ == Task.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "autoReload" in kvargs and kvargs["autoReload"] is not None:
            if (
                type(kvargs["autoReload"]).__name__
                == Task.__annotations__["autoReload"]
            ):
                self_.autoReload = kvargs["autoReload"]
            else:
                self_.autoReload = kvargs["autoReload"]
        if "autoReloadPartial" in kvargs and kvargs["autoReloadPartial"] is not None:
            if (
                type(kvargs["autoReloadPartial"]).__name__
                == Task.__annotations__["autoReloadPartial"]
            ):
                self_.autoReloadPartial = kvargs["autoReloadPartial"]
            else:
                self_.autoReloadPartial = kvargs["autoReloadPartial"]
        if "endDateTime" in kvargs and kvargs["endDateTime"] is not None:
            if (
                type(kvargs["endDateTime"]).__name__
                == Task.__annotations__["endDateTime"]
            ):
                self_.endDateTime = kvargs["endDateTime"]
            else:
                self_.endDateTime = kvargs["endDateTime"]
        if "partial" in kvargs and kvargs["partial"] is not None:
            if type(kvargs["partial"]).__name__ == Task.__annotations__["partial"]:
                self_.partial = kvargs["partial"]
            else:
                self_.partial = kvargs["partial"]
        if "recurrence" in kvargs and kvargs["recurrence"] is not None:
            if (
                type(kvargs["recurrence"]).__name__
                == Task.__annotations__["recurrence"]
            ):
                self_.recurrence = kvargs["recurrence"]
            else:
                self_.recurrence = kvargs["recurrence"]
        if "startDateTime" in kvargs and kvargs["startDateTime"] is not None:
            if (
                type(kvargs["startDateTime"]).__name__
                == Task.__annotations__["startDateTime"]
            ):
                self_.startDateTime = kvargs["startDateTime"]
            else:
                self_.startDateTime = kvargs["startDateTime"]
        if "timeZone" in kvargs and kvargs["timeZone"] is not None:
            if type(kvargs["timeZone"]).__name__ == Task.__annotations__["timeZone"]:
                self_.timeZone = kvargs["timeZone"]
            else:
                self_.timeZone = kvargs["timeZone"]
        if "fortressId" in kvargs and kvargs["fortressId"] is not None:
            if (
                type(kvargs["fortressId"]).__name__
                == Task.__annotations__["fortressId"]
            ):
                self_.fortressId = kvargs["fortressId"]
            else:
                self_.fortressId = kvargs["fortressId"]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == Task.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "lastExecutionTime" in kvargs and kvargs["lastExecutionTime"] is not None:
            if (
                type(kvargs["lastExecutionTime"]).__name__
                == Task.__annotations__["lastExecutionTime"]
            ):
                self_.lastExecutionTime = kvargs["lastExecutionTime"]
            else:
                self_.lastExecutionTime = kvargs["lastExecutionTime"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Task.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = SelfLink(**kvargs["links"])
        if "log" in kvargs and kvargs["log"] is not None:
            if type(kvargs["log"]).__name__ == Task.__annotations__["log"]:
                self_.log = kvargs["log"]
            else:
                self_.log = kvargs["log"]
        if "nextExecutionTime" in kvargs and kvargs["nextExecutionTime"] is not None:
            if (
                type(kvargs["nextExecutionTime"]).__name__
                == Task.__annotations__["nextExecutionTime"]
            ):
                self_.nextExecutionTime = kvargs["nextExecutionTime"]
            else:
                self_.nextExecutionTime = kvargs["nextExecutionTime"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            if type(kvargs["spaceId"]).__name__ == Task.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "state" in kvargs and kvargs["state"] is not None:
            if type(kvargs["state"]).__name__ == Task.__annotations__["state"]:
                self_.state = kvargs["state"]
            else:
                self_.state = kvargs["state"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            if type(kvargs["tenantId"]).__name__ == Task.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "userId" in kvargs and kvargs["userId"] is not None:
            if type(kvargs["userId"]).__name__ == Task.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Delete a task.


        Parameters
        ----------
        """
        self.auth.rest(
            path="/reload-tasks/{taskId}".replace("{taskId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(self, data: PutTaskBody) -> Task:
        """
        Update an existing task.


        Parameters
        ----------
        data: PutTaskBody
          Request body specifying the task parameters.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/reload-tasks/{taskId}".replace("{taskId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class Href:
    """

    Attributes
    ----------
    href: str
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs and kvargs["href"] is not None:
            if type(kvargs["href"]).__name__ == Href.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PaginationLinks:
    """

    Attributes
    ----------
    self: Href
    next: Href
    prev: Href
    """

    self: Href = None
    next: Href = None
    prev: Href = None

    def __init__(self_, **kvargs):

        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == PaginationLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Href(**kvargs["self"])
        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == PaginationLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Href(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == PaginationLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Href(**kvargs["prev"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PostTaskBody:
    """

    Attributes
    ----------
    appId: str
      The ID of the app.
    autoReload: bool
      A flag that indicates whether a reload is triggered when data of the app is changed
    autoReloadPartial: bool
      A flag that indicates whether it is a partial reload or not for the auto reload
    endDateTime: str
      The time that the task will stop recurring. If the time zone is missing, this is a combined date-time value expressing a time with a fixed UTC offset (formatted according to RFC3339). If a time zone is given, the zone offset must be omitted.
    partial: bool
      The task is partial reload or not
    recurrence: list[str]
      List of RECUR lines for a recurring event, as specified in RFC5545. Note that DTSTART and DTEND lines are not allowed in this field; event start and end times are specified in the start and end fields. This field is omitted for single events or instances of recurring events
    startDateTime: str
      The time that the task execution start recurring. If the time zone is missing, this is a combined date-time value expressing a time with a fixed UTC offset (formatted according to RFC3339). If a time zone is given, the zone offset must be omitted. Field startDateTime should not be before the Unix epoch 00:00:00 UTC on 1 January 1970. Note that the empty string value with the empty recurrence array indicates the scheduled job is not set.
    timeZone: str
      The time zone in which the time is specified. (Formatted as an IANA Time Zone Database name, e.g. Europe/Zurich.) This field specifies the time zone in which the event start/end are expanded. If missing the start/end fields must specify a UTC offset in RFC3339 format.
    type: str
      Type of task being created - only contains the "scheduled_reload" value. Type value is not used for creating a schedule reload. It has been deprecated since 2022-04-05.
    """

    appId: str = None
    autoReload: bool = None
    autoReloadPartial: bool = None
    endDateTime: str = None
    partial: bool = None
    recurrence: list[str] = None
    startDateTime: str = None
    timeZone: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "appId" in kvargs and kvargs["appId"] is not None:
            if type(kvargs["appId"]).__name__ == PostTaskBody.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "autoReload" in kvargs and kvargs["autoReload"] is not None:
            if (
                type(kvargs["autoReload"]).__name__
                == PostTaskBody.__annotations__["autoReload"]
            ):
                self_.autoReload = kvargs["autoReload"]
            else:
                self_.autoReload = kvargs["autoReload"]
        if "autoReloadPartial" in kvargs and kvargs["autoReloadPartial"] is not None:
            if (
                type(kvargs["autoReloadPartial"]).__name__
                == PostTaskBody.__annotations__["autoReloadPartial"]
            ):
                self_.autoReloadPartial = kvargs["autoReloadPartial"]
            else:
                self_.autoReloadPartial = kvargs["autoReloadPartial"]
        if "endDateTime" in kvargs and kvargs["endDateTime"] is not None:
            if (
                type(kvargs["endDateTime"]).__name__
                == PostTaskBody.__annotations__["endDateTime"]
            ):
                self_.endDateTime = kvargs["endDateTime"]
            else:
                self_.endDateTime = kvargs["endDateTime"]
        if "partial" in kvargs and kvargs["partial"] is not None:
            if (
                type(kvargs["partial"]).__name__
                == PostTaskBody.__annotations__["partial"]
            ):
                self_.partial = kvargs["partial"]
            else:
                self_.partial = kvargs["partial"]
        if "recurrence" in kvargs and kvargs["recurrence"] is not None:
            if (
                type(kvargs["recurrence"]).__name__
                == PostTaskBody.__annotations__["recurrence"]
            ):
                self_.recurrence = kvargs["recurrence"]
            else:
                self_.recurrence = kvargs["recurrence"]
        if "startDateTime" in kvargs and kvargs["startDateTime"] is not None:
            if (
                type(kvargs["startDateTime"]).__name__
                == PostTaskBody.__annotations__["startDateTime"]
            ):
                self_.startDateTime = kvargs["startDateTime"]
            else:
                self_.startDateTime = kvargs["startDateTime"]
        if "timeZone" in kvargs and kvargs["timeZone"] is not None:
            if (
                type(kvargs["timeZone"]).__name__
                == PostTaskBody.__annotations__["timeZone"]
            ):
                self_.timeZone = kvargs["timeZone"]
            else:
                self_.timeZone = kvargs["timeZone"]
        if "type" in kvargs and kvargs["type"] is not None:
            if type(kvargs["type"]).__name__ == PostTaskBody.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class PutTaskBody:
    """

    Attributes
    ----------
    appId: str
      The ID of the app.
    autoReload: bool
      A flag that indicates whether a reload is triggered when data of the app is changed
    autoReloadPartial: bool
      A flag that indicates whether it is a partial reload or not for the auto reload
    endDateTime: str
      The time that the task will stop recurring. If the time zone is missing, this is a combined date-time value expressing a time with a fixed UTC offset (formatted according to RFC3339). If a time zone is given, the zone offset must be omitted.
    partial: bool
      The task is partial reload or not
    recurrence: list[str]
      List of RECUR lines for a recurring event, as specified in RFC5545. Note that DTSTART and DTEND lines are not allowed in this field; event start and end times are specified in the start and end fields. This field is omitted for single events or instances of recurring events
    startDateTime: str
      The time that the task execution start recurring. If the time zone is missing, this is a combined date-time value expressing a time with a fixed UTC offset (formatted according to RFC3339). If a time zone is given, the zone offset must be omitted. Field startDateTime should not be before the Unix epoch 00:00:00 UTC on 1 January 1970. Note that the empty string value with the empty recurrence array indicates the scheduled job is not set.
    timeZone: str
      The time zone in which the time is specified. (Formatted as an IANA Time Zone Database name, e.g. Europe/Zurich.) This field specifies the time zone in which the event start/end are expanded. If missing the start/end fields must specify a UTC offset in RFC3339 format.
    state: str
      Toggle for enabling and disabling the reload task
    """

    appId: str = None
    autoReload: bool = None
    autoReloadPartial: bool = None
    endDateTime: str = None
    partial: bool = None
    recurrence: list[str] = None
    startDateTime: str = None
    timeZone: str = None
    state: str = None

    def __init__(self_, **kvargs):

        if "appId" in kvargs and kvargs["appId"] is not None:
            if type(kvargs["appId"]).__name__ == PutTaskBody.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "autoReload" in kvargs and kvargs["autoReload"] is not None:
            if (
                type(kvargs["autoReload"]).__name__
                == PutTaskBody.__annotations__["autoReload"]
            ):
                self_.autoReload = kvargs["autoReload"]
            else:
                self_.autoReload = kvargs["autoReload"]
        if "autoReloadPartial" in kvargs and kvargs["autoReloadPartial"] is not None:
            if (
                type(kvargs["autoReloadPartial"]).__name__
                == PutTaskBody.__annotations__["autoReloadPartial"]
            ):
                self_.autoReloadPartial = kvargs["autoReloadPartial"]
            else:
                self_.autoReloadPartial = kvargs["autoReloadPartial"]
        if "endDateTime" in kvargs and kvargs["endDateTime"] is not None:
            if (
                type(kvargs["endDateTime"]).__name__
                == PutTaskBody.__annotations__["endDateTime"]
            ):
                self_.endDateTime = kvargs["endDateTime"]
            else:
                self_.endDateTime = kvargs["endDateTime"]
        if "partial" in kvargs and kvargs["partial"] is not None:
            if (
                type(kvargs["partial"]).__name__
                == PutTaskBody.__annotations__["partial"]
            ):
                self_.partial = kvargs["partial"]
            else:
                self_.partial = kvargs["partial"]
        if "recurrence" in kvargs and kvargs["recurrence"] is not None:
            if (
                type(kvargs["recurrence"]).__name__
                == PutTaskBody.__annotations__["recurrence"]
            ):
                self_.recurrence = kvargs["recurrence"]
            else:
                self_.recurrence = kvargs["recurrence"]
        if "startDateTime" in kvargs and kvargs["startDateTime"] is not None:
            if (
                type(kvargs["startDateTime"]).__name__
                == PutTaskBody.__annotations__["startDateTime"]
            ):
                self_.startDateTime = kvargs["startDateTime"]
            else:
                self_.startDateTime = kvargs["startDateTime"]
        if "timeZone" in kvargs and kvargs["timeZone"] is not None:
            if (
                type(kvargs["timeZone"]).__name__
                == PutTaskBody.__annotations__["timeZone"]
            ):
                self_.timeZone = kvargs["timeZone"]
            else:
                self_.timeZone = kvargs["timeZone"]
        if "state" in kvargs and kvargs["state"] is not None:
            if type(kvargs["state"]).__name__ == PutTaskBody.__annotations__["state"]:
                self_.state = kvargs["state"]
            else:
                self_.state = kvargs["state"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SelfLink:
    """

    Attributes
    ----------
    self: Href
    """

    self: Href = None

    def __init__(self_, **kvargs):

        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == SelfLink.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Href(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Tasks:
    """

    Attributes
    ----------
    data: list[Task]
    links: PaginationLinks
    """

    data: list[Task] = None
    links: PaginationLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == Tasks.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Task(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == Tasks.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = PaginationLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class ReloadTasks:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get(self, taskId: str) -> Task:
        """
        Find and return a task.


        Parameters
        ----------
        taskId: str
          The unique identifier of the task.
        """
        response = self.auth.rest(
            path="/reload-tasks/{taskId}".replace("{taskId}", taskId),
            method="GET",
            params={},
            data=None,
        )
        obj = Task(**response.json())
        obj.auth = self.auth
        return obj

    def get_reload_tasks(
        self,
        appId: str = None,
        limit: int = 10,
        next: str = None,
        partial: bool = None,
        prev: str = None,
        max_items: int = 10,
    ) -> ListableResource[Task]:
        """
        Find and return the tasks that the user can access.


        Parameters
        ----------
        appId: str = None
          The case sensitive string used to search for a task by app ID.
        limit: int = 10
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        partial: bool = None
          The boolean value used to search for a task is partial or not
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        """
        query_params = {}
        if appId is not None:
            query_params["appId"] = appId
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if partial is not None:
            query_params["partial"] = partial
        if prev is not None:
            query_params["prev"] = prev
        response = self.auth.rest(
            path="/reload-tasks",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Task,
            auth=self.auth,
            path="/reload-tasks",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: PostTaskBody) -> Task:
        """
        Create a task for a specified app.


        Parameters
        ----------
        data: PostTaskBody
          Request body specifying the task parameters.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/reload-tasks",
            method="POST",
            params={},
            data=data,
        )
        obj = Task(**response.json())
        obj.auth = self.auth
        return obj
