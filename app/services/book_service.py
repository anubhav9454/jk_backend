"""Book service for business logic."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.models import Book
from app.exceptions.exceptions import (
    BookNotFoundError,
    AuthorNotFoundError,
    GenreNotFoundError,
)
import asyncio
from app.services.search_service import rag_pipeline


class BookService:
    """Service for book business logic."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize book service.
        
        Args:
            db: Database session
        """
        self.repo = BookRepository(Book, db)
    
    async def create_book(self, data: BookCreate) -> Book:
        """
        Create a new book with validation.
        
        Args:
            data: Book creation data
            
        Returns:
            Created book
            
        Raises:
            AuthorNotFoundError: If author doesn't exist
            GenreNotFoundError: If genre doesn't exist
        """
        # Verify author exists
        if not await self.repo.verify_author_exists(data.author_id):
            raise AuthorNotFoundError(f"Author with id {data.author_id} not found")
        
        # Verify genre exists
        if not await self.repo.verify_genre_exists(data.genre_id):
            raise GenreNotFoundError(f"Genre with id {data.genre_id} not found")
        
        # Create book
        book = await self.repo.create(data)
        
        # Index book for RAG (async task)
        asyncio.create_task(rag_pipeline.index_book(self.repo.db, book.id))
        
        return book
    
    async def get_book(self, book_id: int) -> Book:
        """
        Get a book by ID.
        
        Args:
            book_id: Book ID
            
        Returns:
            Book instance
            
        Raises:
            BookNotFoundError: If book doesn't exist
        """
        book = await self.repo.get(book_id)
        if not book:
            raise BookNotFoundError(f"Book with id {book_id} not found")
        return book
    
    async def get_book_with_relations(self, book_id: int) -> Book:
        """
        Get a book with author and genre loaded.
        
        Args:
            book_id: Book ID
            
        Returns:
            Book instance with relations
            
        Raises:
            BookNotFoundError: If book doesn't exist
        """
        book = await self.repo.get_with_relations(book_id)
        if not book:
            raise BookNotFoundError(f"Book with id {book_id} not found")
        return book
    
    async def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """
        Get all books with relations.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of books
        """
        return await self.repo.get_all_with_relations(skip=skip, limit=limit)
    
    async def update_book(self, book_id: int, data: BookUpdate) -> Book:
        """
        Update a book.
        
        Args:
            book_id: Book ID
            data: Update data
            
        Returns:
            Updated book
            
        Raises:
            BookNotFoundError: If book doesn't exist
            AuthorNotFoundError: If author doesn't exist
            GenreNotFoundError: If genre doesn't exist
        """
        book = await self.repo.get(book_id)
        if not book:
            raise BookNotFoundError(f"Book with id {book_id} not found")
        
        # Verify author if being updated
        if data.author_id is not None:
            if not await self.repo.verify_author_exists(data.author_id):
                raise AuthorNotFoundError(f"Author with id {data.author_id} not found")
        
        # Verify genre if being updated
        if data.genre_id is not None:
            if not await self.repo.verify_genre_exists(data.genre_id):
                raise GenreNotFoundError(f"Genre with id {data.genre_id} not found")
        
        return await self.repo.update(book, data)
    
    async def delete_book(self, book_id: int) -> bool:
        """
        Delete a book.
        
        Args:
            book_id: Book ID
            
        Returns:
            True if deleted
            
        Raises:
            BookNotFoundError: If book doesn't exist
        """
        book = await self.repo.get(book_id)
        if not book:
            raise BookNotFoundError(f"Book with id {book_id} not found")
        
        return await self.repo.delete(book_id)
    
    def to_response(self, book: Book) -> BookResponse:
        """
        Convert book model to response schema.
        
        Args:
            book: Book model instance
            
        Returns:
            BookResponse schema
        """
        return BookResponse(
            id=book.id,
            title=book.title,
            author_id=book.author_id,
            genre_id=book.genre_id,
            year_published=book.year_published,
            summary=book.summary,
            author_name=book.author.name if book.author else None,
            genre_name=book.genre.name if book.genre else None,
        )

