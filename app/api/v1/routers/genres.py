"""Genre endpoints."""
from fastapi import APIRouter, Depends, status
from typing import List

from app.services.genre_service import GenreService
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse
from app.api.deps import get_genre_service

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.post("/", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
async def create_genre(
    genre: GenreCreate,
    service: GenreService = Depends(get_genre_service)
):
    """Create a new genre."""
    return await service.create_genre(genre)


@router.get("/", response_model=List[GenreResponse])
async def get_genres(
    service: GenreService = Depends(get_genre_service)
):
    """Get all genres."""
    return await service.get_all_genres()


@router.put("/{genre_id}", response_model=GenreResponse)
async def update_genre(
    genre_id: int,
    genre_update: GenreUpdate,
    service: GenreService = Depends(get_genre_service)
):
    """Update a genre."""
    return await service.update_genre(genre_id, genre_update)


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
    genre_id: int,
    service: GenreService = Depends(get_genre_service)
):
    """Delete a genre."""
    await service.delete_genre(genre_id)
    return None

