"""Author service for business logic."""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.author_repository import AuthorRepository
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.models import Author
from app.exceptions.exceptions import (
    AuthorNotFoundError,
    AuthorAlreadyExistsError,
)


class AuthorService:
    """Service for author business logic."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize author service.
        
        Args:
            db: Database session
        """
        self.repo = AuthorRepository(Author, db)
    
    async def create_author(self, data: AuthorCreate) -> Author:
        """
        Create a new author.
        
        Args:
            data: Author creation data
            
        Returns:
            Created author
            
        Raises:
            AuthorAlreadyExistsError: If author already exists
        """
        # Check if author already exists
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise AuthorAlreadyExistsError(f"Author '{data.name}' already exists")
        
        return await self.repo.create(data)
    
    async def get_author(self, author_id: int) -> Author:
        """
        Get an author by ID.
        
        Args:
            author_id: Author ID
            
        Returns:
            Author instance
            
        Raises:
            AuthorNotFoundError: If author doesn't exist
        """
        author = await self.repo.get(author_id)
        if not author:
            raise AuthorNotFoundError(f"Author with id {author_id} not found")
        return author
    
    async def get_all_authors(self) -> List[Author]:
        """
        Get all authors.
        
        Returns:
            List of authors
        """
        return await self.repo.get_all(order_by="name")
    
    async def update_author(self, author_id: int, data: AuthorUpdate) -> Author:
        """
        Update an author.
        
        Args:
            author_id: Author ID
            data: Update data
            
        Returns:
            Updated author
            
        Raises:
            AuthorNotFoundError: If author doesn't exist
            AuthorAlreadyExistsError: If name already exists
        """
        author = await self.repo.get(author_id)
        if not author:
            raise AuthorNotFoundError(f"Author with id {author_id} not found")
        
        # Check if new name already exists
        if data.name is not None and data.name != author.name:
            existing = await self.repo.get_by_name(data.name)
            if existing:
                raise AuthorAlreadyExistsError(f"Author '{data.name}' already exists")
        
        return await self.repo.update(author, data)
    
    async def delete_author(self, author_id: int) -> bool:
        """
        Delete an author.
        
        Args:
            author_id: Author ID
            
        Returns:
            True if deleted
            
        Raises:
            AuthorNotFoundError: If author doesn't exist
            ValueError: If author has books
        """
        author = await self.repo.get(author_id)
        if not author:
            raise AuthorNotFoundError(f"Author with id {author_id} not found")
        
        # Check if author has books
        if await self.repo.check_has_books(author_id):
            raise ValueError("Cannot delete author with existing books")
        
        return await self.repo.delete(author_id)

