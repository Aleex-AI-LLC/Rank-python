from __future__ import annotations

from typing import List, Optional

from .catalog import CatalogField
from .shared import RankModel


class ReportProfile(RankModel):
    """How a report is shaped: methodology, overlays, audience, formats."""

    id: int = 0
    owner_type: str = ""
    owner_id: int = 0
    name: str = ""
    methodology: str = ""
    compliance_overlays: List[str] = []
    audience: str = ""
    default_formats: List[str] = []
    include_unvalidated_appendix: bool = True
    is_default: bool = False


class ReportProfileResponse(RankModel):
    """Response from ``GET /report-profiles`` and the team equivalent."""

    profile: Optional[ReportProfile] = None
    system_default: Optional[ReportProfile] = None
    fields: List[CatalogField] = []


class ReportSettingsResponse(RankModel):
    """Response from ``GET /pentests/{id}/report-settings``."""

    effective: Optional[ReportProfile] = None
    fields: List[CatalogField] = []


class IssuedReport(RankModel):
    """A sealed issued-report file (PDF, HTML, Markdown, DOCX, or JSON)."""

    id: int
    pentest_id: Optional[int] = None
    issuance_group: Optional[str] = None
    report_profile_id: Optional[int] = None
    methodology: Optional[str] = None
    audience: Optional[str] = None
    language: Optional[str] = None
    recipient_email: Optional[str] = None
    format: str = ""
    payload_sha256: Optional[str] = None
    content_sha256: Optional[str] = None
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    status: Optional[str] = None
    signature: Optional[str] = None
    signature_alg: Optional[str] = None
    sealed_at: Optional[str] = None
    created_at: Optional[str] = None


class IssuedReportListResponse(RankModel):
    """Response from ``GET /pentests/{id}/reports``."""

    items: List[IssuedReport] = []


class IssuedReportDownload(RankModel):
    """Sealed report metadata plus a time-limited download URL."""

    report: Optional[IssuedReport] = None
    url: Optional[str] = None
