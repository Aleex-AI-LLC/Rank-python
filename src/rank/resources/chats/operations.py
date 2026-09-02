from __future__ import annotations

from typing import Any, Dict, List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.chat import AssignOperationsResponse, ChatOperationListResponse
from ...types.shared import MessageResponse
from .._base import AsyncAPIResource, SyncAPIResource

# ---------------------------------------------------------------------------
# Operations (sync)
# ---------------------------------------------------------------------------


class Operations(SyncAPIResource):
    """Manage operations (message exchanges) within a chat.

    Access via ``client.chats.operations``.

    Example::

        # List operations in a chat
        ops = client.chats.operations.list(chat_id=10)
        for op in ops.items:
            print(op.user_prompt[:50])

        # Assign operations to a chat
        client.chats.operations.assign(chat_id=10, operations=[4, 12, 33])

        # Remove an operation
        client.chats.operations.delete(chat_id=10, operation_id=4)
    """

    def list(
        self,
        chat_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ChatOperationListResponse:
        """List operations (conversations) in a chat.

        Args:
            chat_id: ID of the chat.
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"/chats/{chat_id}/operations",
            params=params or None,
            model=ChatOperationListResponse,
        )

    def assign(
        self,
        chat_id: int,
        *,
        operations: Union[int, List[int]],
    ) -> AssignOperationsResponse:
        """Assign one or more operations to a chat.

        Args:
            chat_id: ID of the chat.
            operations: A single operation ID or a list of operation IDs.
        """
        if isinstance(operations, int):
            body: Dict[str, Any] = {"operation": operations}
        else:
            body = {"operation": operations}
        return self._client.post(
            f"/chats/{chat_id}/operations",
            body=body,
            model=AssignOperationsResponse,
        )

    def delete(self, chat_id: int, operation_id: int) -> MessageResponse:
        """Remove an operation from a chat (soft delete).

        Args:
            chat_id: ID of the chat.
            operation_id: ID of the operation to remove.
        """
        return self._client.delete(
            f"/chats/{chat_id}/operations/{operation_id}",
            model=MessageResponse,
        )


# ---------------------------------------------------------------------------
# Operations (async)
# ---------------------------------------------------------------------------


class AsyncOperations(AsyncAPIResource):
    """Async variant of :class:`Operations`."""

    async def list(
        self,
        chat_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ChatOperationListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"/chats/{chat_id}/operations",
            params=params or None,
            model=ChatOperationListResponse,
        )

    async def assign(
        self,
        chat_id: int,
        *,
        operations: Union[int, List[int]],
    ) -> AssignOperationsResponse:
        if isinstance(operations, int):
            body: Dict[str, Any] = {"operation": operations}
        else:
            body = {"operation": operations}
        return await self._client.post(
            f"/chats/{chat_id}/operations",
            body=body,
            model=AssignOperationsResponse,
        )

    async def delete(self, chat_id: int, operation_id: int) -> MessageResponse:
        return await self._client.delete(
            f"/chats/{chat_id}/operations/{operation_id}",
            model=MessageResponse,
        )
