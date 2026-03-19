"""Rank - The official Python SDK for the Rank API.

Usage:
    import rank

    # Synchronous
    client = rank.Rank(api_key="rk_...")
    pentests = client.pentests.list()

    # Asynchronous
    async_client = rank.AsyncRank(api_key="rk_...")
    pentests = await async_client.pentests.list()

    # Streaming (AI chat)
    with client.ai.chat.stream(agent_id=1, user_prompt="Scan target") as stream:
        for event in stream:
            print(event.content, end="")
"""

from __future__ import annotations

from ._client import AsyncRank, Rank
from ._constants import PACKAGE_VERSION
from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RankError,
    RateLimitError,
    UnprocessableEntityError,
)
from ._streaming import AsyncStream, ServerSentEvent, Stream
from ._utils._transform import NOT_GIVEN
from .types import (
    ApiToken,
    ApiTokenCreateResponse,
    ApiTokenLimits,
    ApiTokenListResponse,
    ApiTokenTeam,
    AvailablePermissionsResponse,
    AvailableTeam,
    ErrorDetail,
    MessageResponse,
    PaginatedResponse,
    PaginationInfo,
    PaginationMeta,
    Permission,
    ProfileUpdateResponse,
    RankModel,
    Session,
    SessionListResponse,
    SessionUserData,
    Subscription,
    SuccessResponse,
    Tier,
    Trial,
    UpdateEmailResponse,
    UpdateUsernameResponse,
    User,
    UserTeam,
    UserTeamRole,
)

__version__ = PACKAGE_VERSION

__all__ = [
    # Clients
    "Rank",
    "AsyncRank",
    # Exceptions
    "RankError",
    "APIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    "APIConnectionError",
    "APITimeoutError",
    # Streaming
    "Stream",
    "AsyncStream",
    "ServerSentEvent",
    # Utilities
    "NOT_GIVEN",
    # Shared types
    "RankModel",
    "PaginatedResponse",
    "PaginationMeta",
    "PaginationInfo",
    "Permission",
    "MessageResponse",
    "SuccessResponse",
    "ErrorDetail",
    # Auth types
    "User",
    "Tier",
    "Trial",
    "Subscription",
    "UserTeam",
    "UserTeamRole",
    "Session",
    "SessionListResponse",
    "SessionUserData",
    "ApiToken",
    "ApiTokenTeam",
    "AvailableTeam",
    "ApiTokenLimits",
    "ApiTokenListResponse",
    "ApiTokenCreateResponse",
    "AvailablePermissionsResponse",
    "ProfileUpdateResponse",
    "UpdateEmailResponse",
    "UpdateUsernameResponse",
    # Version
    "__version__",
]
