from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_optional_current_user
from app.data_access.inquiry_repository import InquiryRepository
from app.db.session import get_db
from app.schemas.auth import AuthUser
from app.schemas.inquiry import InquiryInput
from app.schemas.review import ReviewInput
from app.services.agent_service import (
    analyze_inquiry,
    create_review,
    get_inquiry_detail,
    list_inquiries,
)


router = APIRouter(prefix="/inquiries", tags=["inquiries"])


@router.post("/analyze")
def analyze_inquiry_endpoint(
    inquiry_input: InquiryInput, db: Session = Depends(get_db)
) -> dict:
    try:
        output = analyze_inquiry(inquiry_input, db)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze inquiry: {exc}",
        ) from exc

    return {
        "status": "success",
        "inquiry_id": output["inquiry_id"],
        "agent_result_id": output["agent_result_id"],
        "agent_result": output["agent_result"].model_dump(mode="json"),
    }


@router.get("/samples")
def list_sample_inquiries() -> dict:
    try:
        samples = InquiryRepository().list_sample_inquiries()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load sample inquiries: {exc}",
        ) from exc

    return {
        "status": "success",
        "samples": samples,
    }


@router.get("")
def list_inquiries_endpoint(
    status: str | None = None,
    channel: str | None = None,
    product_category: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
) -> dict:
    items = list_inquiries(
        db,
        status=status,
        channel=channel,
        product_category=product_category,
        limit=limit,
        offset=offset,
    )
    return {
        "status": "success",
        "items": items,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{inquiry_id}")
def get_inquiry_detail_endpoint(
    inquiry_id: int, db: Session = Depends(get_db)
) -> dict:
    detail = get_inquiry_detail(inquiry_id, db)
    if detail is None:
        raise HTTPException(status_code=404, detail="Inquiry not found.")
    return detail


@router.post("/{inquiry_id}/review")
def create_review_endpoint(
    inquiry_id: int,
    review_input: ReviewInput,
    db: Session = Depends(get_db),
    current_user: AuthUser | None = Depends(get_optional_current_user),
) -> dict:
    reviewer_name = current_user.email if current_user else review_input.reviewer_name
    log = create_review(
        db,
        inquiry_id=inquiry_id,
        reviewer_name=reviewer_name,
        review_status=review_input.review_status,
        edited_reply=review_input.edited_reply,
        reviewer_note=review_input.reviewer_note,
    )
    if log is None:
        raise HTTPException(status_code=404, detail="Inquiry not found.")
    return {
        "status": "success",
        "inquiry_id": inquiry_id,
        "review_status": review_input.review_status,
    }
