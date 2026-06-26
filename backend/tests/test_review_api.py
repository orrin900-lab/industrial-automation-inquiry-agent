from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_review_api_creates_review_log_and_updates_status():
    analyze = client.post(
        "/api/inquiries/analyze",
        json={
            "channel": "website",
            "subject": "HMI inquiry",
            "message": "We need a 7 inch HMI with Ethernet and Modbus TCP for packaging line.",
        },
    )
    assert analyze.status_code == 200
    inquiry_id = analyze.json()["inquiry_id"]

    review = client.post(
        f"/api/inquiries/{inquiry_id}/review",
        json={
            "reviewer_name": "Sales User",
            "review_status": "need_clarification",
            "edited_reply": "Thank you for your inquiry. Could you confirm the PLC model?",
            "reviewer_note": "Need to confirm PLC compatibility.",
        },
    )

    assert review.status_code == 200
    assert review.json() == {
        "status": "success",
        "inquiry_id": inquiry_id,
        "review_status": "need_clarification",
    }

    detail = client.get(f"/api/inquiries/{inquiry_id}")
    assert detail.status_code == 200
    body = detail.json()
    assert body["inquiry"]["status"] == "need_clarification"
    assert len(body["review_logs"]) == 1
    assert body["review_logs"][0]["reviewer_name"] == "Sales User"
