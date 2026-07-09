from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import model_validator

from .shared import PaginationInfo, RankModel, ReasoningEffort


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------


class Agent(RankModel):
    """Full agent object returned by show, create, update, and clone.

    The list endpoint (``toListArray``) returns flat fields like
    ``phase_id`` / ``model_id``.  The detail endpoint (``toDetailArray``)
    nests them as ``phase: {id, name}`` / ``model: {id, name}``.
    A pre-validator normalises both shapes so ``phase_id``, ``phase_name``,
    ``model_id``, and ``model_name`` are always populated.
    """

    id: int
    name: str = ""
    description: Optional[str] = None
    instructions: Optional[str] = None
    system_prompt: Optional[str] = None
    agent_type: Optional[str] = None
    phase_id: Optional[int] = None
    phase_name: Optional[str] = None
    model_id: Optional[int] = None
    model_name: Optional[str] = None
    effort: Optional[ReasoningEffort] = None
    thinking_enabled: Optional[bool] = None
    supports_effort: Optional[bool] = None
    effort_values: List[ReasoningEffort] = []
    default_effort: Optional[ReasoningEffort] = None
    supports_thinking_toggle: Optional[bool] = None
    is_default: Optional[bool] = None
    protected: Optional[bool] = None
    created_by: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    tools: List[Any] = []
    phase: Optional[Any] = None
    model: Optional[Any] = None

    @model_validator(mode="before")
    @classmethod
    def _flatten_nested_objects(cls, data: Any) -> Any:
        """Extract ``phase_id``/``model_id`` from nested dicts when absent."""
        if not isinstance(data, dict):
            return data
        phase = data.get("phase")
        if isinstance(phase, dict):
            if data.get("phase_id") is None:
                data["phase_id"] = phase.get("id")
            if data.get("phase_name") is None:
                data["phase_name"] = phase.get("name")
        model_obj = data.get("model")
        if isinstance(model_obj, dict):
            if data.get("model_id") is None:
                data["model_id"] = model_obj.get("id")
            if data.get("model_name") is None:
                data["model_name"] = model_obj.get("name")
        return data


class AgentCreateResponse(RankModel):
    """Response from ``POST /agents``.

    The backend wraps the created agent under an ``agent`` key alongside
    a confirmation message.
    """

    message: str = ""
    agent: Optional[Agent] = None


class AgentUpdateResponse(RankModel):
    """Response from ``PUT /agents/{id}``.

    Same wrapping as create: ``message`` + ``agent``.
    """

    message: str = ""
    agent: Optional[Agent] = None


class AgentCloneResponse(RankModel):
    """Response from ``POST /agents/{id}/clone``.

    Same wrapping as create: ``message`` + ``agent``.
    """

    message: str = ""
    agent: Optional[Agent] = None


class AgentDeleteResponse(RankModel):
    """Response from ``DELETE /agents/{id}``."""

    message: str = ""
    agent_id: Optional[int] = None


class AgentListResponse(RankModel):
    """Paginated list of agents returned when using ``type`` filter.

    Used by ``GET /agents?type=pentest`` and ``GET /agents/mine``.
    """

    items: List[Agent] = []
    pagination: Optional[PaginationInfo] = None


class TeamAgentGroup(RankModel):
    """A team's agents within the grouped response.

    Each entry represents one team and contains the agents belonging to it.
    """

    team_id: Optional[int] = None
    team_name: Optional[str] = None
    agents: List[Agent] = []
    count: Optional[int] = None


class AgentGroupedResponse(RankModel):
    """Grouped agent list returned by ``GET /agents`` without ``type`` filter.

    Contains the user's own agents, team agents grouped by team, and
    default (global) agents.
    """

    own_agents: List[Agent] = []
    team_agents: List[TeamAgentGroup] = []
    default_agents: List[Agent] = []
    total_own: Optional[int] = None
    total_team: Optional[int] = None
    can_create: Optional[bool] = None
    max_agents: Optional[int] = None


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


class AgentTool(RankModel):
    """A tool that can be assigned to an agent.

    Fields match the backend ``toPublicArray`` output.  The
    ``assigned`` flag is only present in the available-tools endpoint.
    """

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Any] = None
    tool_type: Optional[str] = None
    command: Optional[str] = None
    execution_mode: Optional[str] = None
    assigned: Optional[bool] = None


class AgentToolListResponse(RankModel):
    """Response from ``GET /agents/{id}/tools``."""

    tools: List[AgentTool] = []
    total: Optional[int] = None
    agent_id: Optional[int] = None


class AvailableToolListResponse(RankModel):
    """Response from ``GET /agents/{id}/available-tools``."""

    available_tools: List[AgentTool] = []
    total: Optional[int] = None
    agent_id: Optional[int] = None
    phase_id: Optional[int] = None
    phase_name: Optional[str] = None


class AssignToolsResponse(RankModel):
    """Response from ``POST /agents/{id}/tools``."""

    message: str = ""
    assigned: Optional[int] = None
    skipped: Optional[int] = None
    agent_id: Optional[int] = None
    tool_ids: List[int] = []


class RemoveToolResponse(RankModel):
    """Response from ``DELETE /agents/{id}/tools/{toolId}``."""

    message: str = ""
    agent_id: Optional[int] = None
    tool_id: Optional[int] = None


# ---------------------------------------------------------------------------
# MCPs
# ---------------------------------------------------------------------------


class AgentMcp(RankModel):
    """An MCP server assigned to an agent.

    Fields match the backend ``toOwnerArray`` output.
    """

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    transport_type: Optional[str] = None
    url: Optional[str] = None
    command: Optional[str] = None
    args: List[Any] = []
    env: List[Any] = []
    headers: List[Any] = []
    auth_type: Optional[str] = None
    auth_config: Optional[Any] = None
    enabled: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class AgentMcpListResponse(RankModel):
    """Response from ``GET /agents/{id}/mcps``."""

    mcp_servers: List[AgentMcp] = []
    total: Optional[int] = None
    agent_id: Optional[int] = None


class AssignMcpsResponse(RankModel):
    """Response from ``POST /agents/{id}/mcps``."""

    message: str = ""
    assigned: Optional[int] = None
    skipped: Optional[int] = None
    agent_id: Optional[int] = None
    mcp_server_ids: List[int] = []


class RemoveMcpResponse(RankModel):
    """Response from ``DELETE /agents/{id}/mcps/{mcpId}``."""

    message: str = ""
    agent_id: Optional[int] = None
    mcp_server_id: Optional[int] = None


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------

__all__ = [
    # Agent
    "Agent",
    "AgentCreateResponse",
    "AgentUpdateResponse",
    "AgentCloneResponse",
    "AgentDeleteResponse",
    "TeamAgentGroup",
    "AgentListResponse",
    "AgentGroupedResponse",
    # Tools
    "AgentTool",
    "AgentToolListResponse",
    "AvailableToolListResponse",
    "AssignToolsResponse",
    "RemoveToolResponse",
    # MCPs
    "AgentMcp",
    "AgentMcpListResponse",
    "AssignMcpsResponse",
    "RemoveMcpResponse",
]
