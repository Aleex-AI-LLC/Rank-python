from __future__ import annotations

from typing import Optional

from .shared import RankModel

# ---------------------------------------------------------------------------
# Chat name generation
# ---------------------------------------------------------------------------


class ChatMessage(RankModel):
    """A single user/AI message pair used as context for chat name generation.

    The field names match the Go backend's ``ChatContext`` struct
    (``userPrompt`` / ``aiResponse``).
    """

    userPrompt: str
    aiResponse: str


class ChatNameResponse(RankModel):
    """Response from ``POST /handle_chat_name``.

    Contains the LLM-generated chat name or an error message.
    """

    chat_name: str = ""
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------

__all__ = [
    "ChatMessage",
    "ChatNameResponse",
]
