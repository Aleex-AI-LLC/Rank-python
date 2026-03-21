from __future__ import annotations

from typing import List

from ...types.agent import (
    AgentToolListResponse,
    AssignToolsResponse,
    AvailableToolListResponse,
    RemoveToolResponse,
)
from .._base import AsyncAPIResource, SyncAPIResource


# ---------------------------------------------------------------------------
# AgentTools (sync)
# ---------------------------------------------------------------------------


class AgentTools(SyncAPIResource):
    """Manage tools assigned to an agent.

    Access via ``client.agents.tools``.

    Example::

        # List tools assigned to an agent
        tools = client.agents.tools.list(agent_id=42)
        for t in tools.tools:
            print(t.name, t.category)

        # Assign tools
        client.agents.tools.assign(agent_id=42, tool_ids=[46, 47])

        # Remove a tool
        client.agents.tools.remove(agent_id=42, tool_id=46)
    """

    def list(self, agent_id: int) -> AgentToolListResponse:
        """List tools assigned to an agent.

        Args:
            agent_id: ID of the agent.
        """
        return self._client.get(
            f"/agents/{agent_id}/tools", model=AgentToolListResponse,
        )

    def available(self, agent_id: int) -> AvailableToolListResponse:
        """List tools available for assignment to an agent.

        Returns tools compatible with the agent's phase that are not
        already assigned.

        Args:
            agent_id: ID of the agent.
        """
        return self._client.get(
            f"/agents/{agent_id}/available-tools", model=AvailableToolListResponse,
        )

    def assign(self, agent_id: int, *, tool_ids: List[int]) -> AssignToolsResponse:
        """Assign one or more tools to an agent.

        Only the agent's owner can modify tools. Default and protected
        agents cannot be modified.

        Args:
            agent_id: ID of the agent.
            tool_ids: List of tool IDs to assign.
        """
        return self._client.post(
            f"/agents/{agent_id}/tools",
            body={"tool_ids": tool_ids},
            model=AssignToolsResponse,
        )

    def remove(self, agent_id: int, tool_id: int) -> RemoveToolResponse:
        """Remove a tool from an agent.

        Args:
            agent_id: ID of the agent.
            tool_id: ID of the tool to remove.
        """
        return self._client.delete(
            f"/agents/{agent_id}/tools/{tool_id}", model=RemoveToolResponse,
        )


# ---------------------------------------------------------------------------
# AgentTools (async)
# ---------------------------------------------------------------------------


class AsyncAgentTools(AsyncAPIResource):
    """Async variant of :class:`AgentTools`."""

    async def list(self, agent_id: int) -> AgentToolListResponse:
        return await self._client.get(
            f"/agents/{agent_id}/tools", model=AgentToolListResponse,
        )

    async def available(self, agent_id: int) -> AvailableToolListResponse:
        return await self._client.get(
            f"/agents/{agent_id}/available-tools", model=AvailableToolListResponse,
        )

    async def assign(self, agent_id: int, *, tool_ids: List[int]) -> AssignToolsResponse:
        return await self._client.post(
            f"/agents/{agent_id}/tools",
            body={"tool_ids": tool_ids},
            model=AssignToolsResponse,
        )

    async def remove(self, agent_id: int, tool_id: int) -> RemoveToolResponse:
        return await self._client.delete(
            f"/agents/{agent_id}/tools/{tool_id}", model=RemoveToolResponse,
        )
