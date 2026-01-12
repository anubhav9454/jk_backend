"""User schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.base import BaseSchema


class UserCreate(BaseModel):
    """Schema for creating a user."""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    role_names: Optional[List[str]] = Field(default=[], description="List of role names")


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    is_active: Optional[bool] = None
    role_names: Optional[List[str]] = None


class UserResponse(BaseSchema):
    """Schema for user response."""
    id: int
    username: str
    is_active: bool
    roles: List[str] = []

