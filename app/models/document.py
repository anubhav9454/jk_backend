"""Document model."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


class Document(Base):
    """Document model."""
    
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), index=True)
    file_size = Column(Integer, default=0)  # File size in bytes
    uploaded_by = Column(Integer, ForeignKey("users.id"), index=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="uploaded", index=True)  # uploaded | ingested | failed

