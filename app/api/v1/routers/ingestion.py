"""Ingestion endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from datetime import datetime, timedelta
import asyncio

from app.db.session import get_db
from app.models import IngestionJob, Document
from app.services.document_service import DocumentService
from app.api.deps import get_document_service

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.post("/trigger/{document_id}")
async def trigger_ingestion(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    doc_service: DocumentService = Depends(get_document_service)
):
    """Trigger ingestion for a document."""
    # Verify document exists
    await doc_service.get_document(document_id)
    
    # Create job
    job = IngestionJob(document_id=document_id, status="running")
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    # Simulate processing
    asyncio.create_task(process_ingestion_job(job.id))
    
    return {"message": "Ingestion started", "job_id": job.id}


async def process_ingestion_job(job_id: int):
    """Process ingestion job."""
    await asyncio.sleep(2)  # Simulate processing
    
    from app.db.session import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(IngestionJob).where(IngestionJob.id == job_id))
        job = result.scalar_one_or_none()
        if job:
            job.status = "completed"
            await db.commit()


@router.get("/status/{job_id}")
async def ingestion_status(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get ingestion job status."""
    result = await db.execute(select(IngestionJob).where(IngestionJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": job.status, "created_at": job.created_at}


@router.get("/jobs")
async def list_ingestion_jobs(db: AsyncSession = Depends(get_db)):
    """List all ingestion jobs."""
    result = await db.execute(
        select(IngestionJob, Document.filename)
        .join(Document, IngestionJob.document_id == Document.id)
        .order_by(IngestionJob.created_at.desc())
    )
    jobs = result.all()
    
    return [{
        "id": job.IngestionJob.id,
        "document_id": job.IngestionJob.document_id,
        "filename": job.filename,
        "status": job.IngestionJob.status,
        "created_at": job.IngestionJob.created_at
    } for job in jobs]


@router.get("/today-count")
async def today_processed_count(
    doc_service: DocumentService = Depends(get_document_service)
):
    """Get today's processed job count."""
    count = await doc_service.get_today_processed_count()
    return {"today_processed": count}


@router.post("/complete-stuck-jobs")
async def complete_stuck_jobs(db: AsyncSession = Depends(get_db)):
    """Complete stuck jobs."""
    cutoff_time = datetime.now() - timedelta(minutes=5)
    
    result = await db.execute(
        select(IngestionJob)
        .where(
            and_(
                IngestionJob.status == "running",
                IngestionJob.created_at < cutoff_time
            )
        )
    )
    stuck_jobs = result.scalars().all()
    
    for job in stuck_jobs:
        job.status = "completed"
    
    await db.commit()
    
    return {
        "message": f"Completed {len(stuck_jobs)} stuck jobs",
        "completed_jobs": len(stuck_jobs)
    }

