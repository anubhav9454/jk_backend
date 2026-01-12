"""Authentication service."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.repositories.user_repository import UserRepository
from app.models import User, Role
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.exceptions.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
)


class AuthService:
    """Service for authentication logic."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize auth service.
        
        Args:
            db: Database session
        """
        self.repo = UserRepository(User, db)
        self.db = db
    
    async def signup(self, data: SignupRequest) -> dict:
        """
        Register a new user.
        
        Args:
            data: Signup request data
            
        Returns:
            Success message
            
        Raises:
            UserAlreadyExistsError: If username already exists
        """
        # Check if user exists
        existing = await self.repo.get_by_username(data.username)
        if existing:
            raise UserAlreadyExistsError(f"Username '{data.username}' already exists")
        
        # Get or create default user role
        result = await self.db.execute(
            select(Role).where(Role.name == "user")
        )
        user_role = result.scalar_one_or_none()
        
        if not user_role:
            user_role = Role(
                name="user",
                can_read=True,
                can_write=False,
                can_delete=False,
                is_admin=False
            )
            self.db.add(user_role)
            await self.db.flush()
        
        # Create user
        user = User(
            username=data.username,
            password_hash=hash_password(data.password)
        )
        self.db.add(user)
        await self.db.flush()
        
        # Assign default user role
        user.roles = [user_role]
        await self.db.commit()
        
        return {"message": "User registered successfully"}
    
    async def login(self, data: LoginRequest) -> TokenResponse:
        """
        Authenticate user and return JWT token.
        
        Args:
            data: Login request data
            
        Returns:
            Token response with access token
            
        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        # Get user with roles
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.username == data.username)
        )
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsError("Invalid username or password")
        
        if not user.is_active:
            raise InvalidCredentialsError("User account is inactive")
        
        # Get user roles
        role_names = [role.name for role in user.roles] if user.roles else []
        
        # Create access token
        token = create_access_token({
            "sub": user.username,
            "roles": role_names
        })
        
        return TokenResponse(
            access_token=token,
            token_type="bearer"
        )
    
    async def create_admin(self, data: SignupRequest) -> dict:
        """
        Create an admin user.
        
        Args:
            data: Signup request data
            
        Returns:
            Success message
        """
        # Check if admin role exists, create if not
        result = await self.db.execute(
            select(Role).where(Role.name == "admin")
        )
        admin_role = result.scalar_one_or_none()
        
        if not admin_role:
            admin_role = Role(
                name="admin",
                can_read=True,
                can_write=True,
                can_delete=True,
                is_admin=True
            )
            self.db.add(admin_role)
            await self.db.flush()
        
        # Check if user exists
        existing = await self.repo.get_by_username(data.username)
        if existing:
            raise UserAlreadyExistsError(f"Username '{data.username}' already exists")
        
        # Create admin user
        user = User(
            username=data.username,
            password_hash=hash_password(data.password)
        )
        self.db.add(user)
        await self.db.flush()
        
        # Assign admin role
        user.roles = [admin_role]
        await self.db.commit()
        
        return {"message": "Admin user created successfully"}

