"""User service for business logic."""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.models import User, Role
from app.core.security import hash_password
from app.exceptions.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
)


class UserService:
    """Service for user management logic."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize user service.
        
        Args:
            db: Database session
        """
        self.repo = UserRepository(User, db)
        self.db = db
    
    async def create_user(self, data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            data: User creation data
            
        Returns:
            Created user
            
        Raises:
            UserAlreadyExistsError: If username already exists
        """
        # Check if user exists
        existing = await self.repo.get_by_username(data.username)
        if existing:
            raise UserAlreadyExistsError(f"Username '{data.username}' already exists")
        
        # Create user
        user = User(
            username=data.username,
            password_hash=hash_password(data.password)
        )
        self.db.add(user)
        await self.db.flush()
        
        # Assign roles
        await self.repo.assign_roles(user, data.role_names or [])
        
        return user
    
    async def get_user(self, user_id: int) -> User:
        """
        Get a user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User instance
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = await self.repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user
    
    async def get_all_users(self) -> List[User]:
        """
        Get all users with roles.
        
        Returns:
            List of users
        """
        return await self.repo.get_all_with_roles()
    
    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        """
        Update a user.
        
        Args:
            user_id: User ID
            data: Update data
            
        Returns:
            Updated user
            
        Raises:
            UserNotFoundError: If user doesn't exist
            UserAlreadyExistsError: If username already exists
        """
        user = await self.repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        # Check if username is being changed and already exists
        if data.username and data.username != user.username:
            existing = await self.repo.get_by_username(data.username)
            if existing:
                raise UserAlreadyExistsError(f"Username '{data.username}' already exists")
        
        # Update user fields
        if data.username:
            user.username = data.username
        if data.is_active is not None:
            user.is_active = data.is_active
        
        # Update roles if provided
        if data.role_names is not None:
            await self.repo.assign_roles(user, data.role_names)
        else:
            await self.db.commit()
            await self.db.refresh(user)
        
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = await self.repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        return await self.repo.delete(user_id)
    
    def to_response(self, user: User) -> UserResponse:
        """
        Convert user model to response schema.
        
        Args:
            user: User model instance
            
        Returns:
            UserResponse schema
        """
        return UserResponse(
            id=user.id,
            username=user.username,
            is_active=user.is_active,
            roles=[role.name for role in user.roles] if user.roles else []
        )

