from fastapi.testclient import TestClient

from app.main import app
from app.services.llm_client import LLMClient


client = TestClient(app)


def test_analyze_api_returns_agent_result_with_trace_and_retrieval(monkeypatch):
    monkeypatch.setattr(LLMClient, "is_available", lambda self: False)
    monkeypatch.setattr(LLMClient, "complete_json", lambda self, *args, **kwargs: None)

    payload = {
        "channel": "website",
        "customer_name": "John Smith",
        "customer_email": "john@example.com",
        "company": "ABC Automation",
        "country": "Vietnam",
        "subject": "PLC inquiry",
        "message": "We need a Siemens compatible PLC with 16DI and 8DO, 24V DC, RS485 communication.",
        "attachments": [],
    }

    response = client.post("/api/inquiries/analyze", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "success"
    assert "agent_result" in body

    result = body["agent_result"]
    assert result["product_category"] == "PLC"
    assert result["matched_products"]
    assert result["english_reply_draft"]
    assert result["risk_flags"]
    assert result["agent_trace"]
    assert result["retrieved_knowledge"]
    assert any(trace["mode"] == "fallback" for trace in result["agent_trace"])
