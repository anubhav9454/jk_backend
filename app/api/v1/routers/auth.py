"""Authentication endpoints."""
from fastapi import APIRouter, Depends

from app.services.auth_service import AuthService
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.api.deps import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(
    data: SignupRequest,
    service: AuthService = Depends(get_auth_service)
):
    """Register a new user."""
    return await service.signup(data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    """User login."""
    return await service.login(data)


@router.post("/create-admin")
async def create_admin(
    data: SignupRequest,
    service: AuthService = Depends(get_auth_service)
):
    """Create an admin user."""
    return await service.create_admin(data)


@router.post("/logout")
async def logout():
    """User logout (handled client-side with JWT invalidation)."""
    return {"message": "Logout handled on client side (JWT invalidation)"}

