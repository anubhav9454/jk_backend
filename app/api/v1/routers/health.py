"""Health check endpoints."""
from fastapi import APIRouter
import time

from app.core.config import settings
from app.db.health import db_health
from app.middleware.metrics import get_metrics_data

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with database and metrics."""
    db_healthy = await db_health.check_health()
    app_metrics = get_metrics_data()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "environment": settings.APP_ENV,
        "database": {
            "status": "healthy" if db_healthy else "unhealthy",
            "last_check": db_health.last_check
        },
        "metrics": app_metrics
    }


@router.get("/metrics")
async def get_metrics():
    """Application metrics endpoint."""
    return get_metrics_data()

