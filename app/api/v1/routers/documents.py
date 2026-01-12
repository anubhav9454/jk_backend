"""Document endpoints."""
from fastapi import APIRouter, UploadFile, File, Depends, status
from fastapi.responses import StreamingResponse, RedirectResponse
from typing import List
import io

from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse
from app.api.deps import get_document_service
from app.core.dependencies import get_current_username
from app.core.config import settings
from app.integrations.s3_service import s3_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
    username: str = Depends(get_current_username)
):
    """Upload a document."""
    file_content = await file.read()
    
    # Get user ID from username (simplified - in real app, get from token)
    doc = await service.upload_document(
        filename=file.filename,
        file_content=file_content
    )
    
    response = {
        "message": "Document uploaded successfully",
        "document_id": doc.id,
        "filename": file.filename,
        "file_size": len(file_content)
    }
    
    if settings.USE_S3:
        response["s3_key"] = file.filename
        response["download_url"] = s3_service.get_file_url(file.filename)
    
    return response


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    service: DocumentService = Depends(get_document_service)
):
    """List all documents."""
    docs = await service.get_all_documents()
    return [service.to_response(doc) for doc in docs]


@router.get("/{document_id}/download")
async def download_document(
    document_id: int,
    service: DocumentService = Depends(get_document_service)
):
    """Download a document."""
    doc = await service.get_document(document_id)
    
    if not settings.USE_S3:
        # Development: return placeholder
        content = f"Document: {doc.filename}\nUploaded: {doc.uploaded_at}\nSize: {doc.file_size} bytes"
        return StreamingResponse(
            io.BytesIO(content.encode()),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={doc.filename}"}
        )
    
    # Production: redirect to S3
    download_url = s3_service.get_file_url(doc.filename)
    if download_url:
        return RedirectResponse(url=download_url)
    raise Exception("File not found in storage")


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    service: DocumentService = Depends(get_document_service),
    _: str = Depends(get_current_username)
):
    """Delete a document."""
    await service.delete_document(document_id)
    return None

