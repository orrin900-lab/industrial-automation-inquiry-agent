from typing import Any

from pydantic import BaseModel, Field

from app.schemas.agent_trace import AgentTrace
from app.schemas.product import ProductCandidate
from app.schemas.requirement import ExtractedRequirement


class AgentResult(BaseModel):
    inquiry_type: str
    customer_intent: str
    product_category: str
    extracted_requirements: ExtractedRequirement
    missing_information: list[str] = Field(default_factory=list)
    matched_products: list[ProductCandidate] = Field(default_factory=list)
    clarification_questions: list[str] = Field(default_factory=list)
    english_reply_draft: str
    risk_flags: list[str] = Field(default_factory=list)
    sales_follow_up_suggestion: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    agent_trace: list[AgentTrace] = Field(default_factory=list)
    retrieved_knowledge: list[dict[str, Any]] = Field(default_factory=list)
