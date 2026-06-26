from pydantic import BaseModel, Field


class ReviewInput(BaseModel):
    reviewer_name: str = Field(min_length=1)
    review_status: str = Field(min_length=1)
    edited_reply: str | None = None
    reviewer_note: str | None = None
