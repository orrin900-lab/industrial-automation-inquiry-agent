from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ReviewLog


class ReviewRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        inquiry_id: int,
        reviewer_name: str,
        review_status: str,
        reviewer_role: str | None = None,
        edited_reply: str | None = None,
        reviewer_note: str | None = None,
    ) -> ReviewLog:
        log = ReviewLog(
            inquiry_id=inquiry_id,
            reviewer_name=reviewer_name,
            reviewer_role=reviewer_role,
            review_status=review_status,
            edited_reply=edited_reply,
            reviewer_note=reviewer_note,
        )
        self.db.add(log)
        self.db.flush()
        return log

    def list_for_inquiry(self, inquiry_id: int) -> list[ReviewLog]:
        stmt = (
            select(ReviewLog)
            .where(ReviewLog.inquiry_id == inquiry_id)
            .order_by(ReviewLog.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())


def review_log_to_dict(log: ReviewLog) -> dict:
    return {
        "id": log.id,
        "inquiry_id": log.inquiry_id,
        "reviewer_name": log.reviewer_name,
        "reviewer_role": log.reviewer_role,
        "review_status": log.review_status,
        "edited_reply": log.edited_reply,
        "reviewer_note": log.reviewer_note,
        "created_at": log.created_at.isoformat() if log.created_at else None,
    }
