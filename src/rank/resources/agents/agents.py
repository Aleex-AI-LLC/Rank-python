from __future__ import annotations

from typing import Any, Dict, Union

from ..._base_client import AsyncAPIClient, SyncAPIClient
from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.agent import (
    Agent,
    AgentCloneResponse,
    AgentCreateResponse,
    AgentDeleteResponse,
    AgentGroupedResponse,
    AgentListResponse,
    AgentUpdateResponse,
)
from ...types.shared import ReasoningEffort
from .._base import AsyncAPIResource, SyncAPIResource
from .agent_mcps import AgentMcps, AsyncAgentMcps
from .mcp_servers import AsyncMcpServers, McpServers
from .models import AIModels, AsyncAIModels
from .tools import AgentTools, AsyncAgentTools

_AGENTS = "/agents"


# ---------------------------------------------------------------------------
# Agents (sync)
# ---------------------------------------------------------------------------


class Agents(SyncAPIResource):
    """Agent management resource — CRUD, cloning, tools, and MCP servers.

    Access via ``client.agents``.

    Example::

        # List all available agents (grouped by own/team/default)
        grouped = client.agents.list()
        for a in grouped.own_agents:
            print(a.name, a.agent_type)

        # List pentest agents (flat paginated)
        pentest_agents = client.agents.list(type="pentest")

        # Create a new agent
        agent = client.agents.create(
            name="Recon Agent",
            instructions="Perform reconnaissance on the target",
            agent_type="pentest",
            phase_id=1,
            model_id=6,
        )

        # Manage tools
        tools = client.agents.tools.list(agent_id=agent.id)
    """

    tools: AgentTools
    mcps: AgentMcps
    models: AIModels
    mcp_servers: McpServers

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.tools = AgentTools(client)
        self.mcps = AgentMcps(client)
        self.models = AIModels(client)
        self.mcp_servers = McpServers(client)

    # -- CRUD ---------------------------------------------------------------

    def list(
        self,
        *,
        type: Union[str, _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> Union[AgentListResponse, AgentGroupedResponse]:
        """List available agents.

        When ``type`` is provided (``"pentest"`` or ``"general"``), returns a
        flat paginated list. When omitted, returns agents grouped into
        ``own_agents``, ``team_agents``, and ``default_agents``.

        Args:
            type: Filter by agent type (``"pentest"`` or ``"general"``).
            phase_id: Filter pentest agents by phase (only valid with
                ``type="pentest"``).
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({
            "type": type,
            "phase_id": phase_id,
            "page": page,
            "per_page": per_page,
        })
        model = AgentListResponse if not isinstance(type, _NotGiven) else AgentGroupedResponse
        return self._client.get(_AGENTS, params=params or None, model=model)

    def mine(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> AgentListResponse:
        """List the authenticated user's own agents.

        Args:
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"{_AGENTS}/mine", params=params or None, model=AgentListResponse,
        )

    def retrieve(self, agent_id: int) -> Agent:
        """Get full details of an agent.

        Args:
            agent_id: ID of the agent.
        """
        return self._client.get(f"{_AGENTS}/{agent_id}", model=Agent)

    def create(
        self,
        *,
        name: str,
        instructions: str,
        agent_type: str,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
        effort: Union[ReasoningEffort, _NotGiven] = NOT_GIVEN,
        thinking_enabled: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> AgentCreateResponse:
        """Create a new agent.

        Args:
            name: Agent display name (2-255 chars).
            instructions: System prompt / instructions (10-50000 chars).
            agent_type: ``"pentest"`` or ``"general"``.
            description: Optional description (max 2000 chars).
            phase_id: Required when ``agent_type`` is ``"pentest"`` (1-5).
            model_id: AI model ID.
            effort: Reasoning-effort override for the agent. One of
                ``"none"``, ``"minimal"``, ``"low"``, ``"medium"``, ``"high"``,
                ``"xhigh"``, ``"max"``. Must be supported by the model. When
                omitted, the agent inherits the model default.
            thinking_enabled: Whether the agent's thinking/reasoning is on.
                When omitted, the agent inherits the model default.

        Returns:
            Response containing the newly created agent under ``.agent``.
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
            "effort": effort,
            "thinking_enabled": thinking_enabled,
        }))
        return self._client.post(_AGENTS, body=body, model=AgentCreateResponse)

    def update(
        self,
        agent_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        instructions: Union[str, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
        agent_type: Union[str, _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        effort: Union[ReasoningEffort, _NotGiven] = NOT_GIVEN,
        thinking_enabled: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> AgentUpdateResponse:
        """Update an agent.

        At least one field must be provided. Only the agent's owner can
        update it. Default and protected agents cannot be modified.

        Args:
            agent_id: ID of the agent.
            name: New display name.
            description: New description.
            instructions: New system prompt / instructions.
            model_id: New AI model ID.
            agent_type: ``"pentest"`` or ``"general"``.
            phase_id: New phase ID (required for pentest agents).
            effort: Reasoning-effort override for the agent. One of
                ``"none"``, ``"minimal"``, ``"low"``, ``"medium"``, ``"high"``,
                ``"xhigh"``, ``"max"``. Must be supported by the model.
            thinking_enabled: Whether the agent's thinking/reasoning is on.

        Returns:
            Response containing the updated agent under ``.agent``.
        """
        body = strip_not_given({
            "name": name,
            "description": description,
            "instructions": instructions,
            "model_id": model_id,
            "agent_type": agent_type,
            "phase_id": phase_id,
            "effort": effort,
            "thinking_enabled": thinking_enabled,
        })
        return self._client.put(f"{_AGENTS}/{agent_id}", body=body, model=AgentUpdateResponse)

    def delete(self, agent_id: int) -> AgentDeleteResponse:
        """Delete an agent (soft delete).

        Only the agent's owner can delete it. Default and protected agents
        cannot be deleted.

        Args:
            agent_id: ID of the agent.
        """
        return self._client.delete(f"{_AGENTS}/{agent_id}", model=AgentDeleteResponse)

    # -- Actions ------------------------------------------------------------

    def clone(self, agent_id: int) -> AgentCloneResponse:
        """Clone an existing agent.

        Creates a copy of the agent with all its configuration. The clone
        belongs to the authenticated user.

        Args:
            agent_id: ID of the agent to clone.

        Returns:
            Response containing the cloned agent under ``.agent``.
        """
        return self._client.post(f"{_AGENTS}/{agent_id}/clone", model=AgentCloneResponse)


# ---------------------------------------------------------------------------
# Agents (async)
# ---------------------------------------------------------------------------


class AsyncAgents(AsyncAPIResource):
    """Async variant of :class:`Agents`."""

    tools: AsyncAgentTools
    mcps: AsyncAgentMcps
    models: AsyncAIModels
    mcp_servers: AsyncMcpServers

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.tools = AsyncAgentTools(client)
        self.mcps = AsyncAgentMcps(client)
        self.models = AsyncAIModels(client)
        self.mcp_servers = AsyncMcpServers(client)

    # -- CRUD ---------------------------------------------------------------

    async def list(
        self,
        *,
        type: Union[str, _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> Union[AgentListResponse, AgentGroupedResponse]:
        params = strip_not_given({
            "type": type,
            "phase_id": phase_id,
            "page": page,
            "per_page": per_page,
        })
        model = AgentListResponse if not isinstance(type, _NotGiven) else AgentGroupedResponse
        return await self._client.get(_AGENTS, params=params or None, model=model)

    async def mine(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> AgentListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"{_AGENTS}/mine", params=params or None, model=AgentListResponse,
        )

    async def retrieve(self, agent_id: int) -> Agent:
        return await self._client.get(f"{_AGENTS}/{agent_id}", model=Agent)

    async def create(
        self,
        *,
        name: str,
        instructions: str,
        agent_type: str,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
        effort: Union[ReasoningEffort, _NotGiven] = NOT_GIVEN,
        thinking_enabled: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> AgentCreateResponse:
        body: Dict[str, Any] = {
            "name": name,
            "instructions": instructions,
            "agent_type": agent_type,
        }
        body.update(strip_not_given({
            "description": description,
            "phase_id": phase_id,
            "model_id": model_id,
            "effort": effort,
            "thinking_enabled": thinking_enabled,
        }))
        return await self._client.post(_AGENTS, body=body, model=AgentCreateResponse)

    async def update(
        self,
        agent_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        instructions: Union[str, _NotGiven] = NOT_GIVEN,
        model_id: Union[int, _NotGiven] = NOT_GIVEN,
        agent_type: Union[str, _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        effort: Union[ReasoningEffort, _NotGiven] = NOT_GIVEN,
        thinking_enabled: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> AgentUpdateResponse:
        body = strip_not_given({
            "name": name,
            "description": description,
            "instructions": instructions,
            "model_id": model_id,
            "agent_type": agent_type,
            "phase_id": phase_id,
            "effort": effort,
            "thinking_enabled": thinking_enabled,
        })
        return await self._client.put(f"{_AGENTS}/{agent_id}", body=body, model=AgentUpdateResponse)

    async def delete(self, agent_id: int) -> AgentDeleteResponse:
        return await self._client.delete(f"{_AGENTS}/{agent_id}", model=AgentDeleteResponse)

    # -- Actions ------------------------------------------------------------

    async def clone(self, agent_id: int) -> AgentCloneResponse:
        return await self._client.post(f"{_AGENTS}/{agent_id}/clone", model=AgentCloneResponse)
