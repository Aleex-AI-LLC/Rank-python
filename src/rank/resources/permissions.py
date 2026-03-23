from __future__ import annotations

from typing import Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.shared import Permission, PermissionListResponse
from ._base import AsyncAPIResource, SyncAPIResource

_PERMISSIONS = "/permissions"


# ---------------------------------------------------------------------------
# Permissions (sync)
# ---------------------------------------------------------------------------


class Permissions(SyncAPIResource):
    """API permission listing.

    Access via ``client.permissions``.

    Example::

        perms = client.permissions.list()
        for p in perms.items:
            print(p.name, p.tag)
    """

    def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> PermissionListResponse:
        """List all available API permissions.

        Args:
            page: Page number.
        """
        params = strip_not_given({"page": page})
        return self._client.get(
            _PERMISSIONS, params=params or None, model=PermissionListResponse,
        )

    def retrieve(self, permission_id: int) -> Permission:
        """Get a single permission by ID.

        Args:
            permission_id: ID of the permission.
        """
        return self._client.get(
            f"{_PERMISSIONS}/{permission_id}", model=Permission,
        )


# ---------------------------------------------------------------------------
# Permissions (async)
# ---------------------------------------------------------------------------


class AsyncPermissions(AsyncAPIResource):
    """Async variant of :class:`Permissions`."""

    async def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> PermissionListResponse:
        params = strip_not_given({"page": page})
        return await self._client.get(
            _PERMISSIONS, params=params or None, model=PermissionListResponse,
        )

    async def retrieve(self, permission_id: int) -> Permission:
        return await self._client.get(
            f"{_PERMISSIONS}/{permission_id}", model=Permission,
        )
