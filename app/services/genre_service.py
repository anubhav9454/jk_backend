"""Genre service for business logic."""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.genre_repository import GenreRepository
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse
from app.models import Genre
from app.exceptions.exceptions import (
    GenreNotFoundError,
    GenreAlreadyExistsError,
)


class GenreService:
    """Service for genre business logic."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize genre service.
        
        Args:
            db: Database session
        """
        self.repo = GenreRepository(Genre, db)
    
    async def create_genre(self, data: GenreCreate) -> Genre:
        """
        Create a new genre.
        
        Args:
            data: Genre creation data
            
        Returns:
            Created genre
            
        Raises:
            GenreAlreadyExistsError: If genre already exists
        """
        # Check if genre already exists
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise GenreAlreadyExistsError(f"Genre '{data.name}' already exists")
        
        return await self.repo.create(data)
    
    async def get_genre(self, genre_id: int) -> Genre:
        """
        Get a genre by ID.
        
        Args:
            genre_id: Genre ID
            
        Returns:
            Genre instance
            
        Raises:
            GenreNotFoundError: If genre doesn't exist
        """
        genre = await self.repo.get(genre_id)
        if not genre:
            raise GenreNotFoundError(f"Genre with id {genre_id} not found")
        return genre
    
    async def get_all_genres(self) -> List[Genre]:
        """
        Get all genres.
        
        Returns:
            List of genres
        """
        return await self.repo.get_all(order_by="name")
    
    async def update_genre(self, genre_id: int, data: GenreUpdate) -> Genre:
        """
        Update a genre.
        
        Args:
            genre_id: Genre ID
            data: Update data
            
        Returns:
            Updated genre
            
        Raises:
            GenreNotFoundError: If genre doesn't exist
            GenreAlreadyExistsError: If name already exists
        """
        genre = await self.repo.get(genre_id)
        if not genre:
            raise GenreNotFoundError(f"Genre with id {genre_id} not found")
        
        # Check if new name already exists
        if data.name is not None and data.name != genre.name:
            existing = await self.repo.get_by_name(data.name)
            if existing:
                raise GenreAlreadyExistsError(f"Genre '{data.name}' already exists")
        
        return await self.repo.update(genre, data)
    
    async def delete_genre(self, genre_id: int) -> bool:
        """
        Delete a genre.
        
        Args:
            genre_id: Genre ID
            
        Returns:
            True if deleted
            
        Raises:
            GenreNotFoundError: If genre doesn't exist
            ValueError: If genre has books
        """
        genre = await self.repo.get(genre_id)
        if not genre:
            raise GenreNotFoundError(f"Genre with id {genre_id} not found")
        
        # Check if genre has books
        if await self.repo.check_has_books(genre_id):
            raise ValueError("Cannot delete genre with existing books")
        
        return await self.repo.delete(genre_id)

