from __future__ import annotations

from typing import Any, Optional

import httpx


class RankError(Exception):
    """Base exception for all Rank SDK errors."""


class APIError(RankError):
    """Error returned by the Rank API.

    Attributes:
        message: Human-readable error description.
        status_code: HTTP status code.
        body: Raw response body (parsed JSON or string).
        request: The httpx.Request that caused the error.
        response: The httpx.Response received.
    """

    message: str
    status_code: int
    body: Any
    request: httpx.Request
    response: httpx.Response

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        body: Any = None,
        request: httpx.Request,
        response: httpx.Response,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body
        self.request = request
        self.response = response

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, status_code={self.status_code})"


class AuthenticationError(APIError):
    """401 - Invalid or missing API key."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__("Invalid or missing API key", **kwargs)


class PermissionDeniedError(APIError):
    """403 - Insufficient permissions for this action."""


class NotFoundError(APIError):
    """404 - The requested resource does not exist."""


class ConflictError(APIError):
    """409 - Conflict with the current state of the resource."""


class UnprocessableEntityError(APIError):
    """422 - Validation error in request body."""


class RateLimitError(APIError):
    """429 - Too many requests. Back off and retry."""

    retry_after: Optional[float]

    def __init__(self, *, retry_after: Optional[float] = None, **kwargs: Any) -> None:
        super().__init__("Rate limit exceeded", **kwargs)
        self.retry_after = retry_after


class InternalServerError(APIError):
    """5xx - Server-side error."""


class APIConnectionError(RankError):
    """Failed to connect to the Rank API (network issue, DNS, etc.)."""

    request: Optional[httpx.Request]

    def __init__(
        self,
        message: str = "Connection error",
        *,
        request: Optional[httpx.Request] = None,
    ) -> None:
        super().__init__(message)
        self.request = request


class APITimeoutError(APIConnectionError):
    """Request timed out."""

    def __init__(self, *, request: Optional[httpx.Request] = None) -> None:
        super().__init__("Request timed out", request=request)


def _make_status_error(
    *,
    message: str,
    status_code: int,
    body: Any,
    request: httpx.Request,
    response: httpx.Response,
) -> APIError:
    """Create the appropriate APIError subclass based on HTTP status code."""
    kwargs: dict[str, Any] = {
        "message": message,
        "status_code": status_code,
        "body": body,
        "request": request,
        "response": response,
    }

    if status_code == 401:
        return AuthenticationError(status_code=status_code, body=body, request=request, response=response)
    if status_code == 403:
        return PermissionDeniedError(**kwargs)
    if status_code == 404:
        return NotFoundError(**kwargs)
    if status_code == 409:
        return ConflictError(**kwargs)
    if status_code == 422:
        return UnprocessableEntityError(**kwargs)
    if status_code == 429:
        retry_after = _parse_retry_after(response)
        return RateLimitError(retry_after=retry_after, status_code=status_code, body=body, request=request, response=response)
    if status_code >= 500:
        return InternalServerError(**kwargs)

    return APIError(**kwargs)


def _parse_retry_after(response: httpx.Response) -> Optional[float]:
    """Extract Retry-After header value in seconds, if present."""
    header = response.headers.get("retry-after")
    if header is None:
        return None
    try:
        return float(header)
    except (ValueError, TypeError):
        return None
