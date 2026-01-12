"""Association tables for many-to-many relationships."""
from sqlalchemy import Column, Integer, ForeignKey, Table
from app.models.base import Base

# Association table for User-Role many-to-many relationship
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

