from __future__ import annotations

from typing import Any, Dict, List, Union

from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.chat import (
    AssignVulnerabilitiesResponse,
    ChatVulnerabilityListResponse,
    RemoveVulnerabilityResponse,
)
from .._base import AsyncAPIResource, SyncAPIResource

# ---------------------------------------------------------------------------
# Vulnerabilities (sync)
# ---------------------------------------------------------------------------


class Vulnerabilities(SyncAPIResource):
    """Manage vulnerabilities linked to a chat.

    Access via ``client.chats.vulnerabilities``.

    Linking a finding to a chat does not move ownership — the pentest
    still owns the vulnerability.  ``delete`` only removes the association.

    Example::

        vulns = client.chats.vulnerabilities.list(chat_id=10)
        for v in vulns.items:
            print(v.title, v.severity)

        client.chats.vulnerabilities.assign(chat_id=10, vulnerabilities=[5, 12])

        client.chats.vulnerabilities.delete(chat_id=10, vulnerability_id=5)
    """

    def list(
        self,
        chat_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ChatVulnerabilityListResponse:
        """List vulnerabilities assigned to a chat.

        Args:
            chat_id: ID of the chat.
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            f"/chats/{chat_id}/vulnerabilities",
            params=params or None,
            model=ChatVulnerabilityListResponse,
        )

    def assign(
        self,
        chat_id: int,
        *,
        vulnerabilities: Union[int, List[int]],
    ) -> AssignVulnerabilitiesResponse:
        """Assign one or more pentest findings to a chat.

        Args:
            chat_id: ID of the chat.
            vulnerabilities: A single vulnerability ID or a list of IDs.
        """
        body: Dict[str, Any] = {
            "vulnerability": (
                vulnerabilities if isinstance(vulnerabilities, int)
                else list(vulnerabilities)
            ),
        }
        return self._client.post(
            f"/chats/{chat_id}/vulnerabilities",
            body=body,
            model=AssignVulnerabilitiesResponse,
        )

    def delete(self, chat_id: int, vulnerability_id: int) -> RemoveVulnerabilityResponse:
        """Remove a vulnerability association from a chat.

        The pentest finding itself is not deleted.

        Args:
            chat_id: ID of the chat.
            vulnerability_id: ID of the vulnerability to unlink.
        """
        return self._client.delete(
            f"/chats/{chat_id}/vulnerabilities/{vulnerability_id}",
            model=RemoveVulnerabilityResponse,
        )


# ---------------------------------------------------------------------------
# Vulnerabilities (async)
# ---------------------------------------------------------------------------


class AsyncVulnerabilities(AsyncAPIResource):
    """Async variant of :class:`Vulnerabilities`."""

    async def list(
        self,
        chat_id: int,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> ChatVulnerabilityListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            f"/chats/{chat_id}/vulnerabilities",
            params=params or None,
            model=ChatVulnerabilityListResponse,
        )

    async def assign(
        self,
        chat_id: int,
        *,
        vulnerabilities: Union[int, List[int]],
    ) -> AssignVulnerabilitiesResponse:
        body: Dict[str, Any] = {
            "vulnerability": (
                vulnerabilities if isinstance(vulnerabilities, int)
                else list(vulnerabilities)
            ),
        }
        return await self._client.post(
            f"/chats/{chat_id}/vulnerabilities",
            body=body,
            model=AssignVulnerabilitiesResponse,
        )

    async def delete(
        self, chat_id: int, vulnerability_id: int,
    ) -> RemoveVulnerabilityResponse:
        return await self._client.delete(
            f"/chats/{chat_id}/vulnerabilities/{vulnerability_id}",
            model=RemoveVulnerabilityResponse,
        )
