"""Document service for business logic."""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentResponse
from app.models import Document
from app.exceptions.exceptions import DocumentNotFoundError
from app.integrations.s3_service import s3_service
from app.core.config import settings


class DocumentService:
    """Service for document management logic."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize document service.
        
        Args:
            db: Database session
        """
        self.repo = DocumentRepository(Document, db)
        self.db = db
    
    async def upload_document(
        self,
        filename: str,
        file_content: bytes,
        uploaded_by: int = None
    ) -> Document:
        """
        Upload a document.
        
        Args:
            filename: Document filename
            file_content: File content bytes
            uploaded_by: User ID who uploaded
            
        Returns:
            Created document record
        """
        # Upload file (S3 in production, local in development)
        file_path = await s3_service.upload_file(file_content, filename)
        
        if not file_path:
            raise ValueError("Failed to upload file")
        
        # Create document record
        doc_data = DocumentCreate(
            filename=filename,
            file_size=len(file_content)
        )
        doc = await self.repo.create(doc_data)
        
        if uploaded_by:
            doc.uploaded_by = uploaded_by
            await self.db.commit()
            await self.db.refresh(doc)
        
        return doc
    
    async def get_document(self, document_id: int) -> Document:
        """
        Get a document by ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            Document instance
            
        Raises:
            DocumentNotFoundError: If document doesn't exist
        """
        doc = await self.repo.get(document_id)
        if not doc:
            raise DocumentNotFoundError(f"Document with id {document_id} not found")
        return doc
    
    async def get_all_documents(self) -> List[Document]:
        """
        Get all documents.
        
        Returns:
            List of documents
        """
        return await self.repo.get_all()
    
    async def delete_document(self, document_id: int) -> bool:
        """
        Delete a document.
        
        Args:
            document_id: Document ID
            
        Returns:
            True if deleted
            
        Raises:
            DocumentNotFoundError: If document doesn't exist
        """
        doc = await self.repo.get(document_id)
        if not doc:
            raise DocumentNotFoundError(f"Document with id {document_id} not found")
        
        return await self.repo.delete(document_id)
    
    async def get_today_processed_count(self) -> int:
        """
        Get count of documents processed today.
        
        Returns:
            Count of completed ingestion jobs today
        """
        return await self.repo.get_today_processed_count()
    
    def to_response(self, doc: Document) -> DocumentResponse:
        """
        Convert document model to response schema.
        
        Args:
            doc: Document model instance
            
        Returns:
            DocumentResponse schema
        """
        return DocumentResponse(
            id=doc.id,
            filename=doc.filename,
            uploaded_at=doc.uploaded_at,
            status=doc.status,
            file_size=doc.file_size,
            uploaded_by=doc.uploaded_by
        )

