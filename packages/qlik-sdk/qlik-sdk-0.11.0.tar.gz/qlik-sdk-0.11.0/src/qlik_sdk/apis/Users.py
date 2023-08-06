# This is spectacularly generated code by spectacular v0.8.0 based on
# Qlik Cloud Services 0.529.8

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass
from typing import List

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class User:
    """
    A user object.

    Attributes
    ----------
    assignedGroups: list[UserAssignedGroups]
      An array of group references.
    assignedRoles: list[UserAssignedRoles]
      An array of role references.
    created: str
      Deprecated. Use `createdAt` instead.
    createdAt: str
      The timestamp for when the user record was created.
    email: str
      The email address for the user.
    id: str
      The unique user identifier.
    inviteExpiry: float
      The number of seconds until the user invitation will expire.
    lastUpdated: str
      Deprecated. Use `lastUpdatedAt` instead.
    lastUpdatedAt: str
      The timestamp for when the user record was last updated.
    links: UserLinks
      Pagination links to the user.
    locale: str
      Represents the end-user's language tag.
    name: str
      The name of the user.
    picture: str
      A static url linking to the avatar of the user.
    preferredLocale: str
      Represents the end-user's preferred language tag.
    preferredZoneinfo: str
      Represents the end-user's preferred time zone.
    roles: list[str]
      List of system roles to which the user has been assigned. Only returned when permitted by access control. Deprecated. Use `assignedRoles` instead.
    status: str
      The status of the user within the tenant.
    subject: str
      The unique user identitier from an identity provider.
    tenantId: str
      The tenant that the user belongs too.
    zoneinfo: str
      Represents the end-user's time zone.
    """

    assignedGroups: list[UserAssignedGroups] = None
    assignedRoles: list[UserAssignedRoles] = None
    created: str = None
    createdAt: str = None
    email: str = None
    id: str = None
    inviteExpiry: float = None
    lastUpdated: str = None
    lastUpdatedAt: str = None
    links: UserLinks = None
    locale: str = None
    name: str = None
    picture: str = None
    preferredLocale: str = None
    preferredZoneinfo: str = None
    roles: list[str] = None
    status: str = None
    subject: str = None
    tenantId: str = None
    zoneinfo: str = None

    def __init__(self_, **kvargs):

        if "assignedGroups" in kvargs and kvargs["assignedGroups"] is not None:
            if (
                len(kvargs["assignedGroups"]) > 0
                and f"list[{type(kvargs['assignedGroups'][0]).__name__}]"
                == User.__annotations__["assignedGroups"]
            ):
                self_.assignedGroups = kvargs["assignedGroups"]
            else:
                self_.assignedGroups = [
                    UserAssignedGroups(**e) for e in kvargs["assignedGroups"]
                ]
        if "assignedRoles" in kvargs and kvargs["assignedRoles"] is not None:
            if (
                len(kvargs["assignedRoles"]) > 0
                and f"list[{type(kvargs['assignedRoles'][0]).__name__}]"
                == User.__annotations__["assignedRoles"]
            ):
                self_.assignedRoles = kvargs["assignedRoles"]
            else:
                self_.assignedRoles = [
                    UserAssignedRoles(**e) for e in kvargs["assignedRoles"]
                ]
        if "created" in kvargs and kvargs["created"] is not None:
            if type(kvargs["created"]).__name__ == User.__annotations__["created"]:
                self_.created = kvargs["created"]
            else:
                self_.created = kvargs["created"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            if type(kvargs["createdAt"]).__name__ == User.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "email" in kvargs and kvargs["email"] is not None:
            if type(kvargs["email"]).__name__ == User.__annotations__["email"]:
                self_.email = kvargs["email"]
            else:
                self_.email = kvargs["email"]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == User.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "inviteExpiry" in kvargs and kvargs["inviteExpiry"] is not None:
            if (
                type(kvargs["inviteExpiry"]).__name__
                == User.__annotations__["inviteExpiry"]
            ):
                self_.inviteExpiry = kvargs["inviteExpiry"]
            else:
                self_.inviteExpiry = kvargs["inviteExpiry"]
        if "lastUpdated" in kvargs and kvargs["lastUpdated"] is not None:
            if (
                type(kvargs["lastUpdated"]).__name__
                == User.__annotations__["lastUpdated"]
            ):
                self_.lastUpdated = kvargs["lastUpdated"]
            else:
                self_.lastUpdated = kvargs["lastUpdated"]
        if "lastUpdatedAt" in kvargs and kvargs["lastUpdatedAt"] is not None:
            if (
                type(kvargs["lastUpdatedAt"]).__name__
                == User.__annotations__["lastUpdatedAt"]
            ):
                self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
            else:
                self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == User.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = UserLinks(**kvargs["links"])
        if "locale" in kvargs and kvargs["locale"] is not None:
            if type(kvargs["locale"]).__name__ == User.__annotations__["locale"]:
                self_.locale = kvargs["locale"]
            else:
                self_.locale = kvargs["locale"]
        if "name" in kvargs and kvargs["name"] is not None:
            if type(kvargs["name"]).__name__ == User.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "picture" in kvargs and kvargs["picture"] is not None:
            if type(kvargs["picture"]).__name__ == User.__annotations__["picture"]:
                self_.picture = kvargs["picture"]
            else:
                self_.picture = kvargs["picture"]
        if "preferredLocale" in kvargs and kvargs["preferredLocale"] is not None:
            if (
                type(kvargs["preferredLocale"]).__name__
                == User.__annotations__["preferredLocale"]
            ):
                self_.preferredLocale = kvargs["preferredLocale"]
            else:
                self_.preferredLocale = kvargs["preferredLocale"]
        if "preferredZoneinfo" in kvargs and kvargs["preferredZoneinfo"] is not None:
            if (
                type(kvargs["preferredZoneinfo"]).__name__
                == User.__annotations__["preferredZoneinfo"]
            ):
                self_.preferredZoneinfo = kvargs["preferredZoneinfo"]
            else:
                self_.preferredZoneinfo = kvargs["preferredZoneinfo"]
        if "roles" in kvargs and kvargs["roles"] is not None:
            if type(kvargs["roles"]).__name__ == User.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "status" in kvargs and kvargs["status"] is not None:
            if type(kvargs["status"]).__name__ == User.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            if type(kvargs["subject"]).__name__ == User.__annotations__["subject"]:
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            if type(kvargs["tenantId"]).__name__ == User.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "zoneinfo" in kvargs and kvargs["zoneinfo"] is not None:
            if type(kvargs["zoneinfo"]).__name__ == User.__annotations__["zoneinfo"]:
                self_.zoneinfo = kvargs["zoneinfo"]
            else:
                self_.zoneinfo = kvargs["zoneinfo"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Delete user by ID
        Deletes the requested user.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/users/{userId}".replace("{userId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, data: JSONPatchArray) -> None:
        """
        Update user by ID
        Updates fields for a user resource

        Parameters
        ----------
        data: JSONPatchArray

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/users/{userId}".replace("{userId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )


@dataclass
class Filter:
    """
    An advanced query filter to be used for complex user querying in the tenant.

    Attributes
    ----------
    filter: str
      The advanced filtering to be applied the query. All conditional statements within this query parameter are case insensitive.
    """

    filter: str = None

    def __init__(self_, **kvargs):

        if "filter" in kvargs and kvargs["filter"] is not None:
            if type(kvargs["filter"]).__name__ == Filter.__annotations__["filter"]:
                self_.filter = kvargs["filter"]
            else:
                self_.filter = kvargs["filter"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class JSONPatch:
    """
    A JSON Patch document as defined in http://tools.ietf.org/html/rfc6902.

    Attributes
    ----------
    op: str
      The operation to be performed.
    path: str
      A JSON Pointer.
    value: object
      The value to be used for this operation.
    """

    op: str = None
    path: str = None
    value: object = None

    def __init__(self_, **kvargs):

        if "op" in kvargs and kvargs["op"] is not None:
            if type(kvargs["op"]).__name__ == JSONPatch.__annotations__["op"]:
                self_.op = kvargs["op"]
            else:
                self_.op = kvargs["op"]
        if "path" in kvargs and kvargs["path"] is not None:
            if type(kvargs["path"]).__name__ == JSONPatch.__annotations__["path"]:
                self_.path = kvargs["path"]
            else:
                self_.path = kvargs["path"]
        if "value" in kvargs and kvargs["value"] is not None:
            if type(kvargs["value"]).__name__ == JSONPatch.__annotations__["value"]:
                self_.value = kvargs["value"]
            else:
                self_.value = kvargs["value"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class JSONPatchArray(List["JSONPatch"]):
    """
    An array of JSON Patch documents

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(JSONPatch(**e))


@dataclass
class Metadata:
    """
    An object containing the metadata for the user configuration.

    Attributes
    ----------
    valid_roles: list[str]
      List of system roles to which the user can be assigned.
    """

    valid_roles: list[str] = None

    def __init__(self_, **kvargs):

        if "valid_roles" in kvargs and kvargs["valid_roles"] is not None:
            if (
                type(kvargs["valid_roles"]).__name__
                == Metadata.__annotations__["valid_roles"]
            ):
                self_.valid_roles = kvargs["valid_roles"]
            else:
                self_.valid_roles = kvargs["valid_roles"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserAssignedGroups:
    """
    represents a group entity stored in the database

    Attributes
    ----------
    assignedRoles: list[UserAssignedGroupsAssignedRoles]
      An array of role references.
    id: str
      The unique group identitier
    name: str
      The group name
    """

    assignedRoles: list[UserAssignedGroupsAssignedRoles] = None
    id: str = None
    name: str = None

    def __init__(self_, **kvargs):

        if "assignedRoles" in kvargs and kvargs["assignedRoles"] is not None:
            if (
                len(kvargs["assignedRoles"]) > 0
                and f"list[{type(kvargs['assignedRoles'][0]).__name__}]"
                == UserAssignedGroups.__annotations__["assignedRoles"]
            ):
                self_.assignedRoles = kvargs["assignedRoles"]
            else:
                self_.assignedRoles = [
                    UserAssignedGroupsAssignedRoles(**e)
                    for e in kvargs["assignedRoles"]
                ]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == UserAssignedGroups.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == UserAssignedGroups.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserAssignedGroupsAssignedRoles:
    """
    represents a role entity stored in the database

    Attributes
    ----------
    id: str
      The unique role identitier
    level: str
      The role level
    name: str
      The role name
    permissions: list[str]
      An array of permissions associated to a given role.
    type: str
      The type of role
    """

    id: str = None
    level: str = None
    name: str = None
    permissions: list[str] = None
    type: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if (
                type(kvargs["id"]).__name__
                == UserAssignedGroupsAssignedRoles.__annotations__["id"]
            ):
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "level" in kvargs and kvargs["level"] is not None:
            if (
                type(kvargs["level"]).__name__
                == UserAssignedGroupsAssignedRoles.__annotations__["level"]
            ):
                self_.level = kvargs["level"]
            else:
                self_.level = kvargs["level"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == UserAssignedGroupsAssignedRoles.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "permissions" in kvargs and kvargs["permissions"] is not None:
            if (
                type(kvargs["permissions"]).__name__
                == UserAssignedGroupsAssignedRoles.__annotations__["permissions"]
            ):
                self_.permissions = kvargs["permissions"]
            else:
                self_.permissions = kvargs["permissions"]
        if "type" in kvargs and kvargs["type"] is not None:
            if (
                type(kvargs["type"]).__name__
                == UserAssignedGroupsAssignedRoles.__annotations__["type"]
            ):
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserAssignedRoles:
    """
    represents a role entity stored in the database

    Attributes
    ----------
    id: str
      The unique role identitier
    level: str
      The role level
    name: str
      The role name
    permissions: list[str]
      An array of permissions associated to a given role.
    type: str
      The type of role
    """

    id: str = None
    level: str = None
    name: str = None
    permissions: list[str] = None
    type: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == UserAssignedRoles.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "level" in kvargs and kvargs["level"] is not None:
            if (
                type(kvargs["level"]).__name__
                == UserAssignedRoles.__annotations__["level"]
            ):
                self_.level = kvargs["level"]
            else:
                self_.level = kvargs["level"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == UserAssignedRoles.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "permissions" in kvargs and kvargs["permissions"] is not None:
            if (
                type(kvargs["permissions"]).__name__
                == UserAssignedRoles.__annotations__["permissions"]
            ):
                self_.permissions = kvargs["permissions"]
            else:
                self_.permissions = kvargs["permissions"]
        if "type" in kvargs and kvargs["type"] is not None:
            if (
                type(kvargs["type"]).__name__
                == UserAssignedRoles.__annotations__["type"]
            ):
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserCount:
    """
    The result object for the user count.

    Attributes
    ----------
    total: float
      The total number of users in the tenant.
    """

    total: float = None

    def __init__(self_, **kvargs):

        if "total" in kvargs and kvargs["total"] is not None:
            if type(kvargs["total"]).__name__ == UserCount.__annotations__["total"]:
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserLinks:
    """
    Pagination links to the user.

    Attributes
    ----------
    self: UserLinksSelf
      A link to this user.
    """

    self: UserLinksSelf = None

    def __init__(self_, **kvargs):

        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == UserLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = UserLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserLinksSelf:
    """
    A link to this user.

    Attributes
    ----------
    href: str
      URL that defines the resource.
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs and kvargs["href"] is not None:
            if type(kvargs["href"]).__name__ == UserLinksSelf.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserPostSchema:
    """

    Attributes
    ----------
    assignedRoles: list[UserPostSchemaAssignedRolesRefIDs]
      An array of role reference identifiers.
    email: str
      The email address for the user. This is a required field when inviting a user.
    name: str
      The name of the user.
    picture: str
      A static url linking to the avatar of the user.
    roles: list[str]
      List of system roles to which the user has been assigned. Only returned when permitted by access control.
    status: str
      The status of the created user within the tenant.
    subject: str
      The unique user identitier from an identity provider.
    tenantId: str
      The tenant that the user will belong too.
    """

    assignedRoles: list[UserPostSchemaAssignedRolesRefIDs] = None
    email: str = None
    name: str = None
    picture: str = None
    roles: list[str] = None
    status: str = None
    subject: str = None
    tenantId: str = None

    def __init__(self_, **kvargs):

        if "assignedRoles" in kvargs and kvargs["assignedRoles"] is not None:
            if (
                len(kvargs["assignedRoles"]) > 0
                and f"list[{type(kvargs['assignedRoles'][0]).__name__}]"
                == UserPostSchema.__annotations__["assignedRoles"]
            ):
                self_.assignedRoles = kvargs["assignedRoles"]
            else:
                self_.assignedRoles = [
                    UserPostSchemaAssignedRolesRefIDs(**e)
                    for e in kvargs["assignedRoles"]
                ]
        if "email" in kvargs and kvargs["email"] is not None:
            if (
                type(kvargs["email"]).__name__
                == UserPostSchema.__annotations__["email"]
            ):
                self_.email = kvargs["email"]
            else:
                self_.email = kvargs["email"]
        if "name" in kvargs and kvargs["name"] is not None:
            if type(kvargs["name"]).__name__ == UserPostSchema.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "picture" in kvargs and kvargs["picture"] is not None:
            if (
                type(kvargs["picture"]).__name__
                == UserPostSchema.__annotations__["picture"]
            ):
                self_.picture = kvargs["picture"]
            else:
                self_.picture = kvargs["picture"]
        if "roles" in kvargs and kvargs["roles"] is not None:
            if (
                type(kvargs["roles"]).__name__
                == UserPostSchema.__annotations__["roles"]
            ):
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "status" in kvargs and kvargs["status"] is not None:
            if (
                type(kvargs["status"]).__name__
                == UserPostSchema.__annotations__["status"]
            ):
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "subject" in kvargs and kvargs["subject"] is not None:
            if (
                type(kvargs["subject"]).__name__
                == UserPostSchema.__annotations__["subject"]
            ):
                self_.subject = kvargs["subject"]
            else:
                self_.subject = kvargs["subject"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            if (
                type(kvargs["tenantId"]).__name__
                == UserPostSchema.__annotations__["tenantId"]
            ):
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UserPostSchemaAssignedRolesRefIDs:
    """
    represents a role entity stored in the database

    Attributes
    ----------
    id: str
      The unique role identitier
    """

    id: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if (
                type(kvargs["id"]).__name__
                == UserPostSchemaAssignedRolesRefIDs.__annotations__["id"]
            ):
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UsersClass:
    """

    Attributes
    ----------
    data: list[User]
      List of users.
    links: UsersLinks
      Pagination links
    """

    data: list[User] = None
    links: UsersLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == UsersClass.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [User(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == UsersClass.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = UsersLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UsersLinks:
    """
    Pagination links

    Attributes
    ----------
    next: UsersLinksNext
      Link information for next page
    prev: UsersLinksPrev
      Link information for previous page
    self: UsersLinksSelf
      Link information for current page
    """

    next: UsersLinksNext = None
    prev: UsersLinksPrev = None
    self: UsersLinksSelf = None

    def __init__(self_, **kvargs):

        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == UsersLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = UsersLinksNext(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == UsersLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = UsersLinksPrev(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == UsersLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = UsersLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UsersLinksNext:
    """
    Link information for next page

    Attributes
    ----------
    href: str
      URL to the next page of records
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs and kvargs["href"] is not None:
            if type(kvargs["href"]).__name__ == UsersLinksNext.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UsersLinksPrev:
    """
    Link information for previous page

    Attributes
    ----------
    href: str
      URL to the previous page of records
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs and kvargs["href"] is not None:
            if type(kvargs["href"]).__name__ == UsersLinksPrev.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class UsersLinksSelf:
    """
    Link information for current page

    Attributes
    ----------
    href: str
      URL to the current page of records
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs and kvargs["href"] is not None:
            if type(kvargs["href"]).__name__ == UsersLinksSelf.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Users:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def count(self, tenantId: str = None) -> UserCount:
        """
        Count users
        Returns the number of users in a given tenant

        Parameters
        ----------
        tenantId: str = None
          The tenant ID to filter by.
        """
        query_params = {}
        if tenantId is not None:
            query_params["tenantId"] = tenantId
            warnings.warn("tenantId is deprecated", DeprecationWarning, stacklevel=2)
        response = self.auth.rest(
            path="/users/actions/count",
            method="GET",
            params=query_params,
            data=None,
        )
        obj = UserCount(**response.json())
        obj.auth = self.auth
        return obj

    def filter(
        self,
        data: Filter = None,
        fields: str = None,
        limit: float = 20,
        next: str = None,
        prev: str = None,
        sort: str = "+name",
        max_items: int = 20,
    ) -> ListableResource[User]:
        """
        Filter users
        Retrieves a list of users matching the filter using an advanced query string.

        Parameters
        ----------
        fields: str = None
          A comma-delimited string of the requested fields per entity. If the 'links' value is omitted, then the entity HATEOAS link will also be omitted.
        limit: float = 20
          The number of user entries to retrieve.
        next: str = None
          Get users with IDs that are higher than the target user ID. Cannot be used in conjunction with prev.
        prev: str = None
          Get users with IDs that are lower than the target user ID. Cannot be used in conjunction with next.
        sort: str = "+name"
          The field to sort by, with +/- prefix indicating sort order
        data: Filter = None
          Will contain the query filter to apply. It shall not contain more than 50 ids.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        query_params = {}
        if fields is not None:
            query_params["fields"] = fields
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/users/actions/filter",
            method="POST",
            params=query_params,
            data=data,
        )
        return ListableResource(
            response=response.json(),
            cls=User,
            auth=self.auth,
            path="/users/actions/filter",
            max_items=max_items,
            query_params=query_params,
        )

    def get_me(self) -> User:
        """
        Get my user
        Redirects to retrieve the user resource associated with the JWT claims.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/users/me",
            method="GET",
            params={},
            data=None,
        )
        obj = User(**response.json())
        obj.auth = self.auth
        return obj

    def get_metadata(self) -> Metadata:
        """
        Get configuration metadata
        Returns the metadata with regard to the user configuration. Deprecated, use GET /v1/roles instead.

        Parameters
        ----------
        """
        warnings.warn("get_metadata is deprecated", DeprecationWarning, stacklevel=2)
        response = self.auth.rest(
            path="/users/metadata",
            method="GET",
            params={},
            data=None,
        )
        obj = Metadata(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, userId: str) -> User:
        """
        Get user by ID
        Returns the requested user.

        Parameters
        ----------
        userId: str
          The user's unique identifier
        """
        response = self.auth.rest(
            path="/users/{userId}".replace("{userId}", userId),
            method="GET",
            params={},
            data=None,
        )
        obj = User(**response.json())
        obj.auth = self.auth
        return obj

    def get_users(
        self,
        fields: str = None,
        filter: str = None,
        limit: float = 20,
        next: str = None,
        prev: str = None,
        sort: str = "+name",
        email: str = None,
        endingBefore: str = None,
        role: str = None,
        sortBy: str = "name",
        sortOrder: str = "asc",
        startingAfter: str = None,
        status: str = "active",
        subject: str = None,
        tenantId: str = None,
        max_items: int = 20,
    ) -> ListableResource[User]:
        """
        List users
        Returns a list of users using cursor-based pagination.

        Parameters
        ----------
        fields: str = None
          A comma-delimited string of the requested fields per entity. If the 'links' value is omitted, then the entity HATEOAS link will also be omitted.
        filter: str = None
          The advanced filtering to use for the query. Refer to RFC 7644 https://datatracker.ietf.org/doc/rfc7644/ for the syntax. Cannot be combined with any of the fields marked as deprecated. All conditional statements within this query parameter are case insensitive.

          The following fields support the `eq` operator: `id`, `subject`, `name`, `email`, `status`, `clientId`, `assignedRoles.id` `assignedRoles.name`, `assignedGroups.id`, `assignedGroupsAssignedRoles.name`

          Additionally, the following fields support the `co` operator: `name`, `email`, `subject`

          Queries may be rate limited if they differ greatly from these examples:

          ```
          (id eq "62716ab404a7bd8626af9bd6" or id eq "62716ac4c7e500e13ff5fa22") and (status eq "active" or status eq "disabled")
          ```

          ```
          name co "query" or email co "query" or subject co "query" or id eq "query" or assignedRoles.name eq "query"
          ```

          Any filters for status must be grouped together and applied to the whole query.

          Valid:

          ```
          (name eq "Bob" or name eq "Alice") and (status eq "active" or status eq "disabled")
          ```

          Invalid:

          ```
          name eq "Bob" or name eq "Alice" and (status eq "active" or status eq "disabled")
          ```

        limit: float = 20
          The number of user entries to retrieve.
        next: str = None
          Get users that come after this cursor value when sorted. Cannot be used in conjunction with `prev`.
        prev: str = None
          Get users that come before this cursor value when sorted. Cannot be used in conjunction with `next`.
        sort: str = "+name"
          The field to sort by, with +/- prefix indicating sort order
        email: str = None
          The email to filter by. Deprecated. Use the new `filter` parameter to provide an advanced query filter.
        endingBefore: str = None
          Get users with IDs that are lower than the target user ID. Cannot be used in conjunction with startingAfter. Deprecated. Use `prev` instead.
        role: str = None
          The role to filter by. Deprecated.
        sortBy: str = "name"
          The user parameter to sort by. Deprecated. Use `sort` instead.
        sortOrder: str = "asc"
          The sort order, either ascending or descending. Deprecated. Use `sort` instead.
        startingAfter: str = None
          Get users with IDs that are higher than the target user ID. Cannot be used in conjunction with endingBefore. Deprecated. Use `next` instead.
        status: str = "active"
          The status to filter by. Supports multiple values delimited by commas. Deprecated. Use the new `filter` parameter to provide an advanced query filter.
        subject: str = None
          The subject to filter by. Deprecated. Use the new `filter` parameter to provide an advanced query filter.
        tenantId: str = None
          The tenant ID to filter by. Deprecated.
        """
        query_params = {}
        if fields is not None:
            query_params["fields"] = fields
        if filter is not None:
            query_params["filter"] = filter
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        if email is not None:
            query_params["email"] = email
            warnings.warn("email is deprecated", DeprecationWarning, stacklevel=2)
        if endingBefore is not None:
            query_params["endingBefore"] = endingBefore
            warnings.warn(
                "endingBefore is deprecated", DeprecationWarning, stacklevel=2
            )
        if role is not None:
            query_params["role"] = role
            warnings.warn("role is deprecated", DeprecationWarning, stacklevel=2)
        if sortBy is not None:
            query_params["sortBy"] = sortBy
            warnings.warn("sortBy is deprecated", DeprecationWarning, stacklevel=2)
        if sortOrder is not None:
            query_params["sortOrder"] = sortOrder
            warnings.warn("sortOrder is deprecated", DeprecationWarning, stacklevel=2)
        if startingAfter is not None:
            query_params["startingAfter"] = startingAfter
            warnings.warn(
                "startingAfter is deprecated", DeprecationWarning, stacklevel=2
            )
        if status is not None:
            query_params["status"] = status
            warnings.warn("status is deprecated", DeprecationWarning, stacklevel=2)
        if subject is not None:
            query_params["subject"] = subject
            warnings.warn("subject is deprecated", DeprecationWarning, stacklevel=2)
        if tenantId is not None:
            query_params["tenantId"] = tenantId
            warnings.warn("tenantId is deprecated", DeprecationWarning, stacklevel=2)
        response = self.auth.rest(
            path="/users",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=User,
            auth=self.auth,
            path="/users",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: UserPostSchema) -> User:
        """
        Create user
        Creates an invited user.

        Parameters
        ----------
        data: UserPostSchema

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/users",
            method="POST",
            params={},
            data=data,
        )
        obj = User(**response.json())
        obj.auth = self.auth
        return obj
