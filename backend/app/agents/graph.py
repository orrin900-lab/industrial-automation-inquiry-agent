from app.agents.nodes import (
    build_final_result,
    check_missing_information,
    check_risks,
    classify_intent,
    classify_product_category,
    extract_requirements,
    generate_reply_draft,
    match_product_candidates,
    normalize_inquiry,
    retrieve_knowledge,
)
from app.agents.state import AgentState
from app.schemas.agent_result import AgentResult
from app.schemas.inquiry import InquiryInput


def run_inquiry_agent(inquiry_input: InquiryInput | dict) -> AgentResult:
    """Run the C+ prototype agent with deterministic fallback logic."""
    validated_input = (
        inquiry_input
        if isinstance(inquiry_input, InquiryInput)
        else InquiryInput.model_validate(inquiry_input)
    )
    state = AgentState(inquiry_input=validated_input)

    for node in [
        normalize_inquiry,
        classify_intent,
        classify_product_category,
        extract_requirements,
        check_missing_information,
        retrieve_knowledge,
        match_product_candidates,
        generate_reply_draft,
        check_risks,
        build_final_result,
    ]:
        state = node(state)

    if state.final_result is None:
        raise RuntimeError("Agent workflow completed without a final result.")
    return state.final_result
