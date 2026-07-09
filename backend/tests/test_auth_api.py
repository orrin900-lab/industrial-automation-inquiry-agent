from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_me_and_logout_for_demo_admin():
    login = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "admin123"},
    )

    assert login.status_code == 200
    body = login.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"] == {
        "email": "admin@example.com",
        "name": "Admin User",
        "role": "admin",
    }

    me = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {body['access_token']}"},
    )

    assert me.status_code == 200
    assert me.json()["role"] == "admin"

    logout = client.post("/api/auth/logout")
    assert logout.status_code == 200
    assert logout.json()["status"] == "success"


def test_login_rejects_invalid_password():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "wrong"},
    )

    assert response.status_code == 401


def test_me_requires_authentication():
    response = client.get("/api/auth/me")

    assert response.status_code == 401

