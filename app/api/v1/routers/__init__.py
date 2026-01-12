"""API v1 routers."""
from app.api.v1.routers import (
    auth,
    books,
    authors,
    genres,
    users,
    documents,
    ingestion,
    search,
    health,
)

__all__ = [
    "auth",
    "books",
    "authors",
    "genres",
    "users",
    "documents",
    "ingestion",
    "search",
    "health",
]

