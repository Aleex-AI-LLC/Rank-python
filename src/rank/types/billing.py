from __future__ import annotations

from typing import Any, Dict, List, Optional

from .shared import RankModel


class BillingTrialStatusResponse(RankModel):
    """Response from ``GET /billing/trial/status``."""

    active: Optional[bool] = None
    tier_id: Optional[int] = None
    tier_name: Optional[str] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    days_remaining: Optional[int] = None
    trial_used: Optional[bool] = None


class BillingSubscription(RankModel):
    """Subscription details within billing status."""

    status: Optional[str] = None
    tier_id: Optional[int] = None
    tier_name: Optional[str] = None
    billing_interval: Optional[str] = None
    current_period_start: Optional[str] = None
    current_period_end: Optional[str] = None
    cancel_at: Optional[str] = None
    cancel_at_period_end: Optional[bool] = None


class BillingStatusResponse(RankModel):
    """Response from ``GET /billing/status``."""

    has_subscription: Optional[bool] = None
    subscription: Optional[BillingSubscription] = None
    trial: Optional[BillingTrialStatusResponse] = None


class BillingInvoice(RankModel):
    """A billing invoice."""

    id: Optional[str] = None
    number: Optional[str] = None
    status: Optional[str] = None
    amount_due: Optional[int] = None
    amount_paid: Optional[int] = None
    currency: Optional[str] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    invoice_pdf: Optional[str] = None
    hosted_invoice_url: Optional[str] = None
    created_at: Optional[str] = None


class BillingInvoicesResponse(RankModel):
    """Response from ``GET /billing/invoices``.

    The API returns a raw list when there are invoices, or an empty
    list ``[]`` when there are none.  The ``model_validate`` override
    wraps bare lists into ``{"invoices": [...]}``.
    """

    invoices: List[BillingInvoice] = []

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):  # type: ignore[override]
        if isinstance(obj, list):
            obj = {"invoices": obj}
        return super().model_validate(obj, *args, **kwargs)


__all__ = [
    "BillingTrialStatusResponse",
    "BillingSubscription",
    "BillingStatusResponse",
    "BillingInvoice",
    "BillingInvoicesResponse",
]
