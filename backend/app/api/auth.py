from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.auth import AuthUser, LoginRequest, LoginResponse, LogoutResponse
from app.services.auth_service import authenticate_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    result = authenticate_user(payload.email, payload.password)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    return result


@router.get("/me", response_model=AuthUser)
def get_me(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    return user


@router.post("/logout", response_model=LogoutResponse)
def logout() -> LogoutResponse:
    return LogoutResponse()

