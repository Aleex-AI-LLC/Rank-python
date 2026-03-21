from __future__ import annotations

from typing import Any, Dict, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.shared import MessageResponse
from ...types.team import InvitationCreateResponse, InvitationListResponse
from .._base import AsyncAPIResource, SyncAPIResource


# ---------------------------------------------------------------------------
# Invitations (sync)
# ---------------------------------------------------------------------------


class Invitations(SyncAPIResource):
    """Manage invitations for a team.

    Access via ``client.teams.invitations``.

    Example::

        # Invite a user
        resp = client.teams.invitations.create(
            team_id=1, email="user@example.com", role_id=3,
        )
        print(f"Invitation {resp.invitation_id} expires at {resp.expires_at}")

        # List pending invitations
        inv_list = client.teams.invitations.list(team_id=1, status="pending")
    """

    def list(
        self,
        team_id: int,
        *,
        status: Union[str, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> InvitationListResponse:
        """List invitations for a team.

        Args:
            team_id: ID of the team.
            status: Filter by status (``"pending"``, ``"accepted"``,
                ``"rejected"``, ``"expired"``, ``"cancelled"``).
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({
            "status": status,
            "page": page,
            "per_page": per_page,
        })
        return self._client.get(
            f"/teams/{team_id}/invitations",
            params=params or None,
            model=InvitationListResponse,
        )

    def create(
        self,
        team_id: int,
        *,
        email: str,
        role_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> InvitationCreateResponse:
        """Invite a user to join a team by email.

        The user must not already be a member and must not have a pending
        invitation for this team.

        Args:
            team_id: ID of the team.
            email: Email address of the person to invite.
            role_id: Optional role ID to assign on acceptance
                (cannot be the Administrator role).
        """
        body: Dict[str, Any] = {"email": email}
        body.update(strip_not_given({"role_id": role_id}))
        return self._client.post(
            f"/teams/{team_id}/invitations",
            body=body,
            model=InvitationCreateResponse,
        )

    def resend(self, team_id: int, invitation_id: int) -> InvitationCreateResponse:
        """Resend a pending invitation.

        The invitation must still be in ``pending`` status.

        Args:
            team_id: ID of the team.
            invitation_id: ID of the invitation to resend.
        """
        return self._client.post(
            f"/teams/{team_id}/invitations/{invitation_id}/resend",
            model=InvitationCreateResponse,
        )

    def cancel(self, team_id: int, invitation_id: int) -> MessageResponse:
        """Cancel a pending invitation.

        Args:
            team_id: ID of the team.
            invitation_id: ID of the invitation to cancel.
        """
        return self._client.delete(
            f"/teams/{team_id}/invitations/{invitation_id}",
            model=MessageResponse,
        )


# ---------------------------------------------------------------------------
# Invitations (async)
# ---------------------------------------------------------------------------


class AsyncInvitations(AsyncAPIResource):
    """Async variant of :class:`Invitations`."""

    async def list(
        self,
        team_id: int,
        *,
        status: Union[str, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> InvitationListResponse:
        params = strip_not_given({
            "status": status,
            "page": page,
            "per_page": per_page,
        })
        return await self._client.get(
            f"/teams/{team_id}/invitations",
            params=params or None,
            model=InvitationListResponse,
        )

    async def create(
        self,
        team_id: int,
        *,
        email: str,
        role_id: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> InvitationCreateResponse:
        body: Dict[str, Any] = {"email": email}
        body.update(strip_not_given({"role_id": role_id}))
        return await self._client.post(
            f"/teams/{team_id}/invitations",
            body=body,
            model=InvitationCreateResponse,
        )

    async def resend(
        self, team_id: int, invitation_id: int,
    ) -> InvitationCreateResponse:
        return await self._client.post(
            f"/teams/{team_id}/invitations/{invitation_id}/resend",
            model=InvitationCreateResponse,
        )

    async def cancel(self, team_id: int, invitation_id: int) -> MessageResponse:
        return await self._client.delete(
            f"/teams/{team_id}/invitations/{invitation_id}",
            model=MessageResponse,
        )
