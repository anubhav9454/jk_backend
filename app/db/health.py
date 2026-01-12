"""Database health check functionality."""
import time
from sqlalchemy import text
from app.db.session import engine
from app.core.logging import get_logger

logger = get_logger(__name__)


class DatabaseHealthCheck:
    """Database health monitoring."""
    
    def __init__(self, check_interval: int = 30):
        """
        Initialize health checker.
        
        Args:
            check_interval: Minimum seconds between health checks
        """
        self.last_check = 0
        self.is_healthy = True
        self.check_interval = check_interval
    
    async def check_health(self) -> bool:
        """
        Check database connectivity and performance.
        
        Returns:
            True if database is healthy, False otherwise
        """
        current_time = time.time()
        
        # Skip if recently checked
        if current_time - self.last_check < self.check_interval:
            return self.is_healthy
        
        try:
            async with engine.begin() as conn:
                start_time = time.time()
                await conn.execute(text("SELECT 1"))
                query_time = time.time() - start_time
                
                # Log slow queries
                if query_time > 1.0:
                    logger.warning(f"Slow database health check: {query_time:.2f}s")
                
                self.is_healthy = True
                self.last_check = current_time
                
                logger.debug(f"Database health check passed: {query_time:.3f}s")
                return True
                
        except Exception as e:
            self.is_healthy = False
            logger.error(f"Database health check failed: {str(e)}")
            return False


# Global health checker instance
db_health = DatabaseHealthCheck()

