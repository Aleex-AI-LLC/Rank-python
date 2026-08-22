from __future__ import annotations

from typing import Any, List, Optional

from pydantic import model_validator

from .shared import PaginationInfo, RankModel

# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


class Chat(RankModel):
    """Chat object returned by show, create, and update.

    The backend uses ``nombre`` for the chat name and ``archived`` for the
    archive flag.  A pre-validator syncs convenience aliases (``owner_id``
    from ``user_id``, ``is_archived`` from ``archived``) so both forms work.
    """

    id: int
    nombre: Optional[str] = None
    user_id: Optional[int] = None
    owner_username: Optional[str] = None
    archived: Optional[bool] = None
    total_operations: Optional[int] = None
    shared_teams: List[Any] = []
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    # Convenience aliases populated by the validator
    owner_id: Optional[int] = None
    is_archived: Optional[bool] = None
    name: Optional[str] = None
    is_team_chat: Optional[bool] = None
    team_id: Optional[int] = None
    archived_at: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _sync_aliases(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if data.get("owner_id") is None and data.get("user_id") is not None:
            data["owner_id"] = data["user_id"]
        if data.get("is_archived") is None and data.get("archived") is not None:
            data["is_archived"] = data["archived"]
        if data.get("name") is None and data.get("nombre") is not None:
            data["name"] = data["nombre"]
        return data


class ChatListResponse(RankModel):
    """Response from ``GET /chats`` (all chats: own + shared).

    The structure may vary: it can be a flat paginated list or a grouped
    response with ``own_chats`` and ``shared_chats`` sections.
    """

    own_chats: List[Chat] = []
    shared_chats: List[Chat] = []
    totals: Optional[Any] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


class ChatMineResponse(RankModel):
    """Paginated list of the user's own chats."""

    items: List[Chat] = []
    pagination: Optional[PaginationInfo] = None


class ChatSharedResponse(RankModel):
    """Paginated list of chats shared with the user's teams."""

    items: List[Chat] = []
    pagination: Optional[PaginationInfo] = None


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------


class ChatOperation(RankModel):
    """An operation (message exchange) within a chat.

    The backend returns ``prompt`` / ``answer`` and ``operation_id``.
    A pre-validator maps them to the friendlier ``user_prompt`` /
    ``ai_response`` / ``id`` aliases.
    """

    relation_id: Optional[int] = None
    chat_id: Optional[int] = None
    operation_id: Optional[int] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
    prompt: Optional[str] = None
    answer: Optional[str] = None
    deleted: Optional[int] = None
    created_at: Optional[str] = None
    # Convenience aliases
    id: Optional[int] = None
    user_prompt: Optional[str] = None
    ai_response: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _sync_aliases(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if data.get("id") is None and data.get("operation_id") is not None:
            data["id"] = data["operation_id"]
        if data.get("user_prompt") is None and data.get("prompt") is not None:
            data["user_prompt"] = data["prompt"]
        if data.get("ai_response") is None and data.get("answer") is not None:
            data["ai_response"] = data["answer"]
        return data


class ChatOperationListResponse(RankModel):
    """Paginated list of chat operations."""

    items: List[ChatOperation] = []
    pagination: Optional[PaginationInfo] = None


class AssignOperationsResponse(RankModel):
    """Response from ``POST /chats/{id}/operations``."""

    message: str = ""
    chat_id: Optional[int] = None
    assigned_operations: List[int] = []
    total_operations: Optional[int] = None


# ---------------------------------------------------------------------------
# Vulnerabilities
# ---------------------------------------------------------------------------


class ChatVulnerability(RankModel):
    """A vulnerability linked to a chat (``chat_has_vulns`` join).

    PHP returns ``vulnerability`` as the finding title and
    ``vulnerability_id`` as the pentest finding id.  Aliases ``title`` /
    ``id`` are filled in so both forms work.
    """

    relation_id: Optional[int] = None
    chat_id: Optional[int] = None
    vulnerability_id: Optional[int] = None
    vulnerability: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    resolution: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    created_at: Optional[str] = None
    # Convenience aliases
    id: Optional[int] = None
    title: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _sync_aliases(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if data.get("id") is None and data.get("vulnerability_id") is not None:
            data["id"] = data["vulnerability_id"]
        if data.get("title") is None and data.get("vulnerability") is not None:
            data["title"] = data["vulnerability"]
        return data


class ChatVulnerabilityListResponse(RankModel):
    """Paginated list from ``GET /chats/{id}/vulnerabilities``."""

    items: List[ChatVulnerability] = []
    pagination: Optional[PaginationInfo] = None


class AssignVulnerabilitiesResponse(RankModel):
    """Response from ``POST /chats/{id}/vulnerabilities``."""

    message: str = ""
    chat_id: Optional[int] = None
    assigned_vulnerabilities: List[int] = []
    total_vulnerabilities: Optional[int] = None


class RemoveVulnerabilityResponse(RankModel):
    """Response from ``DELETE /chats/{id}/vulnerabilities/{vulnId}``.

    Only the chat link is removed; the pentest finding is preserved.
    """

    message: str = ""
    chat_id: Optional[int] = None
    vulnerability_id: Optional[int] = None


# ---------------------------------------------------------------------------
# Share
# ---------------------------------------------------------------------------


class ChatShareResponse(RankModel):
    """Response from ``POST /chats/{id}/share``."""

    message: str = ""
    shared_teams: List[Any] = []


class ChatUnshareResponse(RankModel):
    """Response from ``DELETE /chats/{id}/share``."""

    message: str = ""


# ---------------------------------------------------------------------------
# Archive
# ---------------------------------------------------------------------------


class ChatArchiveResponse(RankModel):
    """Response from ``PATCH /chats/{id}/archive`` and ``unarchive``."""

    message: str = ""


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------

__all__ = [
    # Chat
    "Chat",
    "ChatListResponse",
    "ChatMineResponse",
    "ChatSharedResponse",
    # Operations
    "ChatOperation",
    "ChatOperationListResponse",
    "AssignOperationsResponse",
    # Vulnerabilities
    "ChatVulnerability",
    "ChatVulnerabilityListResponse",
    "AssignVulnerabilitiesResponse",
    "RemoveVulnerabilityResponse",
    # Share
    "ChatShareResponse",
    "ChatUnshareResponse",
    # Archive
    "ChatArchiveResponse",
]
