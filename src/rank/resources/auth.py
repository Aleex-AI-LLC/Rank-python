from __future__ import annotations

from typing import List, Union

from .._base_client import AsyncAPIClient, SyncAPIClient
from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.auth import (
    ApiTokenCreateResponse,
    ApiTokenListResponse,
    AvailablePermissionsResponse,
    ProfileUpdateResponse,
    SessionListResponse,
    UpdateEmailResponse,
    UpdateUsernameResponse,
    User,
)
from ..types.shared import MessageResponse
from ._base import AsyncAPIResource, SyncAPIResource

_AUTH_ME = "/auth/me"
_AUTH_PROFILE = "/auth/profile"
_AUTH_EMAIL = "/auth/email"
_AUTH_PASSWORD = "/auth/password"
_AUTH_USERNAME = "/auth/username"
_AUTH_SESSIONS = "/auth/sessions"
_AUTH_SESSIONS_ACTIVE = "/auth/sessions-active"
_AUTH_SESSION = "/auth/session"
_AUTH_API_TOKENS = "/auth/api-tokens"
_AUTH_API_TOKENS_PERMISSIONS = "/auth/api-tokens/available-permissions"


# ---------------------------------------------------------------------------
# ApiTokens (sub-resource)
# ---------------------------------------------------------------------------


class ApiTokens(SyncAPIResource):
    """Manage API tokens for the authenticated user.

    Access via ``client.auth.api_tokens``.
    """

    def list(
        self,
        *,
        include_revoked: Union[bool, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ApiTokenListResponse:
        """List API tokens for the current user.

        Args:
            include_revoked: When ``True``, include revoked tokens.
            page: Page number for pagination.
            per_page: Items per page.

        Returns:
            Paginated token list with usage limits.
        """
        params = strip_not_given(
            {"include_revoked": include_revoked, "page": page, "per_page": per_page}
        )
        return self._client.get(_AUTH_API_TOKENS, params=params or None, model=ApiTokenListResponse)

    def create(
        self,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        permission_ids: Union[List[int], _NotGiven] = NOT_GIVEN,
        tags: Union[List[str], _NotGiven] = NOT_GIVEN,
        team_ids: Union[List[int], _NotGiven] = NOT_GIVEN,
    ) -> ApiTokenCreateResponse:
        """Create a new API token.

        The plaintext token is returned **only once** in the response.
        Omitting all scope parameters creates a full-access token.

        Args:
            name: Human-readable name for the token (max 100 chars).
            permission_ids: Permission IDs to scope the token.
            tags: Permission tag names to scope the token (e.g. ``["pentest", "team"]``).
                Combined with ``permission_ids`` as a union.
            team_ids: Team IDs to restrict the token to specific teams.

        Returns:
            The created token info including the plaintext token value.
        """
        body = strip_not_given(
            {"name": name, "permission_ids": permission_ids, "tags": tags, "team_ids": team_ids}
        )
        return self._client.post(_AUTH_API_TOKENS, body=body, model=ApiTokenCreateResponse)

    def update(
        self,
        *,
        token_id: int,
        name: str,
    ) -> MessageResponse:
        """Rename an existing API token.

        Args:
            token_id: ID of the token to update.
            name: New name for the token.
        """
        return self._client.put(
            _AUTH_API_TOKENS, body={"token_id": token_id, "name": name}, model=MessageResponse
        )

    def revoke(
        self,
        *,
        token_id: int,
    ) -> MessageResponse:
        """Revoke an API token.

        Args:
            token_id: ID of the token to revoke.
        """
        return self._client.delete(
            _AUTH_API_TOKENS, body={"token_id": token_id}, model=MessageResponse
        )

    def available_permissions(self) -> AvailablePermissionsResponse:
        """List permissions available for scoping new API tokens."""
        return self._client.get(
            _AUTH_API_TOKENS_PERMISSIONS, model=AvailablePermissionsResponse
        )


class AsyncApiTokens(AsyncAPIResource):
    """Async variant of :class:`ApiTokens`."""

    async def list(
        self,
        *,
        include_revoked: Union[bool, _NotGiven] = NOT_GIVEN,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ApiTokenListResponse:
        params = strip_not_given(
            {"include_revoked": include_revoked, "page": page, "per_page": per_page}
        )
        return await self._client.get(
            _AUTH_API_TOKENS, params=params or None, model=ApiTokenListResponse
        )

    async def create(
        self,
        *,
        name: Union[str, _NotGiven] = NOT_GIVEN,
        permission_ids: Union[List[int], _NotGiven] = NOT_GIVEN,
        tags: Union[List[str], _NotGiven] = NOT_GIVEN,
        team_ids: Union[List[int], _NotGiven] = NOT_GIVEN,
    ) -> ApiTokenCreateResponse:
        body = strip_not_given(
            {"name": name, "permission_ids": permission_ids, "tags": tags, "team_ids": team_ids}
        )
        return await self._client.post(
            _AUTH_API_TOKENS, body=body, model=ApiTokenCreateResponse
        )

    async def update(
        self,
        *,
        token_id: int,
        name: str,
    ) -> MessageResponse:
        return await self._client.put(
            _AUTH_API_TOKENS, body={"token_id": token_id, "name": name}, model=MessageResponse
        )

    async def revoke(
        self,
        *,
        token_id: int,
    ) -> MessageResponse:
        return await self._client.delete(
            _AUTH_API_TOKENS, body={"token_id": token_id}, model=MessageResponse
        )

    async def available_permissions(self) -> AvailablePermissionsResponse:
        return await self._client.get(
            _AUTH_API_TOKENS_PERMISSIONS, model=AvailablePermissionsResponse
        )


# ---------------------------------------------------------------------------
# Auth (main resource)
# ---------------------------------------------------------------------------


class Auth(SyncAPIResource):
    """Authentication and profile management.

    Access via ``client.auth``.

    Example::

        user = client.auth.me()
        print(user.email)

        tokens = client.auth.api_tokens.list()
        for t in tokens.items:
            print(t.name)
    """

    api_tokens: ApiTokens

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.api_tokens = ApiTokens(client)

    def me(self) -> User:
        """Retrieve the authenticated user's full profile.

        Includes tier, trial, subscription, teams, and assigned resources.
        """
        return self._client.get(_AUTH_ME, model=User)

    def update_profile(
        self,
        *,
        country: Union[str, _NotGiven] = NOT_GIVEN,
        region: Union[str, _NotGiven] = NOT_GIVEN,
        language: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> ProfileUpdateResponse:
        """Update the user's profile fields.

        Args:
            country: ISO country code (e.g. ``"ES"``).
            region: Region or state name.
            language: Language code (e.g. ``"es"``).

        Returns:
            The raw user row with updated fields.  Use :meth:`me` to get the
            full enriched profile after updating.
        """
        body = strip_not_given({"country": country, "region": region, "language": language})
        return self._client.patch(_AUTH_PROFILE, body=body, model=ProfileUpdateResponse)

    def update_email(
        self,
        *,
        email: str,
    ) -> UpdateEmailResponse:
        """Change the account email address.

        A verification email is sent to the new address.

        Args:
            email: The new email address.
        """
        return self._client.patch(_AUTH_EMAIL, body={"email": email}, model=UpdateEmailResponse)

    def update_password(
        self,
        *,
        current_password: str,
        new_password: str,
    ) -> MessageResponse:
        """Change the account password.

        Args:
            current_password: The current password for verification.
            new_password: The new password.
        """
        return self._client.patch(
            _AUTH_PASSWORD,
            body={"current_password": current_password, "new_password": new_password},
            model=MessageResponse,
        )

    def update_username(
        self,
        *,
        username: str,
    ) -> UpdateUsernameResponse:
        """Change the account username.

        Args:
            username: The new username.
        """
        return self._client.patch(
            _AUTH_USERNAME, body={"username": username}, model=UpdateUsernameResponse
        )

    def sessions(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> SessionListResponse:
        """List all sessions (active, expired, and revoked).

        Args:
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(_AUTH_SESSIONS, params=params or None, model=SessionListResponse)

    def active_sessions(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> SessionListResponse:
        """List only active (non-expired, non-revoked) sessions.

        Args:
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            _AUTH_SESSIONS_ACTIVE, params=params or None, model=SessionListResponse
        )

    def revoke_session(
        self,
        *,
        session_id: int,
    ) -> MessageResponse:
        """Revoke a specific session by its ID.

        Args:
            session_id: The session to revoke.
        """
        return self._client.delete(
            _AUTH_SESSION, body={"session_id": session_id}, model=MessageResponse
        )


class AsyncAuth(AsyncAPIResource):
    """Async variant of :class:`Auth`."""

    api_tokens: AsyncApiTokens

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.api_tokens = AsyncApiTokens(client)

    async def me(self) -> User:
        return await self._client.get(_AUTH_ME, model=User)

    async def update_profile(
        self,
        *,
        country: Union[str, _NotGiven] = NOT_GIVEN,
        region: Union[str, _NotGiven] = NOT_GIVEN,
        language: Union[str, _NotGiven] = NOT_GIVEN,
    ) -> ProfileUpdateResponse:
        body = strip_not_given({"country": country, "region": region, "language": language})
        return await self._client.patch(_AUTH_PROFILE, body=body, model=ProfileUpdateResponse)

    async def update_email(
        self,
        *,
        email: str,
    ) -> UpdateEmailResponse:
        return await self._client.patch(
            _AUTH_EMAIL, body={"email": email}, model=UpdateEmailResponse
        )

    async def update_password(
        self,
        *,
        current_password: str,
        new_password: str,
    ) -> MessageResponse:
        return await self._client.patch(
            _AUTH_PASSWORD,
            body={"current_password": current_password, "new_password": new_password},
            model=MessageResponse,
        )

    async def update_username(
        self,
        *,
        username: str,
    ) -> UpdateUsernameResponse:
        return await self._client.patch(
            _AUTH_USERNAME, body={"username": username}, model=UpdateUsernameResponse
        )

    async def sessions(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> SessionListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            _AUTH_SESSIONS, params=params or None, model=SessionListResponse
        )

    async def active_sessions(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> SessionListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            _AUTH_SESSIONS_ACTIVE, params=params or None, model=SessionListResponse
        )

    async def revoke_session(
        self,
        *,
        session_id: int,
    ) -> MessageResponse:
        return await self._client.delete(
            _AUTH_SESSION, body={"session_id": session_id}, model=MessageResponse
        )
