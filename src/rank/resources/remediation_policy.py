from __future__ import annotations

from typing import Any, Dict, List, Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.policy import RemediationPolicy, RemediationPolicyResponse
from ._base import AsyncAPIResource, SyncAPIResource

_POLICY = "/remediation-policy"


def _policy_body(
    *,
    sla_hours: Union[Dict[str, Any], _NotGiven],
    retest_sla_hours: Union[int, _NotGiven],
    quality_gate_rules: Union[List[Dict[str, Any]], _NotGiven],
    auto_retest_on_resolve: Union[bool, _NotGiven],
    auto_retest_on_ticket_close: Union[bool, _NotGiven],
    retest_cooldown_minutes: Union[int, _NotGiven],
    retest_outside_window: Union[bool, _NotGiven],
) -> Dict[str, Any]:
    return strip_not_given({
        "sla_hours": sla_hours,
        "retest_sla_hours": retest_sla_hours,
        "quality_gate_rules": quality_gate_rules,
        "auto_retest_on_resolve": auto_retest_on_resolve,
        "auto_retest_on_ticket_close": auto_retest_on_ticket_close,
        "retest_cooldown_minutes": retest_cooldown_minutes,
        "retest_outside_window": retest_outside_window,
    })


class RemediationPolicies(SyncAPIResource):
    """Caller's SLA, quality-gate and retest defaults.

    Access via ``client.remediation_policy``.
    """

    def retrieve(self) -> RemediationPolicyResponse:
        """Get the caller's policy and the system default."""
        return self._client.get(_POLICY, model=RemediationPolicyResponse)

    def update(
        self,
        *,
        sla_hours: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        retest_sla_hours: Union[int, _NotGiven] = NOT_GIVEN,
        quality_gate_rules: Union[List[Dict[str, Any]], _NotGiven] = NOT_GIVEN,
        auto_retest_on_resolve: Union[bool, _NotGiven] = NOT_GIVEN,
        auto_retest_on_ticket_close: Union[bool, _NotGiven] = NOT_GIVEN,
        retest_cooldown_minutes: Union[int, _NotGiven] = NOT_GIVEN,
        retest_outside_window: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> RemediationPolicy:
        """Create or replace the caller's remediation policy."""
        return self._client.put(
            _POLICY,
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


class AsyncRemediationPolicies(AsyncAPIResource):
    """Async variant of :class:`RemediationPolicies`."""

    async def retrieve(self) -> RemediationPolicyResponse:
        return await self._client.get(_POLICY, model=RemediationPolicyResponse)

    async def update(
        self,
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
            _POLICY,
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
