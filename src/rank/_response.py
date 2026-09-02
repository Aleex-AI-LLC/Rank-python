from __future__ import annotations

from typing import Generic, List, Type, TypeVar

import httpx

T = TypeVar("T")


class APIResponse(Generic[T]):
    """Wrapper around an API response providing typed access to the data.

    Attributes:
        data: Parsed response body as the expected model type.
        status_code: HTTP status code.
        headers: Response headers.
        raw_response: The underlying httpx.Response.
    """

    data: T
    status_code: int
    headers: httpx.Headers
    raw_response: httpx.Response

    def __init__(
        self,
        *,
        data: T,
        raw_response: httpx.Response,
    ) -> None:
        self.data = data
        self.status_code = raw_response.status_code
        self.headers = raw_response.headers
        self.raw_response = raw_response

    def __repr__(self) -> str:
        return f"APIResponse(status_code={self.status_code}, data={type(self.data).__name__})"


def parse_response(
    *,
    response: httpx.Response,
    model: Type[T],
) -> T:
    """Parse an httpx.Response into a Pydantic model.

    Handles the Rank API convention where data lives under a "data" key.
    For primitive types (str, dict, list), returns the payload directly.
    """
    json_data = response.json()

    if isinstance(json_data, dict) and "data" in json_data:
        payload = json_data["data"]
    else:
        payload = json_data

    if model in (str, dict, list):
        return payload  # type: ignore[return-value]

    return model.model_validate(payload)  # type: ignore[union-attr]


def parse_response_list(
    *,
    response: httpx.Response,
    model: Type[T],
) -> List[T]:
    """Parse an httpx.Response into a list of Pydantic models."""
    json_data = response.json()

    if isinstance(json_data, dict) and "data" in json_data:
        payload = json_data["data"]
    else:
        payload = json_data

    if not isinstance(payload, list):
        payload = [payload]

    return [model.model_validate(item) for item in payload]  # type: ignore[union-attr]
