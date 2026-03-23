from __future__ import annotations

from ..types.shared import MessageResponse
from ..types.team import (
    InvitationAcceptResponse,
    InvitationDetail,
    UserInvitationListResponse,
)
from ._base import AsyncAPIResource, SyncAPIResource

_INVITATIONS = "/invitations"


# ---------------------------------------------------------------------------
# UserInvitations (sync)
# ---------------------------------------------------------------------------


class UserInvitations(SyncAPIResource):
    """Manage the authenticated user's team invitations.

    Access via ``client.invitations``.

    Example::

        # List pending invitations
        resp = client.invitations.list()
        for inv in resp.items:
            print(inv.team_name, inv.inviter_name)

        # Accept an invitation by token
        client.invitations.accept("abc123token...")
    """

    def list(self) -> UserInvitationListResponse:
        """List all pending invitations for the authenticated user."""
        return self._client.get(_INVITATIONS, model=UserInvitationListResponse)

    def retrieve(self, token: str) -> InvitationDetail:
        """Get details of a specific invitation by token.

        Args:
            token: The 64-character invitation token.
        """
        return self._client.get(f"{_INVITATIONS}/{token}", model=InvitationDetail)

    def accept(self, token: str) -> InvitationAcceptResponse:
        """Accept a team invitation.

        Args:
            token: The 64-character invitation token.
        """
        return self._client.post(
            f"{_INVITATIONS}/{token}/accept", model=InvitationAcceptResponse,
        )

    def reject(self, token: str) -> MessageResponse:
        """Reject a team invitation.

        Args:
            token: The 64-character invitation token.
        """
        return self._client.post(
            f"{_INVITATIONS}/{token}/reject", model=MessageResponse,
        )


# ---------------------------------------------------------------------------
# UserInvitations (async)
# ---------------------------------------------------------------------------


class AsyncUserInvitations(AsyncAPIResource):
    """Async variant of :class:`UserInvitations`."""

    async def list(self) -> UserInvitationListResponse:
        """List all pending invitations for the authenticated user."""
        return await self._client.get(_INVITATIONS, model=UserInvitationListResponse)

    async def retrieve(self, token: str) -> InvitationDetail:
        """Get details of a specific invitation by token.

        Args:
            token: The 64-character invitation token.
        """
        return await self._client.get(
            f"{_INVITATIONS}/{token}", model=InvitationDetail,
        )

    async def accept(self, token: str) -> InvitationAcceptResponse:
        """Accept a team invitation.

        Args:
            token: The 64-character invitation token.
        """
        return await self._client.post(
            f"{_INVITATIONS}/{token}/accept", model=InvitationAcceptResponse,
        )

    async def reject(self, token: str) -> MessageResponse:
        """Reject a team invitation.

        Args:
            token: The 64-character invitation token.
        """
        return await self._client.post(
            f"{_INVITATIONS}/{token}/reject", model=MessageResponse,
        )
