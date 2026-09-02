from __future__ import annotations

from typing import Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.catalog import (
    ApprovalClassListResponse,
    AttackTechnique,
    AttackTechniqueListResponse,
    CweEntry,
    CweListResponse,
    ReportProfileFieldsResponse,
)
from ._base import AsyncAPIResource, SyncAPIResource

_CATALOGS = "/catalogs"


class Catalogs(SyncAPIResource):
    """Security taxonomy catalogs.

    Access via ``client.catalogs``.
    """

    def list_cwe(
        self,
        *,
        q: Union[str, _NotGiven] = NOT_GIVEN,
        mapping: Union[str, _NotGiven] = NOT_GIVEN,
        detail: Union[str, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> CweListResponse:
        """List CWE weaknesses.

        Args:
            q: Case-insensitive match on ``cwe_id`` or name.
            mapping: Pass ``"allowed"`` to restrict to weaknesses a finding
                may be mapped to.
            detail: Pass ``"full"`` to include description columns.
            page: Page number.
            per_page: Items per page (default 20, max 100).
        """
        params = strip_not_given({
            "q": q, "mapping": mapping, "detail": detail,
            "page": page, "per_page": per_page,
        })
        return self._client.get(
            f"{_CATALOGS}/cwe", params=params or None, model=CweListResponse,
        )

    def retrieve_cwe(self, cwe_id: str) -> CweEntry:
        """Get one CWE weakness (e.g. ``CWE-89``)."""
        return self._client.get(f"{_CATALOGS}/cwe/{cwe_id}", model=CweEntry)

    def list_attack_techniques(
        self,
        *,
        tactic: Union[str, _NotGiven] = NOT_GIVEN,
        detail: Union[str, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> AttackTechniqueListResponse:
        """List MITRE ATT&CK techniques.

        Args:
            tactic: Exact tactic name, e.g. ``"Initial Access"``.
            detail: Pass ``"full"`` to include the description column.
            page: Page number.
            per_page: Items per page (default 20, max 100).
        """
        params = strip_not_given({
            "tactic": tactic, "detail": detail,
            "page": page, "per_page": per_page,
        })
        return self._client.get(
            f"{_CATALOGS}/attack-techniques",
            params=params or None,
            model=AttackTechniqueListResponse,
        )

    def retrieve_attack_technique(self, technique_id: str) -> AttackTechnique:
        """Get one ATT&CK technique (e.g. ``T1190`` or ``T1190.001``)."""
        return self._client.get(
            f"{_CATALOGS}/attack-techniques/{technique_id}",
            model=AttackTechnique,
        )

    def list_approval_classes(self) -> ApprovalClassListResponse:
        """List the fixed vocabulary of ``requires_approval_for``."""
        return self._client.get(
            f"{_CATALOGS}/approval-classes",
            model=ApprovalClassListResponse,
        )

    def list_report_profile_fields(self) -> ReportProfileFieldsResponse:
        """List report-profile fields and the values the API will store."""
        return self._client.get(
            f"{_CATALOGS}/report-profiles",
            model=ReportProfileFieldsResponse,
        )


class AsyncCatalogs(AsyncAPIResource):
    """Async variant of :class:`Catalogs`."""

    async def list_cwe(
        self,
        *,
        q: Union[str, _NotGiven] = NOT_GIVEN,
        mapping: Union[str, _NotGiven] = NOT_GIVEN,
        detail: Union[str, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> CweListResponse:
        params = strip_not_given({
            "q": q, "mapping": mapping, "detail": detail,
            "page": page, "per_page": per_page,
        })
        return await self._client.get(
            f"{_CATALOGS}/cwe", params=params or None, model=CweListResponse,
        )

    async def retrieve_cwe(self, cwe_id: str) -> CweEntry:
        return await self._client.get(f"{_CATALOGS}/cwe/{cwe_id}", model=CweEntry)

    async def list_attack_techniques(
        self,
        *,
        tactic: Union[str, _NotGiven] = NOT_GIVEN,
        detail: Union[str, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> AttackTechniqueListResponse:
        params = strip_not_given({
            "tactic": tactic, "detail": detail,
            "page": page, "per_page": per_page,
        })
        return await self._client.get(
            f"{_CATALOGS}/attack-techniques",
            params=params or None,
            model=AttackTechniqueListResponse,
        )

    async def retrieve_attack_technique(self, technique_id: str) -> AttackTechnique:
        return await self._client.get(
            f"{_CATALOGS}/attack-techniques/{technique_id}",
            model=AttackTechnique,
        )

    async def list_approval_classes(self) -> ApprovalClassListResponse:
        return await self._client.get(
            f"{_CATALOGS}/approval-classes",
            model=ApprovalClassListResponse,
        )

    async def list_report_profile_fields(self) -> ReportProfileFieldsResponse:
        return await self._client.get(
            f"{_CATALOGS}/report-profiles",
            model=ReportProfileFieldsResponse,
        )
