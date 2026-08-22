from __future__ import annotations

from typing import Any, Dict, List, Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.integration import (
    IntegrationCreateResponse,
    IntegrationLinkListResponse,
    IntegrationListResponse,
    IntegrationProviderListResponse,
    IntegrationShowResponse,
    IntegrationSyncResult,
    IntegrationTestResponse,
)
from ..types.shared import MessageResponse
from ._base import AsyncAPIResource, SyncAPIResource

_INTEGRATIONS = "/integrations"


class Integrations(SyncAPIResource):
    """Outbound issue-tracker and chat integrations (Jira, GitHub, Slack).

    Access via ``client.integrations``.

    Create the integration **before** creating and launching pentests so
    ``vulnerability.created`` / ``vulnerability.validated`` events open tickets
    automatically. An integration created after findings already exist does not
    backfill them — use :meth:`sync` to push a pentest after the fact.
    """

    def providers(self) -> IntegrationProviderListResponse:
        """Describe what each provider needs to be configured."""
        return self._client.get(
            f"{_INTEGRATIONS}/providers",
            model=IntegrationProviderListResponse,
        )

    def list(self) -> IntegrationListResponse:
        """List integrations the caller manages (compact rows)."""
        return self._client.get(_INTEGRATIONS, model=IntegrationListResponse)

    def create(
        self,
        *,
        provider: str,
        name: str,
        credentials: Dict[str, Any],
        config: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        events: Union[List[str], _NotGiven] = NOT_GIVEN,
        field_mappings: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        base_url: Union[str, _NotGiven] = NOT_GIVEN,
        sync_inbound: Union[bool, _NotGiven] = NOT_GIVEN,
        team_id: Union[int, _NotGiven] = NOT_GIVEN,
        active: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> IntegrationCreateResponse:
        """Configure an integration for the caller or a team.

        Args:
            provider: ``jira``, ``github``, or ``slack``. Cannot be changed later.
            name: Display name.
            credentials: Provider credentials (encrypted at rest, never returned).
            config: Provider-specific settings (project key, repo, channel, …).
            events: Events that push automatically. Empty means manual :meth:`sync` only.
            field_mappings: Severity → priority map and escalation flags.
            base_url: Provider base URL (Jira Cloud/Server).
            sync_inbound: Enable the ticket-closed callback. Requires
                ``config.inbound_secret``.
            team_id: Own as this team; omit for personal.
            active: Whether the integration is on (default ``True``).
        """
        body: Dict[str, Any] = {
            "provider": provider,
            "name": name,
            "credentials": credentials,
        }
        body.update(strip_not_given({
            "config": config,
            "events": events,
            "field_mappings": field_mappings,
            "base_url": base_url,
            "sync_inbound": sync_inbound,
            "team_id": team_id,
            "active": active,
        }))
        return self._client.post(
            _INTEGRATIONS, body=body, model=IntegrationCreateResponse,
        )

    def retrieve(self, integration_id: int) -> IntegrationShowResponse:
        """Get one integration, including config, mappings and recent deliveries."""
        return self._client.get(
            f"{_INTEGRATIONS}/{integration_id}",
            model=IntegrationShowResponse,
        )

    def update(
        self,
        integration_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        credentials: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        config: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        events: Union[List[str], _NotGiven] = NOT_GIVEN,
        field_mappings: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        base_url: Union[str, _NotGiven] = NOT_GIVEN,
        sync_inbound: Union[bool, _NotGiven] = NOT_GIVEN,
        active: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> IntegrationShowResponse:
        """Edit destination, credentials, mapping or inbound settings.

        Sending ``config`` **replaces** the object. Resend ``********`` to keep
        a masked secret.
        """
        body = strip_not_given({
            "name": name,
            "credentials": credentials,
            "config": config,
            "events": events,
            "field_mappings": field_mappings,
            "base_url": base_url,
            "sync_inbound": sync_inbound,
            "active": active,
        })
        return self._client.put(
            f"{_INTEGRATIONS}/{integration_id}",
            body=body,
            model=IntegrationShowResponse,
        )

    def delete(
        self,
        integration_id: int,
        *,
        discard_pending_retests: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> MessageResponse:
        """Delete the integration. External tickets are left in place.

        Refused if links are ``closed_pending_retest`` unless
        ``discard_pending_retests=True``.
        """
        params = strip_not_given({
            "discard_pending_retests": (
                True if discard_pending_retests is True else NOT_GIVEN
            ),
        })
        return self._client.delete(
            f"{_INTEGRATIONS}/{integration_id}",
            params=params or None,
            model=MessageResponse,
        )

    def test(self, integration_id: int) -> IntegrationTestResponse:
        """Prove credentials and configuration work. Does not create a ticket."""
        return self._client.post(
            f"{_INTEGRATIONS}/{integration_id}/test",
            model=IntegrationTestResponse,
        )

    def sync(
        self,
        integration_id: int,
        *,
        pentest_id: int,
        vulnerability_ids: Union[List[int], _NotGiven] = NOT_GIVEN,
    ) -> IntegrationSyncResult:
        """Push findings of a pentest to the provider.

        Skips findings this integration already filed unless *vulnerability_ids*
        is set. Caps at 100 findings / ~60 seconds per call.
        """
        body: Dict[str, Any] = {"pentest_id": pentest_id}
        body.update(strip_not_given({"vulnerability_ids": vulnerability_ids}))
        return self._client.post(
            f"{_INTEGRATIONS}/{integration_id}/sync",
            body=body,
            model=IntegrationSyncResult,
        )

    def links(
        self,
        integration_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> IntegrationLinkListResponse:
        """Which finding became which ticket, plus inbound failures."""
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"{_INTEGRATIONS}/{integration_id}/links",
            params=params or None,
            model=IntegrationLinkListResponse,
        )


class AsyncIntegrations(AsyncAPIResource):
    """Async variant of :class:`Integrations`."""

    async def providers(self) -> IntegrationProviderListResponse:
        return await self._client.get(
            f"{_INTEGRATIONS}/providers",
            model=IntegrationProviderListResponse,
        )

    async def list(self) -> IntegrationListResponse:
        return await self._client.get(_INTEGRATIONS, model=IntegrationListResponse)

    async def create(
        self,
        *,
        provider: str,
        name: str,
        credentials: Dict[str, Any],
        config: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        events: Union[List[str], _NotGiven] = NOT_GIVEN,
        field_mappings: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        base_url: Union[str, _NotGiven] = NOT_GIVEN,
        sync_inbound: Union[bool, _NotGiven] = NOT_GIVEN,
        team_id: Union[int, _NotGiven] = NOT_GIVEN,
        active: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> IntegrationCreateResponse:
        body: Dict[str, Any] = {
            "provider": provider,
            "name": name,
            "credentials": credentials,
        }
        body.update(strip_not_given({
            "config": config,
            "events": events,
            "field_mappings": field_mappings,
            "base_url": base_url,
            "sync_inbound": sync_inbound,
            "team_id": team_id,
            "active": active,
        }))
        return await self._client.post(
            _INTEGRATIONS, body=body, model=IntegrationCreateResponse,
        )

    async def retrieve(self, integration_id: int) -> IntegrationShowResponse:
        return await self._client.get(
            f"{_INTEGRATIONS}/{integration_id}",
            model=IntegrationShowResponse,
        )

    async def update(
        self,
        integration_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        credentials: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        config: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        events: Union[List[str], _NotGiven] = NOT_GIVEN,
        field_mappings: Union[Dict[str, Any], _NotGiven] = NOT_GIVEN,
        base_url: Union[str, _NotGiven] = NOT_GIVEN,
        sync_inbound: Union[bool, _NotGiven] = NOT_GIVEN,
        active: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> IntegrationShowResponse:
        body = strip_not_given({
            "name": name,
            "credentials": credentials,
            "config": config,
            "events": events,
            "field_mappings": field_mappings,
            "base_url": base_url,
            "sync_inbound": sync_inbound,
            "active": active,
        })
        return await self._client.put(
            f"{_INTEGRATIONS}/{integration_id}",
            body=body,
            model=IntegrationShowResponse,
        )

    async def delete(
        self,
        integration_id: int,
        *,
        discard_pending_retests: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> MessageResponse:
        params = strip_not_given({
            "discard_pending_retests": (
                True if discard_pending_retests is True else NOT_GIVEN
            ),
        })
        return await self._client.delete(
            f"{_INTEGRATIONS}/{integration_id}",
            params=params or None,
            model=MessageResponse,
        )

    async def test(self, integration_id: int) -> IntegrationTestResponse:
        return await self._client.post(
            f"{_INTEGRATIONS}/{integration_id}/test",
            model=IntegrationTestResponse,
        )

    async def sync(
        self,
        integration_id: int,
        *,
        pentest_id: int,
        vulnerability_ids: Union[List[int], _NotGiven] = NOT_GIVEN,
    ) -> IntegrationSyncResult:
        body: Dict[str, Any] = {"pentest_id": pentest_id}
        body.update(strip_not_given({"vulnerability_ids": vulnerability_ids}))
        return await self._client.post(
            f"{_INTEGRATIONS}/{integration_id}/sync",
            body=body,
            model=IntegrationSyncResult,
        )

    async def links(
        self,
        integration_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> IntegrationLinkListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"{_INTEGRATIONS}/{integration_id}/links",
            params=params or None,
            model=IntegrationLinkListResponse,
        )
