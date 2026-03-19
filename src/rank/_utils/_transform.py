from __future__ import annotations

from typing import Any, Mapping

# Sentinel for parameters not provided by the user.
# Distinct from None, which is a valid value.

class _NotGiven:
    """Sentinel class to distinguish missing arguments from None."""

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = _NotGiven()


def strip_not_given(data: dict[str, Any]) -> dict[str, Any]:
    """Remove keys whose value is NOT_GIVEN from a dict."""
    return {k: v for k, v in data.items() if not isinstance(v, _NotGiven)}


def maybe_transform(data: Mapping[str, Any] | None) -> dict[str, Any] | None:
    """Transform a mapping into a clean dict, stripping NOT_GIVEN values.

    Returns None if input is None.
    """
    if data is None:
        return None
    return strip_not_given(dict(data))
