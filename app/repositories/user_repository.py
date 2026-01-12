"""User repository."""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import User, Role
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repository for User model."""
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            User instance or None
        """
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_all_with_roles(self) -> List[User]:
        """
        Get all users with roles loaded.
        
        Returns:
            List of users with roles
        """
        result = await self.db.execute(
            select(User).options(selectinload(User.roles))
        )
        return result.scalars().all()
    
    async def assign_roles(self, user: User, role_names: List[str]) -> User:
        """
        Assign roles to user.
        
        Args:
            user: User instance
            role_names: List of role names
            
        Returns:
            Updated user instance
        """
        if role_names:
            result = await self.db.execute(
                select(Role).where(Role.name.in_(role_names))
            )
            roles = result.scalars().all()
            user.roles = roles
        else:
            # Assign default user role
            result = await self.db.execute(
                select(Role).where(Role.name == "user")
            )
            default_role = result.scalar_one_or_none()
            if default_role:
                user.roles = [default_role]
        
        await self.db.commit()
        await self.db.refresh(user)
        return user

