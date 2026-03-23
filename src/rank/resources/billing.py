from __future__ import annotations

from ..types.billing import (
    BillingInvoicesResponse,
    BillingStatusResponse,
    BillingTrialStatusResponse,
)
from ._base import AsyncAPIResource, SyncAPIResource

_BILLING = "/billing"


# ---------------------------------------------------------------------------
# Billing (sync)
# ---------------------------------------------------------------------------


class Billing(SyncAPIResource):
    """Billing information — trial status, subscription, and invoices.

    Access via ``client.billing``.

    Example::

        trial = client.billing.trial_status()
        print(trial.days_remaining)

        status = client.billing.status()
        if status.has_subscription:
            print(status.subscription.tier_name)
    """

    def trial_status(self) -> BillingTrialStatusResponse:
        """Get the current user's trial status."""
        return self._client.get(
            f"{_BILLING}/trial/status", model=BillingTrialStatusResponse,
        )

    def status(self) -> BillingStatusResponse:
        """Get the current user's billing/subscription status."""
        return self._client.get(
            f"{_BILLING}/status", model=BillingStatusResponse,
        )

    def invoices(self) -> BillingInvoicesResponse:
        """List the current user's invoices."""
        return self._client.get(
            f"{_BILLING}/invoices", model=BillingInvoicesResponse,
        )

    def team_trial_status(self, team_id: int) -> BillingTrialStatusResponse:
        """Get a team's trial status.

        Args:
            team_id: ID of the team.
        """
        return self._client.get(
            f"{_BILLING}/teams/{team_id}/trial/status",
            model=BillingTrialStatusResponse,
        )

    def team_status(self, team_id: int) -> BillingStatusResponse:
        """Get a team's billing/subscription status.

        Args:
            team_id: ID of the team.
        """
        return self._client.get(
            f"{_BILLING}/teams/{team_id}/status", model=BillingStatusResponse,
        )

    def team_invoices(self, team_id: int) -> BillingInvoicesResponse:
        """List a team's invoices.

        Args:
            team_id: ID of the team.
        """
        return self._client.get(
            f"{_BILLING}/teams/{team_id}/invoices", model=BillingInvoicesResponse,
        )


# ---------------------------------------------------------------------------
# Billing (async)
# ---------------------------------------------------------------------------


class AsyncBilling(AsyncAPIResource):
    """Async variant of :class:`Billing`."""

    async def trial_status(self) -> BillingTrialStatusResponse:
        """Get the current user's trial status."""
        return await self._client.get(
            f"{_BILLING}/trial/status", model=BillingTrialStatusResponse,
        )

    async def status(self) -> BillingStatusResponse:
        return await self._client.get(
            f"{_BILLING}/status", model=BillingStatusResponse,
        )

    async def invoices(self) -> BillingInvoicesResponse:
        return await self._client.get(
            f"{_BILLING}/invoices", model=BillingInvoicesResponse,
        )

    async def team_trial_status(self, team_id: int) -> BillingTrialStatusResponse:
        return await self._client.get(
            f"{_BILLING}/teams/{team_id}/trial/status",
            model=BillingTrialStatusResponse,
        )

    async def team_status(self, team_id: int) -> BillingStatusResponse:
        return await self._client.get(
            f"{_BILLING}/teams/{team_id}/status", model=BillingStatusResponse,
        )

    async def team_invoices(self, team_id: int) -> BillingInvoicesResponse:
        return await self._client.get(
            f"{_BILLING}/teams/{team_id}/invoices", model=BillingInvoicesResponse,
        )
