# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.384.10

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class AssignmentsActionsAddRequest:
    """

    Attributes
    ----------
    add: list[AssignmentsActionsAddRequestAdd]
    """

    add: list[AssignmentsActionsAddRequestAdd] = None

    def __init__(self_, **kvargs):

        if "add" in kvargs:
            if type(kvargs["add"]).__name__ == self_.__annotations__["add"]:
                self_.add = kvargs["add"]
            else:
                self_.add = [
                    AssignmentsActionsAddRequestAdd(**e) for e in kvargs["add"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsAddRequestAdd:
    """

    Attributes
    ----------
    name: str
      User name
    subject: str
      User subject
    type: str
      Allotment type
    userId: str
      User ID
    """

    name: str = None
    subject: str = None
    type: str = None
    userId: str = None

    def __init__(self_, **kvargs):

        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ == self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "userId" in kvargs:
            if type(kvargs["userId"]).__name__ == self_.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsAddResponse:
    """

    Attributes
    ----------
    data: list[AssignmentsActionsAddResponseData]
    """

    data: list[AssignmentsActionsAddResponseData] = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    AssignmentsActionsAddResponseData(**e) for e in kvargs["data"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsAddResponseData:
    """

    Attributes
    ----------
    code: str
      Error code
    status: int
      Response status
    subject: str
      Subject
    title: str
      Error title
    type: str
      Allotment type
    """

    code: str = None
    status: int = None
    subject: str = None
    title: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "code" in kvargs:
            if type(kvargs["code"]).__name__ == self_.__annotations__["code"]:
                self_.code = kvargs["code"]
            else:
                self_.code = kvargs["code"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ == self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ == self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "title" in kvargs:
            if type(kvargs["title"]).__name__ == self_.__annotations__["title"]:
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsDeleteRequest:
    """

    Attributes
    ----------
    delete: list[AssignmentsActionsDeleteRequestDelete]
    """

    delete: list[AssignmentsActionsDeleteRequestDelete] = None

    def __init__(self_, **kvargs):

        if "delete" in kvargs:
            if type(kvargs["delete"]).__name__ == self_.__annotations__["delete"]:
                self_.delete = kvargs["delete"]
            else:
                self_.delete = [
                    AssignmentsActionsDeleteRequestDelete(**e) for e in kvargs["delete"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsDeleteRequestDelete:
    """

    Attributes
    ----------
    subject: str
      User subject
    type: str
      Allotment type
    """

    subject: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ == self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsDeleteResponse:
    """

    Attributes
    ----------
    data: list[AssignmentsActionsDeleteResponseData]
    """

    data: list[AssignmentsActionsDeleteResponseData] = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    AssignmentsActionsDeleteResponseData(**e) for e in kvargs["data"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsDeleteResponseData:
    """

    Attributes
    ----------
    code: str
      Error code
    status: int
      Response status
    subject: str
      Subject
    title: str
      Error title
    type: str
      Allotment type
    """

    code: str = None
    status: int = None
    subject: str = None
    title: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "code" in kvargs:
            if type(kvargs["code"]).__name__ == self_.__annotations__["code"]:
                self_.code = kvargs["code"]
            else:
                self_.code = kvargs["code"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ == self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ == self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "title" in kvargs:
            if type(kvargs["title"]).__name__ == self_.__annotations__["title"]:
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsUpdateRequest:
    """

    Attributes
    ----------
    update: list[AssignmentsActionsUpdateRequestUpdate]
    """

    update: list[AssignmentsActionsUpdateRequestUpdate] = None

    def __init__(self_, **kvargs):

        if "update" in kvargs:
            if type(kvargs["update"]).__name__ == self_.__annotations__["update"]:
                self_.update = kvargs["update"]
            else:
                self_.update = [
                    AssignmentsActionsUpdateRequestUpdate(**e) for e in kvargs["update"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsUpdateRequestUpdate:
    """

    Attributes
    ----------
    sourceType: str
      Current assignment type.
    subject: str
      User subject
    type: str
      Target assignment type.
    """

    sourceType: str = None
    subject: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "sourceType" in kvargs:
            if (
                type(kvargs["sourceType"]).__name__
                == self_.__annotations__["sourceType"]
            ):
                self_.sourceType = kvargs["sourceType"]
            else:
                self_.sourceType = kvargs["sourceType"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ == self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsUpdateResponse:
    """

    Attributes
    ----------
    data: list[AssignmentsActionsUpdateResponseData]
    """

    data: list[AssignmentsActionsUpdateResponseData] = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    AssignmentsActionsUpdateResponseData(**e) for e in kvargs["data"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsActionsUpdateResponseData:
    """

    Attributes
    ----------
    code: str
      Error code
    sourceType: str
      Current allotment type.
    status: int
      Response status
    subject: str
      Subject
    title: str
      Error title
    type: str
      Target allotment type.
    """

    code: str = None
    sourceType: str = None
    status: int = None
    subject: str = None
    title: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "code" in kvargs:
            if type(kvargs["code"]).__name__ == self_.__annotations__["code"]:
                self_.code = kvargs["code"]
            else:
                self_.code = kvargs["code"]
        if "sourceType" in kvargs:
            if (
                type(kvargs["sourceType"]).__name__
                == self_.__annotations__["sourceType"]
            ):
                self_.sourceType = kvargs["sourceType"]
            else:
                self_.sourceType = kvargs["sourceType"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ == self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ == self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "title" in kvargs:
            if type(kvargs["title"]).__name__ == self_.__annotations__["title"]:
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsResponse:
    """

    Attributes
    ----------
    data: list[AssignmentsResponseData]
    links: AssignmentsResponseLinks
    """

    data: list[AssignmentsResponseData] = None
    links: AssignmentsResponseLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [AssignmentsResponseData(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = AssignmentsResponseLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsResponseData:
    """

    Attributes
    ----------
    created: str
      Assignment created date.
    excess: bool
      Assignment excess status.
    name: str
      User name
    subject: str
      Subject
    type: str
      Allotment type
    userId: str
      User ID
    """

    created: str = None
    excess: bool = None
    name: str = None
    subject: str = None
    type: str = None
    userId: str = None

    def __init__(self_, **kvargs):

        if "created" in kvargs:
            if type(kvargs["created"]).__name__ == self_.__annotations__["created"]:
                self_.created = kvargs["created"]
            else:
                self_.created = kvargs["created"]
        if "excess" in kvargs:
            if type(kvargs["excess"]).__name__ == self_.__annotations__["excess"]:
                self_.excess = kvargs["excess"]
            else:
                self_.excess = kvargs["excess"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "subject" in kvargs:
            if type(kvargs["subject"]).__name__ == self_.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "userId" in kvargs:
            if type(kvargs["userId"]).__name__ == self_.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsResponseLinks:
    """

    Attributes
    ----------
    next: Licenseshref
    prev: Licenseshref
    """

    next: Licenseshref = None
    prev: Licenseshref = None

    def __init__(self_, **kvargs):

        if "next" in kvargs:
            if type(kvargs["next"]).__name__ == self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Licenseshref(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ == self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Licenseshref(**kvargs["prev"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConsumptionEventsResponse:
    """

    Attributes
    ----------
    data: list[ConsumptionEventsResponseData]
    links: ConsumptionEventsResponseLinks
    """

    data: list[ConsumptionEventsResponseData] = None
    links: ConsumptionEventsResponseLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [
                    ConsumptionEventsResponseData(**e) for e in kvargs["data"]
                ]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ConsumptionEventsResponseLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConsumptionEventsResponseData:
    """

    Attributes
    ----------
    allotmentId: str
      Allotment ID
    appId: str
      App ID
    capacityUsed: int
      Analyzer capacity chunks consumed.
    duration: str
      Engine session duration.
    endTime: str
      Engine session end time.
    id: str
      ID
    licenseUsage: str
      License usage
    minutesUsed: int
      Analyzer capacity minutes consumed.
    sessionId: str
      Engine session ID.
    userId: str
      User ID
    """

    allotmentId: str = None
    appId: str = None
    capacityUsed: int = None
    duration: str = None
    endTime: str = None
    id: str = None
    licenseUsage: str = None
    minutesUsed: int = None
    sessionId: str = None
    userId: str = None

    def __init__(self_, **kvargs):

        if "allotmentId" in kvargs:
            if (
                type(kvargs["allotmentId"]).__name__
                == self_.__annotations__["allotmentId"]
            ):
                self_.allotmentId = kvargs["allotmentId"]
            else:
                self_.allotmentId = kvargs["allotmentId"]
        if "appId" in kvargs:
            if type(kvargs["appId"]).__name__ == self_.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "capacityUsed" in kvargs:
            if (
                type(kvargs["capacityUsed"]).__name__
                == self_.__annotations__["capacityUsed"]
            ):
                self_.capacityUsed = kvargs["capacityUsed"]
            else:
                self_.capacityUsed = kvargs["capacityUsed"]
        if "duration" in kvargs:
            if type(kvargs["duration"]).__name__ == self_.__annotations__["duration"]:
                self_.duration = kvargs["duration"]
            else:
                self_.duration = kvargs["duration"]
        if "endTime" in kvargs:
            if type(kvargs["endTime"]).__name__ == self_.__annotations__["endTime"]:
                self_.endTime = kvargs["endTime"]
            else:
                self_.endTime = kvargs["endTime"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ == self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "licenseUsage" in kvargs:
            if (
                type(kvargs["licenseUsage"]).__name__
                == self_.__annotations__["licenseUsage"]
            ):
                self_.licenseUsage = kvargs["licenseUsage"]
            else:
                self_.licenseUsage = kvargs["licenseUsage"]
        if "minutesUsed" in kvargs:
            if (
                type(kvargs["minutesUsed"]).__name__
                == self_.__annotations__["minutesUsed"]
            ):
                self_.minutesUsed = kvargs["minutesUsed"]
            else:
                self_.minutesUsed = kvargs["minutesUsed"]
        if "sessionId" in kvargs:
            if type(kvargs["sessionId"]).__name__ == self_.__annotations__["sessionId"]:
                self_.sessionId = kvargs["sessionId"]
            else:
                self_.sessionId = kvargs["sessionId"]
        if "userId" in kvargs:
            if type(kvargs["userId"]).__name__ == self_.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ConsumptionEventsResponseLinks:
    """

    Attributes
    ----------
    next: Licenseshref
    prev: Licenseshref
    """

    next: Licenseshref = None
    prev: Licenseshref = None

    def __init__(self_, **kvargs):

        if "next" in kvargs:
            if type(kvargs["next"]).__name__ == self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Licenseshref(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ == self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Licenseshref(**kvargs["prev"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverview:
    """

    Attributes
    ----------
    allotments: list[LicenseOverviewAllotments]
    licenseKey: str
    licenseNumber: str
    origin: str
      Origin of license key.
    parameters: list[LicenseOverviewParameters]
      The license parameters.
    product: str
      The product the license is valid for.
    status: str
      Enum with status of license. Only status Ok grants license. access.
    trial: bool
      Boolean indicating if it is a trial license.
    updated: str
      An ISO 8601 timestamp for when the license was last updated.
    valid: str
      Period that the license is currently set to be active. Represented as an ISO 8601 time interval with start and end.
    """

    allotments: list[LicenseOverviewAllotments] = None
    licenseKey: str = None
    licenseNumber: str = None
    origin: str = None
    parameters: list[LicenseOverviewParameters] = None
    product: str = None
    status: str = None
    trial: bool = None
    updated: str = None
    valid: str = None

    def __init__(self_, **kvargs):

        if "allotments" in kvargs:
            if (
                type(kvargs["allotments"]).__name__
                == self_.__annotations__["allotments"]
            ):
                self_.allotments = kvargs["allotments"]
            else:
                self_.allotments = [
                    LicenseOverviewAllotments(**e) for e in kvargs["allotments"]
                ]
        if "licenseKey" in kvargs:
            if (
                type(kvargs["licenseKey"]).__name__
                == self_.__annotations__["licenseKey"]
            ):
                self_.licenseKey = kvargs["licenseKey"]
            else:
                self_.licenseKey = kvargs["licenseKey"]
        if "licenseNumber" in kvargs:
            if (
                type(kvargs["licenseNumber"]).__name__
                == self_.__annotations__["licenseNumber"]
            ):
                self_.licenseNumber = kvargs["licenseNumber"]
            else:
                self_.licenseNumber = kvargs["licenseNumber"]
        if "origin" in kvargs:
            if type(kvargs["origin"]).__name__ == self_.__annotations__["origin"]:
                self_.origin = kvargs["origin"]
            else:
                self_.origin = kvargs["origin"]
        if "parameters" in kvargs:
            if (
                type(kvargs["parameters"]).__name__
                == self_.__annotations__["parameters"]
            ):
                self_.parameters = kvargs["parameters"]
            else:
                self_.parameters = [
                    LicenseOverviewParameters(**e) for e in kvargs["parameters"]
                ]
        if "product" in kvargs:
            if type(kvargs["product"]).__name__ == self_.__annotations__["product"]:
                self_.product = kvargs["product"]
            else:
                self_.product = kvargs["product"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ == self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "trial" in kvargs:
            if type(kvargs["trial"]).__name__ == self_.__annotations__["trial"]:
                self_.trial = kvargs["trial"]
            else:
                self_.trial = kvargs["trial"]
        if "updated" in kvargs:
            if type(kvargs["updated"]).__name__ == self_.__annotations__["updated"]:
                self_.updated = kvargs["updated"]
            else:
                self_.updated = kvargs["updated"]
        if "valid" in kvargs:
            if type(kvargs["valid"]).__name__ == self_.__annotations__["valid"]:
                self_.valid = kvargs["valid"]
            else:
                self_.valid = kvargs["valid"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverviewAllotments:
    """

    Attributes
    ----------
    name: str
    overage: int
      Overage value; -1 means unbounded overage.
    units: int
    unitsUsed: int
    usageClass: str
    """

    name: str = None
    overage: int = None
    units: int = None
    unitsUsed: int = None
    usageClass: str = None

    def __init__(self_, **kvargs):

        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "overage" in kvargs:
            if type(kvargs["overage"]).__name__ == self_.__annotations__["overage"]:
                self_.overage = kvargs["overage"]
            else:
                self_.overage = kvargs["overage"]
        if "units" in kvargs:
            if type(kvargs["units"]).__name__ == self_.__annotations__["units"]:
                self_.units = kvargs["units"]
            else:
                self_.units = kvargs["units"]
        if "unitsUsed" in kvargs:
            if type(kvargs["unitsUsed"]).__name__ == self_.__annotations__["unitsUsed"]:
                self_.unitsUsed = kvargs["unitsUsed"]
            else:
                self_.unitsUsed = kvargs["unitsUsed"]
        if "usageClass" in kvargs:
            if (
                type(kvargs["usageClass"]).__name__
                == self_.__annotations__["usageClass"]
            ):
                self_.usageClass = kvargs["usageClass"]
            else:
                self_.usageClass = kvargs["usageClass"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverviewParameters:
    """

    Attributes
    ----------
    access: LicenseOverviewParametersAccess
      Parameters for licenses to control access to the parameters.
    name: str
      Parameter set (provision) name.
    valid: str
      Time interval for parameter validity.
    values: LicenseOverviewParametersValues
      Parameter values
    """

    access: LicenseOverviewParametersAccess = None
    name: str = None
    valid: str = None
    values: LicenseOverviewParametersValues = None

    def __init__(self_, **kvargs):

        if "access" in kvargs:
            if type(kvargs["access"]).__name__ == self_.__annotations__["access"]:
                self_.access = kvargs["access"]
            else:
                self_.access = LicenseOverviewParametersAccess(**kvargs["access"])
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "valid" in kvargs:
            if type(kvargs["valid"]).__name__ == self_.__annotations__["valid"]:
                self_.valid = kvargs["valid"]
            else:
                self_.valid = kvargs["valid"]
        if "values" in kvargs:
            if type(kvargs["values"]).__name__ == self_.__annotations__["values"]:
                self_.values = kvargs["values"]
            else:
                self_.values = LicenseOverviewParametersValues(**kvargs["values"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverviewParametersAccess:
    """
    Parameters for licenses to control access to the parameters.

    Attributes
    ----------
    allotment: str
      Name of an allotment that the user must have access to. to
    """

    allotment: str = None

    def __init__(self_, **kvargs):

        if "allotment" in kvargs:
            if type(kvargs["allotment"]).__name__ == self_.__annotations__["allotment"]:
                self_.allotment = kvargs["allotment"]
            else:
                self_.allotment = kvargs["allotment"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseOverviewParametersValues:
    """
    Parameter values

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class LicenseStatus:
    """

    Attributes
    ----------
    origin: str
      Origin of license key.
    product: str
      The product the license is valid for.
    status: str
      Enum with status of license. Only status Ok grants license. access.
    trial: bool
      Boolean indicating if it is a trial license.
    type: str
      Type of license key.
    valid: str
      Period that the license is currently set to be active. Represented as an ISO 8601 time interval with start and end.
    """

    origin: str = None
    product: str = None
    status: str = None
    trial: bool = None
    type: str = None
    valid: str = None

    def __init__(self_, **kvargs):

        if "origin" in kvargs:
            if type(kvargs["origin"]).__name__ == self_.__annotations__["origin"]:
                self_.origin = kvargs["origin"]
            else:
                self_.origin = kvargs["origin"]
        if "product" in kvargs:
            if type(kvargs["product"]).__name__ == self_.__annotations__["product"]:
                self_.product = kvargs["product"]
            else:
                self_.product = kvargs["product"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ == self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "trial" in kvargs:
            if type(kvargs["trial"]).__name__ == self_.__annotations__["trial"]:
                self_.trial = kvargs["trial"]
            else:
                self_.trial = kvargs["trial"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "valid" in kvargs:
            if type(kvargs["valid"]).__name__ == self_.__annotations__["valid"]:
                self_.valid = kvargs["valid"]
            else:
                self_.valid = kvargs["valid"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Licenseshref:
    """

    Attributes
    ----------
    href: str
      link
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs:
            if type(kvargs["href"]).__name__ == self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SettingsBody:
    """

    Attributes
    ----------
    autoAssignAnalyzer: bool
      If analyzer users are available, they will be automatically assigned. Otherwise, analyzer capacity will be assigned, if available.
    autoAssignProfessional: bool
      If professional users are available, they will be automatically assigned. Otherwise, analyzer capacity will be assigned, if available.
    """

    autoAssignAnalyzer: bool = None
    autoAssignProfessional: bool = None

    def __init__(self_, **kvargs):

        if "autoAssignAnalyzer" in kvargs:
            if (
                type(kvargs["autoAssignAnalyzer"]).__name__
                == self_.__annotations__["autoAssignAnalyzer"]
            ):
                self_.autoAssignAnalyzer = kvargs["autoAssignAnalyzer"]
            else:
                self_.autoAssignAnalyzer = kvargs["autoAssignAnalyzer"]
        if "autoAssignProfessional" in kvargs:
            if (
                type(kvargs["autoAssignProfessional"]).__name__
                == self_.__annotations__["autoAssignProfessional"]
            ):
                self_.autoAssignProfessional = kvargs["autoAssignProfessional"]
            else:
                self_.autoAssignProfessional = kvargs["autoAssignProfessional"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Licenses:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def add(self, data: AssignmentsActionsAddRequest) -> AssignmentsActionsAddResponse:
        """
        Assigns license access to the given users

        Parameters
        ----------
        authorization: str = None
          Authentication token
        data: AssignmentsActionsAddRequest
          List of subjects to allocate assignments for.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/licenses/assignments/actions/add",
            method="POST",
            params={},
            data=data,
        )
        obj = AssignmentsActionsAddResponse(**response.json())
        obj.auth = self.auth
        return obj

    def delete(
        self, data: AssignmentsActionsDeleteRequest
    ) -> AssignmentsActionsDeleteResponse:
        """
        Removes license access for the given users

        Parameters
        ----------
        authorization: str = None
          Authentication token
        data: AssignmentsActionsDeleteRequest
          List of assignments to delete.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/licenses/assignments/actions/delete",
            method="POST",
            params={},
            data=data,
        )
        obj = AssignmentsActionsDeleteResponse(**response.json())
        obj.auth = self.auth
        return obj

    def update(
        self, data: AssignmentsActionsUpdateRequest
    ) -> AssignmentsActionsUpdateResponse:
        """
        Updates license access for the given users

        Parameters
        ----------
        authorization: str = None
          Authentication token
        data: AssignmentsActionsUpdateRequest
          List of assignments to update.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/licenses/assignments/actions/update",
            method="POST",
            params={},
            data=data,
        )
        obj = AssignmentsActionsUpdateResponse(**response.json())
        obj.auth = self.auth
        return obj

    def get_assignments(
        self,
        filter: str = None,
        limit: int = 20,
        page: str = None,
        sort: str = None,
        max_items: int = 20,
    ) -> ListableResource[AssignmentsResponseData]:
        """
        Retrieves assignments for the current tenant

        Parameters
        ----------
        authorization: str = None
          Authentication token
        filter: str = None
          The filter for finding entries.
        limit: int = 20
          The preferred number of entries to return.
        page: str = None
          The requested page.
        sort: str = None
          The field to sort on; can be prefixed with +/- for ascending/descending sort order.
        """
        query_params = {}
        if filter is not None:
            query_params["filter"] = filter
        if limit is not None:
            query_params["limit"] = limit
        if page is not None:
            query_params["page"] = page
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/licenses/assignments",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=AssignmentsResponseData,
            auth=self.auth,
            path="/licenses/assignments",
            max_items=max_items,
            query_params=query_params,
        )

    def get_consumptions(
        self,
        filter: str = None,
        limit: int = 200,
        page: str = None,
        sort: str = None,
        max_items: int = 200,
    ) -> ListableResource[ConsumptionEventsResponseData]:
        """
        Retrieves license consumption for the current tenant

        Parameters
        ----------
        authorization: str = None
          Authentication token
        filter: str = None
          The filter for finding entries.
        limit: int = 200
          The preferred number of entries to return.
        page: str = None
          The requested page.
        sort: str = None
          The field to sort on; can be prefixed with +/- for ascending/descending sort order.
        """
        query_params = {}
        if filter is not None:
            query_params["filter"] = filter
        if limit is not None:
            query_params["limit"] = limit
        if page is not None:
            query_params["page"] = page
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/licenses/consumption",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ConsumptionEventsResponseData,
            auth=self.auth,
            path="/licenses/consumption",
            max_items=max_items,
            query_params=query_params,
        )

    def get_overview(self) -> LicenseOverview:
        """
        Gets the general information of the license applied to the current tenant

        Parameters
        ----------
        authorization: str = None
          Authentication token. In the case of a user token, the tenant admin role is required.
        """
        response = self.auth.rest(
            path="/licenses/overview",
            method="GET",
            params={},
            data=None,
        )
        obj = LicenseOverview(**response.json())
        obj.auth = self.auth
        return obj

    def get_settings(self) -> SettingsBody:
        """
        Get auto assign settings for tenant.

        Parameters
        ----------
        authorization: str = None
          Authentication token
        """
        response = self.auth.rest(
            path="/licenses/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = SettingsBody(**response.json())
        obj.auth = self.auth
        return obj

    def set_settings(self, data: SettingsBody = None) -> SettingsBody:
        """
        Set auto assign settings for tenant

        Parameters
        ----------
        authorization: str = None
          Authentication token
        data: SettingsBody = None
          Dynamic assignment settings for professional and analyzer users. If professional users and analyzer users are both set, professional users will be automatically assigned, if available. Otherwise, analyzer users will be assigned. If neither of those users are available, analyzer capacity will be assigned, if available.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/licenses/settings",
            method="PUT",
            params={},
            data=data,
        )
        obj = SettingsBody(**response.json())
        obj.auth = self.auth
        return obj

    def get_status(self) -> LicenseStatus:
        """
        Gets the license status information of the current tenant

        Parameters
        ----------
        authorization: str = None
          Authentication token
        """
        response = self.auth.rest(
            path="/licenses/status",
            method="GET",
            params={},
            data=None,
        )
        obj = LicenseStatus(**response.json())
        obj.auth = self.auth
        return obj
