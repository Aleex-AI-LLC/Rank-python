from __future__ import annotations

from typing import Any, Dict, List, Union

from ..._base_client import AsyncAPIClient, SyncAPIClient
from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.pentest import PentestListResponse
from ...types.shared import MessageResponse
from ...types.team import Team, TeamListResponse
from .._base import AsyncAPIResource, SyncAPIResource
from .agents import AsyncTeamAgents, TeamAgents
from .invitations import AsyncInvitations, Invitations
from .members import AsyncMembers, Members
from .roles import AsyncRoles, Roles
from .usage import AsyncTeamUsage, TeamUsage

_TEAMS = "/teams"


# ---------------------------------------------------------------------------
# Teams (sync)
# ---------------------------------------------------------------------------


class Teams(SyncAPIResource):
    """Team management resource — CRUD, membership, roles, and sub-resources.

    Access via ``client.teams``.

    Example::

        # List all teams
        teams = client.teams.list()
        for t in teams.items:
            print(t.name, t.member_count)

        # Create a team
        team = client.teams.create(name="Security Team")

        # List team members
        members = client.teams.members.list(team_id=team.id)

        # Invite someone
        client.teams.invitations.create(team_id=team.id, email="user@example.com")
    """

    members: Members
    roles: Roles
    invitations: Invitations
    agents: TeamAgents
    usage: TeamUsage

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.members = Members(client)
        self.roles = Roles(client)
        self.invitations = Invitations(client)
        self.agents = TeamAgents(client)
        self.usage = TeamUsage(client)

    # -- CRUD ---------------------------------------------------------------

    def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> TeamListResponse:
        """List teams the authenticated user belongs to.

        Args:
            page: Page number (default 1).
            per_page: Items per page (default 20, or ``"all"``).
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(_TEAMS, params=params or None, model=TeamListResponse)

    def create(
        self,
        *,
        name: str,
        description: str,
        max_members: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> Team:
        """Create a new team.

        The authenticated user becomes the owner.

        Args:
            name: Team name.
            description: Team description (required by the backend).
            max_members: Maximum number of members (default 10).

        Returns:
            The newly created team.
        """
        body: Dict[str, Any] = {"name": name, "description": description}
        body.update(strip_not_given({
            "max_members": max_members,
        }))
        return self._client.post(_TEAMS, body=body, model=Team)

    def mine(self) -> List[Team]:
        """List teams the authenticated user belongs to, with full details.

        Unlike :meth:`list`, this returns a flat list (not paginated) with
        richer team information.
        """
        return self._client.get_list(f"{_TEAMS}/mine", model=Team)

    def retrieve(self, team_id: int) -> Team:
        """Get full details of a team.

        Includes members and available roles when the user has access.

        Args:
            team_id: ID of the team.
        """
        return self._client.get(f"{_TEAMS}/{team_id}", model=Team)

    def update(
        self,
        team_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        max_members: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> Team:
        """Update a team's details.

        Args:
            team_id: ID of the team.
            name: New team name.
            description: New description.
            max_members: New maximum member count.

        Returns:
            The updated team.
        """
        body = strip_not_given({
            "name": name,
            "description": description,
            "max_members": max_members,
        })
        return self._client.put(f"{_TEAMS}/{team_id}", body=body, model=Team)

    def delete(self, team_id: int) -> MessageResponse:
        """Delete a team.

        Only the team owner can delete a team.

        Args:
            team_id: ID of the team.
        """
        return self._client.delete(f"{_TEAMS}/{team_id}", model=MessageResponse)

    # -- Actions ------------------------------------------------------------

    def leave(self, team_id: int) -> MessageResponse:
        """Leave a team.

        The team owner cannot leave; transfer ownership first.

        Args:
            team_id: ID of the team.
        """
        return self._client.post(f"{_TEAMS}/{team_id}/leave", model=MessageResponse)

    def transfer(self, team_id: int, *, new_owner_id: int) -> MessageResponse:
        """Transfer team ownership to another member.

        Only the current owner can transfer ownership.

        Args:
            team_id: ID of the team.
            new_owner_id: User ID of the new owner (must be a member).
        """
        return self._client.post(
            f"{_TEAMS}/{team_id}/transfer",
            body={"new_owner_id": new_owner_id},
            model=MessageResponse,
        )

    def pentests(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> PentestListResponse:
        """List pentests belonging to a team.

        Args:
            team_id: ID of the team.
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"{_TEAMS}/{team_id}/pentests",
            params=params or None,
            model=PentestListResponse,
        )


# ---------------------------------------------------------------------------
# Teams (async)
# ---------------------------------------------------------------------------


class AsyncTeams(AsyncAPIResource):
    """Async variant of :class:`Teams`."""

    members: AsyncMembers
    roles: AsyncRoles
    invitations: AsyncInvitations
    agents: AsyncTeamAgents
    usage: AsyncTeamUsage

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.members = AsyncMembers(client)
        self.roles = AsyncRoles(client)
        self.invitations = AsyncInvitations(client)
        self.agents = AsyncTeamAgents(client)
        self.usage = AsyncTeamUsage(client)

    # -- CRUD ---------------------------------------------------------------

    async def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> TeamListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(_TEAMS, params=params or None, model=TeamListResponse)

    async def create(
        self,
        *,
        name: str,
        description: str,
        max_members: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> Team:
        body: Dict[str, Any] = {"name": name, "description": description}
        body.update(strip_not_given({
            "max_members": max_members,
        }))
        return await self._client.post(_TEAMS, body=body, model=Team)

    async def mine(self) -> List[Team]:
        return await self._client.get_list(f"{_TEAMS}/mine", model=Team)

    async def retrieve(self, team_id: int) -> Team:
        return await self._client.get(f"{_TEAMS}/{team_id}", model=Team)

    async def update(
        self,
        team_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        max_members: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> Team:
        body = strip_not_given({
            "name": name,
            "description": description,
            "max_members": max_members,
        })
        return await self._client.put(f"{_TEAMS}/{team_id}", body=body, model=Team)

    async def delete(self, team_id: int) -> MessageResponse:
        return await self._client.delete(f"{_TEAMS}/{team_id}", model=MessageResponse)

    # -- Actions ------------------------------------------------------------

    async def leave(self, team_id: int) -> MessageResponse:
        return await self._client.post(f"{_TEAMS}/{team_id}/leave", model=MessageResponse)

    async def transfer(self, team_id: int, *, new_owner_id: int) -> MessageResponse:
        return await self._client.post(
            f"{_TEAMS}/{team_id}/transfer",
            body={"new_owner_id": new_owner_id},
            model=MessageResponse,
        )

    async def pentests(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> PentestListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"{_TEAMS}/{team_id}/pentests",
            params=params or None,
            model=PentestListResponse,
        )
