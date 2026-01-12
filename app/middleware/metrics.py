"""Metrics middleware."""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting application metrics."""
    
    def __init__(self, app):
        super().__init__(app)
        self.request_count = 0
        self.error_count = 0
        self.response_times = []
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        self.request_count += 1
        
        try:
            response = await call_next(request)
            
            # Track response time
            duration = time.time() - start_time
            self.response_times.append(duration)
            
            # Keep only last 1000 response times
            if len(self.response_times) > 1000:
                self.response_times = self.response_times[-1000:]
            
            return response
            
        except Exception as e:
            self.error_count += 1
            raise e
    
    def get_metrics(self) -> dict:
        """Get current metrics."""
        avg_response_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times else 0
        )
        
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "recent_requests": len(self.response_times)
        }


# Global metrics instance (will be set by app)
_metrics_instance: MetricsMiddleware = None


def set_metrics_instance(instance: MetricsMiddleware):
    """Set the global metrics instance."""
    global _metrics_instance
    _metrics_instance = instance


def get_metrics_data() -> dict:
    """Get metrics from the middleware instance."""
    if _metrics_instance:
        return _metrics_instance.get_metrics()
    return {
        "request_count": 0,
        "error_count": 0,
        "error_rate": 0,
        "avg_response_time_ms": 0,
        "recent_requests": 0
    }

