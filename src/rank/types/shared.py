from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, TypeVar, Union, get_origin

from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import Literal

try:
    from types import UnionType
except ImportError:  # Python 3.8 / 3.9
    UnionType = None  # type: ignore[misc, assignment]

ReasoningEffort = Literal["none", "minimal", "low", "medium", "high", "xhigh", "max"]
"""Canonical reasoning-effort scale accepted by the API, ordered by ascending intensity."""

_SKIP = object()


def _is_union(origin: Any) -> bool:
    if origin is Union:
        return True
    return UnionType is not None and origin is UnionType


def _empty_for_null_collection(annotation: Any) -> Any:
    """JSON ``null`` → ``[]`` / ``{}`` for required collection fields.

    ``Optional[List[...]]`` keeps ``None``: the annotation already opted into
    a missing collection. Bare ``List`` / ``Dict`` fields default to empty.
    """
    origin = get_origin(annotation)
    if _is_union(origin):
        return _SKIP
    if origin in (list, List):
        return []
    if origin in (dict, Dict):
        return {}
    return _SKIP


class RankModel(BaseModel):
    """Base model for all Rank API response types.

    Configured with:
    - Extra fields allowed (forward-compatible with new API fields).
    - Population by field name (snake_case).
    - JSON ``null`` coerced to ``[]`` / ``{}`` on required list and dict fields
      (PHP ``json_decode`` of an empty JSON/JSONB column).
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )

    @model_validator(mode="before")
    @classmethod
    def _coerce_null_collections(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        coerced = None
        for name, field in cls.model_fields.items():
            if name not in data or data[name] is not None:
                continue
            empty = _empty_for_null_collection(field.annotation)
            if empty is _SKIP:
                continue
            if coerced is None:
                coerced = dict(data)
            coerced[name] = empty
        return data if coerced is None else coerced


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
    """API permission object used across auth, teams, and roles.

    The PHP ``Permission::toArray()`` returns ``id``, ``name``, ``method``,
    ``tag``, and ``protected``.  It does **not** return ``description``.
    """

    id: int
    name: str = ""
    method: str = ""
    tag: str = ""
    protected: Optional[bool] = None


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


class PermissionListResponse(RankModel):
    """Response from ``GET /permissions``."""

    items: List[Permission] = []
    pagination: Optional[PaginationInfo] = None
