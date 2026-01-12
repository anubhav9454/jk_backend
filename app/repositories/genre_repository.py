"""Genre repository."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Genre
from app.repositories.base import BaseRepository
from app.schemas.genre import GenreCreate, GenreUpdate


class GenreRepository(BaseRepository[Genre, GenreCreate, GenreUpdate]):
    """Repository for Genre model."""
    
    async def get_by_name(self, name: str) -> Optional[Genre]:
        """
        Get genre by name.
        
        Args:
            name: Genre name
            
        Returns:
            Genre instance or None
        """
        result = await self.db.execute(
            select(Genre).where(Genre.name == name)
        )
        return result.scalar_one_or_none()
    
    async def check_has_books(self, genre_id: int) -> bool:
        """
        Check if genre has any books.
        
        Args:
            genre_id: Genre ID
            
        Returns:
            True if genre has books
        """
        from app.models import Book
        result = await self.db.execute(
            select(Book).where(Book.genre_id == genre_id).limit(1)
        )
        return result.scalar_one_or_none() is not None

