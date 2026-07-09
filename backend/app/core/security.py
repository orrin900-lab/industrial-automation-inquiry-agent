import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any


AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "demo-auth-secret-change-me")
AUTH_TOKEN_TTL_SECONDS = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "28800"))
PASSWORD_SALT = os.getenv("AUTH_PASSWORD_SALT", "industrial-agent-demo-salt")


def hash_password(password: str) -> str:
    return hashlib.sha256(f"{PASSWORD_SALT}:{password}".encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


def create_access_token(payload: dict[str, Any]) -> str:
    token_payload = {
        **payload,
        "exp": int(time.time()) + AUTH_TOKEN_TTL_SECONDS,
    }
    body = _base64url_encode(json.dumps(token_payload, separators=(",", ":")).encode("utf-8"))
    signature = _sign(body)
    return f"{body}.{signature}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        body, signature = token.split(".", 1)
    except ValueError as exc:
        raise ValueError("Invalid token format.") from exc

    expected_signature = _sign(body)
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Invalid token signature.")

    try:
        payload = json.loads(_base64url_decode(body).decode("utf-8"))
    except Exception as exc:
        raise ValueError("Invalid token payload.") from exc

    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(time.time()):
        raise ValueError("Token has expired.")

    return payload


def _sign(body: str) -> str:
    digest = hmac.new(AUTH_SECRET_KEY.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    return _base64url_encode(digest)


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}".encode("ascii"))

