from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterator, Optional, AsyncIterator

import httpx


@dataclass
class ServerSentEvent:
    """A single Server-Sent Event parsed from an SSE stream.

    Attributes:
        event: Event type (defaults to "message").
        data: Event payload, parsed as JSON if possible.
        id: Optional event ID.
        retry: Optional retry interval in milliseconds.
        raw_data: The raw string data before JSON parsing.
    """

    event: str = "message"
    data: Any = None
    id: Optional[str] = None
    retry: Optional[int] = None
    raw_data: str = ""

    @property
    def type(self) -> str:
        """Alias for event type. Matches the Rank stream protocol (content, complete, error, etc.)."""
        if isinstance(self.data, dict) and "type" in self.data:
            return self.data["type"]
        return self.event

    @property
    def content(self) -> str:
        """Extract content string from the event data."""
        if isinstance(self.data, dict):
            return self.data.get("content", "")
        return ""

    @property
    def error(self) -> Optional[str]:
        """Extract error string from the event data, if any."""
        if isinstance(self.data, dict):
            err = self.data.get("error")
            if err:
                return str(err)
        return None

    @property
    def timestamp(self) -> Optional[float]:
        if isinstance(self.data, dict):
            return self.data.get("timestamp")
        return None

    @property
    def metadata(self) -> dict[str, Any]:
        """Extra data fields beyond type/content/error/timestamp."""
        if isinstance(self.data, dict):
            return self.data.get("data", {})
        return {}


def _parse_sse_line(line: str, current: dict[str, Any]) -> Optional[ServerSentEvent]:
    """Parse a single SSE line, accumulating state in `current`.

    Returns a ServerSentEvent when a blank line (event boundary) is encountered.
    """
    if not line:
        if current.get("data") is not None:
            raw = current["data"]
            try:
                parsed = json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                parsed = raw

            event = ServerSentEvent(
                event=current.get("event", "message"),
                data=parsed,
                id=current.get("id"),
                retry=current.get("retry"),
                raw_data=raw,
            )
            current.clear()
            return event
        current.clear()
        return None

    if line.startswith(":"):
        return None

    if ":" in line:
        field, _, value = line.partition(":")
        value = value.lstrip(" ")
    else:
        field = line
        value = ""

    if field == "data":
        existing = current.get("data")
        current["data"] = f"{existing}\n{value}" if existing else value
    elif field == "event":
        current["event"] = value
    elif field == "id":
        current["id"] = value
    elif field == "retry":
        try:
            current["retry"] = int(value)
        except ValueError:
            pass

    return None


def _flush_pending(current: dict[str, Any]) -> Optional[ServerSentEvent]:
    """Flush any buffered data as a final event when the stream ends without a trailing blank line."""
    if current.get("data") is not None:
        raw = current["data"]
        try:
            parsed = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            parsed = raw

        event = ServerSentEvent(
            event=current.get("event", "message"),
            data=parsed,
            id=current.get("id"),
            retry=current.get("retry"),
            raw_data=raw,
        )
        current.clear()
        return event
    return None


class Stream:
    """Synchronous iterator over an SSE stream from the Rank API.

    Usage:
        with client.ai.chat.stream(...) as stream:
            for event in stream:
                if event.type == "content":
                    print(event.content, end="")
    """

    _response: httpx.Response
    _decoder: Iterator[str]
    _current: dict[str, Any]

    def __init__(self, response: httpx.Response) -> None:
        self._response = response
        self._decoder = response.iter_lines()
        self._current = {}

    def __iter__(self) -> Iterator[ServerSentEvent]:
        return self._stream()

    def _stream(self) -> Iterator[ServerSentEvent]:
        for line in self._decoder:
            event = _parse_sse_line(line, self._current)
            if event is not None:
                yield event
                if event.type in ("complete", "error", "cancelled"):
                    return

        pending = _flush_pending(self._current)
        if pending is not None:
            yield pending

    def close(self) -> None:
        self._response.close()

    def __enter__(self) -> Stream:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncStream:
    """Asynchronous iterator over an SSE stream from the Rank API.

    Usage:
        async with client.ai.chat.stream(...) as stream:
            async for event in stream:
                if event.type == "content":
                    print(event.content, end="")
    """

    _response: httpx.Response
    _current: dict[str, Any]

    def __init__(self, response: httpx.Response) -> None:
        self._response = response
        self._current = {}

    def __aiter__(self) -> AsyncIterator[ServerSentEvent]:
        return self._stream()

    async def _stream(self) -> AsyncIterator[ServerSentEvent]:
        async for line in self._response.aiter_lines():
            event = _parse_sse_line(line, self._current)
            if event is not None:
                yield event
                if event.type in ("complete", "error", "cancelled"):
                    return

        pending = _flush_pending(self._current)
        if pending is not None:
            yield pending

    async def close(self) -> None:
        await self._response.aclose()

    async def __aenter__(self) -> AsyncStream:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
