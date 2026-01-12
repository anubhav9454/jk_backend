"""Common schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List, Generic, TypeVar

T = TypeVar('T')


class GenerateSummaryRequest(BaseModel):
    """Schema for summary generation request."""
    content: str = Field(..., min_length=1)


class GenerateSummaryResponse(BaseModel):
    """Schema for summary generation response."""
    summary: str


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)


class PaginatedResponse(BaseModel, Generic[T]):
    """Schema for paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

