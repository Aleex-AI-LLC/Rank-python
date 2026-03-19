from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict


class RankModel(BaseModel):
    """Base model for all Rank API response types.

    Configured with:
    - Extra fields allowed (forward-compatible with new API fields).
    - Population by field name (snake_case).
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )


T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Pagination metadata included in list responses."""

    current_page: int = 1
    per_page: int = 20
    total: int = 0
    last_page: int = 1


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response shape from the Rank API."""

    data: List[T] = []  # type: ignore[assignment]
    meta: Optional[PaginationMeta] = None


class Permission(RankModel):
    """API permission object used across auth, teams, and roles."""

    id: int
    name: str = ""
    method: str = ""
    tag: str = ""
    description: Optional[str] = None


class PaginationInfo(RankModel):
    """Pagination metadata returned by the PHP ResponseHelper.

    This differs from PaginationMeta (Laravel-style) in field names:
    uses ``total_pages`` instead of ``last_page`` and includes ``count``.
    """

    total: int = 0
    count: int = 0
    per_page: int = 20
    current_page: int = 1
    total_pages: int = 1


class MessageResponse(RankModel):
    """Generic response containing only a message."""

    message: str = ""


class SuccessResponse(RankModel):
    """Generic success response with status and message."""

    status: str = "success"
    message: str = ""


class ErrorDetail(BaseModel):
    """Structured error detail from the API."""

    field: Optional[str] = None
    message: str = ""
    code: Optional[str] = None
