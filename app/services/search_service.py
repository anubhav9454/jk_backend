"""Search service for RAG-based book search."""
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Book, Review
from app.core.logging import get_logger

logger = get_logger(__name__)


class MinimalRAGPipeline:
    """Minimal RAG pipeline for book search."""
    
    def __init__(self):
        self.embeddings_store = {}
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Simple hash-based embeddings for minimal footprint."""
        # Simple character frequency based embedding
        chars = {}
        for char in text.lower():
            chars[char] = chars.get(char, 0) + 1
        
        # Create 100-dim vector from character frequencies
        embedding = [0.0] * 100
        for i, char in enumerate(sorted(chars.keys())[:100]):
            embedding[i] = chars[char] / len(text) if len(text) > 0 else 0.0
        
        return embedding
    
    async def index_book(self, db: AsyncSession, book_id: int):
        """Index a book's content for search."""
        try:
            # Load book with relationships
            result = await db.execute(
                select(Book)
                .options(
                    selectinload(Book.author),
                    selectinload(Book.genre)
                )
                .where(Book.id == book_id)
            )
            book = result.scalar_one_or_none()
            
            if not book:
                return
            
            # Load reviews
            reviews_result = await db.execute(
                select(Review).where(Review.book_id == book_id)
            )
            reviews = reviews_result.scalars().all()
            
            content_parts = [
                f"Title: {book.title}",
            ]
            
            if book.author:
                content_parts.append(f"Author: {book.author.name}")
            if book.genre:
                content_parts.append(f"Genre: {book.genre.name}")
            
            if book.summary:
                content_parts.append(f"Summary: {book.summary}")
            
            if reviews:
                review_texts = [r.review_text for r in reviews if r.review_text]
                if review_texts:
                    content_parts.append(f"Reviews: {' '.join(review_texts[:3])}")
            
            content = " ".join(content_parts)
            embedding = self.generate_embeddings(content)
            
            self.embeddings_store[book_id] = {
                "embedding": embedding,
                "metadata": {
                    "book_id": book_id,
                    "title": book.title,
                    "author": book.author.name if book.author else None,
                    "genre": book.genre.name if book.genre else None,
                },
                "content": content
            }
        except Exception as e:
            logger.error(f"Failed to index book {book_id}: {str(e)}")
    
    def search_similar_books(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Simple text matching search."""
        if not self.embeddings_store:
            return []
        
        query_lower = query.lower()
        results = []
        query_words = query_lower.split()
        
        for book_id, data in self.embeddings_store.items():
            content_lower = data["content"].lower()
            
            # Simple keyword matching score
            score = 0.0
            for word in query_words:
                if word in content_lower:
                    score += 1.0
            
            if score > 0:
                results.append({
                    "book_id": book_id,
                    "similarity_score": score / len(query_words) if query_words else 0.0,
                    "metadata": data["metadata"],
                    "content": data["content"]
                })
        
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:n_results]


# Global instance
rag_pipeline = MinimalRAGPipeline()


class SearchService:
    """Service for book search functionality."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize search service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.rag = rag_pipeline
    
    async def search_books(
        self,
        query: str,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Search books using RAG with database fallback.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            Search results dictionary
        """
        # Try RAG search first
        results = self.rag.search_similar_books(query, limit)
        
        # Fallback to database search if no RAG results
        if not results:
            result = await self.db.execute(
                select(Book)
                .options(
                    selectinload(Book.author),
                    selectinload(Book.genre)
                )
                .where(
                    Book.title.ilike(f"%{query}%")
                )
                .limit(limit)
            )
            books = result.scalars().all()
            
            results = [
                {
                    "book_id": book.id,
                    "similarity_score": 1.0,
                    "metadata": {
                        "book_id": book.id,
                        "title": book.title,
                        "author": book.author.name if book.author else None,
                        "genre": book.genre.name if book.genre else None,
                    },
                    "content": f"Title: {book.title}"
                }
                for book in books
            ]
        
        return {"query": query, "results": results}
    
    async def reindex_all_books(self) -> Dict[str, Any]:
        """
        Reindex all books for RAG.
        
        Returns:
            Reindexing statistics
        """
        result = await self.db.execute(select(Book))
        books = result.scalars().all()
        
        indexed_count = 0
        for book in books:
            try:
                await self.rag.index_book(self.db, book.id)
                indexed_count += 1
            except Exception as e:
                logger.warning(f"Failed to index book {book.id}: {str(e)}")
        
        return {
            "message": f"Reindexed {indexed_count} books successfully",
            "total_books": len(books),
            "indexed_count": indexed_count,
            "total_in_store": len(self.rag.embeddings_store)
        }

