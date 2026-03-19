from __future__ import annotations

from .._base_client import AsyncAPIClient, SyncAPIClient


class SyncAPIResource:
    """Base class for synchronous API resource namespaces."""

    _client: SyncAPIClient

    def __init__(self, client: SyncAPIClient) -> None:
        self._client = client


class AsyncAPIResource:
    """Base class for asynchronous API resource namespaces."""

    _client: AsyncAPIClient

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client
