from __future__ import annotations

from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar, Any

if TYPE_CHECKING:
    from .._base_client import SyncAPIClient, AsyncAPIClient

from ..types.shared import PaginationMeta

T = TypeVar("T")


class SyncPage(Generic[T]):
    """Synchronous page of results with auto-paging support."""

    data: List[T]
    meta: PaginationMeta
    _client: SyncAPIClient
    _path: str
    _params: dict[str, Any]
    _model: type[T]

    def __init__(
        self,
        *,
        data: List[T],
        meta: PaginationMeta,
        client: SyncAPIClient,
        path: str,
        params: dict[str, Any],
        model: type[T],
    ) -> None:
        self.data = data
        self.meta = meta
        self._client = client
        self._path = path
        self._params = params
        self._model = model

    def has_next_page(self) -> bool:
        return self.meta.current_page < self.meta.last_page

    def next_page(self) -> SyncPage[T]:
        if not self.has_next_page():
            raise StopIteration("No more pages")
        params = {**self._params, "page": self.meta.current_page + 1}
        return self._client._get_page(
            path=self._path,
            params=params,
            model=self._model,
        )

    def auto_paging_iter(self):
        """Iterate over all items across all pages."""
        page = self
        while True:
            yield from page.data
            if not page.has_next_page():
                break
            page = page.next_page()

    def __iter__(self):
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)


class AsyncPage(Generic[T]):
    """Asynchronous page of results with auto-paging support."""

    data: List[T]
    meta: PaginationMeta
    _client: AsyncAPIClient
    _path: str
    _params: dict[str, Any]
    _model: type[T]

    def __init__(
        self,
        *,
        data: List[T],
        meta: PaginationMeta,
        client: AsyncAPIClient,
        path: str,
        params: dict[str, Any],
        model: type[T],
    ) -> None:
        self.data = data
        self.meta = meta
        self._client = client
        self._path = path
        self._params = params
        self._model = model

    def has_next_page(self) -> bool:
        return self.meta.current_page < self.meta.last_page

    async def next_page(self) -> AsyncPage[T]:
        if not self.has_next_page():
            raise StopAsyncIteration("No more pages")
        params = {**self._params, "page": self.meta.current_page + 1}
        return await self._client._get_page(
            path=self._path,
            params=params,
            model=self._model,
        )

    async def auto_paging_iter(self):
        """Iterate over all items across all pages."""
        page = self
        while True:
            for item in page.data:
                yield item
            if not page.has_next_page():
                break
            page = await page.next_page()

    def __iter__(self):
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)
