from __future__ import annotations

from typing import Any, Dict, List, Optional

from .shared import RankModel


class RetestSummary(RankModel):
    """Live result tallies for a retest run."""

    pending: int = 0
    fixed: int = 0
    still_vulnerable: int = 0
    inconclusive: int = 0
    skipped: int = 0


class RetestRun(RankModel):
    """A retest batch. Compact on list; full on retrieve (includes findings)."""

    id: int
    pentest_id: Optional[int] = None
    origin: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[str] = None
    due_at: Optional[str] = None
    claimed_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    retest_outside_window: Optional[bool] = None
    summary: Optional[Dict[str, int]] = None
    finding_count: Optional[int] = None
    findings: List[Dict[str, Any]] = []
    requested_by: Optional[int] = None
    created_at: Optional[str] = None


class RetestRunListResponse(RankModel):
    """Response from ``GET /pentests/{id}/retests``.

    The API returns a raw array under ``data``; the validator wraps it.
    """

    items: List[RetestRun] = []

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):  # type: ignore[override]
        if isinstance(obj, list):
            obj = {"items": obj}
        return super().model_validate(obj, *args, **kwargs)


class VulnerabilityReviewResponse(RankModel):
    """Response from ``POST .../vulnerabilities/{id}/review``."""

    message: Optional[str] = None
    vulnerability_id: Optional[int] = None
    previous_validation_status: Optional[str] = None
    validation_status: Optional[str] = None
    reviewed_by: Optional[int] = None
