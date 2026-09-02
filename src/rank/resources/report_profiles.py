from __future__ import annotations

from typing import Any, Dict, List, Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.report import ReportProfile, ReportProfileResponse
from ._base import AsyncAPIResource, SyncAPIResource

_PROFILES = "/report-profiles"


def _profile_body(
    *,
    name: Union[str, _NotGiven],
    methodology: Union[str, _NotGiven],
    compliance_overlays: Union[List[str], _NotGiven],
    audience: Union[str, _NotGiven],
    default_formats: Union[List[str], _NotGiven],
    include_unvalidated_appendix: Union[bool, _NotGiven],
) -> Dict[str, Any]:
    return strip_not_given({
        "name": name,
        "methodology": methodology,
        "compliance_overlays": compliance_overlays,
        "audience": audience,
        "default_formats": default_formats,
        "include_unvalidated_appendix": include_unvalidated_appendix,
    })


class ReportProfiles(SyncAPIResource):
    """Caller's default report shape.

    Access via ``client.report_profiles``.
    """

    def retrieve(self) -> ReportProfileResponse:
        """Get the caller's profile, the system default, and field descriptors."""
        return self._client.get(_PROFILES, model=ReportProfileResponse)

    def update(
        self,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        methodology: Union[str, _NotGiven] = NOT_GIVEN,
        compliance_overlays: Union[List[str], _NotGiven] = NOT_GIVEN,
        audience: Union[str, _NotGiven] = NOT_GIVEN,
        default_formats: Union[List[str], _NotGiven] = NOT_GIVEN,
        include_unvalidated_appendix: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ReportProfile:
        """Create or replace the caller's default report profile."""
        return self._client.put(
            _PROFILES,
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


class AsyncReportProfiles(AsyncAPIResource):
    """Async variant of :class:`ReportProfiles`."""

    async def retrieve(self) -> ReportProfileResponse:
        return await self._client.get(_PROFILES, model=ReportProfileResponse)

    async def update(
        self,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        methodology: Union[str, _NotGiven] = NOT_GIVEN,
        compliance_overlays: Union[List[str], _NotGiven] = NOT_GIVEN,
        audience: Union[str, _NotGiven] = NOT_GIVEN,
        default_formats: Union[List[str], _NotGiven] = NOT_GIVEN,
        include_unvalidated_appendix: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ReportProfile:
        return await self._client.put(
            _PROFILES,
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
