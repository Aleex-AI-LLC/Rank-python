from __future__ import annotations

from typing import Union

from ..._base_client import AsyncAPIClient, SyncAPIClient
from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.chat import (
    Chat,
    ChatArchiveResponse,
    ChatListResponse,
    ChatMineResponse,
    ChatSharedResponse,
    ChatShareResponse,
    ChatUnshareResponse,
)
from ...types.shared import MessageResponse
from .._base import AsyncAPIResource, SyncAPIResource
from .operation_logs import AsyncOperationLogs, OperationLogs
from .operations import AsyncOperations, Operations

_CHATS = "/chats"


# ---------------------------------------------------------------------------
# Chats (sync)
# ---------------------------------------------------------------------------


class Chats(SyncAPIResource):
    """Chat management resource — CRUD, archiving, sharing, and operations.

    Access via ``client.chats``.

    Example::

        # List all chats (own + shared)
        chats = client.chats.list()

        # Create a new chat
        chat = client.chats.create(nombre="Security Research")

        # Archive a chat
        client.chats.archive(chat_id=chat.id)

        # Share with a team
        client.chats.share(chat_id=chat.id, team_id=4)

        # List operations (message history)
        ops = client.chats.operations.list(chat_id=chat.id)
    """

    operations: Operations
    operation_logs: OperationLogs

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.operations = Operations(client)
        self.operation_logs = OperationLogs(client)

    # -- CRUD ---------------------------------------------------------------

    def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        include_archived: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ChatListResponse:
        """List all chats (own + shared) for the authenticated user.

        Args:
            page: Page number.
            per_page: Items per page.
            include_archived: Include archived chats (default ``False``).
        """
        params = strip_not_given({
            "page": page,
            "per_page": per_page,
            "include_archived": include_archived,
        })
        return self._client.get(_CHATS, params=params or None, model=ChatListResponse)

    def mine(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        include_archived: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ChatMineResponse:
        """List only the authenticated user's own chats.

        Args:
            page: Page number.
            per_page: Items per page.
            include_archived: Include archived chats.
        """
        params = strip_not_given({
            "page": page,
            "per_page": per_page,
            "include_archived": include_archived,
        })
        return self._client.get(
            f"{_CHATS}/mine", params=params or None, model=ChatMineResponse,
        )

    def shared(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        include_archived: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ChatSharedResponse:
        """List chats shared with the authenticated user's teams.

        Args:
            page: Page number.
            per_page: Items per page.
            include_archived: Include archived chats.
        """
        params = strip_not_given({
            "page": page,
            "per_page": per_page,
            "include_archived": include_archived,
        })
        return self._client.get(
            f"{_CHATS}/shared", params=params or None, model=ChatSharedResponse,
        )

    def retrieve(self, chat_id: int) -> Chat:
        """Get full details of a chat.

        Args:
            chat_id: ID of the chat.
        """
        return self._client.get(f"{_CHATS}/{chat_id}", model=Chat)

    def create(self, *, nombre: str) -> Chat:
        """Create a new chat.

        Args:
            nombre: Chat display name.

        Returns:
            The newly created chat.
        """
        return self._client.post(_CHATS, body={"nombre": nombre}, model=Chat)

    def update(self, chat_id: int, *, nombre: str) -> Chat:
        """Rename a chat.

        Args:
            chat_id: ID of the chat.
            nombre: New chat name.

        Returns:
            The updated chat.
        """
        return self._client.patch(
            f"{_CHATS}/{chat_id}", body={"nombre": nombre}, model=Chat,
        )

    def delete(self, chat_id: int) -> MessageResponse:
        """Soft-delete a chat.

        Args:
            chat_id: ID of the chat.
        """
        return self._client.delete(f"{_CHATS}/{chat_id}", model=MessageResponse)

    # -- Actions ------------------------------------------------------------

    def archive(self, chat_id: int) -> ChatArchiveResponse:
        """Archive a chat.

        Args:
            chat_id: ID of the chat to archive.
        """
        return self._client.patch(
            f"{_CHATS}/{chat_id}/archive", model=ChatArchiveResponse,
        )

    def unarchive(self, chat_id: int) -> ChatArchiveResponse:
        """Unarchive a previously archived chat.

        Args:
            chat_id: ID of the chat to unarchive.
        """
        return self._client.patch(
            f"{_CHATS}/{chat_id}/unarchive", model=ChatArchiveResponse,
        )

    # -- Sharing ------------------------------------------------------------

    def share(self, chat_id: int, *, team_id: int) -> ChatShareResponse:
        """Share a chat with a team.

        Args:
            chat_id: ID of the chat.
            team_id: ID of the team to share with.
        """
        return self._client.post(
            f"{_CHATS}/{chat_id}/share",
            body={"team_id": team_id},
            model=ChatShareResponse,
        )

    def unshare(self, chat_id: int, *, team_id: int) -> ChatUnshareResponse:
        """Stop sharing a chat with a specific team.

        Args:
            chat_id: ID of the chat.
            team_id: ID of the team to unshare from.
        """
        return self._client.delete(
            f"{_CHATS}/{chat_id}/share",
            body={"team_id": team_id},
            model=ChatUnshareResponse,
        )

    def unshare_all(self, chat_id: int) -> MessageResponse:
        """Stop sharing a chat with all teams.

        Args:
            chat_id: ID of the chat.
        """
        return self._client.delete(
            f"{_CHATS}/{chat_id}/share/all", model=MessageResponse,
        )


# ---------------------------------------------------------------------------
# Chats (async)
# ---------------------------------------------------------------------------


class AsyncChats(AsyncAPIResource):
    """Async variant of :class:`Chats`."""

    operations: AsyncOperations
    operation_logs: AsyncOperationLogs

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.operations = AsyncOperations(client)
        self.operation_logs = AsyncOperationLogs(client)

    # -- CRUD ---------------------------------------------------------------

    async def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        include_archived: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ChatListResponse:
        params = strip_not_given({
            "page": page,
            "per_page": per_page,
            "include_archived": include_archived,
        })
        return await self._client.get(
            _CHATS, params=params or None, model=ChatListResponse,
        )

    async def mine(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        include_archived: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ChatMineResponse:
        params = strip_not_given({
            "page": page,
            "per_page": per_page,
            "include_archived": include_archived,
        })
        return await self._client.get(
            f"{_CHATS}/mine", params=params or None, model=ChatMineResponse,
        )

    async def shared(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        include_archived: Union[bool, _NotGiven] = NOT_GIVEN,
    ) -> ChatSharedResponse:
        params = strip_not_given({
            "page": page,
            "per_page": per_page,
            "include_archived": include_archived,
        })
        return await self._client.get(
            f"{_CHATS}/shared", params=params or None, model=ChatSharedResponse,
        )

    async def retrieve(self, chat_id: int) -> Chat:
        return await self._client.get(f"{_CHATS}/{chat_id}", model=Chat)

    async def create(self, *, nombre: str) -> Chat:
        return await self._client.post(
            _CHATS, body={"nombre": nombre}, model=Chat,
        )

    async def update(self, chat_id: int, *, nombre: str) -> Chat:
        return await self._client.patch(
            f"{_CHATS}/{chat_id}", body={"nombre": nombre}, model=Chat,
        )

    async def delete(self, chat_id: int) -> MessageResponse:
        return await self._client.delete(
            f"{_CHATS}/{chat_id}", model=MessageResponse,
        )

    # -- Actions ------------------------------------------------------------

    async def archive(self, chat_id: int) -> ChatArchiveResponse:
        return await self._client.patch(
            f"{_CHATS}/{chat_id}/archive", model=ChatArchiveResponse,
        )

    async def unarchive(self, chat_id: int) -> ChatArchiveResponse:
        return await self._client.patch(
            f"{_CHATS}/{chat_id}/unarchive", model=ChatArchiveResponse,
        )

    # -- Sharing ------------------------------------------------------------

    async def share(self, chat_id: int, *, team_id: int) -> ChatShareResponse:
        return await self._client.post(
            f"{_CHATS}/{chat_id}/share",
            body={"team_id": team_id},
            model=ChatShareResponse,
        )

    async def unshare(self, chat_id: int, *, team_id: int) -> ChatUnshareResponse:
        return await self._client.delete(
            f"{_CHATS}/{chat_id}/share",
            body={"team_id": team_id},
            model=ChatUnshareResponse,
        )

    async def unshare_all(self, chat_id: int) -> MessageResponse:
        return await self._client.delete(
            f"{_CHATS}/{chat_id}/share/all", model=MessageResponse,
        )
