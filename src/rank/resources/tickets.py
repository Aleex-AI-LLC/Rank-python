from __future__ import annotations

from typing import Any, Union

from .._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ..types.shared import MessageResponse
from ..types.ticket import (
    JiraComment,
    Ticket,
    TicketAddAttachmentResponse,
    TicketListResponse,
)
from ._base import AsyncAPIResource, SyncAPIResource

_TICKETS = "/tickets"


# ---------------------------------------------------------------------------
# Tickets (sync)
# ---------------------------------------------------------------------------


class Tickets(SyncAPIResource):
    """Jira ticket integration — create, list, comment, and sync tickets.

    Access via ``client.tickets``.

    Example::

        # List tickets
        resp = client.tickets.list()
        for t in resp.items:
            print(t.jira_key, t.summary)

        # Create a ticket
        resp = client.tickets.create(
            summary="Fix login bug",
            description="Users cannot log in with SSO",
            issue_type="Bug",
        )
    """

    def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> TicketListResponse:
        """List all Jira tickets.

        Args:
            page: Page number.
            per_page: Items per page.
        """
        params = strip_not_given({"page": page, "per_page": per_page})
        return self._client.get(
            _TICKETS, params=params or None, model=TicketListResponse,
        )

    def retrieve(self, ticket_id: int) -> Ticket:
        """Get a single ticket.

        Args:
            ticket_id: ID of the ticket.
        """
        return self._client.get(f"{_TICKETS}/{ticket_id}", model=Ticket)

    def create(
        self,
        *,
        summary: str,
        description: str,
        issue_type: str,
    ) -> Ticket:
        """Create a new Jira ticket.

        Args:
            summary: Ticket summary / title.
            description: Detailed description.
            issue_type: Jira issue type (e.g. ``"Bug"``, ``"Task"``).
        """
        body = {
            "summary": summary,
            "description": description,
            "issue_type": issue_type,
        }
        return self._client.post(_TICKETS, body=body, model=Ticket)

    def delete(self, ticket_id: int) -> MessageResponse:
        """Delete a ticket.

        Args:
            ticket_id: ID of the ticket.
        """
        return self._client.delete(
            f"{_TICKETS}/{ticket_id}", model=MessageResponse,
        )

    def add_comment(
        self,
        ticket_id: int,
        *,
        comment: str,
    ) -> JiraComment:
        """Add a comment to a ticket.

        Args:
            ticket_id: ID of the ticket.
            comment: Comment body text.
        """
        return self._client.post(
            f"{_TICKETS}/{ticket_id}/comments",
            body={"comment": comment},
            model=JiraComment,
        )

    def update_comment(
        self,
        ticket_id: int,
        comment_id: str,
        *,
        comment: str,
    ) -> JiraComment:
        """Update an existing comment on a ticket.

        Args:
            ticket_id: ID of the ticket.
            comment_id: Jira comment ID (string).
            comment: New comment body text.
        """
        return self._client.put(
            f"{_TICKETS}/{ticket_id}/comments/{comment_id}",
            body={"comment": comment},
            model=JiraComment,
        )

    def add_attachment(
        self,
        ticket_id: int,
        *,
        file: Any,
    ) -> TicketAddAttachmentResponse:
        """Upload an image attachment to a ticket.

        Files are sent as multipart/form-data.  Pass *file* in the format
        accepted by ``httpx``::

            file = [("file", ("screenshot.png", open("screenshot.png", "rb"), "image/png"))]
            client.tickets.add_attachment(ticket_id=1, file=file)

        Allowed formats: png, jpg, jpeg, gif, webp, svg (max 10 MB).

        Args:
            ticket_id: ID of the ticket.
            file: Multipart file tuple(s) for httpx.
        """
        return self._client.post(
            f"{_TICKETS}/{ticket_id}/attachments",
            files=file,
            model=TicketAddAttachmentResponse,
        )

    def sync(self, ticket_id: int) -> Ticket:
        """Sync a ticket with Jira and return the updated ticket.

        Args:
            ticket_id: ID of the ticket to sync.
        """
        return self._client.post(
            f"{_TICKETS}/{ticket_id}/sync", model=Ticket,
        )


# ---------------------------------------------------------------------------
# Tickets (async)
# ---------------------------------------------------------------------------


class AsyncTickets(AsyncAPIResource):
    """Async variant of :class:`Tickets`."""

    async def list(
        self,
        *,
        page: Union[int, _NotGiven] = NOT_GIVEN,
        per_page: Union[int, _NotGiven] = NOT_GIVEN,
    ) -> TicketListResponse:
        params = strip_not_given({"page": page, "per_page": per_page})
        return await self._client.get(
            _TICKETS, params=params or None, model=TicketListResponse,
        )

    async def retrieve(self, ticket_id: int) -> Ticket:
        return await self._client.get(f"{_TICKETS}/{ticket_id}", model=Ticket)

    async def create(
        self,
        *,
        summary: str,
        description: str,
        issue_type: str,
    ) -> Ticket:
        body = {
            "summary": summary,
            "description": description,
            "issue_type": issue_type,
        }
        return await self._client.post(
            _TICKETS, body=body, model=Ticket,
        )

    async def delete(self, ticket_id: int) -> MessageResponse:
        return await self._client.delete(
            f"{_TICKETS}/{ticket_id}", model=MessageResponse,
        )

    async def add_comment(
        self,
        ticket_id: int,
        *,
        comment: str,
    ) -> JiraComment:
        return await self._client.post(
            f"{_TICKETS}/{ticket_id}/comments",
            body={"comment": comment},
            model=JiraComment,
        )

    async def update_comment(
        self,
        ticket_id: int,
        comment_id: str,
        *,
        comment: str,
    ) -> JiraComment:
        return await self._client.put(
            f"{_TICKETS}/{ticket_id}/comments/{comment_id}",
            body={"comment": comment},
            model=JiraComment,
        )

    async def add_attachment(
        self,
        ticket_id: int,
        *,
        file: Any,
    ) -> TicketAddAttachmentResponse:
        return await self._client.post(
            f"{_TICKETS}/{ticket_id}/attachments",
            files=file,
            model=TicketAddAttachmentResponse,
        )

    async def sync(self, ticket_id: int) -> Ticket:
        return await self._client.post(
            f"{_TICKETS}/{ticket_id}/sync", model=Ticket,
        )
