from __future__ import annotations

from typing import List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.shared import MessageResponse
from ...types.team import MemberListResponse, TeamRole
from .._base import AsyncAPIResource, SyncAPIResource

# ---------------------------------------------------------------------------
# Members (sync)
# ---------------------------------------------------------------------------


class Members(SyncAPIResource):
    """Manage members of a team.

    Access via ``client.teams.members``.
    """

    def list(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> MemberListResponse:
        """List members of a team.

        Args:
            team_id: ID of the team.
            page: Page number (default 1).
            per_page: Items per page (default 20).
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"/teams/{team_id}/members",
            params=params or None,
            model=MemberListResponse,
        )

    def remove(self, team_id: int, user_id: int) -> MessageResponse:
        """Remove a member from a team.

        Only the team owner or users with the appropriate role can
        remove members. The owner cannot be removed.

        Args:
            team_id: ID of the team.
            user_id: ID of the user to remove.
        """
        return self._client.delete(
            f"/teams/{team_id}/members/{user_id}",
            model=MessageResponse,
        )

    def roles(self, team_id: int, user_id: int) -> List[TeamRole]:
        """Get the roles assigned to a specific team member.

        The API returns a flat list of role objects.

        Args:
            team_id: ID of the team.
            user_id: ID of the member.
        """
        return self._client.get_list(
            f"/teams/{team_id}/members/{user_id}/roles",
            model=TeamRole,
        )


# ---------------------------------------------------------------------------
# Members (async)
# ---------------------------------------------------------------------------


class AsyncMembers(AsyncAPIResource):
    """Async variant of :class:`Members`."""

    async def list(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> MemberListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"/teams/{team_id}/members",
            params=params or None,
            model=MemberListResponse,
        )

    async def remove(self, team_id: int, user_id: int) -> MessageResponse:
        return await self._client.delete(
            f"/teams/{team_id}/members/{user_id}",
            model=MessageResponse,
        )

    async def roles(self, team_id: int, user_id: int) -> List[TeamRole]:
        return await self._client.get_list(
            f"/teams/{team_id}/members/{user_id}/roles",
            model=TeamRole,
        )
