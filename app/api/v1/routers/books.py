"""Book endpoints."""
from fastapi import APIRouter, Depends, status
from typing import List

from app.services.book_service import BookService
from app.services.author_service import AuthorService
from app.services.genre_service import GenreService
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.api.deps import get_book_service, get_author_service, get_genre_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
    book: BookCreate,
    service: BookService = Depends(get_book_service)
):
    """Create a new book."""
    book_model = await service.create_book(book)
    return service.to_response(book_model)


@router.get("/", response_model=List[BookResponse])
async def get_books(
    skip: int = 0,
    limit: int = 100,
    service: BookService = Depends(get_book_service)
):
    """Get all books."""
    books = await service.get_all_books(skip=skip, limit=limit)
    return [service.to_response(book) for book in books]


@router.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    """Get a book by ID."""
    book = await service.get_book_with_relations(book_id)
    return service.to_response(book)


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    service: BookService = Depends(get_book_service)
):
    """Update a book."""
    book = await service.update_book(book_id, book_update)
    return service.to_response(book)


@router.get("/dropdown/authors", response_model=List[dict], tags=["Books"])
async def get_authors_dropdown(
    service: AuthorService = Depends(get_author_service)
):
    """Get authors for dropdown."""
    authors = await service.get_all_authors()
    return [{"id": a.id, "name": a.name} for a in authors]


@router.get("/dropdown/genres", response_model=List[dict], tags=["Books"])
async def get_genres_dropdown(
    service: GenreService = Depends(get_genre_service)
):
    """Get genres for dropdown."""
    genres = await service.get_all_genres()
    return [{"id": g.id, "name": g.name} for g in genres]

