from __future__ import annotations

from typing import Any, Dict, List, Optional

from .catalog import ApprovalClass
from .shared import RankModel


class RoeTimeWindow(RankModel):
    """A testing window declared on a Rules of Engagement."""

    start: str = ""
    end: str = ""
    days: Any = None


class EscalationContact(RankModel):
    """A RoE escalation contact."""

    type: Optional[str] = None
    value: Optional[str] = None


class EngagementRoe(RankModel):
    """Full Rules of Engagement version."""

    id: Optional[int] = None
    pentest_id: Optional[int] = None
    version: Optional[int] = None
    status: Optional[str] = None
    allowed_cidrs: List[str] = []
    allowed_domains: List[str] = []
    denied_cidrs: List[str] = []
    denied_domains: List[str] = []
    allowed_techniques: List[str] = []
    forbidden_techniques: List[str] = []
    source_ips: List[str] = []
    time_windows: List[Dict[str, Any]] = []
    timezone: Optional[str] = None
    asset_criticality: Dict[str, str] = {}
    max_rps: Optional[int] = None
    max_concurrency: Optional[int] = None
    authorization_ref: Optional[str] = None
    authorized_by: Optional[int] = None
    authorized_at: Optional[str] = None
    escalation_contacts: List[Dict[str, Any]] = []
    requires_approval_for: List[str] = []
    auto_approve: bool = False
    created_by: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    available_approval_classes: List[ApprovalClass] = []


class RoeVersionSummary(RankModel):
    """Compact RoE version row for history listings."""

    id: Optional[int] = None
    version: Optional[int] = None
    status: Optional[str] = None
    authorization_ref: Optional[str] = None
    authorized_by: Optional[int] = None
    authorized_at: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class RoeResponse(RankModel):
    """Response from ``GET /pentests/{id}/roe``."""

    active: Optional[EngagementRoe] = None
    versions: List[RoeVersionSummary] = []
    available_approval_classes: List[ApprovalClass] = []


class KillResponse(RankModel):
    """Response from ``POST /pentests/{id}/kill``."""

    message: str = ""
    pentest_id: Optional[int] = None
    kill_requested: bool = False
    kill_requested_at: Optional[str] = None
    reason: Optional[str] = None


class Approval(RankModel):
    """A human approval gate for a restricted action."""

    id: int
    pentest_id: Optional[int] = None
    action_class: Optional[str] = None
    action_summary: Optional[str] = None
    target: Optional[str] = None
    confidence: Optional[int] = None
    status: Optional[str] = None
    requested_at: Optional[str] = None
    expires_at: Optional[str] = None
    decided_at: Optional[str] = None
    decided_by: Optional[int] = None
    decision_reason: Optional[str] = None
    auto_approved: bool = False
    action_fingerprint: Optional[str] = None
    action_payload: Optional[Dict[str, Any]] = None
    single_use: bool = True
    consumed_by_this_read: bool = False


class ApprovalListResponse(RankModel):
    """Response from ``GET /pentests/{id}/approvals``."""

    approvals: List[Approval] = []
    total: int = 0
