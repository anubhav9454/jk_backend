"""Document repository."""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from datetime import datetime

from app.models import Document, IngestionJob
from app.repositories.base import BaseRepository
from app.schemas.document import DocumentCreate


class DocumentRepository(BaseRepository[Document, DocumentCreate, dict]):
    """Repository for Document model."""
    
    async def get_by_filename(self, filename: str) -> Optional[Document]:
        """
        Get document by filename.
        
        Args:
            filename: Document filename
            
        Returns:
            Document instance or None
        """
        result = await self.db.execute(
            select(Document).where(Document.filename == filename)
        )
        return result.scalar_one_or_none()
    
    async def get_today_processed_count(self) -> int:
        """
        Get count of documents processed today.
        
        Returns:
            Count of completed ingestion jobs today
        """
        today = datetime.now().date()
        result = await self.db.execute(
            select(func.count(IngestionJob.id))
            .where(
                and_(
                    func.date(IngestionJob.created_at) == today,
                    IngestionJob.status == "completed"
                )
            )
        )
        return result.scalar() or 0

