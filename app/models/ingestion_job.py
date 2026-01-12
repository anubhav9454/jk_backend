"""IngestionJob model."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


class IngestionJob(Base):
    """IngestionJob model."""
    
    __tablename__ = "ingestion_jobs"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), index=True)
    status = Column(String(50), default="pending", index=True)  # pending | running | completed | failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

