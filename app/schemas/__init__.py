"""Pydantic schemas for request/response validation."""
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.auth import SignupRequest, LoginResponse, TokenResponse
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.common import GenerateSummaryRequest, GenerateSummaryResponse

__all__ = [
    "BookCreate",
    "BookUpdate",
    "BookResponse",
    "AuthorCreate",
    "AuthorUpdate",
    "AuthorResponse",
    "GenreCreate",
    "GenreUpdate",
    "GenreResponse",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "SignupRequest",
    "LoginResponse",
    "TokenResponse",
    "DocumentCreate",
    "DocumentResponse",
    "GenerateSummaryRequest",
    "GenerateSummaryResponse",
]

