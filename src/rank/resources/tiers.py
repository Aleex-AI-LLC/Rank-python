from __future__ import annotations

from ..types.auth import TierListResponse
from ._base import AsyncAPIResource, SyncAPIResource

_TIERS = "/tiers"


# ---------------------------------------------------------------------------
# Tiers (sync)
# ---------------------------------------------------------------------------


class Tiers(SyncAPIResource):
    """Subscription tier listing.

    Access via ``client.tiers``.

    Example::

        resp = client.tiers.list()
        for t in resp.individual:
            print(t.name, t.price_monthly)
        for t in resp.team:
            print(t.name, t.price_monthly)
    """

    def list(self) -> TierListResponse:
        """List all available subscription tiers and their features."""
        return self._client.get(_TIERS, model=TierListResponse)


# ---------------------------------------------------------------------------
# Tiers (async)
# ---------------------------------------------------------------------------


class AsyncTiers(AsyncAPIResource):
    """Async variant of :class:`Tiers`."""

    async def list(self) -> TierListResponse:
        """List all available subscription tiers and their features."""
        return await self._client.get(_TIERS, model=TierListResponse)
