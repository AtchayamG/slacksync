from __future__ import annotations

import hashlib
import hmac
import time


MAX_SKEW_SECONDS = 60 * 5


def build_signature(signing_secret: str, timestamp: str, body: bytes) -> str:
    base = b"v0:" + timestamp.encode("utf-8") + b":" + body
    digest = hmac.new(signing_secret.encode("utf-8"), base, hashlib.sha256).hexdigest()
    return f"v0={digest}"


def verify_signature(
    signing_secret: str,
    timestamp: str | None,
    body: bytes,
    slack_signature: str | None,
    now: int | None = None,
) -> bool:
    if not signing_secret or not timestamp or not slack_signature:
        return False
    try:
        ts = int(timestamp)
    except ValueError:
        return False
    current = int(time.time()) if now is None else now
    if abs(current - ts) > MAX_SKEW_SECONDS:
        return False
    expected = build_signature(signing_secret, timestamp, body)
    return hmac.compare_digest(expected, slack_signature)

