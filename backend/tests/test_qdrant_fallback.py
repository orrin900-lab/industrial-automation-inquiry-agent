from app.agents.graph import run_inquiry_agent
from app.rag.retriever import KnowledgeRetriever
from app.schemas.inquiry import InquiryInput
from app.services.llm_client import LLMClient
from app.utils.config import get_config


def test_qdrant_unavailable_falls_back_to_keyword(monkeypatch):
    monkeypatch.setenv("ENABLE_QDRANT_RAG", "true")
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "qdrant")
    monkeypatch.setenv("QDRANT_URL", "http://127.0.0.1:1")
    monkeypatch.setenv("QDRANT_TIMEOUT_SECONDS", "0.2")
    get_config.cache_clear()

    retriever = KnowledgeRetriever()
    results = retriever.retrieve("PLC selection 16DI 8DO RS485", top_k=3)

    assert retriever.last_mode == "keyword_fallback"
    assert retriever.last_error
    assert results
    assert {"content", "score", "metadata"}.issubset(results[0].keys())


def test_agent_trace_records_keyword_fallback_when_qdrant_unavailable(monkeypatch):
    monkeypatch.setenv("ENABLE_QDRANT_RAG", "true")
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "qdrant")
    monkeypatch.setenv("QDRANT_URL", "http://127.0.0.1:1")
    monkeypatch.setenv("QDRANT_TIMEOUT_SECONDS", "0.2")
    monkeypatch.setattr(LLMClient, "is_available", lambda self: False)
    monkeypatch.setattr(LLMClient, "complete_json", lambda self, *args, **kwargs: None)
    get_config.cache_clear()

    result = run_inquiry_agent(
        InquiryInput(
            channel="website",
            customer_name="Test User",
            customer_email="test@example.com",
            company="Demo Automation",
            country="Vietnam",
            subject="PLC inquiry",
            message=(
                "We need a Siemens compatible PLC with 16DI and 8DO, "
                "24V DC, RS485 communication."
            ),
            attachments=[],
        )
    )

    assert result.retrieved_knowledge
    assert any(step.mode == "keyword_fallback" for step in result.agent_trace)
