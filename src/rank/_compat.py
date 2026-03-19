from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):  # type: ignore[no-redef]
        pass


if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


def model_json(model: Any) -> dict[str, Any]:
    """Serialize a Pydantic model to dict, compatible with v2."""
    return model.model_dump(exclude_unset=True)


__all__ = [
    "StrEnum",
    "TypeAlias",
    "Self",
    "override",
    "model_json",
]
