from __future__ import annotations

import json as _json
import os
from typing import IO, Any, Dict, List, Literal, Optional, Tuple, Union

from ..._streaming import AsyncStream, Stream
from ..._utils._transform import NOT_GIVEN, _NotGiven, strip_not_given
from ...types.ai import ChatMessage
from .._base import AsyncAPIResource, SyncAPIResource

_CHAT_PATH = "/chat"

MAX_FILES = 10
MAX_COMBINED_FILE_SIZE = 50 * 1024 * 1024

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


def _resolve_files(
    file: Union[FileTypes, _NotGiven],
    files: Union[List[FileTypes], _NotGiven],
) -> List[FileTypes]:
    """Merge the singular ``file`` and plural ``files`` arguments into a list.

    Validates the per-request count and the combined size (best-effort, when
    the size of each attachment can be determined without consuming it).
    """
    if not isinstance(file, _NotGiven) and not isinstance(files, _NotGiven):
        raise ValueError("Pass either 'file' or 'files', not both")

    if not isinstance(files, _NotGiven):
        if not isinstance(files, list):
            raise ValueError("'files' must be a list; use 'file' for a single attachment")
        resolved = list(files)
    elif not isinstance(file, _NotGiven):
        resolved = [file]
    else:
        return []

    if not resolved:
        return []

    if len(resolved) > MAX_FILES:
        raise ValueError(f"Too many files: max {MAX_FILES} per request")

    total = 0
    for f in resolved:
        size = _known_size(_file_content(f))
        if size is not None:
            total += size
    if total > MAX_COMBINED_FILE_SIZE:
        raise ValueError("Combined file size too large: max 50 MB per request")

    return resolved


def _file_content(f: FileTypes) -> Any:
    """Return the raw content object from a ``FileTypes`` value."""
    if isinstance(f, tuple):
        return f[1]
    return f


def _known_size(content: Any) -> Optional[int]:
    """Return the byte size of ``content`` without consuming it, or ``None``."""
    if isinstance(content, (bytes, bytearray)):
        return len(content)
    try:
        if hasattr(content, "seek") and hasattr(content, "tell") and content.seekable():
            pos = content.tell()
            content.seek(0, os.SEEK_END)
            end = content.tell()
            content.seek(pos)
            return end - pos
    except Exception:
        return None
    return None


def _prepare_multipart(
    body: Dict[str, Any],
    files: List[FileTypes],
) -> Tuple[List[Tuple[str, Any]], Dict[str, str]]:
    """Build ``(multipart_files, form_body)`` for httpx multipart upload.

    The Go backend parses multipart fields as strings, so complex values
    (lists, dicts) are JSON-serialised and integers are stringified. Every
    attachment is sent as a separate ``"file"`` part; the backend reads all
    parts regardless of order.
    """
    form_body: Dict[str, str] = {}
    for key, value in body.items():
        if isinstance(value, (list, dict)):
            form_body[key] = _json.dumps(value)
        elif value is not None:
            form_body[key] = str(value)

    multipart_files: List[Tuple[str, Any]] = []
    for f in files:
        if isinstance(f, (bytes, bytearray)):
            multipart_files.append(("file", ("file", f)))
        elif isinstance(f, tuple):
            multipart_files.append(("file", f))
        else:
            name = os.path.basename(getattr(f, "name", "file"))
            multipart_files.append(("file", (name, f)))

    return multipart_files, form_body


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

        # With a single file attachment
        with open("report.pdf", "rb") as f:
            with client.ai.chat.stream(
                agent_id=23,
                user_prompt="Analiza este documento",
                file=f,
            ) as stream:
                for event in stream:
                    print(event.content, end="")

        # With multiple file attachments
        with open("report.pdf", "rb") as a, open("diagram.png", "rb") as b:
            with client.ai.chat.stream(
                agent_id=23,
                user_prompt="Analiza estos archivos",
                files=[a, b],
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
        files: Union[List[FileTypes], _NotGiven] = NOT_GIVEN,
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
            file: Optional single file attachment.  Accepted formats:
                a file-like object (``open("f.pdf", "rb")``),
                raw ``bytes``, a ``(filename, content)`` tuple, or
                a ``(filename, content, content_type)`` tuple.
            files: Optional list of file attachments (each in the same
                formats accepted by ``file``).  Use this to send several
                attachments in one request.  ``file`` and ``files`` are
                mutually exclusive.
                Supported extensions: PDF, JSON, PNG, JPEG, WEBP, GIF.
                Limits: up to 10 files, 30 MB per file and 50 MB combined.
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

        resolved_files = _resolve_files(file, files)
        if resolved_files:
            multipart_files, form_body = _prepare_multipart(body, resolved_files)
            return self._client.stream_request(
                "POST", _CHAT_PATH, body=form_body, files=multipart_files,
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
        files: Union[List[FileTypes], _NotGiven] = NOT_GIVEN,
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
            file: Optional single file attachment (see sync variant for
                accepted formats).
            files: Optional list of file attachments.  Mutually exclusive
                with ``file``.  Up to 10 files, 30 MB per file and 50 MB
                combined.
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

        resolved_files = _resolve_files(file, files)
        if resolved_files:
            multipart_files, form_body = _prepare_multipart(body, resolved_files)
            return await self._client.stream_request(
                "POST", _CHAT_PATH, body=form_body, files=multipart_files,
            )

        return await self._client.stream_request("POST", _CHAT_PATH, body=body)
