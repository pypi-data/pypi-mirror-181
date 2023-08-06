# This is spectacularly generated code by spectacular v0.8.0 based on
# Qlik Cloud Services 0.529.8

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class ApiKey:
    """

    Attributes
    ----------
    created: str
      When the API key was created.
    createdByUser: str
      The ID of the user who created the key.
    description: str
      A description for the API key.
    expiry: str
      When the API key will expire and no longer be a valid authentication token.
    id: str
      The unique ID for the resource.
    lastUpdated: str
      When the API key was last updated.
    status: str
    sub: str
      The ID of the subject for the API key.
    subType: str
      Type of the subject.
    tenantId: str
      The tenant ID.
    """

    created: str = None
    createdByUser: str = None
    description: str = None
    expiry: str = None
    id: str = None
    lastUpdated: str = None
    status: str = None
    sub: str = None
    subType: str = None
    tenantId: str = None

    def __init__(self_, **kvargs):

        if "created" in kvargs and kvargs["created"] is not None:
            if type(kvargs["created"]).__name__ == ApiKey.__annotations__["created"]:
                self_.created = kvargs["created"]
            else:
                self_.created = kvargs["created"]
        if "createdByUser" in kvargs and kvargs["createdByUser"] is not None:
            if (
                type(kvargs["createdByUser"]).__name__
                == ApiKey.__annotations__["createdByUser"]
            ):
                self_.createdByUser = kvargs["createdByUser"]
            else:
                self_.createdByUser = kvargs["createdByUser"]
        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == ApiKey.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "expiry" in kvargs and kvargs["expiry"] is not None:
            if type(kvargs["expiry"]).__name__ == ApiKey.__annotations__["expiry"]:
                self_.expiry = kvargs["expiry"]
            else:
                self_.expiry = kvargs["expiry"]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == ApiKey.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "lastUpdated" in kvargs and kvargs["lastUpdated"] is not None:
            if (
                type(kvargs["lastUpdated"]).__name__
                == ApiKey.__annotations__["lastUpdated"]
            ):
                self_.lastUpdated = kvargs["lastUpdated"]
            else:
                self_.lastUpdated = kvargs["lastUpdated"]
        if "status" in kvargs and kvargs["status"] is not None:
            if type(kvargs["status"]).__name__ == ApiKey.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "sub" in kvargs and kvargs["sub"] is not None:
            if type(kvargs["sub"]).__name__ == ApiKey.__annotations__["sub"]:
                self_.sub = kvargs["sub"]
            else:
                self_.sub = kvargs["sub"]
        if "subType" in kvargs and kvargs["subType"] is not None:
            if type(kvargs["subType"]).__name__ == ApiKey.__annotations__["subType"]:
                self_.subType = kvargs["subType"]
            else:
                self_.subType = kvargs["subType"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            if type(kvargs["tenantId"]).__name__ == ApiKey.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Deletes or revokes an API key.
        When the owner of the API key sends the request, the key will be removed. When a TenantAdmin sends the request, the key will be revoked.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/api-keys/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, data: ApiKeysPatchSchema) -> None:
        """
        Updates an API key for a given ID.

        Parameters
        ----------
        data: ApiKeysPatchSchema

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/api-keys/{id}".replace("{id}", self.id),
            method="PATCH",
            params={},
            data=data,
        )


@dataclass
class ApiKeyBody:
    """

    Attributes
    ----------
    description: str
      Text that describes the API key.
    expiry: str
      The expiry of the API key, in ISO8601 duration format.
    sub: str
      The ID of the subject for the API key.
    subType: str
      Type of the subject.
    """

    description: str = None
    expiry: str = None
    sub: str = None
    subType: str = None

    def __init__(self_, **kvargs):

        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == ApiKeyBody.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "expiry" in kvargs and kvargs["expiry"] is not None:
            if type(kvargs["expiry"]).__name__ == ApiKeyBody.__annotations__["expiry"]:
                self_.expiry = kvargs["expiry"]
            else:
                self_.expiry = kvargs["expiry"]
        if "sub" in kvargs and kvargs["sub"] is not None:
            if type(kvargs["sub"]).__name__ == ApiKeyBody.__annotations__["sub"]:
                self_.sub = kvargs["sub"]
            else:
                self_.sub = kvargs["sub"]
        if "subType" in kvargs and kvargs["subType"] is not None:
            if (
                type(kvargs["subType"]).__name__
                == ApiKeyBody.__annotations__["subType"]
            ):
                self_.subType = kvargs["subType"]
            else:
                self_.subType = kvargs["subType"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ApiKeyConfigPatch:
    """
    A JSON Patch document as defined in https://datatracker.ietf.org/doc/html/rfc6902.

    Attributes
    ----------
    op: str
      The operation to be performed.
    path: str
      The path for the given resource field to patch.
    value: object
      The value to be used for this operation.
    """

    op: str = None
    path: str = None
    value: object = None

    def __init__(self_, **kvargs):

        if "op" in kvargs and kvargs["op"] is not None:
            if type(kvargs["op"]).__name__ == ApiKeyConfigPatch.__annotations__["op"]:
                self_.op = kvargs["op"]
            else:
                self_.op = kvargs["op"]
        if "path" in kvargs and kvargs["path"] is not None:
            if (
                type(kvargs["path"]).__name__
                == ApiKeyConfigPatch.__annotations__["path"]
            ):
                self_.path = kvargs["path"]
            else:
                self_.path = kvargs["path"]
        if "value" in kvargs and kvargs["value"] is not None:
            if (
                type(kvargs["value"]).__name__
                == ApiKeyConfigPatch.__annotations__["value"]
            ):
                self_.value = kvargs["value"]
            else:
                self_.value = kvargs["value"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ApiKeyPatch:
    """
    A JSON Patch document as defined in https://datatracker.ietf.org/doc/html/rfc6902.

    Attributes
    ----------
    op: str
      The operation to be performed.
    path: str
      The path for the given resource field to patch.
    value: str
      The value to be used for this operation.
    """

    op: str = None
    path: str = None
    value: str = None

    def __init__(self_, **kvargs):

        if "op" in kvargs and kvargs["op"] is not None:
            if type(kvargs["op"]).__name__ == ApiKeyPatch.__annotations__["op"]:
                self_.op = kvargs["op"]
            else:
                self_.op = kvargs["op"]
        if "path" in kvargs and kvargs["path"] is not None:
            if type(kvargs["path"]).__name__ == ApiKeyPatch.__annotations__["path"]:
                self_.path = kvargs["path"]
            else:
                self_.path = kvargs["path"]
        if "value" in kvargs and kvargs["value"] is not None:
            if type(kvargs["value"]).__name__ == ApiKeyPatch.__annotations__["value"]:
                self_.value = kvargs["value"]
            else:
                self_.value = kvargs["value"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ApiKeyWithToken:
    """

    Attributes
    ----------
    created: str
      When the API key was created.
    createdByUser: str
      The id of the user who created the key.
    description: str
      A description for the API key.
    expiry: str
      When the API key will expire and no longer be a valid authentication token.
    id: str
      The unique ID for the resource.
    lastUpdated: str
      When the API key was last updated.
    status: str
    sub: str
      The ID of the subject for the API key.
    subType: str
      Type of the subject.
    tenantId: str
      The tenant ID.
    token: str
      The generated signed JWT.
    """

    created: str = None
    createdByUser: str = None
    description: str = None
    expiry: str = None
    id: str = None
    lastUpdated: str = None
    status: str = None
    sub: str = None
    subType: str = None
    tenantId: str = None
    token: str = None

    def __init__(self_, **kvargs):

        if "created" in kvargs and kvargs["created"] is not None:
            if (
                type(kvargs["created"]).__name__
                == ApiKeyWithToken.__annotations__["created"]
            ):
                self_.created = kvargs["created"]
            else:
                self_.created = kvargs["created"]
        if "createdByUser" in kvargs and kvargs["createdByUser"] is not None:
            if (
                type(kvargs["createdByUser"]).__name__
                == ApiKeyWithToken.__annotations__["createdByUser"]
            ):
                self_.createdByUser = kvargs["createdByUser"]
            else:
                self_.createdByUser = kvargs["createdByUser"]
        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == ApiKeyWithToken.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "expiry" in kvargs and kvargs["expiry"] is not None:
            if (
                type(kvargs["expiry"]).__name__
                == ApiKeyWithToken.__annotations__["expiry"]
            ):
                self_.expiry = kvargs["expiry"]
            else:
                self_.expiry = kvargs["expiry"]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == ApiKeyWithToken.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "lastUpdated" in kvargs and kvargs["lastUpdated"] is not None:
            if (
                type(kvargs["lastUpdated"]).__name__
                == ApiKeyWithToken.__annotations__["lastUpdated"]
            ):
                self_.lastUpdated = kvargs["lastUpdated"]
            else:
                self_.lastUpdated = kvargs["lastUpdated"]
        if "status" in kvargs and kvargs["status"] is not None:
            if (
                type(kvargs["status"]).__name__
                == ApiKeyWithToken.__annotations__["status"]
            ):
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "sub" in kvargs and kvargs["sub"] is not None:
            if type(kvargs["sub"]).__name__ == ApiKeyWithToken.__annotations__["sub"]:
                self_.sub = kvargs["sub"]
            else:
                self_.sub = kvargs["sub"]
        if "subType" in kvargs and kvargs["subType"] is not None:
            if (
                type(kvargs["subType"]).__name__
                == ApiKeyWithToken.__annotations__["subType"]
            ):
                self_.subType = kvargs["subType"]
            else:
                self_.subType = kvargs["subType"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            if (
                type(kvargs["tenantId"]).__name__
                == ApiKeyWithToken.__annotations__["tenantId"]
            ):
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "token" in kvargs and kvargs["token"] is not None:
            if (
                type(kvargs["token"]).__name__
                == ApiKeyWithToken.__annotations__["token"]
            ):
                self_.token = kvargs["token"]
            else:
                self_.token = kvargs["token"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ApiKeysConfig:
    """

    Attributes
    ----------
    api_keys_enabled: bool
      Enables or disables API key functionality for the specified tenant.
    max_api_key_expiry: str
      The maximum lifetime, in ISO8601 duration format, for which an API key can be issued for the specified tenant.
    max_keys_per_user: float
      The maximum number of active API keys that any user can create for the specified tenant.
    scim_externalClient_expiry: str
      The expiry of the scim externalClient token in ISO8601 duration format. Used during the creation of an externalClient API key.
    """

    api_keys_enabled: bool = None
    max_api_key_expiry: str = "PT24H"
    max_keys_per_user: float = 5
    scim_externalClient_expiry: str = "P365D"

    def __init__(self_, **kvargs):

        if "api_keys_enabled" in kvargs and kvargs["api_keys_enabled"] is not None:
            if (
                type(kvargs["api_keys_enabled"]).__name__
                == ApiKeysConfig.__annotations__["api_keys_enabled"]
            ):
                self_.api_keys_enabled = kvargs["api_keys_enabled"]
            else:
                self_.api_keys_enabled = kvargs["api_keys_enabled"]
        if "max_api_key_expiry" in kvargs and kvargs["max_api_key_expiry"] is not None:
            if (
                type(kvargs["max_api_key_expiry"]).__name__
                == ApiKeysConfig.__annotations__["max_api_key_expiry"]
            ):
                self_.max_api_key_expiry = kvargs["max_api_key_expiry"]
            else:
                self_.max_api_key_expiry = kvargs["max_api_key_expiry"]
        if "max_keys_per_user" in kvargs and kvargs["max_keys_per_user"] is not None:
            if (
                type(kvargs["max_keys_per_user"]).__name__
                == ApiKeysConfig.__annotations__["max_keys_per_user"]
            ):
                self_.max_keys_per_user = kvargs["max_keys_per_user"]
            else:
                self_.max_keys_per_user = kvargs["max_keys_per_user"]
        if (
            "scim_externalClient_expiry" in kvargs
            and kvargs["scim_externalClient_expiry"] is not None
        ):
            if (
                type(kvargs["scim_externalClient_expiry"]).__name__
                == ApiKeysConfig.__annotations__["scim_externalClient_expiry"]
            ):
                self_.scim_externalClient_expiry = kvargs["scim_externalClient_expiry"]
            else:
                self_.scim_externalClient_expiry = kvargs["scim_externalClient_expiry"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ApiKeysConfigPatchSchema(List["ApiKeyConfigPatch"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(ApiKeyConfigPatch(**e))


@dataclass
class ApiKeysPatchSchema(List["ApiKeyPatch"]):
    """

    Attributes
    ----------
    """

    def __init__(self_, elements):
        for e in elements:
            self_.append(ApiKeyPatch(**e))


@dataclass
class Link:
    """

    Attributes
    ----------
    href: str
      The URL for the link.
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs and kvargs["href"] is not None:
            if type(kvargs["href"]).__name__ == Link.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ApiKeyPage:
    """

    Attributes
    ----------
    data: list[ApiKey]
    links: ApiKeyPageLinks
    """

    data: list[ApiKey] = None
    links: ApiKeyPageLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == ApiKeyPage.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [ApiKey(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == ApiKeyPage.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ApiKeyPageLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ApiKeyPageLinks:
    """

    Attributes
    ----------
    next: Link
    prev: Link
    self: Link
    """

    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):

        if "next" in kvargs and kvargs["next"] is not None:
            if type(kvargs["next"]).__name__ == ApiKeyPageLinks.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if type(kvargs["prev"]).__name__ == ApiKeyPageLinks.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if type(kvargs["self"]).__name__ == ApiKeyPageLinks.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class ApiKeys:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_config(self, tenantId: str) -> ApiKeysConfig:
        """
        Gets the API keys configuration for a given tenant ID.

        Parameters
        ----------
        tenantId: str
          The tenant ID of the API keys configuration to be retrieved.
        """
        response = self.auth.rest(
            path="/api-keys/configs/{tenantId}".replace("{tenantId}", tenantId),
            method="GET",
            params={},
            data=None,
        )
        obj = ApiKeysConfig(**response.json())
        obj.auth = self.auth
        return obj

    def patch_config(self, tenantId: str, data: ApiKeysConfigPatchSchema) -> None:
        """
        Updates the API keys configuration for a given tenant ID.

        Parameters
        ----------
        tenantId: str
          The tenant ID of the API keys configuration to be retrieved.
        data: ApiKeysConfigPatchSchema

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/api-keys/configs/{tenantId}".replace("{tenantId}", tenantId),
            method="PATCH",
            params={},
            data=data,
        )

    def get(self, id: str) -> ApiKey:
        """
        Gets the API key for a given ID.

        Parameters
        ----------
        id: str
          The ID of the API key resource to be retrieved.
        """
        response = self.auth.rest(
            path="/api-keys/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = ApiKey(**response.json())
        obj.auth = self.auth
        return obj

    def get_api_keys(
        self,
        createdByUser: str = None,
        endingBefore: str = None,
        limit: float = 20,
        sort: str = "-created",
        startingAfter: str = None,
        status: str = None,
        sub: str = None,
        max_items: int = 20,
    ) -> ListableResource[ApiKey]:
        """
        Lists API keys for a given tenant ID.

        Parameters
        ----------
        createdByUser: str = None
          The user ID that created the API key.
        endingBefore: str = None
          Get resources with IDs that are lower than the target resource ID. Cannot be used in conjunction with startingAfter.
        limit: float = 20
          Maximum number of API keys to retrieve.
        sort: str = "-created"
          The field to sort by, with +/- prefix indicating sort order
        startingAfter: str = None
          Get resources with IDs that are higher than the target resource ID. Cannot be used in conjunction with endingBefore.
        status: str = None
          The status of the API key.
        sub: str = None
          The ID of the subject.
        """
        query_params = {}
        if createdByUser is not None:
            query_params["createdByUser"] = createdByUser
        if endingBefore is not None:
            query_params["endingBefore"] = endingBefore
        if limit is not None:
            query_params["limit"] = limit
        if sort is not None:
            query_params["sort"] = sort
        if startingAfter is not None:
            query_params["startingAfter"] = startingAfter
        if status is not None:
            query_params["status"] = status
        if sub is not None:
            query_params["sub"] = sub
        response = self.auth.rest(
            path="/api-keys",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ApiKey,
            auth=self.auth,
            path="/api-keys",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: ApiKeyBody) -> ApiKeyWithToken:
        """
        Creates an API key resource.

        Parameters
        ----------
        data: ApiKeyBody

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/api-keys",
            method="POST",
            params={},
            data=data,
        )
        obj = ApiKeyWithToken(**response.json())
        obj.auth = self.auth
        return obj
