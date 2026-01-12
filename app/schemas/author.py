"""Author schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema


class AuthorCreate(BaseModel):
    """Schema for creating an author."""
    name: str = Field(..., min_length=1, max_length=200)


class AuthorUpdate(BaseModel):
    """Schema for updating an author."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)


class AuthorResponse(BaseSchema):
    """Schema for author response."""
    id: int
    name: str

