from fastapi.testclient import TestClient

from app.main import app
from app.utils.config import get_config


client = TestClient(app)


def _login(email: str = "admin@example.com", password: str = "admin123") -> dict[str, str]:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_public_website_inquiry_submit_creates_pending_record():
    response = client.post(
        "/api/public/inquiries",
        json={
            "name": "Public Buyer",
            "email": "buyer@example.com",
            "company": "Public Automation",
            "country": "Vietnam",
            "product_category": "PLC",
            "message": "We need PLC modules for a packaging machine.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["inquiry"]["channel"] == "website"
    assert body["inquiry"]["status"] == "new"


def test_follow_up_status_update_requires_authenticated_role():
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

    unauthenticated = client.patch(
        f"/api/inquiries/{inquiry_id}/status",
        json={"status": "followed_up"},
    )
    assert unauthenticated.status_code == 401

    response = client.patch(
        f"/api/inquiries/{inquiry_id}/status",
        headers=_login("sales@example.com", "sales123"),
        json={"status": "followed_up"},
    )
    assert response.status_code == 200
    assert response.json()["inquiry"]["status"] == "followed_up"


def test_product_library_admin_api_and_sales_forbidden():
    sales_headers = _login("sales@example.com", "sales123")
    forbidden = client.get("/api/products", headers=sales_headers)
    assert forbidden.status_code == 403

    admin_headers = _login()
    listing = client.get("/api/products?limit=5", headers=admin_headers)
    assert listing.status_code == 200
    body = listing.json()
    assert body["items"]
    assert "CSVProductProvider" in body["provider_note"]

    create = client.post(
        "/api/products",
        headers=admin_headers,
        json={
            "product_id": "DEMO-FINAL-PLC",
            "product_name": "Demo Final PLC",
            "category": "PLC",
            "brand": "Demo",
            "model": "DF-PLC",
            "match_keywords": "plc;demo",
            "is_active": True,
        },
    )
    assert create.status_code == 200

    status = client.patch(
        "/api/products/DEMO-FINAL-PLC/status",
        headers=admin_headers,
        json={"is_active": False},
    )
    assert status.status_code == 200
    assert status.json()["product"]["is_active"] is False


def test_knowledge_upload_validation_and_success(monkeypatch, tmp_path):
    monkeypatch.setenv("ENABLE_QDRANT_RAG", "true")
    get_config.cache_clear()
    config = get_config()
    monkeypatch.setattr(config, "knowledge_upload_dir", tmp_path)

    headers = _login()
    invalid = client.post(
        "/api/knowledge/upload",
        headers=headers,
        json={"file_name": "notes.txt", "content": "not markdown"},
    )
    assert invalid.status_code == 200
    assert invalid.json()["success"] is False

    valid = client.post(
        "/api/knowledge/upload",
        headers=headers,
        json={"file_name": "demo_upload.md", "content": "# Demo\n\nKnowledge upload."},
    )
    assert valid.status_code == 200
    assert valid.json()["success"] is True


def test_system_status_redis_unavailable_fallback(monkeypatch):
    monkeypatch.setenv("ENABLE_REDIS", "true")
    monkeypatch.setenv("REDIS_URL", "redis://127.0.0.1:1/0")
    monkeypatch.setenv("REDIS_TIMEOUT_SECONDS", "0.1")
    get_config.cache_clear()

    response = client.get("/api/system/status")

    assert response.status_code == 200
    body = response.json()
    assert body["redis_enabled"] is True
    assert body["redis_available"] is False


def test_a_final_analyze_and_review_regression():
    analyze = client.post(
        "/api/inquiries/analyze",
        json={
            "channel": "email",
            "customer_name": "Email Buyer",
            "customer_email": "email@example.com",
            "company": "Email Automation",
            "country": "Thailand",
            "subject": "VFD inquiry",
            "message": "Please suggest a VFD for 2.2kW motor, 380V three phase.",
        },
    )
    assert analyze.status_code == 200
    inquiry_id = analyze.json()["inquiry_id"]
    assert analyze.json()["agent_result"]["matched_products"]

    review = client.post(
        f"/api/inquiries/{inquiry_id}/review",
        headers=_login("support@example.com", "support123"),
        json={
            "reviewer_name": "Support User",
            "review_status": "approved",
            "edited_reply": "Thank you for your inquiry. We will confirm details manually.",
            "reviewer_note": "Draft checked; no automatic quotation.",
        },
    )
    assert review.status_code == 200

    detail = client.get(f"/api/inquiries/{inquiry_id}")
    logs = detail.json()["review_logs"]
    assert logs[0]["reviewer_name"] == "support@example.com"
    assert logs[0]["reviewer_role"] == "support"
