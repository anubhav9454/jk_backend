"""Genre model."""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class Genre(Base):
    """Genre model."""
    
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    
    books = relationship("Book", back_populates="genre")

