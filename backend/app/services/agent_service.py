from sqlalchemy.orm import Session

from app.agents.graph import run_inquiry_agent
from app.data_providers.inquiry_source_provider import get_inquiry_source_provider
from app.repositories.agent_result_repository import (
    AgentResultRepository,
    agent_result_to_dict,
)
from app.repositories.agent_run_repository import AgentRunRepository
from app.repositories.inquiry_repository import (
    InquiryDbRepository,
    inquiry_to_dict,
)
from app.repositories.review_repository import ReviewRepository, review_log_to_dict
from app.schemas.agent_result import AgentResult
from app.schemas.inquiry import InquiryInput
from app.utils.config import get_config


def analyze_inquiry(inquiry_input: InquiryInput, db: Session | None = None):
    inquiry_input = get_inquiry_source_provider().normalize(inquiry_input)
    if db is None:
        return run_inquiry_agent(inquiry_input)
    return analyze_and_persist_inquiry(inquiry_input, db)


def analyze_and_persist_inquiry(inquiry_input: InquiryInput, db: Session) -> dict:
    inquiry_repo = InquiryDbRepository(db)
    result_repo = AgentResultRepository(db)
    run_repo = AgentRunRepository(db)

    inquiry = inquiry_repo.create(inquiry_input)
    run = run_repo.create(
        inquiry_id=inquiry.id,
        model_name=get_config().llm.openai_model,
        execution_mode="pending",
    )
    db.commit()

    try:
        inquiry_repo.update_status(inquiry, "pending_analysis")
        agent_result = run_inquiry_agent(inquiry_input)
        result_record = result_repo.create(
            inquiry_id=inquiry.id, agent_result=agent_result
        )
        run_repo.create_steps(agent_run_id=run.id, traces=agent_result.agent_trace)
        run_repo.mark_finished(
            run,
            status="success",
            execution_mode=_execution_mode(agent_result),
        )
        inquiry_repo.update_status(inquiry, "pending_review")
        db.commit()
        db.refresh(inquiry)
        db.refresh(result_record)
        return {
            "inquiry_id": inquiry.id,
            "agent_result_id": result_record.id,
            "agent_result": agent_result,
        }
    except Exception as exc:
        db.rollback()
        run = db.merge(run)
        inquiry = db.merge(inquiry)
        run_repo.mark_finished(run, status="failed", error_message=str(exc))
        inquiry_repo.update_status(inquiry, "pending_analysis")
        db.commit()
        raise RuntimeError(f"Agent execution failed: {exc}") from exc


def list_inquiries(
    db: Session,
    *,
    status: str | None = None,
    channel: str | None = None,
    product_category: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    return InquiryDbRepository(db).list(
        status=status,
        channel=channel,
        product_category=product_category,
        limit=limit,
        offset=offset,
    )


def get_inquiry_detail(inquiry_id: int, db: Session) -> dict | None:
    inquiry_repo = InquiryDbRepository(db)
    result_repo = AgentResultRepository(db)
    review_repo = ReviewRepository(db)

    inquiry = inquiry_repo.get(inquiry_id)
    if inquiry is None:
        return None

    result = result_repo.get_latest_for_inquiry(inquiry_id)
    review_logs = review_repo.list_for_inquiry(inquiry_id)
    return {
        "inquiry": inquiry_to_dict(inquiry),
        "agent_result": agent_result_to_dict(result),
        "review_logs": [review_log_to_dict(log) for log in review_logs],
    }


def create_review(
    db: Session,
    *,
    inquiry_id: int,
    reviewer_name: str,
    review_status: str,
    edited_reply: str | None = None,
    reviewer_note: str | None = None,
) -> dict | None:
    inquiry_repo = InquiryDbRepository(db)
    inquiry = inquiry_repo.get(inquiry_id)
    if inquiry is None:
        return None

    log = ReviewRepository(db).create(
        inquiry_id=inquiry_id,
        reviewer_name=reviewer_name,
        review_status=review_status,
        edited_reply=edited_reply,
        reviewer_note=reviewer_note,
    )
    inquiry_repo.update_status(inquiry, review_status)
    db.commit()
    db.refresh(log)
    return review_log_to_dict(log)


def _execution_mode(agent_result: AgentResult) -> str:
    modes = {trace.mode for trace in agent_result.agent_trace}
    if "llm" in modes and "fallback" in modes:
        return "hybrid"
    if "llm" in modes:
        return "llm"
    if "fallback" in modes:
        return "fallback"
    return "rule"
