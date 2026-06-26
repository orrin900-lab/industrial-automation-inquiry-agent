from fastapi.testclient import TestClient

from app.db.models import AgentResultRecord, AgentStep, Inquiry
from app.db.session import SessionLocal
from app.main import app
from app.services.llm_client import LLMClient


client = TestClient(app)


def test_analyze_persists_inquiry_result_and_steps(monkeypatch):
    monkeypatch.setattr(LLMClient, "is_available", lambda self: False)
    monkeypatch.setattr(LLMClient, "complete_json", lambda self, *args, **kwargs: None)

    response = client.post(
        "/api/inquiries/analyze",
        json={
            "channel": "website",
            "customer_name": "Jane Buyer",
            "customer_email": "jane@example.com",
            "company": "Factory Demo",
            "country": "Vietnam",
            "subject": "PLC inquiry",
            "message": "Need PLC with 16DI, 8DO, 24V DC and RS485 for packaging machine.",
            "attachments": [],
        },
    )

    assert response.status_code == 200
    body = response.json()
    inquiry_id = body["inquiry_id"]
    agent_result_id = body["agent_result_id"]

    with SessionLocal() as db:
        inquiry = db.get(Inquiry, inquiry_id)
        result = db.get(AgentResultRecord, agent_result_id)
        steps = db.query(AgentStep).all()

    assert inquiry is not None
    assert inquiry.status == "pending_review"
    assert result is not None
    assert result.product_category == "PLC"
    assert steps


def test_list_and_detail_endpoints_return_persisted_data():
    analyze = client.post(
        "/api/inquiries/analyze",
        json={
            "channel": "email",
            "subject": "VFD inquiry",
            "message": "We need 2.2kW VFD for water pump, 380V three phase. Quantity 3 pcs.",
        },
    )
    assert analyze.status_code == 200
    inquiry_id = analyze.json()["inquiry_id"]

    list_response = client.get("/api/inquiries")
    assert list_response.status_code == 200
    items = list_response.json()["items"]
    assert items
    assert any(item["id"] == inquiry_id for item in items)

    detail_response = client.get(f"/api/inquiries/{inquiry_id}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["inquiry"]["id"] == inquiry_id
    assert detail["agent_result"]["product_category"] == "VFD"
    assert isinstance(detail["review_logs"], list)
