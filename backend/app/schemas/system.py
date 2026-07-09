from pydantic import BaseModel


class SystemStatusResponse(BaseModel):
    status: str = "ok"
    service: str = "industrial-inquiry-agent-backend"
    redis_enabled: bool
    redis_available: bool
    redis_url: str
    error_message: str | None = None
