"""User management endpoints (admin only)."""
from fastapi import APIRouter, Depends, status
from typing import List

from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.deps import get_user_service
from app.core.dependencies import get_current_admin
from app.models import Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db

router = APIRouter(prefix="/admin/users", tags=["Admin - User Management"])


@router.post("/", response_model=dict)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
    _: None = Depends(get_current_admin)
):
    """Create a new user (admin only)."""
    user = await service.create_user(user_data)
    return {"message": "User created successfully", "user_id": user.id}


@router.get("/", response_model=List[UserResponse], dependencies=[Depends(get_current_admin)])
async def list_users(
    service: UserService = Depends(get_user_service)
):
    """List all users (admin only)."""
    users = await service.get_all_users()
    return [service.to_response(user) for user in users]


@router.put("/{user_id}", response_model=dict, dependencies=[Depends(get_current_admin)])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    """Update a user (admin only)."""
    await service.update_user(user_id, user_data)
    return {"message": "User updated successfully"}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin)])
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Delete a user (admin only)."""
    await service.delete_user(user_id)
    return None


@router.get("/roles", response_model=List[dict], dependencies=[Depends(get_current_admin)])
async def list_roles(db: AsyncSession = Depends(get_db)):
    """List all roles (admin only)."""
    result = await db.execute(select(Role))
    roles = result.scalars().all()
    return [{
        "id": role.id,
        "name": role.name,
        "can_read": role.can_read,
        "can_write": role.can_write,
        "can_delete": role.can_delete,
        "is_admin": role.is_admin
    } for role in roles]

