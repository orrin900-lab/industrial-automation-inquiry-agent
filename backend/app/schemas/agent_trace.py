from typing import Literal

from pydantic import BaseModel, Field


TraceMode = Literal["rule", "llm", "fallback", "mock", "retrieval", "hybrid"]


class AgentTrace(BaseModel):
    step_name: str
    mode: TraceMode
    input_summary: str
    output_summary: str
    success: bool = True
    error_message: str | None = None
    latency_ms: float = Field(ge=0.0)
