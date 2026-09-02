from __future__ import annotations

from typing import List, Optional

from .shared import PaginationInfo, RankModel


class OperationModelInfo(RankModel):
    """Nested model info in an operation detail response."""

    id: Optional[int] = None
    name: Optional[str] = None


class OperationAgentInfo(RankModel):
    """Nested agent info in an operation detail response."""

    id: Optional[int] = None
    name: Optional[str] = None


class OperationPentestInfo(RankModel):
    """Nested pentest info in an operation detail response."""

    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    target: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    total_tokens: Optional[int] = None
    duration: Optional[str] = None


class OperationLog(RankModel):
    """An operation log entry (chat or pentest interaction).

    The API uses two different formats:

    **List** (``GET /operations``, ``formatSummary``):
    ``id``, ``input``, ``output``, ``model_id``, ``model_name``,
    ``estado``, ``created_at``, ``operation_type``, ``pentest_id``, ``type``.

    **Detail** (``GET /operations/{id}``, ``formatDetail``):
    ``id``, ``user_id``, ``user_prompt``, ``alex_response``, ``estado``,
    ``created_at``, ``time_took``, ``total_tokens``, ``input_tokens``,
    ``output_tokens``, ``operation_type``, ``model``, ``agent``, ``pentest``.

    This model covers both; fields only present in one format will
    be ``None`` when parsed from the other.
    """

    id: int

    # -- Common ----------------------------------------------------------------
    operation_type: Optional[str] = None
    estado: Optional[str] = None
    created_at: Optional[str] = None

    # -- List-specific (formatSummary) -----------------------------------------
    type: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    model_id: Optional[int] = None
    model_name: Optional[str] = None
    pentest_id: Optional[int] = None

    # -- Detail-specific (formatDetail) ----------------------------------------
    user_id: Optional[int] = None
    user_prompt: Optional[str] = None
    alex_response: Optional[str] = None
    time_took: Optional[str] = None
    total_tokens: Optional[int] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    model: Optional[OperationModelInfo] = None
    agent: Optional[OperationAgentInfo] = None
    pentest: Optional[OperationPentestInfo] = None


class OperationLogListResponse(RankModel):
    """Response from ``GET /operations``."""

    items: List[OperationLog] = []
    pagination: Optional[PaginationInfo] = None


__all__ = [
    "OperationModelInfo",
    "OperationAgentInfo",
    "OperationPentestInfo",
    "OperationLog",
    "OperationLogListResponse",
]
