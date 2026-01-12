"""Search endpoints."""
from fastapi import APIRouter, Depends

from app.services.search_service import SearchService
from app.api.deps import get_search_service

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("")
@router.get("")
async def search_books(
    query: str,
    limit: int = 5,
    service: SearchService = Depends(get_search_service)
):
    """Semantic book search with fallback."""
    return await service.search_books(query, limit)


@router.post("/reindex-all")
async def reindex_all_books(
    service: SearchService = Depends(get_search_service)
):
    """Reindex all books for RAG."""
    return await service.reindex_all_books()

