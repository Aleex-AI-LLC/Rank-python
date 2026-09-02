from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Iterator, Optional, Union

import httpx

# ---------------------------------------------------------------------------
# AgentEvent — typed payload for type="agent_event" SSE messages
# ---------------------------------------------------------------------------

@dataclass
class AgentEvent:
    """Structured payload carried inside ``type="agent_event"`` SSE messages.

    The ``event_type`` field identifies the specific sub-event (see class
    constants).  ``data`` holds the event-specific payload whose keys depend
    on ``event_type`` — refer to the "Streaming Events Reference" section of
    the README for the full field-by-field breakdown.

    The same envelope is used by the pentest flow and by the general agentic
    flow (``agent_type="general"`` agents running a long-form ReAct loop).
    A few ``event_type`` values carry different ``data`` keys depending on the
    flow (e.g. ``interpretation``, ``progress``, ``context_compaction``);
    treat ``data`` as opaque and read the keys documented for your flow.

    Attributes:
        event_type: Sub-event identifier (e.g. ``"tool_call"``, ``"agent_start"``).
        agent_id: Numeric agent ID, ``"orchestrator"``, or ``None``.
        parent_agent_id: Parent agent ID for sub-agents.
        instance_id: Unique per-execution instance key for demultiplexing.
            General main agents (depth=0) use ``general_<agentId>_<hex>``;
            sub-agents use ``<agentId>_sub<N>`` and match
            ``subagent_spawn.subagent_id``.  Group events by ``instance_id``.
        depth: 0 = top-level agent, 1 = sub-agent.
        iteration: Current iteration of the agent loop.
        timestamp: Unix timestamp of the event.
        data: Event-specific payload dictionary.
    """

    event_type: str = ""
    agent_id: Union[int, str, None] = None
    parent_agent_id: Optional[int] = None
    instance_id: str = ""
    depth: int = 0
    iteration: int = 0
    timestamp: float = 0.0
    data: dict[str, Any] = field(default_factory=dict)

    # -- Agent loop events --------------------------------------------------
    AGENT_START: str = "agent_start"
    PLAN: str = "plan"
    ITERATION_START: str = "iteration_start"
    THINKING: str = "thinking"
    TOOL_CALL: str = "tool_call"
    TOOL_RESULT: str = "tool_result"
    TEXT_CHUNK: str = "text_chunk"
    NUDGE: str = "nudge"
    SUBAGENT_SPAWN: str = "subagent_spawn"
    SUBAGENT_COMPLETE: str = "subagent_complete"
    CONTEXT_COMPACTION: str = "context_compaction"
    SHARED_CONTEXT: str = "shared_context"
    INTERPRETATION: str = "interpretation"
    PROGRESS: str = "progress"
    ITERATION_COMPLETE: str = "iteration_complete"
    AGENT_FINISHED: str = "agent_finished"

    # -- Orchestration events -----------------------------------------------
    ORCHESTRATION_START: str = "orchestration_start"
    ORCHESTRATION_STATUS: str = "orchestration_status"
    AGENT_STATUS_CHANGE: str = "agent_status_change"
    CONSOLIDATION_START: str = "consolidation_start"
    CONSOLIDATION_HEARTBEAT: str = "consolidation_heartbeat"
    CONSOLIDATION_COMPLETE: str = "consolidation_complete"
    ORCHESTRATION_COMPLETE: str = "orchestration_complete"
    ORCHESTRATION_CANCELLED: str = "orchestration_cancelled"
    PHASE_COMPLETE: str = "phase_complete"

    # -- Browser agent events -----------------------------------------------
    BROWSER_AGENT_START: str = "browser_agent_start"

    # -- stop_reason values (agent_finished.data.stop_reason) ---------------
    STOP_GOAL_REACHED: str = "goal_reached"
    STOP_MAX_ITERATIONS: str = "max_iterations"
    STOP_BUDGET: str = "budget"
    STOP_TIMEOUT: str = "timeout"
    STOP_STAGNATION: str = "stagnation"
    STOP_CANCELLED: str = "cancelled"

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> AgentEvent:
        """Build an ``AgentEvent`` from the ``event`` dict inside a StreamMessage."""
        return cls(
            event_type=raw.get("event_type", ""),
            agent_id=raw.get("agent_id"),
            parent_agent_id=raw.get("parent_agent_id"),
            instance_id=raw.get("instance_id", ""),
            depth=raw.get("depth", 0),
            iteration=raw.get("iteration", 0),
            timestamp=raw.get("timestamp", 0.0),
            data=raw.get("data") or {},
        )


# ---------------------------------------------------------------------------
# ServerSentEvent
# ---------------------------------------------------------------------------

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

    # -- Agent-event helpers ------------------------------------------------

    @property
    def is_agent_event(self) -> bool:
        """``True`` when this SSE message carries an ``AgentEvent`` payload."""
        return self.type == "agent_event"

    @property
    def agent_event(self) -> Optional[AgentEvent]:
        """Parse and return the :class:`AgentEvent` when ``type="agent_event"``.

        Returns ``None`` for any other event type.
        """
        if not self.is_agent_event:
            return None
        if isinstance(self.data, dict):
            raw_event = self.data.get("event")
            if isinstance(raw_event, dict):
                return AgentEvent.from_dict(raw_event)
        return None

    @property
    def event_type(self) -> Optional[str]:
        """Shortcut to ``agent_event.event_type`` (``None`` for non-agent events)."""
        ev = self.agent_event
        return ev.event_type if ev is not None else None


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
