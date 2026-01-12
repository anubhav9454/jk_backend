"""API-specific dependencies."""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.book_service import BookService
from app.services.author_service import AuthorService
from app.services.genre_service import GenreService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.document_service import DocumentService
from app.services.search_service import SearchService
from app.services.recommendation_service import RecommendationService


def get_book_service(db: AsyncSession = Depends(get_db)) -> BookService:
    """Get book service instance."""
    return BookService(db)


def get_author_service(db: AsyncSession = Depends(get_db)) -> AuthorService:
    """Get author service instance."""
    return AuthorService(db)


def get_genre_service(db: AsyncSession = Depends(get_db)) -> GenreService:
    """Get genre service instance."""
    return GenreService(db)


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Get user service instance."""
    return UserService(db)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Get auth service instance."""
    return AuthService(db)


def get_document_service(db: AsyncSession = Depends(get_db)) -> DocumentService:
    """Get document service instance."""
    return DocumentService(db)


def get_search_service(db: AsyncSession = Depends(get_db)) -> SearchService:
    """Get search service instance."""
    return SearchService(db)


def get_recommendation_service(db: AsyncSession = Depends(get_db)) -> RecommendationService:
    """Get recommendation service instance."""
    return RecommendationService(db)

