from __future__ import annotations

import time
import logging
from typing import Any, Dict, List, Mapping, Optional, Type, TypeVar, Union, overload

import httpx

from ._constants import (
    AUTH_HEADER,
    DEFAULT_CONNECTION_LIMITS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    USER_AGENT,
)
from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    _make_status_error,
)
from ._response import parse_response, parse_response_list
from ._streaming import AsyncStream, Stream
from ._utils._pagination import AsyncPage, PaginationMeta, SyncPage
from ._utils._transform import strip_not_given

logger = logging.getLogger("rank")

T = TypeVar("T")


RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


class _BaseClient:
    """Shared logic for sync and async API clients."""

    _base_url: str
    _api_key: str
    _api_prefix: str
    _timeout: float
    _max_retries: int
    _custom_headers: Dict[str, str]

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        api_prefix: str = "",
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._api_prefix = api_prefix
        self._timeout = timeout
        self._max_retries = max_retries
        self._custom_headers = custom_headers or {}

    def _build_url(self, path: str) -> str:
        prefix = self._api_prefix
        if path.startswith("/"):
            return f"{self._base_url}{prefix}{path}"
        return f"{self._base_url}{prefix}/{path}"

    def _build_headers(self, extra: Optional[Mapping[str, str]] = None) -> Dict[str, str]:
        headers: Dict[str, str] = {
            AUTH_HEADER: self._api_key,
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
        headers.update(self._custom_headers)
        if extra:
            headers.update(extra)
        return headers

    def _should_retry(self, response: httpx.Response, attempt: int) -> bool:
        if attempt >= self._max_retries:
            return False
        return response.status_code in RETRYABLE_STATUS_CODES

    def _retry_delay(self, attempt: int, response: Optional[httpx.Response] = None) -> float:
        """Calculate delay before next retry using exponential backoff."""
        if response is not None:
            retry_after = response.headers.get("retry-after")
            if retry_after:
                try:
                    return float(retry_after)
                except (ValueError, TypeError):
                    pass
        return min(0.5 * (2 ** attempt), 8.0)

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Raise the appropriate APIError for non-2xx responses."""
        try:
            body = response.json()
        except Exception:
            body = response.text

        message = ""
        if isinstance(body, dict):
            message = body.get("message", "") or body.get("error", "") or str(body)
        else:
            message = str(body)

        raise _make_status_error(
            message=message,
            status_code=response.status_code,
            body=body,
            request=response.request,
            response=response,
        )


class SyncAPIClient(_BaseClient):
    """Synchronous HTTP client for the Rank API."""

    _client: httpx.Client

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        api_prefix: str = "",
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            api_prefix=api_prefix,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=custom_headers,
        )
        self._client = httpx.Client(
            timeout=timeout,
            limits=httpx.Limits(
                max_connections=DEFAULT_CONNECTION_LIMITS["max_connections"],
                max_keepalive_connections=DEFAULT_CONNECTION_LIMITS["max_keepalive_connections"],
            ),
            follow_redirects=True,
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        files: Optional[Any] = None,
        stream: bool = False,
        timeout: Optional[float] = None,
    ) -> httpx.Response:
        url = self._build_url(path)
        req_headers = self._build_headers(headers)

        if files and (headers is None or "Accept" not in headers):
            req_headers.pop("Accept", None)

        if body is not None:
            body = strip_not_given(body)

        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}

        prev_timeout = None
        if timeout is not None:
            prev_timeout = self._client.timeout
            self._client.timeout = httpx.Timeout(timeout)

        try:
            for attempt in range(self._max_retries + 1):
                try:
                    request = self._client.build_request(
                        method,
                        url,
                        json=body if not files else None,
                        data=body if files else None,
                        params=params,
                        headers=req_headers,
                        files=files,
                    )
                    response = self._client.send(request, stream=stream)

                except httpx.TimeoutException as e:
                    if attempt < self._max_retries:
                        time.sleep(self._retry_delay(attempt))
                        continue
                    raise APITimeoutError(request=getattr(e, "request", None)) from e

                except httpx.ConnectError as e:
                    if attempt < self._max_retries:
                        time.sleep(self._retry_delay(attempt))
                        continue
                    raise APIConnectionError(request=getattr(e, "request", None)) from e

                if self._should_retry(response, attempt):
                    if stream:
                        response.close()
                    delay = self._retry_delay(attempt, response)
                    logger.debug("Retrying request to %s (attempt %d, status %d, delay %.1fs)", url, attempt + 1, response.status_code, delay)
                    time.sleep(delay)
                    continue

                if response.status_code >= 400:
                    if stream:
                        response.read()
                    self._handle_error_response(response)

                return response

            raise APIConnectionError("Max retries exceeded")
        finally:
            if prev_timeout is not None:
                self._client.timeout = prev_timeout

    def get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        model: Type[T],
    ) -> T:
        response = self._request("GET", path, params=params)
        return parse_response(response=response, model=model)

    def get_list(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        model: Type[T],
    ) -> List[T]:
        response = self._request("GET", path, params=params)
        return parse_response_list(response=response, model=model)

    def _get_page(
        self,
        *,
        path: str,
        params: Dict[str, Any],
        model: Type[T],
    ) -> SyncPage[T]:
        response = self._request("GET", path, params=params)
        json_data = response.json()

        items_data = json_data.get("data", [])
        items = [model.model_validate(item) for item in items_data]  # type: ignore[union-attr]

        meta_data = json_data.get("meta", json_data.get("pagination", {}))
        meta = PaginationMeta.model_validate(meta_data) if meta_data else PaginationMeta()

        return SyncPage(
            data=items,
            meta=meta,
            client=self,
            path=path,
            params=params,
            model=model,
        )

    def post_list(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        model: Type[T],
    ) -> List[T]:
        response = self._request("POST", path, body=body)
        return parse_response_list(response=response, model=model)

    @overload
    def post(self, path: str, *, body: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., files: Optional[Any] = ..., model: Type[T], timeout: Optional[float] = ...) -> T: ...
    @overload
    def post(self, path: str, *, body: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., files: Optional[Any] = ..., model: None = ..., timeout: Optional[float] = ...) -> Dict[str, Any]: ...
    def post(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Any] = None,
        model: Optional[Type[T]] = None,
        timeout: Optional[float] = None,
    ) -> Union[T, Dict[str, Any]]:
        response = self._request("POST", path, body=body, params=params, files=files, timeout=timeout)
        if model is not None:
            return parse_response(response=response, model=model)
        return response.json()

    @overload
    def put(self, path: str, *, body: Optional[Dict[str, Any]] = ..., model: Type[T]) -> T: ...
    @overload
    def put(self, path: str, *, body: Optional[Dict[str, Any]] = ..., model: None = ...) -> Dict[str, Any]: ...
    def put(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any]]:
        response = self._request("PUT", path, body=body)
        if model is not None:
            return parse_response(response=response, model=model)
        return response.json()

    @overload
    def patch(self, path: str, *, body: Optional[Dict[str, Any]] = ..., model: Type[T]) -> T: ...
    @overload
    def patch(self, path: str, *, body: Optional[Dict[str, Any]] = ..., model: None = ...) -> Dict[str, Any]: ...
    def patch(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any]]:
        response = self._request("PATCH", path, body=body)
        if model is not None:
            return parse_response(response=response, model=model)
        return response.json()

    @overload
    def delete(self, path: str, *, body: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., model: Type[T]) -> T: ...
    @overload
    def delete(self, path: str, *, body: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., model: None = ...) -> Dict[str, Any]: ...
    def delete(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any]]:
        response = self._request("DELETE", path, body=body, params=params)
        if model is not None:
            return parse_response(response=response, model=model)
        return response.json()

    def stream_request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Any] = None,
    ) -> Stream:
        """Make a streaming request and return a Stream of SSE events."""
        headers = {"Accept": "text/event-stream"}
        response = self._request(
            method,
            path,
            body=body,
            params=params,
            headers=headers,
            files=files,
            stream=True,
        )
        return Stream(response)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> SyncAPIClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncAPIClient(_BaseClient):
    """Asynchronous HTTP client for the Rank API."""

    _client: httpx.AsyncClient

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        api_prefix: str = "",
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            api_prefix=api_prefix,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=custom_headers,
        )
        self._client = httpx.AsyncClient(
            timeout=timeout,
            limits=httpx.Limits(
                max_connections=DEFAULT_CONNECTION_LIMITS["max_connections"],
                max_keepalive_connections=DEFAULT_CONNECTION_LIMITS["max_keepalive_connections"],
            ),
            follow_redirects=True,
        )

    async def _request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
        files: Optional[Any] = None,
        stream: bool = False,
        timeout: Optional[float] = None,
    ) -> httpx.Response:
        import anyio

        url = self._build_url(path)
        req_headers = self._build_headers(headers)

        if files and (headers is None or "Accept" not in headers):
            req_headers.pop("Accept", None)

        if body is not None:
            body = strip_not_given(body)

        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}

        prev_timeout = None
        if timeout is not None:
            prev_timeout = self._client.timeout
            self._client.timeout = httpx.Timeout(timeout)

        try:
            for attempt in range(self._max_retries + 1):
                try:
                    request = self._client.build_request(
                        method,
                        url,
                        json=body if not files else None,
                        data=body if files else None,
                        params=params,
                        headers=req_headers,
                        files=files,
                    )
                    response = await self._client.send(request, stream=stream)

                except httpx.TimeoutException as e:
                    if attempt < self._max_retries:
                        await anyio.sleep(self._retry_delay(attempt))
                        continue
                    raise APITimeoutError(request=getattr(e, "request", None)) from e

                except httpx.ConnectError as e:
                    if attempt < self._max_retries:
                        await anyio.sleep(self._retry_delay(attempt))
                        continue
                    raise APIConnectionError(request=getattr(e, "request", None)) from e

                if self._should_retry(response, attempt):
                    if stream:
                        await response.aclose()
                    delay = self._retry_delay(attempt, response)
                    logger.debug("Retrying request to %s (attempt %d, status %d, delay %.1fs)", url, attempt + 1, response.status_code, delay)
                    await anyio.sleep(delay)
                    continue

                if response.status_code >= 400:
                    if stream:
                        await response.aread()
                    self._handle_error_response(response)

                return response

            raise APIConnectionError("Max retries exceeded")
        finally:
            if prev_timeout is not None:
                self._client.timeout = prev_timeout

    async def get(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        model: Type[T],
    ) -> T:
        response = await self._request("GET", path, params=params)
        return parse_response(response=response, model=model)

    async def get_list(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        model: Type[T],
    ) -> List[T]:
        response = await self._request("GET", path, params=params)
        return parse_response_list(response=response, model=model)

    async def _get_page(
        self,
        *,
        path: str,
        params: Dict[str, Any],
        model: Type[T],
    ) -> AsyncPage[T]:
        response = await self._request("GET", path, params=params)
        json_data = response.json()

        items_data = json_data.get("data", [])
        items = [model.model_validate(item) for item in items_data]  # type: ignore[union-attr]

        meta_data = json_data.get("meta", json_data.get("pagination", {}))
        meta = PaginationMeta.model_validate(meta_data) if meta_data else PaginationMeta()

        return AsyncPage(
            data=items,
            meta=meta,
            client=self,
            path=path,
            params=params,
            model=model,
        )

    async def post_list(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        model: Type[T],
    ) -> List[T]:
        response = await self._request("POST", path, body=body)
        return parse_response_list(response=response, model=model)

    @overload
    async def post(self, path: str, *, body: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., files: Optional[Any] = ..., model: Type[T], timeout: Optional[float] = ...) -> T: ...
    @overload
    async def post(self, path: str, *, body: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., files: Optional[Any] = ..., model: None = ..., timeout: Optional[float] = ...) -> Dict[str, Any]: ...
    async def post(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Any] = None,
        model: Optional[Type[T]] = None,
        timeout: Optional[float] = None,
    ) -> Union[T, Dict[str, Any]]:
        response = await self._request("POST", path, body=body, params=params, files=files, timeout=timeout)
        if model is not None:
            return parse_response(response=response, model=model)
        return response.json()

    @overload
    async def put(self, path: str, *, body: Optional[Dict[str, Any]] = ..., model: Type[T]) -> T: ...
    @overload
    async def put(self, path: str, *, body: Optional[Dict[str, Any]] = ..., model: None = ...) -> Dict[str, Any]: ...
    async def put(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any]]:
        response = await self._request("PUT", path, body=body)
        if model is not None:
            return parse_response(response=response, model=model)
        return response.json()

    @overload
    async def patch(self, path: str, *, body: Optional[Dict[str, Any]] = ..., model: Type[T]) -> T: ...
    @overload
    async def patch(self, path: str, *, body: Optional[Dict[str, Any]] = ..., model: None = ...) -> Dict[str, Any]: ...
    async def patch(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any]]:
        response = await self._request("PATCH", path, body=body)
        if model is not None:
            return parse_response(response=response, model=model)
        return response.json()

    @overload
    async def delete(self, path: str, *, body: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., model: Type[T]) -> T: ...
    @overload
    async def delete(self, path: str, *, body: Optional[Dict[str, Any]] = ..., params: Optional[Dict[str, Any]] = ..., model: None = ...) -> Dict[str, Any]: ...
    async def delete(
        self,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        model: Optional[Type[T]] = None,
    ) -> Union[T, Dict[str, Any]]:
        response = await self._request("DELETE", path, body=body, params=params)
        if model is not None:
            return parse_response(response=response, model=model)
        return response.json()

    async def stream_request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Any] = None,
    ) -> AsyncStream:
        """Make a streaming request and return an AsyncStream of SSE events."""
        headers = {"Accept": "text/event-stream"}
        response = await self._request(
            method,
            path,
            body=body,
            params=params,
            headers=headers,
            files=files,
            stream=True,
        )
        return AsyncStream(response)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncAPIClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
