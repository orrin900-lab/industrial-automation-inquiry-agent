from fastapi.testclient import TestClient

from app.main import app
from app.utils.config import get_config


client = TestClient(app)


def _login(email: str, password: str) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_knowledge_api_requires_admin_role(monkeypatch):
    monkeypatch.setenv("ENABLE_QDRANT_RAG", "true")
    monkeypatch.setenv("QDRANT_URL", "http://127.0.0.1:1")
    monkeypatch.setenv("QDRANT_TIMEOUT_SECONDS", "0.2")
    get_config.cache_clear()

    unauthenticated = client.get("/api/knowledge/status")
    assert unauthenticated.status_code == 401

    sales_headers = _login("sales@example.com", "sales123")
    forbidden = client.get("/api/knowledge/status", headers=sales_headers)
    assert forbidden.status_code == 403

    admin_headers = _login("admin@example.com", "admin123")
    allowed = client.get("/api/knowledge/status", headers=admin_headers)
    assert allowed.status_code == 200
    assert allowed.json()["fallback_available"] is True


def test_review_records_authenticated_user():
    analyze = client.post(
        "/api/inquiries/analyze",
        json={
            "channel": "website",
            "subject": "PLC inquiry",
            "message": "We need a PLC with 16DI and 8DO, 24V DC, RS485 communication.",
        },
    )
    assert analyze.status_code == 200
    inquiry_id = analyze.json()["inquiry_id"]

    sales_headers = _login("sales@example.com", "sales123")
    review = client.post(
        f"/api/inquiries/{inquiry_id}/review",
        headers=sales_headers,
        json={
            "reviewer_name": "Manual Name",
            "review_status": "need_clarification",
            "edited_reply": "Thank you for your inquiry. Could you confirm output type?",
            "reviewer_note": "Need to confirm output type.",
        },
    )

    assert review.status_code == 200

    detail = client.get(f"/api/inquiries/{inquiry_id}")
    assert detail.status_code == 200
    logs = detail.json()["review_logs"]
    assert len(logs) == 1
    assert logs[0]["reviewer_name"] == "sales@example.com"
