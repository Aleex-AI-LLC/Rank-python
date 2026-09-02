from __future__ import annotations

from typing import Any, Dict, List, Union

from ..._base_client import AsyncAPIClient, SyncAPIClient
from ...types.ai import ChatMessage, ChatNameResponse
from .._base import AsyncAPIResource, SyncAPIResource
from .chat import AsyncChat, Chat


def _normalize_messages(
    messages: List[Union[ChatMessage, Dict[str, str]]],
) -> List[Dict[str, str]]:
    """Convert any :class:`ChatMessage` instances to plain dicts."""
    return [
        m.model_dump() if isinstance(m, ChatMessage) else m
        for m in messages
    ]


# ---------------------------------------------------------------------------
# AI (sync)
# ---------------------------------------------------------------------------


class AI(SyncAPIResource):
    """AI resource — chat streaming and LLM utilities.

    Access via ``client.ai``.

    Sub-resources:
        - ``client.ai.chat`` -- streaming chat with AI agents.

    Example::

        # Stream a chat response
        with client.ai.chat.stream(
            agent_id=23,
            user_prompt="Investiga las ultimas CVEs criticas de Apache",
            chat_id=14,
        ) as stream:
            for event in stream:
                if event.type == "content":
                    print(event.content, end="")

        # Generate a chat name from the first messages
        result = client.ai.generate_chat_name(
            company_name="google",
            model_alias="gemini-2.5-flash",
            first_messages=[
                ChatMessage(userPrompt="Hola", aiResponse="Hola! Soy Aleex."),
            ],
        )
        print(result.chat_name)
    """

    chat: Chat

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.chat = Chat(client)

    def generate_chat_name(
        self,
        *,
        company_name: str,
        model_alias: str,
        first_messages: List[Union[ChatMessage, Dict[str, str]]],
    ) -> ChatNameResponse:
        """Generate a descriptive name for a chat using an LLM.

        The backend analyses the first messages of the conversation and
        returns a short, contextual name.

        Args:
            company_name: LLM provider name (e.g. ``"google"``,
                ``"openai"``).
            model_alias: Model alias to use (e.g.
                ``"gemini-2.5-flash"``).
            first_messages: List of
                :class:`~rank.types.ai.ChatMessage` objects or dicts
                with keys ``"userPrompt"`` and ``"aiResponse"``.

        Returns:
            A :class:`~rank.types.ai.ChatNameResponse` with the
            generated ``chat_name``.
        """
        body: Dict[str, Any] = {
            "company_name": company_name,
            "model_alias": model_alias,
            "first_messages": _normalize_messages(first_messages),
        }
        return self._client.post(
            "/handle_chat_name", body=body, model=ChatNameResponse,
        )


# ---------------------------------------------------------------------------
# AI (async)
# ---------------------------------------------------------------------------


class AsyncAI(AsyncAPIResource):
    """Async variant of :class:`AI`."""

    chat: AsyncChat

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.chat = AsyncChat(client)

    async def generate_chat_name(
        self,
        *,
        company_name: str,
        model_alias: str,
        first_messages: List[Union[ChatMessage, Dict[str, str]]],
    ) -> ChatNameResponse:
        """Generate a descriptive name for a chat using an LLM.

        Async variant of :meth:`AI.generate_chat_name`.

        Args:
            company_name: LLM provider name.
            model_alias: Model alias to use.
            first_messages: List of
                :class:`~rank.types.ai.ChatMessage` objects or dicts
                with keys ``"userPrompt"`` and ``"aiResponse"``.

        Returns:
            A :class:`~rank.types.ai.ChatNameResponse` with the
            generated ``chat_name``.
        """
        body: Dict[str, Any] = {
            "company_name": company_name,
            "model_alias": model_alias,
            "first_messages": _normalize_messages(first_messages),
        }
        return await self._client.post(
            "/handle_chat_name", body=body, model=ChatNameResponse,
        )
