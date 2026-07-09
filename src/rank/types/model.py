from __future__ import annotations

from typing import Any, List, Optional

from .shared import PaginationInfo, RankModel, ReasoningEffort


class AIModel(RankModel):
    """An AI model available in the Rank platform.

    Field names match the PHP backend ``Model::toUserArray()`` (detail)
    and ``Model::toListArray()`` (listings).  Listing responses omit some
    fields (e.g. prices, tokens), which is why most are ``Optional``.
    """

    id: int
    model_name: str = ""
    model_alias: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    uploaded_at: Optional[str] = None
    reasoning: Optional[bool] = None
    agentic: Optional[bool] = None
    supports_effort: Optional[bool] = None
    effort_values: List[ReasoningEffort] = []
    default_effort: Optional[ReasoningEffort] = None
    supports_thinking_toggle: Optional[bool] = None
    max_input_tokens: Optional[int] = None
    max_output_tokens: Optional[int] = None
    context_size: Optional[int] = None
    support_files: Optional[bool] = None
    price_input: Optional[float] = None
    price_cached_input: Optional[float] = None
    price_cache_write: Optional[float] = None
    price_output: Optional[float] = None


class ModelListResponse(RankModel):
    """Response from ``GET /models`` and ``GET /models/mine``."""
    items: List[AIModel] = []
    pagination: Optional[PaginationInfo] = None


class ModelAssignResponse(RankModel):
    """Response from ``POST /models/assign``.

    When assigning via ``model_ids`` (batch), the API returns ``assigned``
    (list of IDs) and ``errors``.  When assigning via ``model_id`` (single),
    it returns ``model`` with the full model object instead.
    """

    message: str = ""
    assigned: Optional[List[int]] = None
    model: Optional[AIModel] = None
    errors: List[str] = []


__all__ = [
    "AIModel",
    "ModelListResponse",
    "ModelAssignResponse",
]
