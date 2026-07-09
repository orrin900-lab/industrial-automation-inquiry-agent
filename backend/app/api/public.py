from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.repositories.inquiry_repository import InquiryDbRepository
from app.repositories.inquiry_repository import inquiry_to_dict
from app.db.session import get_db
from app.schemas.inquiry import PublicInquiryInput


router = APIRouter(prefix="/public", tags=["public"])


@router.post("/inquiries")
def create_public_inquiry_endpoint(
    payload: PublicInquiryInput,
    db: Session = Depends(get_db),
) -> dict:
    try:
        repo = InquiryDbRepository(db)
        inquiry = repo.create(payload.to_inquiry_input())
        repo.update_status(inquiry, "new")
        db.commit()
        db.refresh(inquiry)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit public inquiry: {exc}",
        ) from exc

    return {
        "status": "success",
        "message": "Website inquiry submitted. Manual sales review is required.",
        "inquiry": inquiry_to_dict(inquiry),
    }
