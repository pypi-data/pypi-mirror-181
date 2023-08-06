# This is spectacularly generated code by spectacular v0.8.0 based on
# Qlik Cloud Services 0.529.8

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Webhook:
    """

    Attributes
    ----------
    createdAt: str
      The UTC timestamp when the webhook was created
    createdByUserId: str
      The id of the user that created the webhook
    description: str
      The reason for creating the webhook
    disabledReason: str
      The reason for the webhook to be disabled
    disabledReasonCode: str
      The unique code for the reason
    enabled: bool
      Whether the webhook is active and sending requests
    eventTypes: list[str]
      Types of events for which the webhook should trigger.
    filter: str
      Filter that should match for a webhook to be triggered.
      Supported attribute names are 'id', 'spaceId' and 'topLevelResourceId'.
      Supported attribute operators are 'eq' and 'ne'.
      Supported logical operators are 'and' and 'or'.
      Note that attribute values must be valid JSON strings, hence they're enclosed with double quotes
      For more detailed information regarding the SCIM filter syntax (RFC7644) used please following link to external documentation.
    headers: object
      Additional headers in the post request
    id: str
      The webhook's unique identifier
    level: str
      Defines at what level the webhook should operate: for all resources belonging to a tenant or restricted to only those accessible by the webhook-creator.
    name: str
      The name for the webhook
    ownerId: str
      The id of the user that owns the webhook, only applicable for user level webhooks
    secret: str
      String used as secret for calculating HMAC hash sent as header
    updatedAt: str
      The UTC timestamp when the webhook was last updated
    updatedByUserId: str
      The id of the user that last updated the webhook
    url: str
      Target URL for webhook HTTPS requests
    """

    createdAt: str = None
    createdByUserId: str = None
    description: str = None
    disabledReason: str = None
    disabledReasonCode: str = None
    enabled: bool = None
    eventTypes: list[str] = None
    filter: str = None
    headers: object = None
    id: str = None
    level: str = "tenant"
    name: str = None
    ownerId: str = None
    secret: str = None
    updatedAt: str = None
    updatedByUserId: str = None
    url: str = None

    def __init__(self_, **kvargs):

        if "createdAt" in kvargs and kvargs["createdAt"] is not None:
            if (
                type(kvargs["createdAt"]).__name__
                == Webhook.__annotations__["createdAt"]
            ):
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdByUserId" in kvargs and kvargs["createdByUserId"] is not None:
            if (
                type(kvargs["createdByUserId"]).__name__
                == Webhook.__annotations__["createdByUserId"]
            ):
                self_.createdByUserId = kvargs["createdByUserId"]
            else:
                self_.createdByUserId = kvargs["createdByUserId"]
        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == Webhook.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "disabledReason" in kvargs and kvargs["disabledReason"] is not None:
            if (
                type(kvargs["disabledReason"]).__name__
                == Webhook.__annotations__["disabledReason"]
            ):
                self_.disabledReason = kvargs["disabledReason"]
            else:
                self_.disabledReason = kvargs["disabledReason"]
        if "disabledReasonCode" in kvargs and kvargs["disabledReasonCode"] is not None:
            if (
                type(kvargs["disabledReasonCode"]).__name__
                == Webhook.__annotations__["disabledReasonCode"]
            ):
                self_.disabledReasonCode = kvargs["disabledReasonCode"]
            else:
                self_.disabledReasonCode = kvargs["disabledReasonCode"]
        if "enabled" in kvargs and kvargs["enabled"] is not None:
            if type(kvargs["enabled"]).__name__ == Webhook.__annotations__["enabled"]:
                self_.enabled = kvargs["enabled"]
            else:
                self_.enabled = kvargs["enabled"]
        if "eventTypes" in kvargs and kvargs["eventTypes"] is not None:
            if (
                type(kvargs["eventTypes"]).__name__
                == Webhook.__annotations__["eventTypes"]
            ):
                self_.eventTypes = kvargs["eventTypes"]
            else:
                self_.eventTypes = kvargs["eventTypes"]
        if "filter" in kvargs and kvargs["filter"] is not None:
            if type(kvargs["filter"]).__name__ == Webhook.__annotations__["filter"]:
                self_.filter = kvargs["filter"]
            else:
                self_.filter = kvargs["filter"]
        if "headers" in kvargs and kvargs["headers"] is not None:
            if type(kvargs["headers"]).__name__ == Webhook.__annotations__["headers"]:
                self_.headers = kvargs["headers"]
            else:
                self_.headers = kvargs["headers"]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == Webhook.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "level" in kvargs and kvargs["level"] is not None:
            if type(kvargs["level"]).__name__ == Webhook.__annotations__["level"]:
                self_.level = kvargs["level"]
            else:
                self_.level = kvargs["level"]
        if "name" in kvargs and kvargs["name"] is not None:
            if type(kvargs["name"]).__name__ == Webhook.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "ownerId" in kvargs and kvargs["ownerId"] is not None:
            if type(kvargs["ownerId"]).__name__ == Webhook.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "secret" in kvargs and kvargs["secret"] is not None:
            if type(kvargs["secret"]).__name__ == Webhook.__annotations__["secret"]:
                self_.secret = kvargs["secret"]
            else:
                self_.secret = kvargs["secret"]
        if "updatedAt" in kvargs and kvargs["updatedAt"] is not None:
            if (
                type(kvargs["updatedAt"]).__name__
                == Webhook.__annotations__["updatedAt"]
            ):
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "updatedByUserId" in kvargs and kvargs["updatedByUserId"] is not None:
            if (
                type(kvargs["updatedByUserId"]).__name__
                == Webhook.__annotations__["updatedByUserId"]
            ):
                self_.updatedByUserId = kvargs["updatedByUserId"]
            else:
                self_.updatedByUserId = kvargs["updatedByUserId"]
        if "url" in kvargs and kvargs["url"] is not None:
            if type(kvargs["url"]).__name__ == Webhook.__annotations__["url"]:
                self_.url = kvargs["url"]
            else:
                self_.url = kvargs["url"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_deliveries(
        self,
        eventType: str = None,
        limit: float = 20,
        next: str = None,
        prev: str = None,
        sort: str = "-triggeredAt",
        status: str = None,
        max_items: int = 20,
    ) -> ListableResource[Delivery]:
        """
        Returns deliveries for a specific webhook

        Parameters
        ----------
        eventType: str = None
          Filter resources by event-type
        limit: float = 20
          Maximum number of deliveries to retrieve
        next: str = None
          Cursor to the next page
        prev: str = None
          Cursor to previous next page
        sort: str = "-triggeredAt"
          Field to sort by, prefix with -/+ to indicate order
        status: str = None
          Filter resources by status (success or fail)
        """
        query_params = {}
        if eventType is not None:
            query_params["eventType"] = eventType
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        if status is not None:
            query_params["status"] = status
        response = self.auth.rest(
            path="/webhooks/{id}/deliveries".replace("{id}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Delivery,
            auth=self.auth,
            path="/webhooks/{id}/deliveries".replace("{id}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def delete(self) -> None:
        """
        Deletes a specific webhook

        Parameters
        ----------
        """
        self.auth.rest(
            path="/webhooks/{id}".replace("{id}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, WebhookPatchData: list[WebhookPatch]) -> None:
        """
        Patches a webhook

        Parameters
        ----------
        WebhookPatchData: list[WebhookPatch]

        """
        data = [asdict(elem) for elem in WebhookPatchData]
        self.auth.rest(
            path="/webhooks/{id}".replace("{id}", self.id),
            method="PATCH",
            params={},
            data=data,
        )

    def set(self, data: Webhook) -> Webhook:
        """
        Updates a webhook

        Parameters
        ----------
        data: Webhook

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/webhooks/{id}".replace("{id}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class Delivery:
    """

    Attributes
    ----------
    eventType: str
      The name of the triggering event-type
    id: str
      The delivery's unique identifier
    request: DeliveryRequest
    response: DeliveryResponse
    status: str
      The status of delivery
    statusMessage: str
      The status message of the delivery
    triggeredAt: str
      The UTC timestamp when the delivery was triggered
    webhookId: str
      The unique webhook identifier that the delivery is for
    """

    eventType: str = None
    id: str = None
    request: DeliveryRequest = None
    response: DeliveryResponse = None
    status: str = None
    statusMessage: str = None
    triggeredAt: str = None
    webhookId: str = None

    def __init__(self_, **kvargs):

        if "eventType" in kvargs and kvargs["eventType"] is not None:
            if (
                type(kvargs["eventType"]).__name__
                == Delivery.__annotations__["eventType"]
            ):
                self_.eventType = kvargs["eventType"]
            else:
                self_.eventType = kvargs["eventType"]
        if "id" in kvargs and kvargs["id"] is not None:
            if type(kvargs["id"]).__name__ == Delivery.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "request" in kvargs and kvargs["request"] is not None:
            if type(kvargs["request"]).__name__ == Delivery.__annotations__["request"]:
                self_.request = kvargs["request"]
            else:
                self_.request = DeliveryRequest(**kvargs["request"])
        if "response" in kvargs and kvargs["response"] is not None:
            if (
                type(kvargs["response"]).__name__
                == Delivery.__annotations__["response"]
            ):
                self_.response = kvargs["response"]
            else:
                self_.response = DeliveryResponse(**kvargs["response"])
        if "status" in kvargs and kvargs["status"] is not None:
            if type(kvargs["status"]).__name__ == Delivery.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "statusMessage" in kvargs and kvargs["statusMessage"] is not None:
            if (
                type(kvargs["statusMessage"]).__name__
                == Delivery.__annotations__["statusMessage"]
            ):
                self_.statusMessage = kvargs["statusMessage"]
            else:
                self_.statusMessage = kvargs["statusMessage"]
        if "triggeredAt" in kvargs and kvargs["triggeredAt"] is not None:
            if (
                type(kvargs["triggeredAt"]).__name__
                == Delivery.__annotations__["triggeredAt"]
            ):
                self_.triggeredAt = kvargs["triggeredAt"]
            else:
                self_.triggeredAt = kvargs["triggeredAt"]
        if "webhookId" in kvargs and kvargs["webhookId"] is not None:
            if (
                type(kvargs["webhookId"]).__name__
                == Delivery.__annotations__["webhookId"]
            ):
                self_.webhookId = kvargs["webhookId"]
            else:
                self_.webhookId = kvargs["webhookId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DeliveryList:
    """

    Attributes
    ----------
    data: list[Delivery]
    links: DeliveryListLinks
    """

    data: list[Delivery] = None
    links: DeliveryListLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == DeliveryList.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Delivery(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == DeliveryList.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = DeliveryListLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DeliveryListLinks:
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
            if (
                type(kvargs["next"]).__name__
                == DeliveryListLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == DeliveryListLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == DeliveryListLinks.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DeliveryRequest:
    """

    Attributes
    ----------
    body: object
      The sent body/payload of the delivery
    headers: object
      Headers sent for this delivery
    url: str
      URL used for this delivery
    """

    body: object = None
    headers: object = None
    url: str = None

    def __init__(self_, **kvargs):

        if "body" in kvargs and kvargs["body"] is not None:
            if type(kvargs["body"]).__name__ == DeliveryRequest.__annotations__["body"]:
                self_.body = kvargs["body"]
            else:
                self_.body = kvargs["body"]
        if "headers" in kvargs and kvargs["headers"] is not None:
            if (
                type(kvargs["headers"]).__name__
                == DeliveryRequest.__annotations__["headers"]
            ):
                self_.headers = kvargs["headers"]
            else:
                self_.headers = kvargs["headers"]
        if "url" in kvargs and kvargs["url"] is not None:
            if type(kvargs["url"]).__name__ == DeliveryRequest.__annotations__["url"]:
                self_.url = kvargs["url"]
            else:
                self_.url = kvargs["url"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class DeliveryResponse:
    """

    Attributes
    ----------
    body: str
      The received body of the delivery
    headers: object
      Headers received for this delivery
    statusCode: float
      The HTTP status code of the response
    """

    body: str = None
    headers: object = None
    statusCode: float = None

    def __init__(self_, **kvargs):

        if "body" in kvargs and kvargs["body"] is not None:
            if (
                type(kvargs["body"]).__name__
                == DeliveryResponse.__annotations__["body"]
            ):
                self_.body = kvargs["body"]
            else:
                self_.body = kvargs["body"]
        if "headers" in kvargs and kvargs["headers"] is not None:
            if (
                type(kvargs["headers"]).__name__
                == DeliveryResponse.__annotations__["headers"]
            ):
                self_.headers = kvargs["headers"]
            else:
                self_.headers = kvargs["headers"]
        if "statusCode" in kvargs and kvargs["statusCode"] is not None:
            if (
                type(kvargs["statusCode"]).__name__
                == DeliveryResponse.__annotations__["statusCode"]
            ):
                self_.statusCode = kvargs["statusCode"]
            else:
                self_.statusCode = kvargs["statusCode"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EventType:
    """

    Attributes
    ----------
    description: str
      Description of the event type
    levels: list[str]
      Specifies which levels that are supported for this event type
    name: str
      Name of the event type
    title: str
      Title of the event type
    """

    description: str = None
    levels: list[str] = None
    name: str = None
    title: str = None

    def __init__(self_, **kvargs):

        if "description" in kvargs and kvargs["description"] is not None:
            if (
                type(kvargs["description"]).__name__
                == EventType.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "levels" in kvargs and kvargs["levels"] is not None:
            if type(kvargs["levels"]).__name__ == EventType.__annotations__["levels"]:
                self_.levels = kvargs["levels"]
            else:
                self_.levels = kvargs["levels"]
        if "name" in kvargs and kvargs["name"] is not None:
            if type(kvargs["name"]).__name__ == EventType.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "title" in kvargs and kvargs["title"] is not None:
            if type(kvargs["title"]).__name__ == EventType.__annotations__["title"]:
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class EventTypes:
    """

    Attributes
    ----------
    data: list[EventType]
    """

    data: list[EventType] = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == EventTypes.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [EventType(**e) for e in kvargs["data"]]
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
      URL to a resource request
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
class WebhookList:
    """

    Attributes
    ----------
    data: list[Webhook]
    links: WebhookListLinks
    """

    data: list[Webhook] = None
    links: WebhookListLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs and kvargs["data"] is not None:
            if (
                len(kvargs["data"]) > 0
                and f"list[{type(kvargs['data'][0]).__name__}]"
                == WebhookList.__annotations__["data"]
            ):
                self_.data = kvargs["data"]
            else:
                self_.data = [Webhook(**e) for e in kvargs["data"]]
        if "links" in kvargs and kvargs["links"] is not None:
            if type(kvargs["links"]).__name__ == WebhookList.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = WebhookListLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class WebhookListLinks:
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
            if (
                type(kvargs["next"]).__name__
                == WebhookListLinks.__annotations__["next"]
            ):
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs and kvargs["prev"] is not None:
            if (
                type(kvargs["prev"]).__name__
                == WebhookListLinks.__annotations__["prev"]
            ):
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs and kvargs["self"] is not None:
            if (
                type(kvargs["self"]).__name__
                == WebhookListLinks.__annotations__["self"]
            ):
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class WebhookPatch:
    """
    A JSON Patch document as defined in https://datatracker.ietf.org/doc/html/rfc6902

    Attributes
    ----------
    op: str
      The operation to be performed
    path: str
      The path for the given resource field to patch
    value: str
      The value to be used for this operation.
    """

    op: str = None
    path: str = None
    value: str = None

    def __init__(self_, **kvargs):

        if "op" in kvargs and kvargs["op"] is not None:
            if type(kvargs["op"]).__name__ == WebhookPatch.__annotations__["op"]:
                self_.op = kvargs["op"]
            else:
                self_.op = kvargs["op"]
        if "path" in kvargs and kvargs["path"] is not None:
            if type(kvargs["path"]).__name__ == WebhookPatch.__annotations__["path"]:
                self_.path = kvargs["path"]
            else:
                self_.path = kvargs["path"]
        if "value" in kvargs and kvargs["value"] is not None:
            if type(kvargs["value"]).__name__ == WebhookPatch.__annotations__["value"]:
                self_.value = kvargs["value"]
            else:
                self_.value = kvargs["value"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Webhooks:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_event_types(self) -> EventTypes:
        """
        List of event-types that are possible to subscribe to.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/webhooks/event-types",
            method="GET",
            params={},
            data=None,
        )
        obj = EventTypes(**response.json())
        obj.auth = self.auth
        return obj

    def resend(self, deliveryId: str, id: str) -> Delivery:
        """
        Resend the delivery with the same payload

        Parameters
        ----------
        deliveryId: str
          The delivery's unique identifier.
        id: str
          The webhook's unique identifier.
        """
        response = self.auth.rest(
            path="/webhooks/{id}/deliveries/{deliveryId}/actions/resend".replace(
                "{deliveryId}", deliveryId
            ).replace("{id}", id),
            method="POST",
            params={},
            data=None,
        )
        obj = Delivery(**response.json())
        obj.auth = self.auth
        return obj

    def get_deliverie(self, deliveryId: str, id: str) -> Delivery:
        """
        Returns details for a specific delivery

        Parameters
        ----------
        deliveryId: str
          The delivery's unique identifier.
        id: str
          The webhook's unique identifier.
        """
        response = self.auth.rest(
            path="/webhooks/{id}/deliveries/{deliveryId}".replace(
                "{deliveryId}", deliveryId
            ).replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = Delivery(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, id: str) -> Webhook:
        """
        Returns details for a specific webhook

        Parameters
        ----------
        id: str
          The webhook's unique identifier.
        """
        response = self.auth.rest(
            path="/webhooks/{id}".replace("{id}", id),
            method="GET",
            params={},
            data=None,
        )
        obj = Webhook(**response.json())
        obj.auth = self.auth
        return obj

    def get_webhooks(
        self,
        createdByUserId: str = None,
        enabled: bool = None,
        eventType: str = None,
        level: str = None,
        limit: float = 20,
        name: str = None,
        next: str = None,
        ownerId: str = None,
        prev: str = None,
        sort: str = "-createdAt",
        updatedByUserId: str = None,
        url: str = None,
        max_items: int = 20,
    ) -> ListableResource[Webhook]:
        """
        Retrieves all webhooks entries for a tenant

        Parameters
        ----------
        createdByUserId: str = None
          Filter resources by user that created it
        enabled: bool = None
          Filter resources by enabled true/false
        eventType: str = None
          Filter resources by event-type
        level: str = None
          Filter resources by level that user has access to (either user or level)
        limit: float = 20
          Maximum number of webhooks to retrieve
        name: str = None
          Filter resources by name (wildcard and case insensitive)
        next: str = None
          Cursor to the next page
        ownerId: str = None
          Filter resources by user that owns it, only applicable for user level webhooks
        prev: str = None
          Cursor to previous next page
        sort: str = "-createdAt"
          Field to sort by, prefix with -/+ to indicate order
        updatedByUserId: str = None
          Filter resources by user that last updated the webhook
        url: str = None
          Filter resources by url (wildcard and case insensitive)
        """
        query_params = {}
        if createdByUserId is not None:
            query_params["createdByUserId"] = createdByUserId
        if enabled is not None:
            query_params["enabled"] = enabled
        if eventType is not None:
            query_params["eventType"] = eventType
        if level is not None:
            query_params["level"] = level
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        if updatedByUserId is not None:
            query_params["updatedByUserId"] = updatedByUserId
        if url is not None:
            query_params["url"] = url
        response = self.auth.rest(
            path="/webhooks",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Webhook,
            auth=self.auth,
            path="/webhooks",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: Webhook) -> Webhook:
        """
        Creates a new webhook

        Parameters
        ----------
        data: Webhook

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/webhooks",
            method="POST",
            params={},
            data=data,
        )
        obj = Webhook(**response.json())
        obj.auth = self.auth
        return obj
