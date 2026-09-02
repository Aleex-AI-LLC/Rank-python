from __future__ import annotations

from typing import List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven
from ...types.report import ReportProfile, ReportProfileResponse
from .._base import AsyncAPIResource, SyncAPIResource
from ..report_profiles import _profile_body


class TeamReportProfiles(SyncAPIResource):
    """Team default report shape. Access via ``client.teams.report_profiles``."""

    def retrieve(self, team_id: int) -> ReportProfileResponse:
        return self._client.get(
            f"/teams/{team_id}/report-profiles",
            model=ReportProfileResponse,
        )

    def update(
        self,
        team_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        methodology: Union[str, _NotGiven] = NOT_GIVEN,
        compliance_overlays: Union[List[str], _NotGiven] = NOT_GIVEN,
        audience: Union[str, _NotGiven] = NOT_GIVEN,
        default_formats: Union[List[str], _NotGiven] = NOT_GIVEN,
        include_unvalidated_appendix: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ReportProfile:
        """Replace the team default. Only the team owner can write."""
        return self._client.put(
            f"/teams/{team_id}/report-profiles",
            body=_profile_body(
                name=name,
                methodology=methodology,
                compliance_overlays=compliance_overlays,
                audience=audience,
                default_formats=default_formats,
                include_unvalidated_appendix=include_unvalidated_appendix,
            ),
            model=ReportProfile,
        )


class AsyncTeamReportProfiles(AsyncAPIResource):
    """Async variant of :class:`TeamReportProfiles`."""

    async def retrieve(self, team_id: int) -> ReportProfileResponse:
        return await self._client.get(
            f"/teams/{team_id}/report-profiles",
            model=ReportProfileResponse,
        )

    async def update(
        self,
        team_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        methodology: Union[str, _NotGiven] = NOT_GIVEN,
        compliance_overlays: Union[List[str], _NotGiven] = NOT_GIVEN,
        audience: Union[str, _NotGiven] = NOT_GIVEN,
        default_formats: Union[List[str], _NotGiven] = NOT_GIVEN,
        include_unvalidated_appendix: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ReportProfile:
        return await self._client.put(
            f"/teams/{team_id}/report-profiles",
            body=_profile_body(
                name=name,
                methodology=methodology,
                compliance_overlays=compliance_overlays,
                audience=audience,
                default_formats=default_formats,
                include_unvalidated_appendix=include_unvalidated_appendix,
            ),
            model=ReportProfile,
        )
