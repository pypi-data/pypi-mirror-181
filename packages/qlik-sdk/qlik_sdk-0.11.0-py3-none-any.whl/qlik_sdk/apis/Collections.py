# This is spectacularly generated code by spectacular v0.8.0 based on
# Qlik Cloud Services 0.529.8

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class CollectionResultResponseBody:
    """
    A collection.

    Attributes
    ----------
    createdAt: str
      The RFC3339 datetime when the collection was created.
    creatorId: str
      The ID of the user who created the collection. This property is only populated if the JWT contains a userId.
    description: str
    id: str
      The collection's unique identifier.
    itemCount: int
      The number of items that have been added to the collection.
    links: CollectionLinksResponseBody
    meta: CollectionMetaResponseBody
      Collection metadata and computed fields.
    name: str
    tenantId: str
      The ID of the tenant that owns the collection. This property is populated by using JWT.
    type: str
      The collection's type.
    updatedAt: str
      The RFC3339 datetime when the collection was last updated.
    updaterId: str
      The ID of the user who last updated the collection. This property is only populated if the JWT contains a userId.
    """

    createdAt: str = None
    creatorId: str = None
    description: str = None
    id: str = None
    itemCount: int = None
    links: CollectionLinksResponseBody = None
    meta: CollectionMetaResponseBody = None
    name: str = None
    tenantId: str = None
    type: str = None
    updatedAt: str = None
    updaterId: str = None

    def __init__(self_, **kvargs):

        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            if (
                type(kvargs["createdAt"]).__name__
                == CollectionResultResponseBody.__annotations__["createdAt"]
            ):
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "creatorId" in kvargs and kvargs["creatorId"] is not None:
            if (
                type(kvargs["creatorId"]).__name__
                == CollectionResultResponseBody.__annotations__["creatorId"]
            ):
                self_.creatorId = kvargs["creatorId"]
            else:
                self_.creatorId = kvargs["creatorId"]
        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == CollectionResultResponseBody.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "id" in kvargs and kvargs["id"] is not None:
            if (
                type(kvargs["id"]).__name__
                == CollectionResultResponseBody.__annotations__["id"]
            ):
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "itemCount" in kvargs and kvargs["itemCount"] is not None:
            if (
                type(kvargs["itemCount"]).__name__
                == CollectionResultResponseBody.__annotations__["itemCount"]
            ):
                self_.itemCount = kvargs["itemCount"]
            else:
                self_.itemCount = kvargs["itemCount"]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == CollectionResultResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = CollectionLinksResponseBody(**kvargs["links"])
        if "meta" in kvargs and kvargs["meta"] is not None:
            if (
                type(kvargs["meta"]).__name__
                == CollectionResultResponseBody.__annotations__["meta"]
            ):
                self_.meta = kvargs["meta"]
            else:
                self_.meta = CollectionMetaResponseBody(**kvargs["meta"])
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == CollectionResultResponseBody.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            if (
                type(kvargs["tenantId"]).__name__
                == CollectionResultResponseBody.__annotations__["tenantId"]
            ):
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs and kvargs["type"] is not None:
            if (
                type(kvargs["type"]).__name__
                == CollectionResultResponseBody.__annotations__["type"]
            ):
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            if (
                type(kvargs["updatedAt"]).__name__
                == CollectionResultResponseBody.__annotations__["updatedAt"]
            ):
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "updaterId" in kvargs and kvargs["updaterId"] is not None:
            if (
                type(kvargs["updaterId"]).__name__
                == CollectionResultResponseBody.__annotations__["updaterId"]
            ):
                self_.updaterId = kvargs["updaterId"]
            else:
                self_.updaterId = kvargs["updaterId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_items(
        self,
        limit: int = 10,
        name: str = None,
        next: str = None,
        prev: str = None,
        query: str = None,
        resourceId: str = None,
        resourceLink: str = None,
        resourceType: str = None,
        shared: bool = None,
        sort: str = None,
        spaceId: str = None,
        noActions: bool = False,
    ) -> CollectionsListCollectionItemsResponseBody:
        """
        Retrieves items in a collection.
        Finds and returns items from a collection that the user has access to.


        Parameters
        ----------
        limit: int = 10
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        name: str = None
          The case-insensitive string used to search for a resource by name.
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        query: str = None
          The case-insensitive string used to search for a resource by name or description.
        resourceId: str = None
          The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
        resourceLink: str = None
          The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
        resourceType: str = None
          The case-sensitive string used to search for an item by resourceType.
        shared: bool = None
          Whether or not to return items in a shared space.
        sort: str = None
          The property of a resource to sort on (default sort is +createdAt). The supported properties are createdAt, updatedAt, and name. A property must be prefixed by + or   - to indicate ascending or descending sort order respectively.
        spaceId: str = None
          The space's unique identifier (supports \'personal\' as spaceId).
        noActions: bool = False
          If set to true, the user's available actions for each item will not be evaluated meaning the actions-array will be omitted from the response (reduces response time).

        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if query is not None:
            query_params["query"] = query
        if resourceId is not None:
            query_params["resourceId"] = resourceId
        if resourceLink is not None:
            query_params["resourceLink"] = resourceLink
        if resourceType is not None:
            query_params["resourceType"] = resourceType
        if shared is not None:
            query_params["shared"] = shared
        if sort is not None:
            query_params["sort"] = sort
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        if noActions is not None:
            query_params["noActions"] = noActions
        response = self.auth.rest(
            path="/collections/{collectionId}/items".replace("{collectionId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        obj = CollectionsListCollectionItemsResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def create_item(
        self, data: CollectionsAddCollectionItemRequestBody
    ) -> ItemResultResponseBody:
        """
        Adds an item to a collection.
        Adds an item to a collection and returns the item.


        Parameters
        ----------
        data: CollectionsAddCollectionItemRequestBody

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/collections/{collectionId}/items".replace("{collectionId}", self.id),
            method="POST",
            params={},
            data=data,
        )
        obj = ItemResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def delete(self) -> None:
        """
        Deletes a collection.
        Deletes a collection and removes all items from the collection.


        Parameters
        ----------
        """
        self.auth.rest(
            path="/collections/{collectionId}".replace("{collectionId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(
        self, data: CollectionsUpdateCollectionRequestBody
    ) -> CollectionResultResponseBody:
        """
        Updates a collection.
        Updates a collection and returns the new collection. Omitted and unsupported fields are ignored. To unset a field, provide the field's zero value.


        Parameters
        ----------
        data: CollectionsUpdateCollectionRequestBody

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/collections/{collectionId}".replace("{collectionId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class CollectionsAddCollectionItemRequestBody:
    """

    Attributes
    ----------
    id: str
      The item's unique identifier.
    """

    id: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if (
                type(kvargs["id"]).__name__
                == CollectionsAddCollectionItemRequestBody.__annotations__["id"]
            ):
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionsCreateCollectionRequestBody:
    """

    Attributes
    ----------
    description: str
    name: str
    type: str
      The collection's type.
    """

    description: str = None
    name: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == CollectionsCreateCollectionRequestBody.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == CollectionsCreateCollectionRequestBody.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "type" in kvargs and kvargs["type"] is not None:
            if (
                type(kvargs["type"]).__name__
                == CollectionsCreateCollectionRequestBody.__annotations__["type"]
            ):
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionsListCollectionItemsResponseBody:
    """
    ListCollectionItemsResponseBody result type

    Attributes
    ----------
    data: list[ItemResultResponseBody]
    """

    data: list[ItemResultResponseBody] = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == CollectionsListCollectionItemsResponseBody.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [ItemResultResponseBody(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionsListCollectionsResponseBody:
    """
    ListCollectionsResponseBody result type

    Attributes
    ----------
    data: list[CollectionResultResponseBody]
    links: CollectionsLinksResponseBody
    """

    data: list[CollectionResultResponseBody] = None
    links: CollectionsLinksResponseBody = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == CollectionsListCollectionsResponseBody.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [CollectionResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == CollectionsListCollectionsResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = CollectionsLinksResponseBody(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionsUpdateCollectionRequestBody:
    """

    Attributes
    ----------
    description: str
    name: str
    """

    description: str = None
    name: str = None

    def __init__(self_, **kvargs):

        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == CollectionsUpdateCollectionRequestBody.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == CollectionsUpdateCollectionRequestBody.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Link:
    """

    Attributes
    ----------
    href: str
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
class CollectionLinksResponseBody:
    """

    Attributes
    ----------
    items: Link
    self: Link
    """

    items: Link = None
    self: Link = None

    def __init__(self_, **kvargs):

        if "items" in kvargs and kvargs["items"] is not None:
            if (
                type(kvargs["items"]).__name__
                == CollectionLinksResponseBody.__annotations__["items"]
            ):
                self_.items = kvargs["items"]
            else:
                self_.items = Link(**kvargs["items"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == CollectionLinksResponseBody.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionMetaResponseBody:
    """
    Collection metadata and computed fields.

    Attributes
    ----------
    items: ItemsResultResponseBody
      Multiple items.
    """

    items: ItemsResultResponseBody = None

    def __init__(self_, **kvargs):

        if "items" in kvargs and kvargs["items"] is not None:
            if (
                type(kvargs["items"]).__name__
                == CollectionMetaResponseBody.__annotations__["items"]
            ):
                self_.items = kvargs["items"]
            else:
                self_.items = ItemsResultResponseBody(**kvargs["items"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionsLinksResponseBody:
    """

    Attributes
    ----------
    item: Link
    next: Link
    prev: Link
    self: Link
    """

    item: Link = None
    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):

        if "item" in kvargs and kvargs["item"] is not None:
            if (
                type(kvargs["item"]).__name__
                == CollectionsLinksResponseBody.__annotations__["item"]
            ):
                self_.item = kvargs["item"]
            else:
                self_.item = Link(**kvargs["item"])
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == CollectionsLinksResponseBody.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == CollectionsLinksResponseBody.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == CollectionsLinksResponseBody.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemLinksResponseBody:
    """

    Attributes
    ----------
    collections: Link
    open: Link
    self: Link
    thumbnail: Link
    """

    collections: Link = None
    open: Link = None
    self: Link = None
    thumbnail: Link = None

    def __init__(self_, **kvargs):

        if "collections" in kvargs and kvargs["collections"] is not None:
            if (
                type(kvargs["collections"]).__name__
                == ItemLinksResponseBody.__annotations__["collections"]
            ):
                self_.collections = kvargs["collections"]
            else:
                self_.collections = Link(**kvargs["collections"])
        if "open" in kvargs and kvargs["open"] is not None:
            if (
                type(kvargs["open"]).__name__
                == ItemLinksResponseBody.__annotations__["open"]
            ):
                self_.open = kvargs["open"]
            else:
                self_.open = Link(**kvargs["open"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == ItemLinksResponseBody.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        if "thumbnail" in kvargs and kvargs["thumbnail"] is not None:
            if (
                type(kvargs["thumbnail"]).__name__
                == ItemLinksResponseBody.__annotations__["thumbnail"]
            ):
                self_.thumbnail = kvargs["thumbnail"]
            else:
                self_.thumbnail = Link(**kvargs["thumbnail"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemMetaResponseBody:
    """
    Item metadata and computed fields.

    Attributes
    ----------
    actions: list[str]
      The actions that the user can perform on the item.
    collections: list[ItemTagResponseBody]
      An array of collections that the item is part of.
    isFavorited: bool
      The flag that indicates if item is in the user's favorites collection.
    tags: list[ItemTagResponseBody]
      An array of tags that the item is part of.
    """

    actions: list[str] = None
    collections: list[ItemTagResponseBody] = None
    isFavorited: bool = None
    tags: list[ItemTagResponseBody] = None

    def __init__(self_, **kvargs):

        if "actions" in kvargs and kvargs["actions"] is not None:
            if (
                type(kvargs["actions"]).__name__
                == ItemMetaResponseBody.__annotations__["actions"]
            ):
                self_.actions = kvargs["actions"]
            else:
                self_.actions = kvargs["actions"]
        if "collections" in kvargs and kvargs["collections"] is not None:
            if (
                len(kvargs["collections"]) > 0
                and f"list[{type(kvargs['collections'][0]).__name__}]"
                == ItemMetaResponseBody.__annotations__["collections"]
            ):
                self_.collections = kvargs["collections"]
            else:
                self_.collections = [
                    ItemTagResponseBody(**e) for e in kvargs["collections"]
                ]
        if "isFavorited" in kvargs and kvargs["isFavorited"] is not None:
            if (
                type(kvargs["isFavorited"]).__name__
                == ItemMetaResponseBody.__annotations__["isFavorited"]
            ):
                self_.isFavorited = kvargs["isFavorited"]
            else:
                self_.isFavorited = kvargs["isFavorited"]
        if "tags" in kvargs and kvargs["tags"] is not None:
            if (
                len(kvargs["tags"]) > 0
                and f"list[{type(kvargs['tags'][0]).__name__}]"
                == ItemMetaResponseBody.__annotations__["tags"]
            ):
                self_.tags = kvargs["tags"]
            else:
                self_.tags = [ItemTagResponseBody(**e) for e in kvargs["tags"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemResultResponseBody:
    """
    An item.

    Attributes
    ----------
    actions: list[str]
      The actions that the user can perform on the item.
    collectionIds: list[str]
      The ID of the collections that the item has been added to.
    createdAt: str
      The RFC3339 datetime when the item was created.
    creatorId: str
      The ID of the user who created the item. This is only populated if the JWT contains a userId.
    description: str
    id: str
      The item's unique identifier.
    isFavorited: bool
      The flag that indicates if item is in the user's favorites collection.
    itemViews: ItemViewsResponseBody
    links: ItemLinksResponseBody
    meta: ItemMetaResponseBody
      Item metadata and computed fields.
    name: str
    ownerId: str
      The ID of the user who owns the item.
    resourceAttributes: object
    resourceCreatedAt: str
      The RFC3339 datetime when the resource that the item references was created.
    resourceCustomAttributes: object
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceReloadEndTime: str
      The RFC3339 datetime when the resource last reload ended.
    resourceReloadStatus: str
      If the resource last reload was successful or not.
    resourceSize: ItemsResourceSizeResponseBody
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    resourceType: str
      The case-sensitive string defining the item's type.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    spaceId: str
      The space's unique identifier.
    tenantId: str
      The ID of the tenant that owns the item. This is populated using the JWT.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    updatedAt: str
      The RFC3339 datetime when the item was last updated.
    updaterId: str
      ID of the user who last updated the item. This is only populated if the JWT contains a userId.
    """

    actions: list[str] = None
    collectionIds: list[str] = None
    createdAt: str = None
    creatorId: str = None
    description: str = None
    id: str = None
    isFavorited: bool = None
    itemViews: ItemViewsResponseBody = None
    links: ItemLinksResponseBody = None
    meta: ItemMetaResponseBody = None
    name: str = None
    ownerId: str = None
    resourceAttributes: object = None
    resourceCreatedAt: str = None
    resourceCustomAttributes: object = None
    resourceId: str = None
    resourceLink: str = None
    resourceReloadEndTime: str = None
    resourceReloadStatus: str = None
    resourceSize: ItemsResourceSizeResponseBody = None
    resourceSubType: str = None
    resourceType: str = None
    resourceUpdatedAt: str = None
    spaceId: str = None
    tenantId: str = None
    thumbnailId: str = None
    updatedAt: str = None
    updaterId: str = None

    def __init__(self_, **kvargs):

        if "actions" in kvargs and kvargs["actions"] is not None:
            if (
                type(kvargs["actions"]).__name__
                == ItemResultResponseBody.__annotations__["actions"]
            ):
                self_.actions = kvargs["actions"]
            else:
                self_.actions = kvargs["actions"]
        if "collectionIds" in kvargs and kvargs["collectionIds"] is not None:
            if (
                type(kvargs["collectionIds"]).__name__
                == ItemResultResponseBody.__annotations__["collectionIds"]
            ):
                self_.collectionIds = kvargs["collectionIds"]
            else:
                self_.collectionIds = kvargs["collectionIds"]
        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            if (
                type(kvargs["createdAt"]).__name__
                == ItemResultResponseBody.__annotations__["createdAt"]
            ):
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "creatorId" in kvargs and kvargs["creatorId"] is not None:
            if (
                type(kvargs["creatorId"]).__name__
                == ItemResultResponseBody.__annotations__["creatorId"]
            ):
                self_.creatorId = kvargs["creatorId"]
            else:
                self_.creatorId = kvargs["creatorId"]
        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == ItemResultResponseBody.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "id" in kvargs and kvargs["id"] is not None:
            if (
                type(kvargs["id"]).__name__
                == ItemResultResponseBody.__annotations__["id"]
            ):
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "isFavorited" in kvargs and kvargs["isFavorited"] is not None:
            if (
                type(kvargs["isFavorited"]).__name__
                == ItemResultResponseBody.__annotations__["isFavorited"]
            ):
                self_.isFavorited = kvargs["isFavorited"]
            else:
                self_.isFavorited = kvargs["isFavorited"]
        if "itemViews" in kvargs and kvargs["itemViews"] is not None:
            if (
                type(kvargs["itemViews"]).__name__
                == ItemResultResponseBody.__annotations__["itemViews"]
            ):
                self_.itemViews = kvargs["itemViews"]
            else:
                self_.itemViews = ItemViewsResponseBody(**kvargs["itemViews"])
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ItemResultResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = ItemLinksResponseBody(**kvargs["links"])
        if "meta" in kvargs and kvargs["meta"] is not None:
            if (
                type(kvargs["meta"]).__name__
                == ItemResultResponseBody.__annotations__["meta"]
            ):
                self_.meta = kvargs["meta"]
            else:
                self_.meta = ItemMetaResponseBody(**kvargs["meta"])
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == ItemResultResponseBody.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            if (
                type(kvargs["ownerId"]).__name__
                == ItemResultResponseBody.__annotations__["ownerId"]
            ):
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "resourceAttributes" in kvargs and kvargs["resourceAttributes"] is not None:
            if (
                type(kvargs["resourceAttributes"]).__name__
                == ItemResultResponseBody.__annotations__["resourceAttributes"]
            ):
                self_.resourceAttributes = kvargs["resourceAttributes"]
            else:
                self_.resourceAttributes = kvargs["resourceAttributes"]
        if "resourceCreatedAt" in kvargs and kvargs["resourceCreatedAt"] is not None:
            if (
                type(kvargs["resourceCreatedAt"]).__name__
                == ItemResultResponseBody.__annotations__["resourceCreatedAt"]
            ):
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
            else:
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
        if (
            "resourceCustomAttributes" in kvargs
            and kvargs["resourceCustomAttributes"] is not None
        ):
            if (
                type(kvargs["resourceCustomAttributes"]).__name__
                == ItemResultResponseBody.__annotations__["resourceCustomAttributes"]
            ):
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
            else:
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceId" in kvargs and kvargs["resourceId"] is not None:
            if (
                type(kvargs["resourceId"]).__name__
                == ItemResultResponseBody.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs and kvargs["resourceLink"] is not None:
            if (
                type(kvargs["resourceLink"]).__name__
                == ItemResultResponseBody.__annotations__["resourceLink"]
            ):
                self_.resourceLink = kvargs["resourceLink"]
            else:
                self_.resourceLink = kvargs["resourceLink"]
        if (
            "resourceReloadEndTime" in kvargs
            and kvargs["resourceReloadEndTime"] is not None
        ):
            if (
                type(kvargs["resourceReloadEndTime"]).__name__
                == ItemResultResponseBody.__annotations__["resourceReloadEndTime"]
            ):
                self_.resourceReloadEndTime = kvargs["resourceReloadEndTime"]
            else:
                self_.resourceReloadEndTime = kvargs["resourceReloadEndTime"]
        if (
            "resourceReloadStatus" in kvargs
            and kvargs["resourceReloadStatus"] is not None
        ):
            if (
                type(kvargs["resourceReloadStatus"]).__name__
                == ItemResultResponseBody.__annotations__["resourceReloadStatus"]
            ):
                self_.resourceReloadStatus = kvargs["resourceReloadStatus"]
            else:
                self_.resourceReloadStatus = kvargs["resourceReloadStatus"]
        if "resourceSize" in kvargs and kvargs["resourceSize"] is not None:
            if (
                type(kvargs["resourceSize"]).__name__
                == ItemResultResponseBody.__annotations__["resourceSize"]
            ):
                self_.resourceSize = kvargs["resourceSize"]
            else:
                self_.resourceSize = ItemsResourceSizeResponseBody(
                    **kvargs["resourceSize"]
                )
        if "resourceSubType" in kvargs and kvargs["resourceSubType"] is not None:
            if (
                type(kvargs["resourceSubType"]).__name__
                == ItemResultResponseBody.__annotations__["resourceSubType"]
            ):
                self_.resourceSubType = kvargs["resourceSubType"]
            else:
                self_.resourceSubType = kvargs["resourceSubType"]
        if "resourceType" in kvargs and kvargs["resourceType"] is not None:
            if (
                type(kvargs["resourceType"]).__name__
                == ItemResultResponseBody.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "resourceUpdatedAt" in kvargs and kvargs["resourceUpdatedAt"] is not None:
            if (
                type(kvargs["resourceUpdatedAt"]).__name__
                == ItemResultResponseBody.__annotations__["resourceUpdatedAt"]
            ):
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
            else:
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
        if "spaceId" in kvargs and kvargs["spaceId"] is not None:
            if (
                type(kvargs["spaceId"]).__name__
                == ItemResultResponseBody.__annotations__["spaceId"]
            ):
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "tenantId" in kvargs and kvargs["tenantId"] is not None:
            if (
                type(kvargs["tenantId"]).__name__
                == ItemResultResponseBody.__annotations__["tenantId"]
            ):
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "thumbnailId" in kvargs and kvargs["thumbnailId"] is not None:
            if (
                type(kvargs["thumbnailId"]).__name__
                == ItemResultResponseBody.__annotations__["thumbnailId"]
            ):
                self_.thumbnailId = kvargs["thumbnailId"]
            else:
                self_.thumbnailId = kvargs["thumbnailId"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            if (
                type(kvargs["updatedAt"]).__name__
                == ItemResultResponseBody.__annotations__["updatedAt"]
            ):
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "updaterId" in kvargs and kvargs["updaterId"] is not None:
            if (
                type(kvargs["updaterId"]).__name__
                == ItemResultResponseBody.__annotations__["updaterId"]
            ):
                self_.updaterId = kvargs["updaterId"]
            else:
                self_.updaterId = kvargs["updaterId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemTagResponseBody:
    """
    Holds basic information about a tag or collection.

    Attributes
    ----------
    id: str
      The ID of the tag/collection.
    name: str
      The name of the tag/collection.
    """

    id: str = None
    name: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == ItemTagResponseBody.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "name" in kvargs and kvargs["name"] is not None:
            if (
                type(kvargs["name"]).__name__
                == ItemTagResponseBody.__annotations__["name"]
            ):
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemViewsResponseBody:
    """

    Attributes
    ----------
    total: int
      Total number of views the resource got during the last 28 days.
    trend: float
      Trend in views over the last 4 weeks.
    unique: int
      Number of unique users who viewed the resource during the last 28 days.
    usedBy: int
      Number of apps this dataset is used in (datasets only).
    week: list[ItemViewsWeeksResponseBody]
    """

    total: int = None
    trend: float = None
    unique: int = None
    usedBy: int = None
    week: list[ItemViewsWeeksResponseBody] = None

    def __init__(self_, **kvargs):

        if "total" in kvargs and kvargs["total"] is not None:
            if (
                type(kvargs["total"]).__name__
                == ItemViewsResponseBody.__annotations__["total"]
            ):
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]
        if "trend" in kvargs and kvargs["trend"] is not None:
            if (
                type(kvargs["trend"]).__name__
                == ItemViewsResponseBody.__annotations__["trend"]
            ):
                self_.trend = kvargs["trend"]
            else:
                self_.trend = kvargs["trend"]
        if "unique" in kvargs and kvargs["unique"] is not None:
            if (
                type(kvargs["unique"]).__name__
                == ItemViewsResponseBody.__annotations__["unique"]
            ):
                self_.unique = kvargs["unique"]
            else:
                self_.unique = kvargs["unique"]
        if "usedBy" in kvargs and kvargs["usedBy"] is not None:
            if (
                type(kvargs["usedBy"]).__name__
                == ItemViewsResponseBody.__annotations__["usedBy"]
            ):
                self_.usedBy = kvargs["usedBy"]
            else:
                self_.usedBy = kvargs["usedBy"]
        if "week" in kvargs and kvargs["week"] is not None:
            if (
                len(kvargs["week"]) > 0
                and f"list[{type(kvargs['week'][0]).__name__}]"
                == ItemViewsResponseBody.__annotations__["week"]
            ):
                self_.week = kvargs["week"]
            else:
                self_.week = [ItemViewsWeeksResponseBody(**e) for e in kvargs["week"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemViewsWeeksResponseBody:
    """

    Attributes
    ----------
    start: str
      The RFC3339 datetime representing the start of the referenced week.
    total: int
      Total number of views the resource got during the referenced week.
    unique: int
      Number of unique users who viewed the resource during the referenced week.
    """

    start: str = None
    total: int = None
    unique: int = None

    def __init__(self_, **kvargs):

        if "start" in kvargs and kvargs["start"] is not None:
            if (
                type(kvargs["start"]).__name__
                == ItemViewsWeeksResponseBody.__annotations__["start"]
            ):
                self_.start = kvargs["start"]
            else:
                self_.start = kvargs["start"]
        if "total" in kvargs and kvargs["total"] is not None:
            if (
                type(kvargs["total"]).__name__
                == ItemViewsWeeksResponseBody.__annotations__["total"]
            ):
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]
        if "unique" in kvargs and kvargs["unique"] is not None:
            if (
                type(kvargs["unique"]).__name__
                == ItemViewsWeeksResponseBody.__annotations__["unique"]
            ):
                self_.unique = kvargs["unique"]
            else:
                self_.unique = kvargs["unique"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsLinksResponseBody:
    """

    Attributes
    ----------
    collection: Link
    next: Link
    prev: Link
    self: Link
    """

    collection: Link = None
    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):

        if "collection" in kvargs and kvargs["collection"] is not None:
            if (
                type(kvargs["collection"]).__name__
                == ItemsLinksResponseBody.__annotations__["collection"]
            ):
                self_.collection = kvargs["collection"]
            else:
                self_.collection = Link(**kvargs["collection"])
        if "next" in kvargs and kvargs["next"] is not None:
            if (
                type(kvargs["next"]).__name__
                == ItemsLinksResponseBody.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == ItemsLinksResponseBody.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == ItemsLinksResponseBody.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsResourceSizeResponseBody:
    """

    Attributes
    ----------
    appFile: float
      Size of the app on disk in bytes.
    appMemory: float
      Size of the app in memory in bytes.
    """

    appFile: float = None
    appMemory: float = None

    def __init__(self_, **kvargs):

        if "appFile" in kvargs and kvargs["appFile"] is not None:
            if (
                type(kvargs["appFile"]).__name__
                == ItemsResourceSizeResponseBody.__annotations__["appFile"]
            ):
                self_.appFile = kvargs["appFile"]
            else:
                self_.appFile = kvargs["appFile"]
        if "appMemory" in kvargs and kvargs["appMemory"] is not None:
            if (
                type(kvargs["appMemory"]).__name__
                == ItemsResourceSizeResponseBody.__annotations__["appMemory"]
            ):
                self_.appMemory = kvargs["appMemory"]
            else:
                self_.appMemory = kvargs["appMemory"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsResultResponseBody:
    """
    Multiple items.

    Attributes
    ----------
    data: list[ItemResultResponseBody]
    links: ItemsLinksResponseBody
    """

    data: list[ItemResultResponseBody] = None
    links: ItemsLinksResponseBody = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == ItemsResultResponseBody.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [ItemResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if (
                type(kvargs["links"]).__name__
                == ItemsResultResponseBody.__annotations__["links"]
            ):
                self_.links = kvargs["links"]
            else:
                self_.links = ItemsLinksResponseBody(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Collections:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_favorite(self) -> any:
        """
        Retrieves the user's favorites collection.
        Finds and returns the user's favorites collection.


        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/collections/favorites",
            method="GET",
            params={},
            data=None,
        )
        return response.json()

    def delete_item(self, collectionId: str, itemId: str) -> None:
        """
        Removes an item from a collection.
        Removes an item from a collection.


        Parameters
        ----------
        collectionId: str
          The collection's unique identifier.
        itemId: str
          The item's unique identifier.
        """
        self.auth.rest(
            path="/collections/{collectionId}/items/{itemId}".replace(
                "{collectionId}", collectionId
            ).replace("{itemId}", itemId),
            method="DELETE",
            params={},
            data=None,
        )

    def get_item(self, collectionId: str, itemId: str) -> ItemResultResponseBody:
        """
        Returns an item in a specific collection.
        Finds and returns an item. See GET /items/{id}


        Parameters
        ----------
        collectionId: str
          The collection's unique identifier.
        itemId: str
          The item's unique identifier.
        """
        response = self.auth.rest(
            path="/collections/{collectionId}/items/{itemId}".replace(
                "{collectionId}", collectionId
            ).replace("{itemId}", itemId),
            method="GET",
            params={},
            data=None,
        )
        obj = ItemResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, collectionId: str) -> CollectionResultResponseBody:
        """
        Returns a collection.
        Finds and returns a collection.


        Parameters
        ----------
        collectionId: str
          The collection's unique identifier.
        """
        response = self.auth.rest(
            path="/collections/{collectionId}".replace("{collectionId}", collectionId),
            method="GET",
            params={},
            data=None,
        )
        obj = CollectionResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def get_collections(
        self,
        creatorId: str = None,
        id: str = None,
        includeItems: str = None,
        limit: int = None,
        name: str = None,
        next: str = None,
        prev: str = None,
        query: str = None,
        sort: str = None,
        type: str = None,
        max_items: int = 10,
    ) -> ListableResource[CollectionResultResponseBody]:
        """
        Retrieves collections that the user has access to.
        Finds and returns the collections that the user can access. This endpoint does not return the user's favorites collection.


        Parameters
        ----------
        creatorId: str = None
          The case-sensitive string used to search for a resource by creatorId.
        id: str = None
          The collection's unique identifier.
        includeItems: str = None
          JSON-formatted string for querying collection items.
        limit: int = None
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        name: str = None
          The case-sensitive string used to search for a collection by name.
        next: str = None
          The cursor to the next page of resources. Provide either the
          next or prev cursor, but not both.

        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        query: str = None
          The case-insensitive string used to search for a resource by name or description.
        sort: str = None
          The property of a resource to sort on (default sort is +createdAt).
          The supported properties are createdAt, updatedAt, and name. A property
          must be prefixed by + or - to indicate ascending or descending sort order
          respectively.

        type: str = None
          The case-sensitive string used to search for a collection by type.
        """
        query_params = {}
        if creatorId is not None:
            query_params["creatorId"] = creatorId
        if id is not None:
            query_params["id"] = id
        if includeItems is not None:
            query_params["includeItems"] = includeItems
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if query is not None:
            query_params["query"] = query
        if sort is not None:
            query_params["sort"] = sort
        if type is not None:
            query_params["type"] = type
        response = self.auth.rest(
            path="/collections",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=CollectionResultResponseBody,
            auth=self.auth,
            path="/collections",
            max_items=max_items,
            query_params=query_params,
        )

    def create(
        self, data: CollectionsCreateCollectionRequestBody
    ) -> CollectionResultResponseBody:
        """
        Creates a new collection.
        Creates and returns a new collection. Collections can have the same name.


        Parameters
        ----------
        data: CollectionsCreateCollectionRequestBody

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/collections",
            method="POST",
            params={},
            data=data,
        )
        obj = CollectionResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj
