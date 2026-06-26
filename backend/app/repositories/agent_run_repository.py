from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import AgentRun, AgentStep
from app.schemas.agent_trace import AgentTrace


class AgentRunRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        inquiry_id: int,
        model_name: str | None = None,
        execution_mode: str | None = None,
    ) -> AgentRun:
        run = AgentRun(
            inquiry_id=inquiry_id,
            status="running",
            model_name=model_name,
            execution_mode=execution_mode,
        )
        self.db.add(run)
        self.db.flush()
        return run

    def mark_finished(
        self,
        run: AgentRun,
        *,
        status: str = "success",
        error_message: str | None = None,
        execution_mode: str | None = None,
    ) -> AgentRun:
        run.status = status
        run.finished_at = datetime.utcnow()
        run.error_message = error_message
        if execution_mode:
            run.execution_mode = execution_mode
        self.db.add(run)
        self.db.flush()
        return run

    def create_steps(self, *, agent_run_id: int, traces: list[AgentTrace]) -> list[AgentStep]:
        steps: list[AgentStep] = []
        for trace in traces:
            step = AgentStep(
                agent_run_id=agent_run_id,
                step_name=trace.step_name,
                mode=trace.mode,
                input_summary=trace.input_summary,
                output_summary=trace.output_summary,
                success=trace.success,
                error_message=trace.error_message,
                latency_ms=trace.latency_ms,
            )
            self.db.add(step)
            steps.append(step)
        self.db.flush()
        return steps


def agent_step_to_dict(step: AgentStep) -> dict:
    return {
        "id": step.id,
        "agent_run_id": step.agent_run_id,
        "step_name": step.step_name,
        "mode": step.mode,
        "input_summary": step.input_summary,
        "output_summary": step.output_summary,
        "success": step.success,
        "error_message": step.error_message,
        "latency_ms": step.latency_ms,
        "created_at": step.created_at.isoformat() if step.created_at else None,
    }
