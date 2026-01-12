"""Book repository."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Book, Author, Genre
from app.repositories.base import BaseRepository
from app.schemas.book import BookCreate, BookUpdate


class BookRepository(BaseRepository[Book, BookCreate, BookUpdate]):
    """Repository for Book model."""
    
    async def get_with_relations(self, book_id: int) -> Optional[Book]:
        """
        Get book with author and genre loaded.
        
        Args:
            book_id: Book ID
            
        Returns:
            Book instance with relations or None
        """
        result = await self.db.execute(
            select(Book)
            .options(
                selectinload(Book.author),
                selectinload(Book.genre)
            )
            .where(Book.id == book_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_with_relations(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """
        Get all books with author and genre loaded.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of books with relations
        """
        result = await self.db.execute(
            select(Book)
            .options(
                selectinload(Book.author),
                selectinload(Book.genre)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def verify_author_exists(self, author_id: int) -> bool:
        """Verify author exists."""
        result = await self.db.execute(
            select(Author).where(Author.id == author_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def verify_genre_exists(self, genre_id: int) -> bool:
        """Verify genre exists."""
        result = await self.db.execute(
            select(Genre).where(Genre.id == genre_id)
        )
        return result.scalar_one_or_none() is not None

