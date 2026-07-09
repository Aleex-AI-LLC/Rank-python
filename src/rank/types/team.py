from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import Field

from .shared import PaginationInfo, Permission, RankModel, ReasoningEffort


# ---------------------------------------------------------------------------
# Team
# ---------------------------------------------------------------------------


class Team(RankModel):
    """Full team object returned by list, show, create, and update.

    Fields that may be absent depending on the endpoint are ``Optional``
    with ``None`` defaults for forward-compatibility.
    """

    id: int
    name: str = ""
    description: Optional[str] = None
    owner_id: Optional[int] = None
    owner_name: Optional[str] = None
    tier_id: Optional[int] = None
    tier_name: Optional[str] = None
    status: Optional[int] = None
    status_name: Optional[str] = None
    on_demand_enabled: Optional[bool] = None
    on_demand_limit_usd: Optional[float] = None
    team_usage_budget_usd: Optional[float] = None
    max_members: Optional[int] = None
    member_count: Optional[int] = None
    enterprise_stripe_price_id: Optional[str] = None
    billing_status: Optional[str] = None
    billing_grace_deadline: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    members: Optional[List[Any]] = None
    available_roles: Optional[List[Any]] = None


class TeamListResponse(RankModel):
    """Paginated list of teams returned by ``GET /teams``."""

    items: List[Team] = []
    pagination: Optional[PaginationInfo] = None


# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------


class TeamMember(RankModel):
    """A member of a team with their roles."""

    id: Optional[int] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    roles: List[Any] = []
    joined_at: Optional[str] = None


class MemberListResponse(RankModel):
    """Paginated list of team members."""

    items: List[TeamMember] = []
    pagination: Optional[PaginationInfo] = None


# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------


class TeamRole(RankModel):
    """A custom role within a team.

    The backend returns ``role_name`` and ``protected``; Pydantic aliases
    map them to the Python-friendly ``name`` and ``is_default``.
    """

    id: int
    name: Optional[str] = Field(None, alias="role_name")
    color: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = Field(None, alias="protected")
    team_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    deleted_at: Optional[str] = None
    created_by: Optional[int] = None


class RoleListResponse(RankModel):
    """Paginated list of team roles."""

    items: List[TeamRole] = []
    pagination: Optional[PaginationInfo] = None


# ---------------------------------------------------------------------------
# Invitations
# ---------------------------------------------------------------------------


class InvitationStats(RankModel):
    """Aggregate counts of invitations by status."""

    total: int = 0
    pending: int = 0
    accepted: int = 0
    rejected: int = 0
    expired: int = 0
    cancelled: int = 0


class TeamInvitation(RankModel):
    """An invitation to join a team."""

    id: int
    team_id: Optional[int] = None
    email: Optional[str] = None
    invited_by: Optional[int] = None
    role_id: Optional[int] = None
    status: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: Optional[str] = None
    inviter_name: Optional[str] = None
    role_name: Optional[str] = None


class InvitationListPagination(RankModel):
    """Pagination info specific to the invitations endpoint."""

    total: int = 0
    page: int = 1
    per_page: int = 20
    total_pages: int = 1


class InvitationListResponse(RankModel):
    """Response from ``GET /teams/{id}/invitations``."""

    invitations: List[TeamInvitation] = []
    pagination: Optional[InvitationListPagination] = None
    stats: Optional[InvitationStats] = None


class UserInvitation(RankModel):
    """An invitation as seen from the recipient user's perspective.

    Returned by ``GET /invitations`` (user-level).  Fields differ from
    :class:`TeamInvitation` (which is the team-admin view).

    The ``token`` is needed to call ``accept()`` or ``reject()``.
    """

    id: int
    token: Optional[str] = None
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    inviter_name: Optional[str] = None
    role_name: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: Optional[str] = None


class UserInvitationListResponse(RankModel):
    """Response from ``GET /invitations`` (user-level, paginated)."""

    items: List[UserInvitation] = []
    pagination: Optional[PaginationInfo] = None


class InvitationDetail(RankModel):
    """Detailed invitation info returned by ``GET /invitations/{token}``."""

    team_name: Optional[str] = None
    inviter_name: Optional[str] = None
    inviter_email: Optional[str] = None
    email: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: Optional[str] = None


class InvitationAcceptResponse(RankModel):
    """Response from ``POST /invitations/{token}/accept``."""

    message: str = ""
    team_id: Optional[int] = None
    team_name: Optional[str] = None


class InvitationCreateResponse(RankModel):
    """Response from creating or resending a team invitation."""

    message: str = ""
    invitation_id: Optional[int] = None
    expires_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Agents (team context)
# ---------------------------------------------------------------------------


class TeamAgentItem(RankModel):
    """An agent available to a team."""

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    agent_type: Optional[str] = None
    phase_id: Optional[int] = None
    phase_name: Optional[str] = None
    model_id: Optional[int] = None
    model_name: Optional[str] = None
    effort: Optional[ReasoningEffort] = None
    thinking_enabled: Optional[bool] = None
    is_default: Optional[bool] = None
    protected: Optional[bool] = None


class TeamAgentDetail(RankModel):
    """Full agent detail returned after creation."""

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    agent_type: Optional[str] = None
    phase: Optional[Any] = None
    model: Optional[Any] = None
    effort: Optional[ReasoningEffort] = None
    thinking_enabled: Optional[bool] = None
    supports_effort: Optional[bool] = None
    effort_values: List[ReasoningEffort] = []
    default_effort: Optional[ReasoningEffort] = None
    supports_thinking_toggle: Optional[bool] = None
    is_default: Optional[bool] = None
    protected: Optional[bool] = None
    created_by: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    tools: List[Any] = []


class TeamAgentListResponse(RankModel):
    """Response from ``GET /teams/{id}/agents``."""

    team_agents: List[TeamAgentItem] = []
    default_agents: List[TeamAgentItem] = []
    total_team: int = 0
    page: Optional[int] = None
    per_page: Optional[int] = None


class TeamAgentCreateResponse(RankModel):
    """Response from ``POST /teams/{id}/agents``."""

    message: str = ""
    agent: Optional[TeamAgentDetail] = None
    team_id: Optional[int] = None


class TeamAgentDeleteResponse(RankModel):
    """Response from ``DELETE /teams/{id}/agents/{agentId}``."""

    message: str = ""
    team_id: Optional[int] = None
    agent_id: Optional[int] = None


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------


class UsageBillingPeriod(RankModel):
    """Billing period date range."""

    start: Optional[str] = None
    end: Optional[str] = None


class UsageTeamTier(RankModel):
    """Tier info inside usage summary."""

    id: Optional[int] = None
    name: Optional[str] = None
    is_custom_pricing: Optional[bool] = None


class UsageTeamInfo(RankModel):
    """Team metadata inside usage summary."""

    id: Optional[int] = None
    name: Optional[str] = None
    member_count: Optional[int] = None
    tier: Optional[UsageTeamTier] = None


class UsageOnDemand(RankModel):
    """On-demand settings inside usage summary."""

    enabled: Optional[bool] = None
    limit_usd: Optional[float] = None


class UsageBudget(RankModel):
    """Budget breakdown inside usage summary."""

    total_pool_usd: Optional[Any] = None
    total_cost_usd: Optional[float] = None
    included_cost_usd: Optional[float] = None
    on_demand_cost_usd: Optional[float] = None
    budget_remaining_usd: Optional[Any] = None


class UsageTotals(RankModel):
    """Aggregate token/operation counts."""

    total_cost_usd: Optional[float] = None
    total_input_tokens: Optional[int] = None
    total_output_tokens: Optional[int] = None
    total_cache_read_tokens: Optional[int] = None
    total_cache_write_tokens: Optional[int] = None
    total_operations: Optional[int] = None
    pentests_count: Optional[int] = None


class UsageModelBreakdown(RankModel):
    """Per-model usage breakdown."""

    model_id: Optional[int] = None
    model_name: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    operations_count: Optional[int] = None
    top_agents: List[Any] = Field(default=[], alias="top_agents")


class UsageSummaryResponse(RankModel):
    """Response from ``GET /teams/{id}/usage/summary``."""

    billing_period: Optional[UsageBillingPeriod] = None
    team: Optional[UsageTeamInfo] = None
    on_demand: Optional[UsageOnDemand] = None
    budget: Optional[UsageBudget] = None
    usage: Optional[UsageTotals] = None
    by_model: List[UsageModelBreakdown] = []


class UsageDailyEntry(RankModel):
    """A single day in daily usage breakdown."""

    date: Optional[str] = None
    cost_usd: Optional[float] = None
    tokens: Optional[int] = None
    operations_count: Optional[int] = None
    cumulative_cost_usd: Optional[float] = None
    by_model: List[Any] = []


class UsageHourlyEntry(RankModel):
    """A single hour in hourly usage breakdown."""

    hour: Optional[str] = None
    cost_usd: Optional[float] = None
    tokens: Optional[int] = None
    operations_count: Optional[int] = None
    by_model: List[Any] = []


class UsageDailyResponse(RankModel):
    """Response from ``GET /teams/{id}/usage/daily``.

    Contains either ``daily`` (when using ``period`` param) or
    ``hourly`` (when using ``date`` param), never both.
    """

    period: Optional[str] = None
    date: Optional[str] = None
    daily: List[UsageDailyEntry] = []
    hourly: List[UsageHourlyEntry] = []


class UsageMemberSummary(RankModel):
    """Per-member usage summary."""

    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    total_cost_usd: Optional[float] = None
    total_tokens: Optional[int] = None
    operations_count: Optional[int] = None
    top_models: List[Any] = []


class UsageMembersResponse(RankModel):
    """Response from ``GET /teams/{id}/usage/members``."""

    members: List[UsageMemberSummary] = []


class UsageMemberInfo(RankModel):
    """Member metadata inside member-detail response."""

    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None


class UsageMemberDetailResponse(RankModel):
    """Response from ``GET /teams/{id}/usage/members/{memberId}``."""

    billing_period: Optional[UsageBillingPeriod] = None
    member: Optional[UsageMemberInfo] = None
    usage: Optional[UsageTotals] = None
    by_model: List[UsageModelBreakdown] = []


class UsageHistoryItem(RankModel):
    """A single entry in the usage history log."""

    id: Optional[int] = None
    date: Optional[str] = None
    type: Optional[str] = None
    model_name: Optional[str] = None
    agent_name: Optional[str] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cache_read_tokens: Optional[int] = None
    cache_write_tokens: Optional[int] = None
    cost_usd: Optional[float] = None


class UsageHistoryResponse(RankModel):
    """Paginated usage history."""

    items: List[UsageHistoryItem] = []
    pagination: Optional[PaginationInfo] = None


class OnDemandToggleResponse(RankModel):
    """Response from ``PATCH /teams/{id}/usage/on-demand``."""

    on_demand_enabled: Optional[bool] = None
    on_demand_limit_usd: Optional[float] = None
    team_usage_budget_usd: Optional[float] = None


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------

__all__ = [
    # Team
    "Team",
    "TeamListResponse",
    # Members
    "TeamMember",
    "MemberListResponse",
    # Roles
    "TeamRole",
    "RoleListResponse",
    # Invitations (team-scoped)
    "InvitationStats",
    "TeamInvitation",
    "InvitationListPagination",
    "InvitationListResponse",
    "InvitationCreateResponse",
    # Invitations (user-level)
    "UserInvitation",
    "UserInvitationListResponse",
    "InvitationDetail",
    "InvitationAcceptResponse",
    # Agents
    "TeamAgentItem",
    "TeamAgentDetail",
    "TeamAgentListResponse",
    "TeamAgentCreateResponse",
    "TeamAgentDeleteResponse",
    # Usage
    "UsageBillingPeriod",
    "UsageTeamTier",
    "UsageTeamInfo",
    "UsageOnDemand",
    "UsageBudget",
    "UsageTotals",
    "UsageModelBreakdown",
    "UsageSummaryResponse",
    "UsageDailyEntry",
    "UsageHourlyEntry",
    "UsageDailyResponse",
    "UsageMemberSummary",
    "UsageMembersResponse",
    "UsageMemberInfo",
    "UsageMemberDetailResponse",
    "UsageHistoryItem",
    "UsageHistoryResponse",
    "OnDemandToggleResponse",
]
