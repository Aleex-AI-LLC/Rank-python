from __future__ import annotations

import json as _json
import os
from typing import IO, Any, Dict, List, Literal, Tuple, Union

from ..._base_client import AsyncAPIClient, SyncAPIClient
from ..._streaming import AsyncStream, Stream
from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.ai import ChatMessage
from .._base import AsyncAPIResource, SyncAPIResource

_CHAT_PATH = "/chat"

FileContent = Union[IO[bytes], bytes]
FileTypes = Union[
    FileContent,
    Tuple[str, FileContent],
    Tuple[str, FileContent, str],
]


def _normalize_context(
    context: Union[List[Union[ChatMessage, Dict[str, str]]], _NotGiven],
) -> Union[List[Dict[str, str]], _NotGiven]:
    """Convert any :class:`ChatMessage` instances to plain dicts."""
    if isinstance(context, _NotGiven):
        return context
    return [
        m.model_dump() if isinstance(m, ChatMessage) else m
        for m in context
    ]


def _prepare_multipart(
    body: Dict[str, Any],
    file: FileTypes,
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Build ``(files_dict, form_body)`` for httpx multipart upload.

    The Go backend parses multipart fields as strings, so complex
    values (lists, dicts) are JSON-serialised and integers are
    stringified.
    """
    form_body: Dict[str, str] = {}
    for key, value in body.items():
        if isinstance(value, (list, dict)):
            form_body[key] = _json.dumps(value)
        elif value is not None:
            form_body[key] = str(value)

    if isinstance(file, (bytes, bytearray)):
        files: Dict[str, Any] = {"file": ("file", file)}
    elif isinstance(file, tuple):
        files = {"file": file}
    else:
        name = os.path.basename(getattr(file, "name", "file"))
        files = {"file": (name, file)}

    return files, form_body


# ---------------------------------------------------------------------------
# Chat (sync)
# ---------------------------------------------------------------------------


class Chat(SyncAPIResource):
    """AI chat streaming sub-resource.

    Access via ``client.ai.chat``.

    Example::

        # General chat
        with client.ai.chat.stream(
            agent_id=23,
            user_prompt="Investiga vulnerabilidades criticas de Apache",
            chat_id=14,
        ) as stream:
            for event in stream:
                if event.type == "content":
                    print(event.content, end="")

        # Pentest automatico
        with client.ai.chat.stream(
            user_prompt="Ejecutar pentest completo",
            pentest_id=32,
            mode="automatic",
            chat_id=28,
        ) as stream:
            for event in stream:
                print(event.type, event.content)

        # Pentest guiado (chat_id para persistencia/contexto entre fases)
        with client.ai.chat.stream(
            user_prompt="Inicia este pentest",
            pentest_id=56,
            mode="guided",
            phase_id=1,
            chat_id=33,
        ) as stream:
            for event in stream:
                print(event.type, event.content)

        # With file attachment
        with open("report.pdf", "rb") as f:
            with client.ai.chat.stream(
                agent_id=23,
                user_prompt="Analiza este documento",
                file=f,
            ) as stream:
                for event in stream:
                    print(event.content, end="")
    """

    def stream(
        self,
        *,
        user_prompt: str,
        agent_id: Union[int, _NotGiven] = NOT_GIVEN,
        agent_type: Union[Literal["general", "pentest"], _NotGiven] = NOT_GIVEN,
        chat_id: Union[int, _NotGiven] = NOT_GIVEN,
        pentest_id: Union[int, _NotGiven] = NOT_GIVEN,
        mode: Union[Literal["guided", "automatic"], _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        context: Union[List[Union[ChatMessage, Dict[str, str]]], _NotGiven] = NOT_GIVEN,
        file: Union[FileTypes, _NotGiven] = NOT_GIVEN,
    ) -> Stream:
        """Send a chat message and stream the AI response via SSE.

        The endpoint supports three modes of operation:

        **General chat** -- provide ``agent_id`` (and optionally ``chat_id``
        for persistence).

        **Pentest automatic** -- provide ``pentest_id`` with
        ``mode="automatic"`` (and optionally ``chat_id``).

        **Pentest guided** -- provide ``pentest_id`` with
        ``mode="guided"`` and ``phase_id`` (and optionally ``chat_id``
        for persistence and cross-phase context).

        Returns a context-manager / iterator yielding
        :class:`~rank.ServerSentEvent` objects.  Typical event types:
        ``content``, ``complete``, ``error``, ``cancelled``,
        ``phase_start``, ``phase_complete``, ``queued``, ``ready``.

        Args:
            user_prompt: The user message to send to the AI agent.
            agent_id: Agent ID to use (required for general chat).
            agent_type: ``"general"`` or ``"pentest"``.  Inferred
                automatically when ``pentest_id`` is provided.
            chat_id: Chat ID for message persistence and conversation
                context.  Applies to all modes.
            pentest_id: Pentest ID (required for pentest modes).
            mode: ``"guided"`` or ``"automatic"`` (pentest only).
            phase_id: Phase ID to execute (required for guided mode).
            context: Explicit conversation context as a list of
                :class:`~rank.types.ai.ChatMessage` objects or dicts
                with keys ``"userPrompt"`` and ``"aiResponse"``.
                If omitted and ``chat_id`` is provided, the backend
                fetches context automatically.
            file: Optional file attachment.  Accepted formats:
                a file-like object (``open("f.pdf", "rb")``),
                raw ``bytes``, a ``(filename, content)`` tuple, or
                a ``(filename, content, content_type)`` tuple.
                Supported extensions: PDF, JSON, PNG, JPEG, WEBP, GIF.
                Max size: 30 MB.
        """
        body: Dict[str, Any] = {"user_prompt": user_prompt}
        body.update(strip_not_given({
            "agent_id": agent_id,
            "agent_type": agent_type,
            "chat_id": chat_id,
            "pentest_id": pentest_id,
            "mode": mode,
            "phase_id": phase_id,
            "context": _normalize_context(context),
        }))

        if not isinstance(file, _NotGiven):
            files, form_body = _prepare_multipart(body, file)
            return self._client.stream_request(
                "POST", _CHAT_PATH, body=form_body, files=files,
            )

        return self._client.stream_request("POST", _CHAT_PATH, body=body)


# ---------------------------------------------------------------------------
# Chat (async)
# ---------------------------------------------------------------------------


class AsyncChat(AsyncAPIResource):
    """Async variant of :class:`Chat`."""

    async def stream(
        self,
        *,
        user_prompt: str,
        agent_id: Union[int, _NotGiven] = NOT_GIVEN,
        agent_type: Union[Literal["general", "pentest"], _NotGiven] = NOT_GIVEN,
        chat_id: Union[int, _NotGiven] = NOT_GIVEN,
        pentest_id: Union[int, _NotGiven] = NOT_GIVEN,
        mode: Union[Literal["guided", "automatic"], _NotGiven] = NOT_GIVEN,
        phase_id: Union[int, _NotGiven] = NOT_GIVEN,
        context: Union[List[Union[ChatMessage, Dict[str, str]]], _NotGiven] = NOT_GIVEN,
        file: Union[FileTypes, _NotGiven] = NOT_GIVEN,
    ) -> AsyncStream:
        """Send a chat message and stream the AI response via SSE.

        Async variant of :meth:`Chat.stream`.  Returns an async
        context-manager / async-iterator yielding
        :class:`~rank.ServerSentEvent` objects.

        Example::

            async with await client.ai.chat.stream(
                agent_id=1, user_prompt="Hello",
            ) as stream:
                async for event in stream:
                    if event.type == "content":
                        print(event.content, end="")

        Args:
            user_prompt: The user message to send to the AI agent.
            agent_id: Agent ID to use (required for general chat).
            agent_type: ``"general"`` or ``"pentest"``.
            chat_id: Chat ID for persistence and context.
            pentest_id: Pentest ID (required for pentest modes).
            mode: ``"guided"`` or ``"automatic"`` (pentest only).
            phase_id: Phase ID to execute (guided mode only).
            context: Explicit conversation context as
                :class:`~rank.types.ai.ChatMessage` objects or dicts.
            file: Optional file attachment (see sync variant for
                accepted formats).
        """
        body: Dict[str, Any] = {"user_prompt": user_prompt}
        body.update(strip_not_given({
            "agent_id": agent_id,
            "agent_type": agent_type,
            "chat_id": chat_id,
            "pentest_id": pentest_id,
            "mode": mode,
            "phase_id": phase_id,
            "context": _normalize_context(context),
        }))

        if not isinstance(file, _NotGiven):
            files, form_body = _prepare_multipart(body, file)
            return await self._client.stream_request(
                "POST", _CHAT_PATH, body=form_body, files=files,
            )

        return await self._client.stream_request("POST", _CHAT_PATH, body=body)
