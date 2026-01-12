"""Application entrypoint - clean version."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Core imports
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.db.session import init_database, close_database
from app.middleware.request_tracking import RequestTrackingMiddleware
from app.middleware.metrics import MetricsMiddleware, set_metrics_instance
from app.exceptions.handlers import (
    custom_exception_handler,
    http_exception_handler,
    general_exception_handler,
)

# API routers
from app.api.v1.routers import (
    auth,
    books,
    authors,
    genres,
    users,
    documents,
    ingestion,
    search,
    health,
)

# Setup logging
setup_logging(log_level=settings.LOG_LEVEL, log_file=settings.LOG_FILE)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode")
    
    try:
        # Initialize database
        await init_database()
        logger.info("Database initialized successfully")
        
        logger.info("Application startup completed")
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    try:
        await close_database()
        logger.info("Application shutdown completed")
    except Exception as e:
        logger.error(f"Shutdown error: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade intelligent book management system with RAG capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Security middleware
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure with actual domains in production
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware (order matters - last added is first executed)
app.add_middleware(RequestTrackingMiddleware)
metrics_middleware = MetricsMiddleware(app)
set_metrics_instance(metrics_middleware)
app.add_middleware(MetricsMiddleware)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(books.router, prefix="/api/v1")
app.include_router(authors.router, prefix="/api/v1")
app.include_router(genres.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(ingestion.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(health.router)

# Legacy routes for backward compatibility (redirect to new paths)
@app.get("/books")
async def legacy_get_books():
    """Legacy endpoint - redirects to new API."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/v1/books")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS if settings.is_production else 1,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
        reload=settings.is_development
    )

