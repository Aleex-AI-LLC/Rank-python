from __future__ import annotations

from typing import Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.team import (
    OnDemandToggleResponse,
    UsageDailyResponse,
    UsageHistoryResponse,
    UsageSummaryResponse,
)
from ._base import AsyncAPIResource, SyncAPIResource

_USAGE = "/usage"


# ---------------------------------------------------------------------------
# Usage (sync)
# ---------------------------------------------------------------------------


class Usage(SyncAPIResource):
    """Personal usage tracking — summary, daily breakdown, and history.

    Access via ``client.usage``.

    Example::

        summary = client.usage.summary()
        print(summary.budget)

        daily = client.usage.daily(period="7d")
        for entry in daily.daily:
            print(entry.date, entry.cost_usd)
    """

    def summary(
        self,
        *,
        month: Union[str, _NotGiven] = NOT_GIVEN,
        from_date: Union[str, _NotGiven] = NOT_GIVEN,
        to_date: Union[str, _NotGiven] = NOT_GIVEN,
        date: Union[str, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> UsageSummaryResponse:
        """Get usage summary with budget and model breakdown.

        Args:
            month: Month filter (e.g. ``"2025-03"``).
            from_date: Start date (sent as ``from`` to the API).
            to_date: End date (sent as ``to`` to the API).
            date: Specific date.
            model_id: Filter by AI model ID.
        """
        params = strip_not_given({
            "month": month,
            "from": from_date,
            "to": to_date,
            "date": date,
            "model_id": model_id,
        })
        return self._client.get(
            f"{_USAGE}/summary", params=params or None, model=UsageSummaryResponse,
        )

    def daily(
        self,
        *,
        period: Union[str, _NotGiven] = NOT_GIVEN,
        date: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> UsageDailyResponse:
        """Get daily or hourly usage breakdown.

        When ``period`` is provided, returns daily entries.
        When ``date`` is provided, returns hourly entries for that day.

        Args:
            period: Time period (e.g. ``"7d"``, ``"30d"``).
            date: Specific date for hourly breakdown.
        """
        params = strip_not_given({"period": period, "date": date})
        return self._client.get(
            f"{_USAGE}/daily", params=params or None, model=UsageDailyResponse,
        )

    def history(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> UsageHistoryResponse:
        """Get paginated usage history log.

        Args:
            page: Page number (default 1).
            per_page: Items per page (default 20, max 100).
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"{_USAGE}/history", params=params or None, model=UsageHistoryResponse,
        )

    def toggle_on_demand(
        self,
        *,
        enabled: bool,
        limit_usd: Union[float, _NotGiven] = NOT_GIVEN,
    ) -> OnDemandToggleResponse:
        """Toggle on-demand usage and optionally set a spending limit.

        Args:
            enabled: Whether to enable on-demand usage.
            limit_usd: Maximum on-demand spend in USD.
        """
        body = strip_not_given({"enabled": enabled, "limit_usd": limit_usd})
        return self._client.patch(
            f"{_USAGE}/on-demand", body=body, model=OnDemandToggleResponse,
        )


# ---------------------------------------------------------------------------
# Usage (async)
# ---------------------------------------------------------------------------


class AsyncUsage(AsyncAPIResource):
    """Async variant of :class:`Usage`."""

    async def summary(
        self,
        *,
        month: Union[str, _NotGiven] = NOT_GIVEN,
        from_date: Union[str, _NotGiven] = NOT_GIVEN,
        to_date: Union[str, _NotGiven] = NOT_GIVEN,
        date: Union[str, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> UsageSummaryResponse:
        params = strip_not_given({
            "month": month,
            "from": from_date,
            "to": to_date,
            "date": date,
            "model_id": model_id,
        })
        return await self._client.get(
            f"{_USAGE}/summary", params=params or None, model=UsageSummaryResponse,
        )

    async def daily(
        self,
        *,
        period: Union[str, _NotGiven] = NOT_GIVEN,
        date: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> UsageDailyResponse:
        params = strip_not_given({"period": period, "date": date})
        return await self._client.get(
            f"{_USAGE}/daily", params=params or None, model=UsageDailyResponse,
        )

    async def history(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> UsageHistoryResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"{_USAGE}/history", params=params or None, model=UsageHistoryResponse,
        )

    async def toggle_on_demand(
        self,
        *,
        enabled: bool,
        limit_usd: Union[float, _NotGiven] = NOT_GIVEN,
    ) -> OnDemandToggleResponse:
        body = strip_not_given({"enabled": enabled, "limit_usd": limit_usd})
        return await self._client.patch(
            f"{_USAGE}/on-demand", body=body, model=OnDemandToggleResponse,
        )
