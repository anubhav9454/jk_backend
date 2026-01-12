"""Author endpoints."""
from fastapi import APIRouter, Depends, status
from typing import List

from app.services.author_service import AuthorService
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.api.deps import get_author_service
from app.exceptions.handlers import custom_exception_handler

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
    author: AuthorCreate,
    service: AuthorService = Depends(get_author_service)
):
    """Create a new author."""
    return await service.create_author(author)


@router.get("/", response_model=List[AuthorResponse])
async def get_authors(
    service: AuthorService = Depends(get_author_service)
):
    """Get all authors."""
    return await service.get_all_authors()


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author_update: AuthorUpdate,
    service: AuthorService = Depends(get_author_service)
):
    """Update an author."""
    return await service.update_author(author_id, author_update)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int,
    service: AuthorService = Depends(get_author_service)
):
    """Delete an author."""
    await service.delete_author(author_id)
    return None

