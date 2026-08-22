from __future__ import annotations

from typing import Any, Dict, List, Optional

from .shared import RankModel


class RemediationPolicy(RankModel):
    """Tenant defaults for SLA, quality gates and automatic retest."""

    id: int = 0
    owner_type: str = ""
    owner_id: int = 0
    sla_hours: Dict[str, Any] = {}
    retest_sla_hours: int = 72
    quality_gate_rules: List[Dict[str, Any]] = []
    auto_retest_on_resolve: bool = False
    auto_retest_on_ticket_close: bool = True
    retest_cooldown_minutes: int = 15
    retest_outside_window: bool = True


class RemediationPolicyResponse(RankModel):
    """Response from ``GET /remediation-policy`` and the team equivalent."""

    policy: Optional[RemediationPolicy] = None
    system_default: Optional[RemediationPolicy] = None
