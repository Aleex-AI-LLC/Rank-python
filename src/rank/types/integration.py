from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import model_validator

from .shared import PaginationInfo, RankModel


class IntegrationProvider(RankModel):
    """What a provider needs to be configured."""

    provider: str = ""
    label: Optional[str] = None
    auth_type: Optional[str] = None
    credential_fields: List[Dict[str, Any]] = []
    required_config: List[Any] = []
    optional_config: List[Any] = []
    secret_config: List[Any] = []
    handled_event_subjects: List[str] = []
    default_base_url: Optional[str] = None
    tracks_issue_state: Optional[bool] = None
    supports_inbound: Optional[bool] = None
    notes: Optional[str] = None
    allowed_host_suffixes: List[str] = []
    host_allowlist_opt_in: Optional[bool] = None


class IntegrationProviderListResponse(RankModel):
    """Response from ``GET /integrations/providers``."""

    providers: List[IntegrationProvider] = []


class Integration(RankModel):
    """An outbound connection to Jira, GitHub Issues, or Slack."""

    id: int
    provider: str = ""
    name: Optional[str] = None
    owner_type: Optional[str] = None
    owner_id: Optional[int] = None
    team_id: Optional[int] = None
    active: Optional[bool] = None
    sync_inbound: Optional[bool] = None
    events: List[str] = []
    base_url: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    field_mappings: Optional[Dict[str, Any]] = None
    callback_url: Optional[str] = None
    has_credentials: Optional[bool] = None
    has_inbound_secret: Optional[bool] = None
    last_error: Optional[str] = None
    last_synced_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    recent_deliveries: List[Dict[str, Any]] = []


class IntegrationListResponse(RankModel):
    """Compact list from ``GET /integrations``."""

    integrations: List[Integration] = []
    total: int = 0


class IntegrationCreateResponse(RankModel):
    """Response from ``POST /integrations``."""

    message: str = ""
    integration: Optional[Integration] = None
    credentials_notice: Optional[str] = None


class IntegrationShowResponse(RankModel):
    """Response from ``GET /integrations/{id}``."""

    integration: Optional[Integration] = None
    recent_deliveries: List[Dict[str, Any]] = []


class IntegrationSyncResult(RankModel):
    """Response from ``POST /integrations/{id}/sync``."""

    message: Optional[str] = None
    summary: Optional[Dict[str, Any]] = None
    results: List[Dict[str, Any]] = []


class IntegrationTestResponse(RankModel):
    """Response from ``POST /integrations/{id}/test``.

    PHP wraps :class:`ConnectorResult` under ``test``. The validator unwraps
    that envelope so ``ok`` / ``error`` sit on this object.
    """

    ok: Optional[bool] = None
    skipped: Optional[bool] = None
    error: Optional[str] = None
    note: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    external_key: Optional[str] = None
    external_url: Optional[str] = None
    external_status: Optional[str] = None
    status_code: Optional[int] = None
    retry_after_seconds: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def _unwrap_test(cls, data: Any) -> Any:
        if isinstance(data, dict) and isinstance(data.get("test"), dict):
            return data["test"]
        return data


class IntegrationLink(RankModel):
    """Which finding became which external ticket."""

    id: Optional[int] = None
    vulnerability_id: Optional[int] = None
    external_id: Optional[str] = None
    external_url: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None


class IntegrationLinkListResponse(RankModel):
    """Paginated finding↔ticket links, plus recent inbound failures."""

    items: List[Dict[str, Any]] = []
    pagination: Optional[PaginationInfo] = None
    inbound_failures: List[Dict[str, Any]] = []
