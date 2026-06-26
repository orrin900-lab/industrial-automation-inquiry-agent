from typing import Any

from pydantic import BaseModel, Field

from app.schemas.agent_result import AgentResult
from app.schemas.agent_trace import AgentTrace
from app.schemas.inquiry import InquiryInput
from app.schemas.product import ProductCandidate
from app.schemas.requirement import ExtractedRequirement


class AgentState(BaseModel):
    inquiry_input: InquiryInput
    normalized_text: str = ""
    inquiry_type: str = "unknown"
    customer_intent: str = "Intent has not been classified yet."
    product_category: str = "Unknown"
    extracted_requirements: ExtractedRequirement = Field(
        default_factory=ExtractedRequirement
    )
    missing_information: list[str] = Field(default_factory=list)
    retrieved_context: list[dict[str, Any]] = Field(default_factory=list)
    matched_products: list[ProductCandidate] = Field(default_factory=list)
    clarification_questions: list[str] = Field(default_factory=list)
    english_reply_draft: str = ""
    risk_flags: list[str] = Field(default_factory=list)
    sales_follow_up_suggestion: str = ""
    confidence_score: float = 0.0
    agent_trace: list[AgentTrace] = Field(default_factory=list)
    final_result: AgentResult | None = None
