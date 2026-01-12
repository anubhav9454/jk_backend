"""Shared dependencies for dependency injection."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.security import decode_access_token, ALGORITHM
from app.core.config import settings
from app.db.session import get_db
from app.models import User


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        payload = decode_access_token(credentials.credentials)
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Fetch user from database
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.username == username)
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        return user
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verify that the current user has admin role.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object (guaranteed to be admin)
        
    Raises:
        HTTPException: If user is not an admin
    """
    # Check if user has admin role
    user_roles = [role.name for role in current_user.roles] if current_user.roles else []
    
    if "admin" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


def get_current_username(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Get username from JWT token (lightweight, no DB query).
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        Username string
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = decode_access_token(credentials.credentials)
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return username
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

