from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.schemas.auth import AuthUser
from app.services.auth_service import get_user_by_email


bearer_scheme = HTTPBearer(auto_error=False)


def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AuthUser | None:
    if credentials is None:
        return None

    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError:
        return None

    email = payload.get("email")
    if not isinstance(email, str):
        return None
    return get_user_by_email(email)


def get_current_user(
    user: AuthUser | None = Depends(get_optional_current_user),
) -> AuthUser:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )
    return user


def require_roles(*roles: str) -> Callable[[AuthUser], AuthUser]:
    allowed_roles = set(roles)

    def dependency(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role permission.",
            )
        return user

    return dependency

