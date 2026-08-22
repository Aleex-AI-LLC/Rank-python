from __future__ import annotations

from typing import Any, Dict, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.team import (
    OnDemandToggleResponse,
    UsageDailyResponse,
    UsageHistoryResponse,
    UsageMemberDetailResponse,
    UsageMembersResponse,
    UsageSummaryResponse,
)
from .._base import AsyncAPIResource, SyncAPIResource

# ---------------------------------------------------------------------------
# TeamUsage (sync)
# ---------------------------------------------------------------------------


class TeamUsage(SyncAPIResource):
    """View and manage usage statistics for a team.

    Access via ``client.teams.usage``.

    Example::

        # Get current billing period summary
        summary = client.teams.usage.summary(team_id=1)
        print(f"Total cost: ${summary.usage.total_cost_usd}")

        # See per-member breakdown
        members = client.teams.usage.members(team_id=1)
        for m in members.members:
            print(f"{m.username}: ${m.total_cost_usd}")
    """

    def summary(
        self,
        team_id: int,
        *,
        month: Union[str, _NotGiven] = NOT_GIVEN,
        from_date: Union[str, _NotGiven] = NOT_GIVEN,
        to_date: Union[str, _NotGiven] = NOT_GIVEN,
        date: Union[str, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> UsageSummaryResponse:
        """Get a usage summary for a team.

        Multiple date filters can be combined:

        - ``month``: ``"YYYY-MM"`` format for a specific month.
        - ``from_date`` / ``to_date``: custom date range.
        - ``date``: single day ``"YYYY-MM-DD"``.
        - ``model_id``: filter by AI model.

        With no filters, returns the current billing period.

        Args:
            team_id: ID of the team.
            month: Month in ``"YYYY-MM"`` format.
            from_date: Start date ``"YYYY-MM-DD"``.
            to_date: End date ``"YYYY-MM-DD"``.
            date: Single date ``"YYYY-MM-DD"``.
            model_id: Filter by model ID.
        """
        params = strip_not_given({
            "month": month,
            "from": from_date,
            "to": to_date,
            "date": date,
            "model_id": model_id,
        })
        return self._client.get(
            f"/teams/{team_id}/usage/summary",
            params=params or None,
            model=UsageSummaryResponse,
        )

    def daily(
        self,
        team_id: int,
        *,
        period: Union[str, _NotGiven] = NOT_GIVEN,
        date: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> UsageDailyResponse:
        """Get daily (or hourly) usage breakdown.

        Use **either** ``period`` or ``date``, not both:

        - ``period``: ``"1d"``, ``"7d"``, or ``"30d"`` (default)
          for a daily breakdown.
        - ``date``: ``"YYYY-MM-DD"`` for an hourly breakdown of
          that specific day.

        Args:
            team_id: ID of the team.
            period: Time period (``"1d"``, ``"7d"``, ``"30d"``).
            date: Specific date for hourly breakdown.
        """
        params = strip_not_given({"period": period, "date": date})
        return self._client.get(
            f"/teams/{team_id}/usage/daily",
            params=params or None,
            model=UsageDailyResponse,
        )

    def members(self, team_id: int) -> UsageMembersResponse:
        """Get per-member usage summary for a team.

        Args:
            team_id: ID of the team.
        """
        return self._client.get(
            f"/teams/{team_id}/usage/members",
            model=UsageMembersResponse,
        )

    def member_detail(
        self, team_id: int, member_id: int,
    ) -> UsageMemberDetailResponse:
        """Get detailed usage for a specific team member.

        Args:
            team_id: ID of the team.
            member_id: User ID of the team member.
        """
        return self._client.get(
            f"/teams/{team_id}/usage/members/{member_id}",
            model=UsageMemberDetailResponse,
        )

    def history(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> UsageHistoryResponse:
        """Get paginated usage history log.

        Each entry represents a single AI operation with its token
        counts and cost.

        Args:
            team_id: ID of the team.
            page: Page number (default 1).
            per_page: Items per page (default 20, max 100).
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"/teams/{team_id}/usage/history",
            params=params or None,
            model=UsageHistoryResponse,
        )

    def toggle_on_demand(
        self,
        team_id: int,
        *,
        enabled: bool,
        limit_usd: Union[float, None, _NotGiven] = NOT_GIVEN,
        budget_usd: Union[float, None, _NotGiven] = NOT_GIVEN,
    ) -> OnDemandToggleResponse:
        """Enable or disable on-demand usage for a team.

        When enabled, the team can exceed its included usage pool at
        additional cost.

        Args:
            team_id: ID of the team.
            enabled: Whether on-demand usage is enabled.
            limit_usd: Maximum on-demand spend in USD, or ``None``
                for unlimited. Cannot be ``0`` when ``enabled`` is
                ``True``.
            budget_usd: Total team usage budget in USD, or ``None``
                for unlimited.
        """
        body: Dict[str, Any] = {"enabled": enabled}
        body.update(strip_not_given({
            "limit_usd": limit_usd,
            "budget_usd": budget_usd,
        }))
        return self._client.patch(
            f"/teams/{team_id}/usage/on-demand",
            body=body,
            model=OnDemandToggleResponse,
        )


# ---------------------------------------------------------------------------
# TeamUsage (async)
# ---------------------------------------------------------------------------


class AsyncTeamUsage(AsyncAPIResource):
    """Async variant of :class:`TeamUsage`."""

    async def summary(
        self,
        team_id: int,
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
            f"/teams/{team_id}/usage/summary",
            params=params or None,
            model=UsageSummaryResponse,
        )

    async def daily(
        self,
        team_id: int,
        *,
        period: Union[str, _NotGiven] = NOT_GIVEN,
        date: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> UsageDailyResponse:
        params = strip_not_given({"period": period, "date": date})
        return await self._client.get(
            f"/teams/{team_id}/usage/daily",
            params=params or None,
            model=UsageDailyResponse,
        )

    async def members(self, team_id: int) -> UsageMembersResponse:
        return await self._client.get(
            f"/teams/{team_id}/usage/members",
            model=UsageMembersResponse,
        )

    async def member_detail(
        self, team_id: int, member_id: int,
    ) -> UsageMemberDetailResponse:
        return await self._client.get(
            f"/teams/{team_id}/usage/members/{member_id}",
            model=UsageMemberDetailResponse,
        )

    async def history(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> UsageHistoryResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"/teams/{team_id}/usage/history",
            params=params or None,
            model=UsageHistoryResponse,
        )

    async def toggle_on_demand(
        self,
        team_id: int,
        *,
        enabled: bool,
        limit_usd: Union[float, None, _NotGiven] = NOT_GIVEN,
        budget_usd: Union[float, None, _NotGiven] = NOT_GIVEN,
    ) -> OnDemandToggleResponse:
        body: Dict[str, Any] = {"enabled": enabled}
        body.update(strip_not_given({
            "limit_usd": limit_usd,
            "budget_usd": budget_usd,
        }))
        return await self._client.patch(
            f"/teams/{team_id}/usage/on-demand",
            body=body,
            model=OnDemandToggleResponse,
        )
