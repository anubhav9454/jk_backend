"""Genre schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema


class GenreCreate(BaseModel):
    """Schema for creating a genre."""
    name: str = Field(..., min_length=1, max_length=100)


class GenreUpdate(BaseModel):
    """Schema for updating a genre."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class GenreResponse(BaseSchema):
    """Schema for genre response."""
    id: int
    name: str

