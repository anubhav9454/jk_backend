"""Review model."""
from sqlalchemy import Column, Integer, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.models.base import Base


class Review(Base):
    """Review model."""
    
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), index=True)
    user_id = Column(Integer, index=True)
    review_text = Column(Text)
    rating = Column(Float)

    book = relationship("Book", back_populates="reviews")

