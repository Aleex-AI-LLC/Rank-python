from __future__ import annotations

from typing import Any, Dict, List, Optional

from .shared import MessageResponse, PaginationInfo, Permission, RankModel


# ---------------------------------------------------------------------------
# Tier / Trial / Subscription (nested in User)
# ---------------------------------------------------------------------------


class Tier(RankModel):
    """Subscription tier with its associated limits and permissions."""

    id: int
    name: str = ""
    price_monthly: Optional[float] = None
    monthly_usage_budget_usd: Optional[float] = None
    max_pentests_per_month: Optional[int] = None
    max_teams: Optional[int] = None
    max_api_tokens: Optional[int] = None
    max_agents: Optional[int] = None
    max_scheduled_pentests: Optional[int] = None
    is_custom_pricing: bool = False
    permissions: List[Permission] = []


class Trial(RankModel):
    """Trial information attached to a user or team."""

    active: bool = False
    trial_tier: Optional[Tier] = None
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    days_remaining: int = 0
    trial_used: bool = False


class Subscription(RankModel):
    """Stripe subscription status summary."""

    status: str = ""
    billing_interval: Optional[str] = None
    current_period_end: Optional[str] = None
    cancel_at: Optional[str] = None


# ---------------------------------------------------------------------------
# User teams (nested in User from /auth/me)
# ---------------------------------------------------------------------------


class UserTeamRole(RankModel):
    """Role assigned to the current user within a team."""

    id: int
    role_name: str = ""
    color: Optional[str] = None
    permissions: List[Permission] = []


class UserTeam(RankModel):
    """Team summary as seen from the authenticated user's perspective."""

    id: int
    name: str = ""
    description: Optional[str] = None
    owner_id: int = 0
    is_owner: bool = False
    tier: Optional[Tier] = None
    status: Optional[int] = None
    billing_status: Optional[str] = None
    max_members: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    roles: List[UserTeamRole] = []


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------


class User(RankModel):
    """Authenticated user profile returned by ``GET /auth/me``."""

    user_id: int
    username: Optional[str] = None
    email: Optional[str] = None
    external_user: bool = False
    login_count: int = 0
    queue_prio: Optional[int] = None
    deleted: bool = False
    deleted_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    language: str = "en"
    verified: bool = False
    tier: Optional[Tier] = None
    trial: Optional[Trial] = None
    subscription: Optional[Subscription] = None
    teams: List[UserTeam] = []
    assigned_models: List[Any] = []
    assigned_agents: List[Any] = []
    assigned_agents_count: int = 0


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------


class SessionUserData(RankModel):
    """Metadata captured when a session was created."""

    ip: Optional[str] = None
    user_agent: Optional[str] = None
    accept_language: Optional[str] = None
    created_at: Optional[str] = None


class Session(RankModel):
    """A single JWT session."""

    id: int
    creation_date: Optional[str] = None
    expiration_date: Optional[str] = None
    userdata: Optional[SessionUserData] = None
    used: Optional[int] = None
    status: Optional[str] = None


class SessionListResponse(RankModel):
    """Paginated list of sessions returned by ``GET /auth/sessions``."""

    items: List[Session] = []
    pagination: Optional[PaginationInfo] = None


# ---------------------------------------------------------------------------
# API Tokens
# ---------------------------------------------------------------------------


class ApiTokenTeam(RankModel):
    """Team scope entry for an API token (from token list/create responses)."""

    id: int
    team_name: str = ""


class AvailableTeam(RankModel):
    """Team entry returned by the available-permissions endpoint."""

    id: int
    name: str = ""


class ApiToken(RankModel):
    """An API token with its metadata, permissions, and team scopes."""

    id: int
    user_id: Optional[int] = None
    name: Optional[str] = None
    scoped: bool = False
    created_at: Optional[str] = None
    last_used_at: Optional[str] = None
    revoked: int = 0
    prefix: Optional[str] = None
    permissions: List[Permission] = []
    teams: List[ApiTokenTeam] = []


class ApiTokenLimits(RankModel):
    """Token creation limits for the current user/team context."""

    max_tokens: Optional[int] = None
    active_tokens: int = 0
    team_active_tokens: Optional[int] = None
    remaining: Optional[int] = None
    is_unlimited: bool = False
    context: str = ""
    context_name: str = ""


class ApiTokenListResponse(RankModel):
    """Paginated list of API tokens with usage limits."""

    items: List[ApiToken] = []
    pagination: Optional[PaginationInfo] = None
    limits: Optional[ApiTokenLimits] = None


class ApiTokenCreateResponse(RankModel):
    """Response after creating a new API token.

    The ``token`` field contains the plaintext token value and is only
    returned once -- it cannot be retrieved again.
    """

    message: str = ""
    token: str = ""
    token_info: Optional[ApiToken] = None
    target_team_id: Optional[int] = None
    limits: Optional[ApiTokenLimits] = None


class AvailablePermissionsResponse(RankModel):
    """Permissions available for scoping API tokens."""

    permissions: Dict[str, List[Permission]] = {}
    tags: List[str] = []
    teams: List[AvailableTeam] = []


# ---------------------------------------------------------------------------
# Profile update response (raw DB row from PATCH /auth/profile)
# ---------------------------------------------------------------------------


class ProfileUpdateResponse(RankModel):
    """Raw user row returned by ``PATCH /auth/profile``.

    Unlike :class:`User` (which is the rich object from ``GET /auth/me``),
    this is the flat database row without nested tier/trial/subscription/teams.
    """

    id: Optional[int] = None
    user_id: int
    email: Optional[str] = None
    username: Optional[str] = None
    external_user: Optional[int] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    login_count: Optional[int] = None
    queue_prio: Optional[int] = None
    deleted: Optional[int] = None
    deleted_at: Optional[str] = None
    tier_id: Optional[int] = None
    country: Optional[str] = None
    region: Optional[str] = None
    language: Optional[str] = None
    trial_tier_id: Optional[int] = None
    trial_starts_at: Optional[str] = None
    trial_ends_at: Optional[str] = None
    trial_used: Optional[int] = None
    email_verified_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Profile update responses
# ---------------------------------------------------------------------------


class UpdateEmailResponse(RankModel):
    """Response after changing the account email address."""

    message: str = ""
    user: Optional[Dict[str, Any]] = None
    email_verification_sent: bool = False


class UpdateUsernameResponse(RankModel):
    """Response after changing the username."""

    message: str = ""
    user: Optional[Dict[str, Any]] = None


# Re-export MessageResponse so callers can import from types.auth directly.
__all__ = [
    "ApiToken",
    "ApiTokenCreateResponse",
    "ApiTokenLimits",
    "ApiTokenListResponse",
    "ApiTokenTeam",
    "AvailableTeam",
    "AvailablePermissionsResponse",
    "MessageResponse",
    "ProfileUpdateResponse",
    "Session",
    "SessionListResponse",
    "SessionUserData",
    "Subscription",
    "Tier",
    "Trial",
    "UpdateEmailResponse",
    "UpdateUsernameResponse",
    "User",
    "UserTeam",
    "UserTeamRole",
]
