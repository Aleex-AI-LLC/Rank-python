from __future__ import annotations

from typing import Any, Dict, List, Optional

from .shared import PaginationInfo, RankModel


class TicketComment(RankModel):
    """A comment on a Jira ticket."""

    id: Optional[int] = None
    body: Optional[str] = None
    author: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class TicketAttachment(RankModel):
    """An attachment on a Jira ticket (as shown in ticket detail)."""

    id: Optional[int] = None
    filename: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    created_at: Optional[str] = None


class JiraAttachment(RankModel):
    """Raw attachment object returned by the Jira REST API after upload.

    Field names match Jira's ``POST /rest/api/3/issue/{key}/attachments``
    response (camelCase).  Extra fields from Jira (``author``, etc.)
    are preserved thanks to ``extra="allow"`` on :class:`RankModel`.
    """

    id: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[int] = None
    mimeType: Optional[str] = None
    content: Optional[str] = None
    created: Optional[str] = None


class Ticket(RankModel):
    """A Jira ticket.

    The DB column is ``jira_issue_key`` (e.g. ``"RANK-15"``).
    Detail responses also include ``user_email``, ``username``,
    ``comments`` and ``attachments`` (fetched from Jira at query time).
    """

    id: int
    jira_issue_key: Optional[str] = None
    jira_issue_id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    issue_type: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None
    user_email: Optional[str] = None
    username: Optional[str] = None
    comments: List[TicketComment] = []
    attachments: List[TicketAttachment] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class TicketListResponse(RankModel):
    """Response from ``GET /tickets``."""

    items: List[Ticket] = []
    pagination: Optional[PaginationInfo] = None


class TicketAddAttachmentResponse(RankModel):
    """Response from ``POST /tickets/{id}/attachments``.

    Jira returns a raw JSON array of attachment objects.  The
    ``model_validate`` override wraps bare lists into
    ``{"attachments": [...]}``.
    """

    attachments: List[JiraAttachment] = []

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):  # type: ignore[override]
        if isinstance(obj, list):
            obj = {"attachments": obj}
        return super().model_validate(obj, *args, **kwargs)


class JiraComment(RankModel):
    """Raw comment object returned by the Jira REST API.

    Returned by ``POST /tickets/{id}/comments`` (add) and
    ``PUT /tickets/{id}/comments/{commentId}`` (update).
    Field names match Jira's REST API v3.
    """

    id: Optional[str] = None
    body: Optional[Any] = None
    created: Optional[str] = None
    updated: Optional[str] = None


class TicketCreateResponse(RankModel):
    """Response from ``POST /tickets``."""

    message: str = ""
    ticket: Optional[Ticket] = None


__all__ = [
    "TicketComment",
    "TicketAttachment",
    "JiraAttachment",
    "JiraComment",
    "Ticket",
    "TicketListResponse",
    "TicketAddAttachmentResponse",
    "TicketCreateResponse",
]
