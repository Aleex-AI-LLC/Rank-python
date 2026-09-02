from __future__ import annotations

from typing import List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.shared import MessageResponse, Permission
from ...types.team import RoleListResponse, TeamRole
from .._base import AsyncAPIResource, SyncAPIResource

# ---------------------------------------------------------------------------
# Roles (sync)
# ---------------------------------------------------------------------------


class Roles(SyncAPIResource):
    """Manage custom roles within a team.

    Access via ``client.teams.roles``.

    Example::

        # Create a role
        role = client.teams.roles.create(
            team_id=1,
            role_name="Reviewer",
            color="#3498db",
        )

        # Assign permissions
        client.teams.roles.add_permissions(
            team_id=1, role_id=role.id, permission_ids=[229, 212],
        )

        # Assign role to a member
        client.teams.roles.assign_to_member(
            team_id=1, user_id=42, role_id=role.id,
        )
    """

    # -- CRUD ---------------------------------------------------------------

    def list(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> RoleListResponse:
        """List active roles in a team.

        Args:
            team_id: ID of the team.
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"/teams/{team_id}/roles",
            params=params or None,
            model=RoleListResponse,
        )

    def create(
        self,
        team_id: int,
        *,
        role_name: str,
        color: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> TeamRole:
        """Create a new role in a team.

        Args:
            team_id: ID of the team.
            role_name: Display name for the role.
            color: Hex color code (e.g. ``"#FF5733"``).
            description: Optional description.

        Returns:
            The newly created role.
        """
        body = {"role_name": role_name}
        body.update(strip_not_given({"color": color, "description": description}))
        return self._client.post(
            f"/teams/{team_id}/roles", body=body, model=TeamRole,
        )

    def retrieve(self, team_id: int, role_id: int) -> TeamRole:
        """Get details of a specific role.

        Args:
            team_id: ID of the team.
            role_id: ID of the role.
        """
        return self._client.get(
            f"/teams/{team_id}/roles/{role_id}", model=TeamRole,
        )

    def update(
        self,
        team_id: int,
        role_id: int,
        *,
        role_name: Union[str, _NotGiven] = NOT_GIVEN,
        color: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> TeamRole:
        """Update a role's properties.

        Args:
            team_id: ID of the team.
            role_id: ID of the role.
            role_name: New display name.
            color: New hex color code.
            description: New description.

        Returns:
            The updated role.
        """
        body = strip_not_given({
            "role_name": role_name,
            "color": color,
            "description": description,
        })
        return self._client.put(
            f"/teams/{team_id}/roles/{role_id}", body=body, model=TeamRole,
        )

    def delete(self, team_id: int, role_id: int) -> MessageResponse:
        """Soft-delete a role.

        The role can be restored later with :meth:`restore`.

        Args:
            team_id: ID of the team.
            role_id: ID of the role.
        """
        return self._client.delete(
            f"/teams/{team_id}/roles/{role_id}", model=MessageResponse,
        )

    # -- Soft-delete lifecycle ----------------------------------------------

    def restore(self, team_id: int, role_id: int) -> TeamRole:
        """Restore a previously soft-deleted role.

        Returns the restored role with its permissions.

        Args:
            team_id: ID of the team.
            role_id: ID of the deleted role.
        """
        return self._client.post(
            f"/teams/{team_id}/roles/{role_id}/restore", model=TeamRole,
        )

    def force_delete(self, team_id: int, role_id: int) -> MessageResponse:
        """Permanently delete a role.

        This action is irreversible. The role must already be soft-deleted.

        Args:
            team_id: ID of the team.
            role_id: ID of the role to permanently delete.
        """
        return self._client.delete(
            f"/teams/{team_id}/roles/{role_id}/force", model=MessageResponse,
        )

    def list_deleted(self, team_id: int) -> RoleListResponse:
        """List soft-deleted roles in a team.

        Args:
            team_id: ID of the team.
        """
        return self._client.get(
            f"/teams/{team_id}/roles/deleted", model=RoleListResponse,
        )

    # -- My roles -----------------------------------------------------------

    def my_roles(self, team_id: int) -> List[TeamRole]:
        """List the authenticated user's roles in a team.

        The API returns a flat list (not paginated).

        Args:
            team_id: ID of the team.
        """
        return self._client.get_list(
            f"/teams/{team_id}/my-roles", model=TeamRole,
        )

    # -- Permissions --------------------------------------------------------

    def list_permissions(self, team_id: int, role_id: int) -> List[Permission]:
        """List permissions assigned to a role.

        The API returns a flat list of permission objects.

        Args:
            team_id: ID of the team.
            role_id: ID of the role.
        """
        return self._client.get_list(
            f"/teams/{team_id}/roles/{role_id}/permissions",
            model=Permission,
        )

    def add_permissions(
        self,
        team_id: int,
        role_id: int,
        *,
        permission_ids: List[int],
    ) -> List[Permission]:
        """Add permissions to a role.

        Returns the updated list of permissions for the role.

        Args:
            team_id: ID of the team.
            role_id: ID of the role.
            permission_ids: List of permission IDs to assign.
        """
        return self._client.post_list(
            f"/teams/{team_id}/roles/{role_id}/permissions",
            body={"permission_ids": permission_ids},
            model=Permission,
        )

    def remove_permission(
        self,
        team_id: int,
        role_id: int,
        permission_id: int,
    ) -> MessageResponse:
        """Remove a single permission from a role.

        Args:
            team_id: ID of the team.
            role_id: ID of the role.
            permission_id: ID of the permission to remove.
        """
        return self._client.delete(
            f"/teams/{team_id}/roles/{role_id}/permissions/{permission_id}",
            model=MessageResponse,
        )

    # -- Member role assignment ---------------------------------------------

    def assign_to_member(
        self,
        team_id: int,
        *,
        user_id: int,
        role_id: int,
    ) -> MessageResponse:
        """Assign a role to a team member.

        Args:
            team_id: ID of the team.
            user_id: ID of the user.
            role_id: ID of the role to assign.
        """
        return self._client.post(
            f"/teams/{team_id}/roles/assign",
            body={"user_id": user_id, "role_id": role_id},
            model=MessageResponse,
        )

    def remove_from_member(
        self,
        team_id: int,
        *,
        user_id: int,
        role_id: int,
    ) -> MessageResponse:
        """Remove a role from a team member.

        Args:
            team_id: ID of the team.
            user_id: ID of the user.
            role_id: ID of the role to remove.
        """
        return self._client.post(
            f"/teams/{team_id}/roles/remove",
            body={"user_id": user_id, "role_id": role_id},
            model=MessageResponse,
        )


# ---------------------------------------------------------------------------
# Roles (async)
# ---------------------------------------------------------------------------


class AsyncRoles(AsyncAPIResource):
    """Async variant of :class:`Roles`."""

    # -- CRUD ---------------------------------------------------------------

    async def list(
        self,
        team_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> RoleListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"/teams/{team_id}/roles",
            params=params or None,
            model=RoleListResponse,
        )

    async def create(
        self,
        team_id: int,
        *,
        role_name: str,
        color: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> TeamRole:
        body = {"role_name": role_name}
        body.update(strip_not_given({"color": color, "description": description}))
        return await self._client.post(
            f"/teams/{team_id}/roles", body=body, model=TeamRole,
        )

    async def retrieve(self, team_id: int, role_id: int) -> TeamRole:
        return await self._client.get(
            f"/teams/{team_id}/roles/{role_id}", model=TeamRole,
        )

    async def update(
        self,
        team_id: int,
        role_id: int,
        *,
        role_name: Union[str, _NotGiven] = NOT_GIVEN,
        color: Union[str, _NotGiven] = NOT_GIVEN,
        description: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> TeamRole:
        body = strip_not_given({
            "role_name": role_name,
            "color": color,
            "description": description,
        })
        return await self._client.put(
            f"/teams/{team_id}/roles/{role_id}", body=body, model=TeamRole,
        )

    async def delete(self, team_id: int, role_id: int) -> MessageResponse:
        return await self._client.delete(
            f"/teams/{team_id}/roles/{role_id}", model=MessageResponse,
        )

    # -- Soft-delete lifecycle ----------------------------------------------

    async def restore(self, team_id: int, role_id: int) -> TeamRole:
        return await self._client.post(
            f"/teams/{team_id}/roles/{role_id}/restore", model=TeamRole,
        )

    async def force_delete(self, team_id: int, role_id: int) -> MessageResponse:
        return await self._client.delete(
            f"/teams/{team_id}/roles/{role_id}/force", model=MessageResponse,
        )

    async def list_deleted(self, team_id: int) -> RoleListResponse:
        return await self._client.get(
            f"/teams/{team_id}/roles/deleted", model=RoleListResponse,
        )

    # -- My roles -----------------------------------------------------------

    async def my_roles(self, team_id: int) -> List[TeamRole]:
        return await self._client.get_list(
            f"/teams/{team_id}/my-roles", model=TeamRole,
        )

    # -- Permissions --------------------------------------------------------

    async def list_permissions(
        self, team_id: int, role_id: int,
    ) -> List[Permission]:
        return await self._client.get_list(
            f"/teams/{team_id}/roles/{role_id}/permissions",
            model=Permission,
        )

    async def add_permissions(
        self,
        team_id: int,
        role_id: int,
        *,
        permission_ids: List[int],
    ) -> List[Permission]:
        return await self._client.post_list(
            f"/teams/{team_id}/roles/{role_id}/permissions",
            body={"permission_ids": permission_ids},
            model=Permission,
        )

    async def remove_permission(
        self,
        team_id: int,
        role_id: int,
        permission_id: int,
    ) -> MessageResponse:
        return await self._client.delete(
            f"/teams/{team_id}/roles/{role_id}/permissions/{permission_id}",
            model=MessageResponse,
        )

    # -- Member role assignment ---------------------------------------------

    async def assign_to_member(
        self,
        team_id: int,
        *,
        user_id: int,
        role_id: int,
    ) -> MessageResponse:
        return await self._client.post(
            f"/teams/{team_id}/roles/assign",
            body={"user_id": user_id, "role_id": role_id},
            model=MessageResponse,
        )

    async def remove_from_member(
        self,
        team_id: int,
        *,
        user_id: int,
        role_id: int,
    ) -> MessageResponse:
        return await self._client.post(
            f"/teams/{team_id}/roles/remove",
            body={"user_id": user_id, "role_id": role_id},
            model=MessageResponse,
        )
