from __future__ import annotations

import os
from typing import Any, Dict, Optional

from ._base_client import AsyncAPIClient, SyncAPIClient
from ._constants import (
    AGENT_BASE_URL,
    AGENT_BASE_URL_ENV_VAR,
    API_KEY_ENV_VAR,
    API_PREFIX,
    BASE_URL,
    BASE_URL_ENV_VAR,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
)
from .resources.agents import Agents, AsyncAgents
from .resources.auth import AsyncAuth, Auth
from .resources.chats import AsyncChats, Chats
from .resources.pentests import AsyncPentests, Pentests
from .resources.teams import AsyncTeams, Teams


class Rank:
    """Synchronous client for the Rank API.

    Usage:
        import rank

        client = rank.Rank(api_key="rk_...")
        pentests = client.pentests.list()
        print(pentests.data)

    The client connects to two backends:
    - PHP backend (base_url): REST API for all CRUD resources.
    - Go backend (agent_base_url): AI chat streaming, reports, pentest control.
    """

    _api_client: SyncAPIClient
    _agent_client: SyncAPIClient

    auth: Auth
    pentests: Pentests
    teams: Teams
    agents: Agents
    chats: Chats

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        agent_base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        resolved_api_key = api_key or os.environ.get(API_KEY_ENV_VAR)
        if not resolved_api_key:
            raise ValueError(
                f"API key is required. Pass it as api_key= or set the {API_KEY_ENV_VAR} environment variable."
            )

        resolved_base_url = base_url or os.environ.get(BASE_URL_ENV_VAR) or BASE_URL
        resolved_agent_url = agent_base_url or os.environ.get(AGENT_BASE_URL_ENV_VAR) or AGENT_BASE_URL

        self._api_client = SyncAPIClient(
            base_url=resolved_base_url,
            api_key=resolved_api_key,
            api_prefix=API_PREFIX,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=custom_headers,
        )

        self._agent_client = SyncAPIClient(
            base_url=resolved_agent_url,
            api_key=resolved_api_key,
            api_prefix="",
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=custom_headers,
        )

        self._init_resources()

    def _init_resources(self) -> None:
        self.auth = Auth(self._api_client)
        self.pentests = Pentests(self._api_client, self._agent_client)
        self.teams = Teams(self._api_client)
        self.agents = Agents(self._api_client)
        self.chats = Chats(self._api_client)

    @property
    def api_client(self) -> SyncAPIClient:
        """Access the underlying PHP backend HTTP client."""
        return self._api_client

    @property
    def agent_client(self) -> SyncAPIClient:
        """Access the underlying Go backend HTTP client."""
        return self._agent_client

    def close(self) -> None:
        """Close underlying HTTP connections."""
        self._api_client.close()
        self._agent_client.close()

    def __enter__(self) -> Rank:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"Rank(base_url={self._api_client._base_url!r})"


class AsyncRank:
    """Asynchronous client for the Rank API.

    Usage:
        import rank

        client = rank.AsyncRank(api_key="rk_...")
        pentests = await client.pentests.list()
        print(pentests.data)

    The client connects to two backends:
    - PHP backend (base_url): REST API for all CRUD resources.
    - Go backend (agent_base_url): AI chat streaming, reports, pentest control.
    """

    _api_client: AsyncAPIClient
    _agent_client: AsyncAPIClient

    auth: AsyncAuth
    pentests: AsyncPentests
    teams: AsyncTeams
    agents: AsyncAgents
    chats: AsyncChats

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        agent_base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        resolved_api_key = api_key or os.environ.get(API_KEY_ENV_VAR)
        if not resolved_api_key:
            raise ValueError(
                f"API key is required. Pass it as api_key= or set the {API_KEY_ENV_VAR} environment variable."
            )

        resolved_base_url = base_url or os.environ.get(BASE_URL_ENV_VAR) or BASE_URL
        resolved_agent_url = agent_base_url or os.environ.get(AGENT_BASE_URL_ENV_VAR) or AGENT_BASE_URL

        self._api_client = AsyncAPIClient(
            base_url=resolved_base_url,
            api_key=resolved_api_key,
            api_prefix=API_PREFIX,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=custom_headers,
        )

        self._agent_client = AsyncAPIClient(
            base_url=resolved_agent_url,
            api_key=resolved_api_key,
            api_prefix="",
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=custom_headers,
        )

        self._init_resources()

    def _init_resources(self) -> None:
        self.auth = AsyncAuth(self._api_client)
        self.pentests = AsyncPentests(self._api_client, self._agent_client)
        self.teams = AsyncTeams(self._api_client)
        self.agents = AsyncAgents(self._api_client)
        self.chats = AsyncChats(self._api_client)

    @property
    def api_client(self) -> AsyncAPIClient:
        """Access the underlying PHP backend HTTP client."""
        return self._api_client

    @property
    def agent_client(self) -> AsyncAPIClient:
        """Access the underlying Go backend HTTP client."""
        return self._agent_client

    async def close(self) -> None:
        """Close underlying HTTP connections."""
        await self._api_client.close()
        await self._agent_client.close()

    async def __aenter__(self) -> AsyncRank:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def __repr__(self) -> str:
        return f"AsyncRank(base_url={self._api_client._base_url!r})"
