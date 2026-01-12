"""Role model."""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.association import user_roles


class Role(Base):
    """Role model."""
    
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    can_read = Column(Boolean, default=True)
    can_write = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
        lazy="selectin"
    )

