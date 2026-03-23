from __future__ import annotations

from typing import Any, Dict, List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.mcp_server import (
    McpServer,
    McpServerCreateResponse,
    McpServerDeleteResponse,
    McpServerListResponse,
)
from .._base import AsyncAPIResource, SyncAPIResource

_MCP_SERVERS = "/mcp-servers"


# ---------------------------------------------------------------------------
# McpServers (sync)
# ---------------------------------------------------------------------------


class McpServers(SyncAPIResource):
    """MCP server management resource.

    Access via ``client.agents.mcp_servers``.

    Example::

        # List all MCP servers
        resp = client.agents.mcp_servers.list()
        for s in resp.items:
            print(s.name, s.transport_type)

        # Retrieve a single MCP server
        server = client.agents.mcp_servers.retrieve(server_id=1)

        # Create an MCP server
        resp = client.agents.mcp_servers.create(
            name="My Server",
            transport_type="sse",
            url="https://example.com/mcp",
        )

        # Update an MCP server
        updated = client.agents.mcp_servers.update(
            server_id=1, name="New Name",
        )

        # Delete an MCP server
        client.agents.mcp_servers.delete(server_id=1)
    """

    def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> McpServerListResponse:
        """List all MCP servers.

        Args:
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            _MCP_SERVERS, params=params or None, model=McpServerListResponse,
        )

    def retrieve(self, server_id: int) -> McpServer:
        """Get details of an MCP server.

        Args:
            server_id: ID of the MCP server.
        """
        return self._client.get(
            f"{_MCP_SERVERS}/{server_id}", model=McpServer,
        )

    def create(
        self,
        *,
        name: str,
        transport_type: str,
        url: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        headers: Union[Dict, _NotGiven] = NOT_GIVEN,
        auth_type: Union[str, _NotGiven] = NOT_GIVEN,
        auth_config: Union[Dict, _NotGiven] = NOT_GIVEN,
    ) -> McpServerCreateResponse:
        """Create a new MCP server.

        Args:
            name: Server display name.
            transport_type: Transport type (e.g. ``"sse"``, ``"stdio"``).
            url: Server URL (required for SSE transport).
            description: Optional description.
            headers: Optional HTTP headers dict.
            auth_type: Optional authentication type.
            auth_config: Optional authentication configuration dict.
        """
        body: Dict[str, Any] = {
            "name": name,
            "transport_type": transport_type,
        }
        body.update(strip_not_given({
            "url": url,
            "description": description,
            "headers": headers,
            "auth_type": auth_type,
            "auth_config": auth_config,
        }))
        return self._client.post(
            _MCP_SERVERS, body=body, model=McpServerCreateResponse,
        )

    def update(
        self,
        server_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        transport_type: Union[str, _NotGiven] = NOT_GIVEN,
        url: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        headers: Union[Dict, _NotGiven] = NOT_GIVEN,
        auth_type: Union[str, _NotGiven] = NOT_GIVEN,
        auth_config: Union[Dict, _NotGiven] = NOT_GIVEN,
    ) -> McpServerCreateResponse:
        """Update an MCP server.

        Args:
            server_id: ID of the MCP server.
            name: New display name.
            transport_type: New transport type.
            url: New server URL.
            description: New description.
            headers: New HTTP headers dict.
            auth_type: New authentication type.
            auth_config: New authentication configuration dict.
        """
        body = strip_not_given({
            "name": name,
            "transport_type": transport_type,
            "url": url,
            "description": description,
            "headers": headers,
            "auth_type": auth_type,
            "auth_config": auth_config,
        })
        return self._client.patch(
            f"{_MCP_SERVERS}/{server_id}", body=body, model=McpServerCreateResponse,
        )

    def delete(self, server_id: int) -> McpServerDeleteResponse:
        """Delete an MCP server.

        Args:
            server_id: ID of the MCP server to delete.
        """
        return self._client.delete(
            f"{_MCP_SERVERS}/{server_id}", model=McpServerDeleteResponse,
        )


# ---------------------------------------------------------------------------
# McpServers (async)
# ---------------------------------------------------------------------------


class AsyncMcpServers(AsyncAPIResource):
    """Async variant of :class:`McpServers`."""

    async def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> McpServerListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            _MCP_SERVERS, params=params or None, model=McpServerListResponse,
        )

    async def retrieve(self, server_id: int) -> McpServer:
        return await self._client.get(
            f"{_MCP_SERVERS}/{server_id}", model=McpServer,
        )

    async def create(
        self,
        *,
        name: str,
        transport_type: str,
        url: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        headers: Union[Dict, _NotGiven] = NOT_GIVEN,
        auth_type: Union[str, _NotGiven] = NOT_GIVEN,
        auth_config: Union[Dict, _NotGiven] = NOT_GIVEN,
    ) -> McpServerCreateResponse:
        body: Dict[str, Any] = {
            "name": name,
            "transport_type": transport_type,
        }
        body.update(strip_not_given({
            "url": url,
            "description": description,
            "headers": headers,
            "auth_type": auth_type,
            "auth_config": auth_config,
        }))
        return await self._client.post(
            _MCP_SERVERS, body=body, model=McpServerCreateResponse,
        )

    async def update(
        self,
        server_id: int,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        transport_type: Union[str, _NotGiven] = NOT_GIVEN,
        url: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
        headers: Union[Dict, _NotGiven] = NOT_GIVEN,
        auth_type: Union[str, _NotGiven] = NOT_GIVEN,
        auth_config: Union[Dict, _NotGiven] = NOT_GIVEN,
    ) -> McpServerCreateResponse:
        body = strip_not_given({
            "name": name,
            "transport_type": transport_type,
            "url": url,
            "description": description,
            "headers": headers,
            "auth_type": auth_type,
            "auth_config": auth_config,
        })
        return await self._client.patch(
            f"{_MCP_SERVERS}/{server_id}", body=body, model=McpServerCreateResponse,
        )

    async def delete(self, server_id: int) -> McpServerDeleteResponse:
        return await self._client.delete(
            f"{_MCP_SERVERS}/{server_id}", model=McpServerDeleteResponse,
        )
