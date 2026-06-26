from time import perf_counter

from app.schemas.agent_trace import AgentTrace, TraceMode


def start_timer() -> float:
    return perf_counter()


def elapsed_ms(start_time: float) -> float:
    return round((perf_counter() - start_time) * 1000, 2)


def append_trace(
    traces: list[AgentTrace],
    *,
    step_name: str,
    mode: TraceMode,
    input_summary: str,
    output_summary: str,
    start_time: float,
    success: bool = True,
    error_message: str | None = None,
) -> None:
    traces.append(
        AgentTrace(
            step_name=step_name,
            mode=mode,
            input_summary=_trim(input_summary),
            output_summary=_trim(output_summary),
            success=success,
            error_message=_trim(error_message) if error_message else None,
            latency_ms=elapsed_ms(start_time),
        )
    )


def summarize_text(text: str | None, limit: int = 140) -> str:
    return _trim(text or "", limit=limit)


def _trim(text: str, limit: int = 240) -> str:
    compact = " ".join(str(text).split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
