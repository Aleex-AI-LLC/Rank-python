from __future__ import annotations

from typing import Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.operation import OperationLog, OperationLogListResponse
from ...types.shared import MessageResponse
from .._base import AsyncAPIResource, SyncAPIResource

_OPERATIONS = "/operations"


# ---------------------------------------------------------------------------
# OperationLogs (sync)
# ---------------------------------------------------------------------------


class OperationLogs(SyncAPIResource):
    """Global operation log — list, retrieve, and delete operation entries.

    Access via ``client.chats.operation_logs``.

    Example::

        # List all operations
        ops = client.chats.operation_logs.list()
        for op in ops.items:
            print(op.model_name, op.total_tokens)

        # Get a single operation
        op = client.chats.operation_logs.retrieve(42)
    """

    def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        type: Union[str, _NotGiven] = NOT_GIVEN,
        operation_type: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> OperationLogListResponse:
        """List operation log entries.

        Args:
            page: Page number.
            per_page: Items per page.
            type: Filter by type (e.g. ``"chat"``, ``"pentest"``).
            operation_type: Filter by operation type.
        """
        params = strip_not_given({
            "page": page,
            "per_page": per_page,
            "type": type,
            "operation_type": operation_type,
        })
        return self._client.get(
            _OPERATIONS, params=params or None, model=OperationLogListResponse,
        )

    def retrieve(self, operation_id: int) -> OperationLog:
        """Get a single operation log entry.

        Args:
            operation_id: ID of the operation.
        """
        return self._client.get(f"{_OPERATIONS}/{operation_id}", model=OperationLog)

    def delete(self, operation_id: int) -> MessageResponse:
        """Delete an operation log entry.

        Args:
            operation_id: ID of the operation.
        """
        return self._client.delete(
            f"{_OPERATIONS}/{operation_id}", model=MessageResponse,
        )


# ---------------------------------------------------------------------------
# OperationLogs (async)
# ---------------------------------------------------------------------------


class AsyncOperationLogs(AsyncAPIResource):
    """Async variant of :class:`OperationLogs`."""

    async def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
        type: Union[str, _NotGiven] = NOT_GIVEN,
        operation_type: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> OperationLogListResponse:
        params = strip_not_given({
            "page": page,
            "per_page": per_page,
            "type": type,
            "operation_type": operation_type,
        })
        return await self._client.get(
            _OPERATIONS, params=params or None, model=OperationLogListResponse,
        )

    async def retrieve(self, operation_id: int) -> OperationLog:
        return await self._client.get(
            f"{_OPERATIONS}/{operation_id}", model=OperationLog,
        )

    async def delete(self, operation_id: int) -> MessageResponse:
        return await self._client.delete(
            f"{_OPERATIONS}/{operation_id}", model=MessageResponse,
        )
