"""Author model."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class Author(Base):
    """Author model."""
    
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    
    books = relationship("Book", back_populates="author")

