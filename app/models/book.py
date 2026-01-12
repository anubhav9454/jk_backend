"""Book model."""
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base


class Book(Base):
    """Book model."""
    
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False, index=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False, index=True)
    year_published = Column(Integer, index=True)
    summary = Column(Text)

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    reviews = relationship("Review", back_populates="book")

