from __future__ import annotations

from typing import Any, Dict, List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven
from ...types.policy import RemediationPolicy, RemediationPolicyResponse
from .._base import AsyncAPIResource, SyncAPIResource
from ..remediation_policy import _policy_body


class TeamRemediationPolicy(SyncAPIResource):
    """Team SLA / quality-gate / retest policy. Access via ``client.teams.remediation_policy``."""

    def retrieve(self, team_id: int) -> RemediationPolicyResponse:
        return self._client.get(
            f"/teams/{team_id}/remediation-policy",
            model=RemediationPolicyResponse,
        )

    def update(
        self,
        team_id: int,
        *,
        sla_hours: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        retest_sla_hours: Union[int, _NotGiven] = NOT_GIVEN,
        quality_gate_rules: Union[List[Dict[str, Any]], _NotGiven] = NOT_GIVEN,
        auto_retest_on_resolve: Union[bool, _NotGiven] = NOT_GIVEN,
        auto_retest_on_ticket_close: Union[bool, _NotGiven] = NOT_GIVEN,
        retest_cooldown_minutes: Union[int, _NotGiven] = NOT_GIVEN,
        retest_outside_window: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> RemediationPolicy:
        return self._client.put(
            f"/teams/{team_id}/remediation-policy",
            body=_policy_body(
                sla_hours=sla_hours,
                retest_sla_hours=retest_sla_hours,
                quality_gate_rules=quality_gate_rules,
                auto_retest_on_resolve=auto_retest_on_resolve,
                auto_retest_on_ticket_close=auto_retest_on_ticket_close,
                retest_cooldown_minutes=retest_cooldown_minutes,
                retest_outside_window=retest_outside_window,
            ),
            model=RemediationPolicy,
        )


class AsyncTeamRemediationPolicy(AsyncAPIResource):
    """Async variant of :class:`TeamRemediationPolicy`."""

    async def retrieve(self, team_id: int) -> RemediationPolicyResponse:
        return await self._client.get(
            f"/teams/{team_id}/remediation-policy",
            model=RemediationPolicyResponse,
        )

    async def update(
        self,
        team_id: int,
        *,
        sla_hours: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        retest_sla_hours: Union[int, _NotGiven] = NOT_GIVEN,
        quality_gate_rules: Union[List[Dict[str, Any]], _NotGiven] = NOT_GIVEN,
        auto_retest_on_resolve: Union[bool, _NotGiven] = NOT_GIVEN,
        auto_retest_on_ticket_close: Union[bool, _NotGiven] = NOT_GIVEN,
        retest_cooldown_minutes: Union[int, _NotGiven] = NOT_GIVEN,
        retest_outside_window: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> RemediationPolicy:
        return await self._client.put(
            f"/teams/{team_id}/remediation-policy",
            body=_policy_body(
                sla_hours=sla_hours,
                retest_sla_hours=retest_sla_hours,
                quality_gate_rules=quality_gate_rules,
                auto_retest_on_resolve=auto_retest_on_resolve,
                auto_retest_on_ticket_close=auto_retest_on_ticket_close,
                retest_cooldown_minutes=retest_cooldown_minutes,
                retest_outside_window=retest_outside_window,
            ),
            model=RemediationPolicy,
        )
