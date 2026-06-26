from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_samples_api_returns_sample_list():
    response = client.get("/api/inquiries/samples")
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "success"
    assert isinstance(body["samples"], list)
    assert body["samples"]
    assert {"id", "channel", "message", "expected_category"}.issubset(
        body["samples"][0].keys()
    )
