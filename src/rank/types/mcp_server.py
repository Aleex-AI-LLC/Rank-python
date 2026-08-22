from __future__ import annotations

from typing import Any, List, Optional

from .shared import PaginationInfo, RankModel


class McpServer(RankModel):
    """An MCP (Model Context Protocol) server."""
    id: int
    name: str = ""
    description: Optional[str] = None
    transport_type: Optional[str] = None
    url: Optional[str] = None
    command: Optional[str] = None
    args: List[Any] = []
    env: List[Any] = []
    headers: Optional[Any] = None
    auth_type: Optional[str] = None
    auth_config: Optional[Any] = None
    enabled: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class McpServerListResponse(RankModel):
    """Response from ``GET /mcp-servers``."""
    items: List[McpServer] = []
    pagination: Optional[PaginationInfo] = None


class McpServerCreateResponse(RankModel):
    """Response from ``POST /mcp-servers`` and ``PATCH /mcp-servers/{id}``."""
    message: str = ""
    mcp_server: Optional[McpServer] = None


class McpServerDeleteResponse(RankModel):
    """Response from ``DELETE /mcp-servers/{id}``."""
    message: str = ""
    mcp_server_id: Optional[int] = None


__all__ = [
    "McpServer",
    "McpServerListResponse",
    "McpServerCreateResponse",
    "McpServerDeleteResponse",
]
