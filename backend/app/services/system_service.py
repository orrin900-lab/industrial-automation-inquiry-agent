from __future__ import annotations

import socket
from urllib.parse import urlparse

from app.schemas.system import SystemStatusResponse
from app.utils.config import AppConfig, get_config


def get_system_status(config: AppConfig | None = None) -> SystemStatusResponse:
    resolved_config = config or get_config()
    redis_available = False
    error_message: str | None = None

    if resolved_config.redis.enable_redis:
        try:
            redis_available = _ping_redis(
                resolved_config.redis.redis_url,
                timeout_seconds=resolved_config.redis.timeout_seconds,
            )
        except Exception as exc:
            error_message = str(exc)

    return SystemStatusResponse(
        redis_enabled=resolved_config.redis.enable_redis,
        redis_available=redis_available,
        redis_url=_redact_url(resolved_config.redis.redis_url),
        error_message=error_message,
    )


def _ping_redis(redis_url: str, *, timeout_seconds: float) -> bool:
    parsed = urlparse(redis_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 6379
    with socket.create_connection((host, port), timeout=timeout_seconds) as sock:
        sock.settimeout(timeout_seconds)
        sock.sendall(b"*1\r\n$4\r\nPING\r\n")
        response = sock.recv(64)
    return response.startswith(b"+PONG")


def _redact_url(redis_url: str) -> str:
    parsed = urlparse(redis_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 6379
    return f"{parsed.scheme or 'redis'}://{host}:{port}/{(parsed.path or '/0').lstrip('/')}"
