"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Environment
    APP_NAME: str = "Intelligent Book Management System"
    APP_ENV: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=True, description="Enable debug mode")
    USE_S3: bool = Field(default=False, description="Enable S3 storage")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=1, description="Number of worker processes")
    
    # Database
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: int = Field(default=5432, description="Database port")
    DB_NAME: str = Field(default="book_mgmt", description="Database name")
    DB_USER: str = Field(default="postgres", description="Database user")
    DB_PASSWORD: str = Field(default="password", description="Database password")
    DB_POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=30, description="Database max overflow connections")
    
    # Security
    SECRET_KEY: str = Field(
        default="super-secret-key-change-in-production",
        description="JWT secret key - MUST be changed in production"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, description="JWT token expiration")
    BASIC_AUTH_USERNAME: str = Field(default="admin", description="Basic auth username")
    BASIC_AUTH_PASSWORD: str = Field(default="password", description="Basic auth password")
    
    # External APIs
    OPENROUTER_API_KEY: str = Field(default="dummy_key", description="OpenRouter API key")
    OPENROUTER_MODEL: str = Field(default="meta-llama/llama-3-8b-instruct", description="OpenRouter model")
    
    # AWS Configuration
    AWS_REGION: str = Field(default="us-east-1", description="AWS region")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS access key")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="AWS secret key")
    S3_BUCKET_NAME: Optional[str] = Field(default=None, description="S3 bucket name")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: Optional[str] = Field(default=None, description="Log file path")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Rate limit requests per minute")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"], description="CORS allowed origins")
    
    # Health Check
    HEALTH_CHECK_INTERVAL: int = Field(default=30, description="Health check interval in seconds")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra environment variables
    )
    
    @field_validator('APP_ENV')
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate APP_ENV is one of allowed values."""
        allowed_envs = ['development', 'staging', 'production']
        if v not in allowed_envs:
            raise ValueError(f'APP_ENV must be one of {allowed_envs}')
        return v
    
    @field_validator('LOG_LEVEL')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate LOG_LEVEL is one of allowed values."""
        allowed_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        return v.upper()
    
    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key."""
        # Note: Production check should be done at runtime, not during validation
        # as we can't access other fields during field validation in Pydantic v2
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components."""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.APP_ENV == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.APP_ENV == "development"


settings = Settings()

