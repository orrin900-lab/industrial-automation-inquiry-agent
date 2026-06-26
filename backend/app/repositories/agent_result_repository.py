from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AgentResultRecord
from app.schemas.agent_result import AgentResult


class AgentResultRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, inquiry_id: int, agent_result: AgentResult) -> AgentResultRecord:
        result_data = agent_result.model_dump(mode="json")
        record = AgentResultRecord(
            inquiry_id=inquiry_id,
            inquiry_type=agent_result.inquiry_type,
            customer_intent=agent_result.customer_intent,
            product_category=agent_result.product_category,
            extracted_requirements_json=result_data["extracted_requirements"],
            missing_information_json=result_data["missing_information"],
            matched_products_json=result_data["matched_products"],
            clarification_questions_json=result_data["clarification_questions"],
            english_reply_draft=agent_result.english_reply_draft,
            risk_flags_json=result_data["risk_flags"],
            sales_follow_up_suggestion=agent_result.sales_follow_up_suggestion,
            confidence_score=agent_result.confidence_score,
            agent_trace_json=result_data["agent_trace"],
            retrieved_knowledge_json=result_data["retrieved_knowledge"],
        )
        self.db.add(record)
        self.db.flush()
        return record

    def get_latest_for_inquiry(self, inquiry_id: int) -> AgentResultRecord | None:
        stmt = (
            select(AgentResultRecord)
            .where(AgentResultRecord.inquiry_id == inquiry_id)
            .order_by(AgentResultRecord.created_at.desc())
        )
        return self.db.execute(stmt).scalars().first()


def agent_result_to_dict(record: AgentResultRecord | None) -> dict | None:
    if record is None:
        return None
    return {
        "id": record.id,
        "inquiry_id": record.inquiry_id,
        "inquiry_type": record.inquiry_type,
        "customer_intent": record.customer_intent,
        "product_category": record.product_category,
        "extracted_requirements": record.extracted_requirements_json,
        "missing_information": record.missing_information_json,
        "matched_products": record.matched_products_json,
        "clarification_questions": record.clarification_questions_json,
        "english_reply_draft": record.english_reply_draft,
        "risk_flags": record.risk_flags_json,
        "sales_follow_up_suggestion": record.sales_follow_up_suggestion,
        "confidence_score": record.confidence_score,
        "agent_trace": record.agent_trace_json,
        "retrieved_knowledge": record.retrieved_knowledge_json,
        "created_at": record.created_at.isoformat() if record.created_at else None,
    }
