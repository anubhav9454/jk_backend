"""Author repository."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Author
from app.repositories.base import BaseRepository
from app.schemas.author import AuthorCreate, AuthorUpdate


class AuthorRepository(BaseRepository[Author, AuthorCreate, AuthorUpdate]):
    """Repository for Author model."""
    
    async def get_by_name(self, name: str) -> Optional[Author]:
        """
        Get author by name.
        
        Args:
            name: Author name
            
        Returns:
            Author instance or None
        """
        result = await self.db.execute(
            select(Author).where(Author.name == name)
        )
        return result.scalar_one_or_none()
    
    async def check_has_books(self, author_id: int) -> bool:
        """
        Check if author has any books.
        
        Args:
            author_id: Author ID
            
        Returns:
            True if author has books
        """
        from app.models import Book
        result = await self.db.execute(
            select(Book).where(Book.author_id == author_id).limit(1)
        )
        return result.scalar_one_or_none() is not None

