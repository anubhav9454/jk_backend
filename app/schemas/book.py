"""Book schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema


class BookBase(BaseModel):
    """Base book schema."""
    title: str = Field(..., min_length=1, max_length=500)
    author_id: int = Field(..., gt=0)
    genre_id: int = Field(..., gt=0)
    year_published: int = Field(..., ge=1000, le=9999)


class BookCreate(BookBase):
    """Schema for creating a book."""
    summary: Optional[str] = Field(None, max_length=5000)


class BookUpdate(BaseModel):
    """Schema for updating a book."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author_id: Optional[int] = Field(None, gt=0)
    genre_id: Optional[int] = Field(None, gt=0)
    year_published: Optional[int] = Field(None, ge=1000, le=9999)
    summary: Optional[str] = Field(None, max_length=5000)


class BookResponse(BaseSchema):
    """Schema for book response."""
    id: int
    title: str
    author_id: int
    genre_id: int
    year_published: int
    summary: Optional[str] = None
    author_name: Optional[str] = None
    genre_name: Optional[str] = None

