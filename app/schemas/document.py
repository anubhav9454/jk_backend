"""Document schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema


class DocumentCreate(BaseModel):
    """Schema for creating a document."""
    filename: str = Field(..., min_length=1, max_length=255)
    file_size: int = Field(default=0, ge=0)


class DocumentResponse(BaseSchema):
    """Schema for document response."""
    id: int
    filename: str
    uploaded_at: Optional[datetime] = None
    status: str
    file_size: int
    uploaded_by: Optional[int] = None

