from fastapi.testclient import TestClient

from app.main import app
from app.services.llm_client import LLMClient
from app.utils.config import get_config


client = TestClient(app)


def _admin_headers() -> dict[str, str]:
    login = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "admin123"},
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_analyze_still_works_when_reserved_product_provider_is_configured(monkeypatch):
    monkeypatch.setenv("PRODUCT_PROVIDER", "erp")
    monkeypatch.setenv("INQUIRY_SOURCE_PROVIDER", "manual")
    get_config.cache_clear()
    monkeypatch.setattr(LLMClient, "is_available", lambda self: False)
    monkeypatch.setattr(LLMClient, "complete_json", lambda self, *args, **kwargs: None)

    response = client.post(
        "/api/inquiries/analyze",
        json={
            "channel": "website",
            "subject": "PLC inquiry",
            "message": "We need a Siemens compatible PLC with 16DI and 8DO, 24V DC, RS485 communication.",
            "attachments": [],
        },
    )

    assert response.status_code == 200
    result = response.json()["agent_result"]
    assert result["product_category"] == "PLC"
    assert result["matched_products"]


def test_knowledge_and_auth_still_work_after_a9_provider_changes(monkeypatch):
    monkeypatch.setenv("QDRANT_URL", "http://127.0.0.1:1")
    monkeypatch.setenv("QDRANT_TIMEOUT_SECONDS", "0.2")
    get_config.cache_clear()

    headers = _admin_headers()
    response = client.get("/api/knowledge/status", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["fallback_available"] is True
    assert "collection_name" in body

