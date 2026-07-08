from fastapi.testclient import TestClient

from app.main import app
from app.schemas.knowledge import KnowledgeReindexResponse
from app.services.llm_client import LLMClient
from app.utils.config import get_config


client = TestClient(app)


def _enable_unavailable_qdrant(monkeypatch):
    monkeypatch.setenv("ENABLE_QDRANT_RAG", "true")
    monkeypatch.setenv("RAG_RETRIEVAL_MODE", "qdrant")
    monkeypatch.setenv("QDRANT_URL", "http://127.0.0.1:1")
    monkeypatch.setenv("QDRANT_TIMEOUT_SECONDS", "0.2")
    get_config.cache_clear()


def test_knowledge_status_does_not_crash_when_qdrant_unavailable(monkeypatch):
    _enable_unavailable_qdrant(monkeypatch)

    response = client.get("/api/knowledge/status")

    assert response.status_code == 200
    body = response.json()
    assert body["qdrant_enabled"] is True
    assert body["qdrant_available"] is False
    assert body["fallback_available"] is True
    assert body["rag_mode"] == "keyword_fallback"
    assert body["collection_name"] == "industrial_agent_knowledge"
    assert body["error_message"]


def test_knowledge_chunks_returns_clear_error_structure(monkeypatch):
    _enable_unavailable_qdrant(monkeypatch)

    response = client.get("/api/knowledge/chunks?limit=5&offset=0")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"
    assert body["items"] == []
    assert body["total"] == 0
    assert body["limit"] == 5
    assert body["offset"] == 0
    assert body["error_message"]


def test_knowledge_reindex_can_be_mocked(monkeypatch):
    def fake_rebuild():
        return KnowledgeReindexResponse(
            success=True,
            collection_name="industrial_agent_knowledge",
            indexed_chunks=21,
            points_count=21,
            message="Qdrant index rebuilt successfully.",
        )

    monkeypatch.setattr("app.api.knowledge.rebuild_knowledge_index", fake_rebuild)

    response = client.post("/api/knowledge/reindex")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["indexed_chunks"] == 21
    assert body["points_count"] == 21


def test_knowledge_api_does_not_break_analyze(monkeypatch):
    _enable_unavailable_qdrant(monkeypatch)
    monkeypatch.setattr(LLMClient, "is_available", lambda self: False)
    monkeypatch.setattr(LLMClient, "complete_json", lambda self, *args, **kwargs: None)

    response = client.post(
        "/api/inquiries/analyze",
        json={
            "channel": "website",
            "customer_name": "John Smith",
            "customer_email": "john@example.com",
            "company": "ABC Automation",
            "country": "Vietnam",
            "subject": "PLC inquiry",
            "message": (
                "We need a Siemens compatible PLC with 16DI and 8DO, "
                "24V DC, RS485 communication."
            ),
            "attachments": [],
        },
    )

    assert response.status_code == 200
    result = response.json()["agent_result"]
    assert result["product_category"] == "PLC"
    assert result["retrieved_knowledge"]
    assert any(step["mode"] == "keyword_fallback" for step in result["agent_trace"])

