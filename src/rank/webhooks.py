"""Helpers for verifying Rank outbound webhook signatures."""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Mapping, Union

from ._exceptions import SignatureVerificationError

DEFAULT_TOLERANCE_SECONDS = 300


def _header(headers: Mapping[str, str], name: str) -> str:
    lower = name.lower()
    for key, value in headers.items():
        if key.lower() == lower:
            return value
    return ""


def verify_signature(
    payload: Union[bytes, str],
    headers: Mapping[str, str],
    secret: str,
    *,
    tolerance: int = DEFAULT_TOLERANCE_SECONDS,
) -> bool:
    """Return ``True`` if the request is a genuine Rank webhook delivery.

    The signature is HMAC-SHA256 of ``{timestamp}.{raw_body}``, prefixed with
    ``v1=``. Compare against ``X-Rank-Signature`` in constant time and reject
    timestamps older than *tolerance* seconds (default 5 minutes).

    Args:
        payload: Raw request body. Must be the bytes as received — do not
            re-serialize parsed JSON.
        headers: Request headers (case-insensitive).
        secret: Shared secret returned when the subscription was created.
        tolerance: Maximum age of ``X-Rank-Timestamp`` in seconds.

    Raises:
        SignatureVerificationError: If the signature, timestamp, or secret
            is missing or does not match.
    """
    raw = payload if isinstance(payload, bytes) else payload.encode("utf-8")
    timestamp = _header(headers, "X-Rank-Timestamp")
    signature = _header(headers, "X-Rank-Signature")

    if not timestamp.isdigit() or not signature.startswith("v1="):
        raise SignatureVerificationError("Missing or malformed Rank webhook signature headers")

    age = abs(time.time() - int(timestamp))
    if age > tolerance:
        raise SignatureVerificationError("Webhook timestamp is outside the allowed tolerance")

    expected = "v1=" + hmac.new(
        secret.encode("utf-8"),
        timestamp.encode("utf-8") + b"." + raw,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise SignatureVerificationError("Webhook signature does not match")

    return True
