from __future__ import annotations

from typing import Any, Dict, List, Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.shared import MessageResponse
from ..types.webhook import (
    WebhookDelivery,
    WebhookDeliveryListResponse,
    WebhookSubscriptionCreateResponse,
    WebhookSubscriptionListResponse,
    WebhookSubscriptionShowResponse,
    WebhookTestResponse,
)
from ._base import AsyncAPIResource, SyncAPIResource

_WEBHOOKS = "/webhooks"


class Webhooks(SyncAPIResource):
    """Tenant-level webhook subscriptions.

    Access via ``client.webhooks``. Subscriptions created here listen to
    **every** pentest of their owner. For a single pentest use
    ``client.pentests.webhooks`` instead.
    """

    def list(
        self,
        *,
        pentest_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> WebhookSubscriptionListResponse:
        """List subscriptions the caller manages.

        Args:
            pentest_id: If set, only subscriptions that fire for that pentest.
        """
        params = strip_not_given({"pentest_id": pentest_id})
        return self._client.get(
            _WEBHOOKS, params=params or None, model=WebhookSubscriptionListResponse,
        )

    def create(
        self,
        *,
        url: str,
        events: List[str],
        secret: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        team_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> WebhookSubscriptionCreateResponse:
        """Register a tenant-level webhook.

        If *secret* is omitted one is generated and returned **once**.

        Args:
            url: HTTPS callback URL (SSRF-checked).
            events: Event types to subscribe to.
            secret: Shared HMAC secret (min 16 chars). Generated if omitted.
            description: Optional label (max 200 chars).
            team_id: Own the subscription as this team; omit for personal.
        """
        body: Dict[str, Any] = {"url": url, "events": events}
        body.update(strip_not_given({
            "secret": secret, "description": description, "team_id": team_id,
        }))
        return self._client.post(
            _WEBHOOKS, body=body, model=WebhookSubscriptionCreateResponse,
        )

    def retrieve(self, webhook_id: int) -> WebhookSubscriptionShowResponse:
        """Get one subscription."""
        return self._client.get(
            f"{_WEBHOOKS}/{webhook_id}", model=WebhookSubscriptionShowResponse,
        )

    def update(
        self,
        webhook_id: int,
        *,
        url: Union[str, _NotGiven] = NOT_GIVEN,
        events: Union[List[str], _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        active: Union[bool, _NotGiven] = NOT_GIVEN,
        secret: Union[str, _NotGiven] = NOT_GIVEN,
        rotate_secret: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> WebhookSubscriptionShowResponse:
        """Edit destination, events, state, or signing secret.

        Pass ``rotate_secret=True`` to generate a new secret (returned once).
        """
        body = strip_not_given({
            "url": url,
            "events": events,
            "description": description,
            "active": active,
            "secret": secret,
            "rotate_secret": rotate_secret,
        })
        return self._client.put(
            f"{_WEBHOOKS}/{webhook_id}",
            body=body,
            model=WebhookSubscriptionShowResponse,
        )

    def delete(self, webhook_id: int) -> MessageResponse:
        """Remove a subscription."""
        return self._client.delete(
            f"{_WEBHOOKS}/{webhook_id}", model=MessageResponse,
        )

    def test(self, webhook_id: int) -> WebhookTestResponse:
        """Send a signed ``ping`` to the subscription."""
        return self._client.post(
            f"{_WEBHOOKS}/{webhook_id}/test", model=WebhookTestResponse,
        )

    def list_deliveries(
        self,
        webhook_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        status: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> WebhookDeliveryListResponse:
        """List recent deliveries (``pending``, ``delivered``, ``dead``)."""
        params = strip_not_given({
            "page": page, "per_page": per_page, "status": status,
        })
        return self._client.get(
            f"{_WEBHOOKS}/{webhook_id}/deliveries",
            params=params or None,
            model=WebhookDeliveryListResponse,
        )

    def retrieve_delivery(
        self, webhook_id: int, delivery_id: int,
    ) -> WebhookDelivery:
        """Get one delivery, including request body and response excerpt."""
        return self._client.get(
            f"{_WEBHOOKS}/{webhook_id}/deliveries/{delivery_id}",
            model=WebhookDelivery,
        )

    def redeliver(self, webhook_id: int, delivery_id: int) -> WebhookTestResponse:
        """Re-send the same envelope (same ``X-Rank-Event-Id``)."""
        return self._client.post(
            f"{_WEBHOOKS}/{webhook_id}/deliveries/{delivery_id}/redeliver",
            model=WebhookTestResponse,
        )


class AsyncWebhooks(AsyncAPIResource):
    """Async variant of :class:`Webhooks`."""

    async def list(
        self,
        *,
        pentest_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> WebhookSubscriptionListResponse:
        params = strip_not_given({"pentest_id": pentest_id})
        return await self._client.get(
            _WEBHOOKS, params=params or None, model=WebhookSubscriptionListResponse,
        )

    async def create(
        self,
        *,
        url: str,
        events: List[str],
        secret: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        team_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> WebhookSubscriptionCreateResponse:
        body: Dict[str, Any] = {"url": url, "events": events}
        body.update(strip_not_given({
            "secret": secret, "description": description, "team_id": team_id,
        }))
        return await self._client.post(
            _WEBHOOKS, body=body, model=WebhookSubscriptionCreateResponse,
        )

    async def retrieve(self, webhook_id: int) -> WebhookSubscriptionShowResponse:
        return await self._client.get(
            f"{_WEBHOOKS}/{webhook_id}", model=WebhookSubscriptionShowResponse,
        )

    async def update(
        self,
        webhook_id: int,
        *,
        url: Union[str, _NotGiven] = NOT_GIVEN,
        events: Union[List[str], _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        active: Union[bool, _NotGiven] = NOT_GIVEN,
        secret: Union[str, _NotGiven] = NOT_GIVEN,
        rotate_secret: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> WebhookSubscriptionShowResponse:
        body = strip_not_given({
            "url": url,
            "events": events,
            "description": description,
            "active": active,
            "secret": secret,
            "rotate_secret": rotate_secret,
        })
        return await self._client.put(
            f"{_WEBHOOKS}/{webhook_id}",
            body=body,
            model=WebhookSubscriptionShowResponse,
        )

    async def delete(self, webhook_id: int) -> MessageResponse:
        return await self._client.delete(
            f"{_WEBHOOKS}/{webhook_id}", model=MessageResponse,
        )

    async def test(self, webhook_id: int) -> WebhookTestResponse:
        return await self._client.post(
            f"{_WEBHOOKS}/{webhook_id}/test", model=WebhookTestResponse,
        )

    async def list_deliveries(
        self,
        webhook_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        status: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> WebhookDeliveryListResponse:
        params = strip_not_given({
            "page": page, "per_page": per_page, "status": status,
        })
        return await self._client.get(
            f"{_WEBHOOKS}/{webhook_id}/deliveries",
            params=params or None,
            model=WebhookDeliveryListResponse,
        )

    async def retrieve_delivery(
        self, webhook_id: int, delivery_id: int,
    ) -> WebhookDelivery:
        return await self._client.get(
            f"{_WEBHOOKS}/{webhook_id}/deliveries/{delivery_id}",
            model=WebhookDelivery,
        )

    async def redeliver(self, webhook_id: int, delivery_id: int) -> WebhookTestResponse:
        return await self._client.post(
            f"{_WEBHOOKS}/{webhook_id}/deliveries/{delivery_id}/redeliver",
            model=WebhookTestResponse,
        )
