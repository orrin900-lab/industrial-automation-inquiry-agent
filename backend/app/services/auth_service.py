from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.auth import AuthUser, LoginResponse


DEMO_USERS = {
    "admin@example.com": {
        "email": "admin@example.com",
        "name": "Admin User",
        "role": "admin",
        "password_hash": hash_password("admin123"),
    },
    "sales@example.com": {
        "email": "sales@example.com",
        "name": "Sales User",
        "role": "sales",
        "password_hash": hash_password("sales123"),
    },
    "support@example.com": {
        "email": "support@example.com",
        "name": "Support User",
        "role": "support",
        "password_hash": hash_password("support123"),
    },
}


def authenticate_user(email: str, password: str) -> LoginResponse | None:
    record = DEMO_USERS.get(email.lower())
    if not record or not verify_password(password, record["password_hash"]):
        return None

    user = AuthUser(email=record["email"], name=record["name"], role=record["role"])
    token = create_access_token(user.model_dump())
    return LoginResponse(access_token=token, user=user)


def get_user_by_email(email: str) -> AuthUser | None:
    record = DEMO_USERS.get(email.lower())
    if not record:
        return None
    return AuthUser(email=record["email"], name=record["name"], role=record["role"])

