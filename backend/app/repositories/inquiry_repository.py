from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db.models import AgentResultRecord, Inquiry
from app.schemas.inquiry import InquiryInput


class InquiryDbRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, inquiry_input: InquiryInput) -> Inquiry:
        inquiry = Inquiry(
            channel=inquiry_input.source,
            customer_name=inquiry_input.name or inquiry_input.customer_name,
            customer_email=inquiry_input.email
            or inquiry_input.customer_email
            or inquiry_input.from_email,
            company=inquiry_input.company,
            country=inquiry_input.country,
            subject=inquiry_input.subject,
            message=inquiry_input.message,
            status="pending_analysis",
        )
        self.db.add(inquiry)
        self.db.flush()
        return inquiry

    def update_status(self, inquiry: Inquiry, status: str) -> Inquiry:
        inquiry.status = status
        self.db.add(inquiry)
        self.db.flush()
        return inquiry

    def get(self, inquiry_id: int) -> Inquiry | None:
        return self.db.get(Inquiry, inquiry_id)

    def list(
        self,
        *,
        status: str | None = None,
        channel: str | None = None,
        product_category: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        stmt: Select = select(Inquiry, AgentResultRecord).outerjoin(
            AgentResultRecord, AgentResultRecord.inquiry_id == Inquiry.id
        )
        if status:
            stmt = stmt.where(Inquiry.status == status)
        if channel:
            stmt = stmt.where(Inquiry.channel == channel)
        if product_category:
            stmt = stmt.where(AgentResultRecord.product_category == product_category)
        stmt = stmt.order_by(Inquiry.created_at.desc()).limit(limit).offset(offset)

        rows = self.db.execute(stmt).all()
        return [
            inquiry_list_item_to_dict(inquiry, agent_result)
            for inquiry, agent_result in rows
        ]


def inquiry_to_dict(inquiry: Inquiry) -> dict:
    return {
        "id": inquiry.id,
        "channel": inquiry.channel,
        "customer_name": inquiry.customer_name,
        "customer_email": inquiry.customer_email,
        "company": inquiry.company,
        "country": inquiry.country,
        "subject": inquiry.subject,
        "message": inquiry.message,
        "status": inquiry.status,
        "created_at": inquiry.created_at.isoformat() if inquiry.created_at else None,
        "updated_at": inquiry.updated_at.isoformat() if inquiry.updated_at else None,
    }


def inquiry_list_item_to_dict(
    inquiry: Inquiry, agent_result: AgentResultRecord | None
) -> dict:
    return {
        "id": inquiry.id,
        "channel": inquiry.channel,
        "customer_name": inquiry.customer_name,
        "company": inquiry.company,
        "country": inquiry.country,
        "subject": inquiry.subject,
        "status": inquiry.status,
        "product_category": agent_result.product_category if agent_result else None,
        "confidence_score": agent_result.confidence_score if agent_result else None,
        "created_at": inquiry.created_at.isoformat() if inquiry.created_at else None,
        "updated_at": inquiry.updated_at.isoformat() if inquiry.updated_at else None,
    }
