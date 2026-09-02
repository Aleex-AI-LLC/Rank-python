from __future__ import annotations

from typing import Any, Dict, List, Optional

from .shared import PaginationInfo, RankModel


class EvidenceArtifact(RankModel):
    """A sealed (or purged) evidence artifact for a pentest run."""

    id: int
    vulnerability_id: Optional[int] = None
    kind: str = ""
    classification: str = ""
    status: str = ""
    sha256: str = ""
    size_bytes: int = 0
    mime_type: str = ""
    label: Optional[str] = None
    captured_at: Optional[str] = None
    captured_by: Optional[str] = None
    retention_until: Optional[str] = None
    sealed_at: Optional[str] = None


class EvidenceArtifactListResponse(RankModel):
    """Paginated sealed artifacts of a run."""

    items: List[EvidenceArtifact] = []
    pagination: Optional[PaginationInfo] = None
    pentest_id: Optional[int] = None


class EvidenceArtifactDetail(RankModel):
    """One artifact plus a signed URL or inline credential bytes."""

    artifact: Optional[EvidenceArtifact] = None
    url: Optional[str] = None
    content_base64: Optional[str] = None


class EvidenceManifest(RankModel):
    """Signed evidence manifest for a completed run."""

    pentest_id: Optional[int] = None
    merkle_root: Optional[str] = None
    signature: Optional[str] = None
    signature_alg: Optional[str] = None
    sealed_at: Optional[str] = None
    signature_valid: Optional[bool] = None
    chain_seq: Optional[int] = None
    chain_hash: Optional[str] = None
    artifact_count: Optional[int] = None
    artifacts: List[Dict[str, Any]] = []


class AuditChainResponse(RankModel):
    """Control-event trail for a pentest."""

    events: List[Dict[str, Any]] = []
    total: Optional[int] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
    intact: Optional[bool] = None


class AuditChainVerifyResponse(RankModel):
    """Integrity check of the hashed control-event chain."""

    intact: bool = False
    checked: Optional[int] = None
    broken_at: Optional[int] = None
    reason: Optional[str] = None


class FindingProvenance(RankModel):
    """Where a finding came from and whether its evidence digest still matches."""

    vulnerability_id: Optional[int] = None
    pentest_id: Optional[int] = None
    evidence_sha256: Optional[str] = None
    evidence_intact: Optional[bool] = None
    validation: Optional[Dict[str, Any]] = None
    origin: Optional[Dict[str, Any]] = None


class RetentionPolicy(RankModel):
    """How long evidence artifacts are kept for a user or team."""

    owner_type: str = ""
    owner_id: int = 0
    retention_days: int = 0
    credential_retention_days: Optional[int] = None
    is_default: bool = False
