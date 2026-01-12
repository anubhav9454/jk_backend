"""Authentication schemas."""
from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    """Schema for user signup."""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)


class LoginRequest(BaseModel):
    """Schema for user login."""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """Schema for login response."""
    access_token: str
    token_type: str = "bearer"
    username: str

