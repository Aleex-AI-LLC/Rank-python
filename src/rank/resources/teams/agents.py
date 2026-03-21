from __future__ import annotations

from typing import Any, Dict, List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.team import (
    TeamAgentCreateResponse,
    TeamAgentDeleteResponse,
    TeamAgentListResponse,
)
from .._base import AsyncAPIResource, SyncAPIResource


# ---------------------------------------------------------------------------
# TeamAgents (sync)
# ---------------------------------------------------------------------------


class TeamAgents(SyncAPIResource):
    """Manage agents available to a team.

    Access via ``client.teams.agents``.

    Example::

        # List team agents (custom + default)
        agents = client.teams.agents.list(team_id=1)
        for a in agents.team_agents:
            print(a.name, a.agent_type)

        # Create a new agent for the team
        resp = client.teams.agents.create(
            team_id=1,
            name="Recon Agent",
            instructions="Perform reconnaissance on the target",
            agent_type="pentest",
            phase_id=1,
            model_id=6,
        )
    """

    def list(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> TeamAgentListResponse:
        """List agents available to a team.

        Returns both custom team agents and default (global) agents.

        Args:
            team_id: ID of the team.
            page: Page number (for team agents).
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"/teams/{team_id}/agents",
            params=params or None,
            model=TeamAgentListResponse,
        )

    def create(
        self,
        team_id: int,
        *,
        name: str,
        instructions: str,
        agent_type: str,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
        tool_ids: Union[List[int], _NotGiven] = NOT_GIVEN,
    ) -> TeamAgentCreateResponse:
        """Create a new agent for a team.

        Args:
            team_id: ID of the team.
            name: Agent display name.
            instructions: System prompt / instructions for the agent.
            agent_type: ``"pentest"`` or ``"general"``.
            description: Optional description.
            phase_id: Required when ``agent_type`` is ``"pentest"``.
            model_id: AI model ID (must be available for the team's tier).
            tool_ids: List of tool IDs to attach.

        Returns:
            Creation confirmation with the full agent details.
        """
        body: Dict[str, Any] = {
            "name": name,
            "instructions": instructions,
            "agent_type": agent_type,
        }
        body.update(strip_not_given({
            "description": description,
            "phase_id": phase_id,
            "model_id": model_id,
            "tool_ids": tool_ids,
        }))
        return self._client.post(
            f"/teams/{team_id}/agents",
            body=body,
            model=TeamAgentCreateResponse,
        )

    def remove(self, team_id: int, agent_id: int) -> TeamAgentDeleteResponse:
        """Remove a custom agent from a team.

        Default and protected agents cannot be removed. Only the team
        owner can perform this action.

        Args:
            team_id: ID of the team.
            agent_id: ID of the agent to remove.
        """
        return self._client.delete(
            f"/teams/{team_id}/agents/{agent_id}",
            model=TeamAgentDeleteResponse,
        )


# ---------------------------------------------------------------------------
# TeamAgents (async)
# ---------------------------------------------------------------------------


class AsyncTeamAgents(AsyncAPIResource):
    """Async variant of :class:`TeamAgents`."""

    async def list(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> TeamAgentListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"/teams/{team_id}/agents",
            params=params or None,
            model=TeamAgentListResponse,
        )

    async def create(
        self,
        team_id: int,
        *,
        name: str,
        instructions: str,
        agent_type: str,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
        tool_ids: Union[List[int], _NotGiven] = NOT_GIVEN,
    ) -> TeamAgentCreateResponse:
        body: Dict[str, Any] = {
            "name": name,
            "instructions": instructions,
            "agent_type": agent_type,
        }
        body.update(strip_not_given({
            "description": description,
            "phase_id": phase_id,
            "model_id": model_id,
            "tool_ids": tool_ids,
        }))
        return await self._client.post(
            f"/teams/{team_id}/agents",
            body=body,
            model=TeamAgentCreateResponse,
        )

    async def remove(self, team_id: int, agent_id: int) -> TeamAgentDeleteResponse:
        return await self._client.delete(
            f"/teams/{team_id}/agents/{agent_id}",
            model=TeamAgentDeleteResponse,
        )
