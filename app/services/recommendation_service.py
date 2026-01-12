"""Recommendation service for book recommendations."""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Book, Genre
from app.exceptions.exceptions import GenreNotFoundError


class RecommendationService:
    """Service for book recommendations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize recommendation service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def recommend_books_by_genre(self, genre_id: int) -> List[Book]:
        """
        Get book recommendations by genre ID.
        
        Args:
            genre_id: Genre ID
            
        Returns:
            List of books in the genre
            
        Raises:
            GenreNotFoundError: If genre doesn't exist
        """
        # Verify genre exists
        result = await self.db.execute(
            select(Genre).where(Genre.id == genre_id)
        )
        genre = result.scalar_one_or_none()
        
        if not genre:
            raise GenreNotFoundError(f"Genre with id {genre_id} not found")
        
        # Get books by genre_id (fix: use genre_id, not genre column)
        result = await self.db.execute(
            select(Book)
            .options(
                selectinload(Book.author),
                selectinload(Book.genre)
            )
            .where(Book.genre_id == genre_id)
        )
        return result.scalars().all()
    
    async def recommend_books_by_genre_name(self, genre_name: str) -> List[Book]:
        """
        Get book recommendations by genre name.
        
        Args:
            genre_name: Genre name
            
        Returns:
            List of books in the genre
            
        Raises:
            GenreNotFoundError: If genre doesn't exist
        """
        # Find genre by name
        result = await self.db.execute(
            select(Genre).where(Genre.name == genre_name)
        )
        genre = result.scalar_one_or_none()
        
        if not genre:
            raise GenreNotFoundError(f"Genre '{genre_name}' not found")
        
        # Get books by genre_id
        result = await self.db.execute(
            select(Book)
            .options(
                selectinload(Book.author),
                selectinload(Book.genre)
            )
            .where(Book.genre_id == genre.id)
        )
        return result.scalars().all()

