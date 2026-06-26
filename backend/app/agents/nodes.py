from typing import Any

from app.agents.prompts import (
    INTENT_CLASSIFICATION_PROMPT,
    PRODUCT_CATEGORY_PROMPT,
    REPLY_DRAFT_PROMPT,
    RISK_CHECK_PROMPT,
    SYSTEM_GUARDRAILS,
)
from app.agents.state import AgentState
from app.data_access.product_repository import normalize_category
from app.rag.retriever import KnowledgeRetriever
from app.schemas.agent_result import AgentResult
from app.schemas.agent_trace import TraceMode
from app.services.llm_client import LLMClient
from app.services.missing_info_checker import MissingInfoChecker
from app.services.product_matcher import ProductMatcher
from app.services.reply_generator import ReplyGenerator
from app.services.requirement_extractor import RequirementExtractor
from app.services.risk_checker import RiskChecker
from app.utils.trace import append_trace, start_timer, summarize_text


ALLOWED_INTENTS = {
    "product_inquiry",
    "replacement_request",
    "technical_question",
    "cooperation_request",
    "after_sales",
    "unknown",
}

ALLOWED_CATEGORIES = {"PLC", "VFD", "HMI", "Industrial Switch", "Unknown"}


def normalize_inquiry(state: AgentState) -> AgentState:
    step_start = start_timer()
    try:
        inquiry = state.inquiry_input
        parts = [
            inquiry.subject or "",
            inquiry.message,
            inquiry.company or "",
            inquiry.country or "",
            inquiry.stated_product_category or "",
        ]
        state.normalized_text = "\n".join(part.strip() for part in parts if part.strip())
        append_trace(
            state.agent_trace,
            step_name="Inquiry Normalizer",
            mode="rule",
            input_summary=f"source={inquiry.source}",
            output_summary=summarize_text(state.normalized_text),
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Inquiry Normalizer", "rule", step_start, exc)
        raise


def classify_intent(state: AgentState) -> AgentState:
    step_start = start_timer()
    mode: TraceMode = "fallback"
    error_message: str | None = None
    try:
        llm_data, llm_mode, llm_error = _try_llm_json(
            INTENT_CLASSIFICATION_PROMPT,
            f"Inquiry text:\n{state.normalized_text}",
            response_name="intent_classification",
        )
        mode = llm_mode
        error_message = llm_error
        if llm_data:
            inquiry_type = str(llm_data.get("inquiry_type", "unknown"))
            customer_intent = str(llm_data.get("customer_intent", "")).strip()
            if inquiry_type in ALLOWED_INTENTS and customer_intent:
                state.inquiry_type = inquiry_type
                state.customer_intent = customer_intent
                append_trace(
                    state.agent_trace,
                    step_name="Intent Classifier",
                    mode="llm",
                    input_summary=summarize_text(state.normalized_text),
                    output_summary=f"{state.inquiry_type}: {state.customer_intent}",
                    start_time=step_start,
                )
                return state
            error_message = "LLM intent JSON missing allowed fields; used rule fallback."

        state.inquiry_type, state.customer_intent = _classify_intent_with_rules(
            state.normalized_text
        )
        append_trace(
            state.agent_trace,
            step_name="Intent Classifier",
            mode=mode if mode == "fallback" else "fallback",
            input_summary=summarize_text(state.normalized_text),
            output_summary=f"{state.inquiry_type}: {state.customer_intent}",
            error_message=error_message,
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Intent Classifier", mode, step_start, exc)
        raise


def classify_product_category(state: AgentState) -> AgentState:
    step_start = start_timer()
    mode: TraceMode = "fallback"
    error_message: str | None = None
    try:
        stated = normalize_category(state.inquiry_input.stated_product_category)
        if stated and stated != "Unknown":
            state.product_category = stated
            append_trace(
                state.agent_trace,
                step_name="Product Category Classifier",
                mode="rule",
                input_summary="User selected product category.",
                output_summary=state.product_category,
                start_time=step_start,
            )
            return state

        llm_data, llm_mode, llm_error = _try_llm_json(
            PRODUCT_CATEGORY_PROMPT,
            f"Inquiry text:\n{state.normalized_text}",
            response_name="product_category",
        )
        mode = llm_mode
        error_message = llm_error
        if llm_data:
            category = normalize_category(str(llm_data.get("product_category", "")))
            if category in ALLOWED_CATEGORIES:
                state.product_category = category
                append_trace(
                    state.agent_trace,
                    step_name="Product Category Classifier",
                    mode="llm",
                    input_summary=summarize_text(state.normalized_text),
                    output_summary=state.product_category,
                    start_time=step_start,
                )
                return state
            error_message = "LLM category JSON missing allowed product_category; used rule fallback."

        state.product_category = _classify_category_with_rules(state.normalized_text)
        append_trace(
            state.agent_trace,
            step_name="Product Category Classifier",
            mode=mode if mode == "fallback" else "fallback",
            input_summary=summarize_text(state.normalized_text),
            output_summary=state.product_category,
            error_message=error_message,
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Product Category Classifier", mode, step_start, exc)
        raise


def extract_requirements(state: AgentState) -> AgentState:
    step_start = start_timer()
    mode: TraceMode = "fallback"
    try:
        output = RequirementExtractor().extract(
            state.normalized_text,
            inquiry_input=state.inquiry_input,
            product_category=state.product_category,
        )
        mode = "llm" if output.used_llm else "fallback"
        state.extracted_requirements = output.requirement
        if output.requirement.product_category in ALLOWED_CATEGORIES:
            state.product_category = (
                output.requirement.product_category or state.product_category
            )
        append_trace(
            state.agent_trace,
            step_name="Requirement Extractor",
            mode=mode,
            input_summary=summarize_text(state.normalized_text),
            output_summary=(
                f"category={state.extracted_requirements.product_category}, "
                f"specs={len(state.extracted_requirements.technical_specs)}, "
                f"quantity={state.extracted_requirements.quantity or 'missing'}"
            ),
            error_message=output.error_message,
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Requirement Extractor", mode, step_start, exc)
        raise


def check_missing_information(state: AgentState) -> AgentState:
    step_start = start_timer()
    try:
        state.missing_information = MissingInfoChecker().check(state.extracted_requirements)
        append_trace(
            state.agent_trace,
            step_name="Missing Info Checker",
            mode="rule",
            input_summary=state.extracted_requirements.product_category or "Unknown",
            output_summary=", ".join(state.missing_information) or "No critical missing info.",
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Missing Info Checker", "rule", step_start, exc)
        raise


def retrieve_knowledge(state: AgentState) -> AgentState:
    step_start = start_timer()
    try:
        query = " ".join(
            [
                state.product_category,
                state.normalized_text,
                " ".join(state.missing_information),
            ]
        )
        state.retrieved_context = KnowledgeRetriever().retrieve(query)
        append_trace(
            state.agent_trace,
            step_name="Knowledge Retriever",
            mode="retrieval",
            input_summary=summarize_text(query),
            output_summary=_retrieval_summary(state.retrieved_context),
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Knowledge Retriever", "retrieval", step_start, exc)
        raise


def match_product_candidates(state: AgentState) -> AgentState:
    step_start = start_timer()
    try:
        state.matched_products = ProductMatcher().match(state.extracted_requirements)
        append_trace(
            state.agent_trace,
            step_name="Product Candidate Matcher",
            mode="rule",
            input_summary=state.extracted_requirements.model_dump_json(),
            output_summary=(
                f"{len(state.matched_products)} candidates: "
                + ", ".join(item.product_id for item in state.matched_products[:3])
            ),
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Product Candidate Matcher", "rule", step_start, exc)
        raise


def generate_reply_draft(state: AgentState) -> AgentState:
    step_start = start_timer()
    mode: TraceMode = "fallback"
    error_message: str | None = None
    try:
        llm_data, llm_mode, llm_error = _try_llm_json(
            REPLY_DRAFT_PROMPT,
            _reply_prompt_payload(state),
            response_name="reply_draft",
        )
        mode = llm_mode
        error_message = llm_error
        if llm_data:
            questions = llm_data.get("clarification_questions", [])
            reply = str(llm_data.get("english_reply_draft", "")).strip()
            if isinstance(questions, list) and reply:
                state.clarification_questions = [str(item) for item in questions if item]
                state.english_reply_draft = reply
                append_trace(
                    state.agent_trace,
                    step_name="Reply Draft Generator",
                    mode="llm",
                    input_summary=f"missing={state.missing_information}",
                    output_summary=summarize_text(state.english_reply_draft),
                    start_time=step_start,
                )
                return state
            error_message = "LLM reply JSON missing required fields; used template fallback."

        generator = ReplyGenerator()
        state.clarification_questions = generator.generate_questions(
            state.extracted_requirements, state.missing_information
        )
        state.english_reply_draft = generator.generate_reply(
            state.extracted_requirements,
            state.missing_information,
            state.matched_products,
            state.retrieved_context,
        )
        append_trace(
            state.agent_trace,
            step_name="Reply Draft Generator",
            mode=mode if mode == "fallback" else "fallback",
            input_summary=f"missing={state.missing_information}",
            output_summary=summarize_text(state.english_reply_draft),
            error_message=error_message,
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Reply Draft Generator", mode, step_start, exc)
        raise


def check_risks(state: AgentState) -> AgentState:
    step_start = start_timer()
    mode: TraceMode = "fallback"
    error_message: str | None = None
    try:
        rule_flags = RiskChecker().check(
            state.english_reply_draft, state.missing_information, state.matched_products
        )
        llm_data, llm_mode, llm_error = _try_llm_json(
            RISK_CHECK_PROMPT,
            _risk_prompt_payload(state),
            response_name="risk_check",
        )
        mode = "hybrid" if llm_mode == "llm" else "fallback"
        error_message = llm_error
        if llm_data and isinstance(llm_data.get("risk_flags"), list):
            state.risk_flags = _unique_strings(
                rule_flags + [str(item) for item in llm_data["risk_flags"] if item]
            )
        else:
            state.risk_flags = rule_flags
        append_trace(
            state.agent_trace,
            step_name="Risk Checker",
            mode=mode,
            input_summary=summarize_text(state.english_reply_draft),
            output_summary=f"{len(state.risk_flags)} risk flags",
            error_message=error_message if mode == "fallback" else None,
            start_time=step_start,
        )
        return state
    except Exception as exc:
        _append_error(state, "Risk Checker", mode, step_start, exc)
        raise


def build_final_result(state: AgentState) -> AgentState:
    step_start = start_timer()
    try:
        known_count = sum(
            1
            for value in [
                state.product_category if state.product_category != "Unknown" else None,
                state.extracted_requirements.quantity,
                state.extracted_requirements.application,
                state.matched_products,
            ]
            if value
        )
        missing_penalty = min(0.35, len(state.missing_information) * 0.05)
        confidence = max(0.2, min(0.9, 0.35 + known_count * 0.12 - missing_penalty))

        if state.missing_information:
            suggestion = (
                "Ask the customer to confirm missing technical fields before preparing quotation."
            )
        elif state.matched_products:
            suggestion = (
                "Review the candidate model manually, then confirm price, stock, and delivery time through the normal sales process."
            )
        else:
            suggestion = "Manual review required because no reliable candidate was found."

        state.sales_follow_up_suggestion = suggestion
        state.confidence_score = round(confidence, 2)
        state.final_result = AgentResult(
            inquiry_type=state.inquiry_type,
            customer_intent=state.customer_intent,
            product_category=state.product_category,
            extracted_requirements=state.extracted_requirements,
            missing_information=state.missing_information,
            matched_products=state.matched_products,
            clarification_questions=state.clarification_questions,
            english_reply_draft=state.english_reply_draft,
            risk_flags=state.risk_flags,
            sales_follow_up_suggestion=state.sales_follow_up_suggestion,
            confidence_score=state.confidence_score,
            agent_trace=state.agent_trace,
            retrieved_knowledge=state.retrieved_context,
        )
        append_trace(
            state.agent_trace,
            step_name="Final Agent Result",
            mode="rule",
            input_summary=f"category={state.product_category}",
            output_summary=f"confidence={state.confidence_score}",
            start_time=step_start,
        )
        if state.final_result:
            state.final_result.agent_trace = state.agent_trace
        return state
    except Exception as exc:
        _append_error(state, "Final Agent Result", "rule", step_start, exc)
        raise


def _try_llm_json(
    instruction_prompt: str, user_payload: str, *, response_name: str
) -> tuple[dict[str, Any] | None, TraceMode, str | None]:
    client = LLMClient()
    if not client.is_available():
        return None, "fallback", "LLM disabled or API key missing; used rule fallback."

    try:
        data = client.complete_json(
            SYSTEM_GUARDRAILS,
            instruction_prompt + "\n\n" + user_payload,
            response_name=response_name,
        )
    except Exception as exc:
        return None, "fallback", f"LLM call failed; used rule fallback: {exc}"

    if data:
        return data, "llm", None
    return None, "fallback", "LLM returned invalid or empty JSON; used rule fallback."


def _classify_intent_with_rules(text: str) -> tuple[str, str]:
    lowered = text.lower()
    if any(keyword in lowered for keyword in ["replacement", "alternative", "compatible"]):
        return (
            "replacement_request",
            "Customer is asking for a compatible or replacement industrial automation product.",
        )
    if any(keyword in lowered for keyword in ["technical", "how to", "compatibility"]):
        return (
            "technical_question",
            "Customer is asking for technical confirmation before product selection.",
        )
    if any(keyword in lowered for keyword in ["distributor", "cooperate", "partnership"]):
        return "cooperation_request", "Customer may be asking for business cooperation."
    if any(keyword in lowered for keyword in ["fault", "repair", "warranty", "after sales"]):
        return "after_sales", "Customer may be asking for after-sales support."
    if any(
        keyword in lowered
        for keyword in ["price", "quote", "quotation", "recommend", "need", "looking for"]
    ):
        return (
            "product_inquiry",
            "Customer is looking for product selection support before quotation.",
        )
    return "unknown", "Customer intent is unclear and needs manual review."


def _classify_category_with_rules(text: str) -> str:
    lowered = text.lower()
    if any(
        keyword in lowered
        for keyword in ["industrial switch", "poe", "gigabit", "fiber port", "factory network"]
    ):
        return "Industrial Switch"
    if any(
        keyword in lowered
        for keyword in ["hmi", "touch panel", "operator panel", "screen size"]
    ):
        return "HMI"
    if any(
        keyword in lowered
        for keyword in ["vfd", "inverter", "variable frequency", "motor drive", "drive for motor"]
    ):
        return "VFD"
    if any(
        keyword in lowered
        for keyword in ["plc", "programmable controller", "digital input", "digital output"]
    ):
        return "PLC"
    return "Unknown"


def _reply_prompt_payload(state: AgentState) -> str:
    return (
        "Generate a reply draft for this structured inquiry.\n"
        f"Extracted requirement JSON:\n{state.extracted_requirements.model_dump_json()}\n"
        f"Missing information: {state.missing_information}\n"
        f"Candidate products: {[item.model_dump(mode='json') for item in state.matched_products]}\n"
        f"Retrieved context: {state.retrieved_context}\n"
    )


def _risk_prompt_payload(state: AgentState) -> str:
    return (
        "Check this reply draft and candidate list.\n"
        f"Reply draft:\n{state.english_reply_draft}\n"
        f"Missing information: {state.missing_information}\n"
        f"Candidate product IDs: {[item.product_id for item in state.matched_products]}\n"
    )


def _retrieval_summary(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No knowledge chunks retrieved."
    sources = []
    for item in results[:3]:
        metadata = item.get("metadata", {})
        sources.append(
            f"{metadata.get('source_file', 'unknown')}:{metadata.get('section_title', 'section')}"
        )
    return f"{len(results)} chunks: " + "; ".join(sources)


def _unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique.append(normalized)
    return unique


def _append_error(
    state: AgentState,
    step_name: str,
    mode: TraceMode,
    step_start: float,
    exc: Exception,
) -> None:
    append_trace(
        state.agent_trace,
        step_name=step_name,
        mode=mode,
        input_summary="Node raised an exception.",
        output_summary="Failed.",
        success=False,
        error_message=str(exc),
        start_time=step_start,
    )
