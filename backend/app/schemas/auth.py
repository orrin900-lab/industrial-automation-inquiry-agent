from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=1)


class AuthUser(BaseModel):
    email: str
    name: str
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser


class LogoutResponse(BaseModel):
    status: str = "success"
    message: str = "Client token can be cleared."
