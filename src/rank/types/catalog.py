from __future__ import annotations

from typing import List, Optional

from .shared import PaginationInfo, RankModel


class CweEntry(RankModel):
    """A CWE catalog entry."""

    cwe_id: str = ""
    name: str = ""
    abstraction: Optional[str] = None
    status: Optional[str] = None
    mapping_usage: Optional[str] = None
    url: Optional[str] = None
    cwe_version: Optional[str] = None
    description: Optional[str] = None
    extended_description: Optional[str] = None


class CweListResponse(RankModel):
    """Paginated CWE catalog list."""

    items: List[CweEntry] = []
    pagination: Optional[PaginationInfo] = None


class AttackTechnique(RankModel):
    """A MITRE ATT&CK technique catalog entry."""

    technique_id: str = ""
    name: str = ""
    is_subtechnique: Optional[bool] = None
    parent_technique_id: Optional[str] = None
    tactics: List[str] = []
    platforms: List[str] = []
    url: Optional[str] = None
    attack_version: Optional[str] = None
    description: Optional[str] = None


class AttackTechniqueListResponse(RankModel):
    """Paginated ATT&CK technique catalog list."""

    items: List[AttackTechnique] = []
    pagination: Optional[PaginationInfo] = None


class ApprovalClass(RankModel):
    """A RoE approval action class."""

    id: str = ""
    description: str = ""


class ApprovalClassListResponse(RankModel):
    """Fixed vocabulary of ``requires_approval_for``."""

    items: List[ApprovalClass] = []
    total: int = 0


class CatalogFieldOption(RankModel):
    """An allowed value for a report-profile enum field."""

    id: str = ""
    label: str = ""
    description: Optional[str] = None


class CatalogField(RankModel):
    """A report-profile field descriptor."""

    key: str = ""
    label: str = ""
    description: Optional[str] = None
    used_in: Optional[str] = None
    type: str = ""
    multiple: bool = False
    max_length: Optional[int] = None
    options: List[CatalogFieldOption] = []


class ReportProfileFieldsResponse(RankModel):
    """Response from ``GET /catalogs/report-profiles``."""

    fields: List[CatalogField] = []


class ValidationMetricsClass(RankModel):
    """False-positive metrics for one vulnerability class."""

    cwe_id: Optional[str] = None
    cwe_name: Optional[str] = None
    total: int = 0
    validated: int = 0
    failed: int = 0
    needs_manual_review: int = 0
    not_validatable: int = 0
    unvalidated: int = 0
    legacy: int = 0
    human_false_positive: int = 0
    automated_fp_rate: Optional[float] = None


class ValidationMetricsResponse(RankModel):
    """Response from ``GET /vulnerabilities/validation-metrics``."""

    by_class: List[ValidationMetricsClass] = []
    pentests_count: int = 0
