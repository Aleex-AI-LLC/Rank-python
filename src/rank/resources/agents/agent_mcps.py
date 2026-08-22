from __future__ import annotations

from typing import List

from ...types.agent import AgentMcpListResponse, AssignMcpsResponse, RemoveMcpResponse
from .._base import AsyncAPIResource, SyncAPIResource

# ---------------------------------------------------------------------------
# AgentMcps (sync)
# ---------------------------------------------------------------------------


class AgentMcps(SyncAPIResource):
    """Manage MCP servers assigned to an agent.

    Access via ``client.agents.mcps``.

    Example::

        # List MCP servers assigned to an agent
        mcps = client.agents.mcps.list(agent_id=42)
        for m in mcps.mcp_servers:
            print(m.name, m.transport_type)

        # Assign MCP servers
        client.agents.mcps.assign(agent_id=42, mcp_server_ids=[1, 2])

        # Remove an MCP server
        client.agents.mcps.remove(agent_id=42, mcp_id=1)
    """

    def list(self, agent_id: int) -> AgentMcpListResponse:
        """List MCP servers assigned to an agent.

        Args:
            agent_id: ID of the agent.
        """
        return self._client.get(
            f"/agents/{agent_id}/mcps", model=AgentMcpListResponse,
        )

    def assign(
        self, agent_id: int, *, mcp_server_ids: List[int],
    ) -> AssignMcpsResponse:
        """Assign one or more MCP servers to an agent.

        Args:
            agent_id: ID of the agent.
            mcp_server_ids: List of MCP server IDs to assign.
        """
        return self._client.post(
            f"/agents/{agent_id}/mcps",
            body={"mcp_server_ids": mcp_server_ids},
            model=AssignMcpsResponse,
        )

    def remove(self, agent_id: int, mcp_id: int) -> RemoveMcpResponse:
        """Remove an MCP server from an agent.

        Args:
            agent_id: ID of the agent.
            mcp_id: ID of the MCP server to remove.
        """
        return self._client.delete(
            f"/agents/{agent_id}/mcps/{mcp_id}", model=RemoveMcpResponse,
        )


# ---------------------------------------------------------------------------
# AgentMcps (async)
# ---------------------------------------------------------------------------


class AsyncAgentMcps(AsyncAPIResource):
    """Async variant of :class:`AgentMcps`."""

    async def list(self, agent_id: int) -> AgentMcpListResponse:
        return await self._client.get(
            f"/agents/{agent_id}/mcps", model=AgentMcpListResponse,
        )

    async def assign(
        self, agent_id: int, *, mcp_server_ids: List[int],
    ) -> AssignMcpsResponse:
        return await self._client.post(
            f"/agents/{agent_id}/mcps",
            body={"mcp_server_ids": mcp_server_ids},
            model=AssignMcpsResponse,
        )

    async def remove(self, agent_id: int, mcp_id: int) -> RemoveMcpResponse:
        return await self._client.delete(
            f"/agents/{agent_id}/mcps/{mcp_id}", model=RemoveMcpResponse,
        )
