from __future__ import annotations

from typing import Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.evidence import RetentionPolicy
from ._base import AsyncAPIResource, SyncAPIResource

_RETENTION = "/evidence/retention-policy"


class EvidenceRetention(SyncAPIResource):
    """Tenant-wide evidence retention.

    Access via ``client.evidence``. Artifact listing lives under
    ``client.pentests.evidence``.
    """

    def get_retention_policy(
        self,
        *,
        team_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> RetentionPolicy:
        """Get how long evidence is kept.

        Args:
            team_id: Team policy. Omit for the caller's personal policy.
        """
        params = strip_not_given({"team_id": team_id})
        return self._client.get(
            _RETENTION, params=params or None, model=RetentionPolicy,
        )

    def set_retention_policy(
        self,
        *,
        retention_days: int,
        credential_retention_days: Union[int, _NotGiven] = NOT_GIVEN,
        team_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> RetentionPolicy:
        """Set how long evidence is kept.

        ``credential_retention_days`` cannot exceed ``retention_days``.
        """
        body = strip_not_given({
            "retention_days": retention_days,
            "credential_retention_days": credential_retention_days,
        })
        params = strip_not_given({"team_id": team_id})
        return self._client.put(
            _RETENTION,
            body=body,
            params=params or None,
            model=RetentionPolicy,
        )


class AsyncEvidenceRetention(AsyncAPIResource):
    """Async variant of :class:`EvidenceRetention`."""

    async def get_retention_policy(
        self,
        *,
        team_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> RetentionPolicy:
        params = strip_not_given({"team_id": team_id})
        return await self._client.get(
            _RETENTION, params=params or None, model=RetentionPolicy,
        )

    async def set_retention_policy(
        self,
        *,
        retention_days: int,
        credential_retention_days: Union[int, _NotGiven] = NOT_GIVEN,
        team_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> RetentionPolicy:
        body = strip_not_given({
            "retention_days": retention_days,
            "credential_retention_days": credential_retention_days,
        })
        params = strip_not_given({"team_id": team_id})
        return await self._client.put(
            _RETENTION,
            body=body,
            params=params or None,
            model=RetentionPolicy,
        )
