from __future__ import annotations

from typing import Any, List, Optional

from pydantic import model_validator

from .shared import PaginationInfo, RankModel


class WebhookSubscription(RankModel):
    """A tenant-level (or pentest-scoped) webhook subscription."""

    id: int
    url: str = ""
    events: List[str] = []
    description: Optional[str] = None
    active: Optional[bool] = None
    pentest_id: Optional[int] = None
    owner_type: Optional[str] = None
    owner_id: Optional[int] = None
    team_id: Optional[int] = None
    scope: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    last_delivery_at: Optional[str] = None
    consecutive_failures: Optional[int] = None


class WebhookSubscriptionListResponse(RankModel):
    """Response from ``GET /webhooks``."""

    webhooks: List[WebhookSubscription] = []
    total: int = 0


class WebhookSubscriptionCreateResponse(RankModel):
    """Response from ``POST /webhooks``.

    ``secret`` is returned only once, at creation (or when rotated).
    """

    message: str = ""
    webhook: Optional[WebhookSubscription] = None
    secret: Optional[str] = None
    secret_notice: Optional[str] = None


class WebhookSubscriptionShowResponse(RankModel):
    """Response from ``GET /webhooks/{id}``."""

    webhook: Optional[WebhookSubscription] = None


class WebhookDelivery(RankModel):
    """One delivery attempt of a signed webhook event."""

    id: int
    event_id: Optional[str] = None
    event: Optional[str] = None
    event_type: Optional[str] = None
    pentest_id: Optional[int] = None
    target_url: Optional[str] = None
    status: Optional[str] = None
    attempt: Optional[int] = None
    max_attempts: Optional[int] = None
    http_status: Optional[int] = None
    response_status: Optional[int] = None
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    created_at: Optional[str] = None
    delivered_at: Optional[str] = None
    next_attempt_at: Optional[str] = None
    request_body: Optional[Any] = None
    payload: Optional[Any] = None
    response_excerpt: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _sync_php_names(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        synced = dict(data)
        if synced.get("event_type") is None and synced.get("event") is not None:
            synced["event_type"] = synced["event"]
        if synced.get("http_status") is None and synced.get("response_status") is not None:
            synced["http_status"] = synced["response_status"]
        if synced.get("request_body") is None and synced.get("payload") is not None:
            synced["request_body"] = synced["payload"]
        return synced


class WebhookDeliveryListResponse(RankModel):
    """Paginated delivery history."""

    items: List[WebhookDelivery] = []
    pagination: Optional[PaginationInfo] = None


class WebhookTestResponse(RankModel):
    """Response from ``POST /webhooks/{id}/test``.

    PHP queues a ping and returns the delivery row, not a flat
    ``delivery_id`` / ``status`` pair.
    """

    message: Optional[str] = None
    delivery: Optional[WebhookDelivery] = None
