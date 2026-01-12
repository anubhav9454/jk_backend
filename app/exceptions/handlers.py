"""Exception handlers for FastAPI."""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.exceptions.exceptions import (
    BookNotFoundError,
    AuthorNotFoundError,
    GenreNotFoundError,
    UserNotFoundError,
    DocumentNotFoundError,
    AuthorAlreadyExistsError,
    GenreAlreadyExistsError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    InsufficientPermissionsError,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle custom domain exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    # Map custom exceptions to HTTP status codes
    exception_mapping = {
        BookNotFoundError: (status.HTTP_404_NOT_FOUND, "Book not found"),
        AuthorNotFoundError: (status.HTTP_404_NOT_FOUND, "Author not found"),
        GenreNotFoundError: (status.HTTP_404_NOT_FOUND, "Genre not found"),
        UserNotFoundError: (status.HTTP_404_NOT_FOUND, "User not found"),
        DocumentNotFoundError: (status.HTTP_404_NOT_FOUND, "Document not found"),
        AuthorAlreadyExistsError: (status.HTTP_400_BAD_REQUEST, "Author already exists"),
        GenreAlreadyExistsError: (status.HTTP_400_BAD_REQUEST, "Genre already exists"),
        UserAlreadyExistsError: (status.HTTP_400_BAD_REQUEST, "User already exists"),
        InvalidCredentialsError: (status.HTTP_401_UNAUTHORIZED, "Invalid credentials"),
        InsufficientPermissionsError: (status.HTTP_403_FORBIDDEN, "Insufficient permissions"),
    }
    
    if type(exc) in exception_mapping:
        status_code, default_message = exception_mapping[type(exc)]
        message = str(exc) if str(exc) else default_message
        
        logger.warning(
            f"Domain exception: {type(exc).__name__}",
            extra={"request_id": request_id, "message": message}
        )
        
        return JSONResponse(
            status_code=status_code,
            content={
                "error": message,
                "error_type": type(exc).__name__,
                "request_id": request_id
            }
        )
    
    # If not a custom exception, let it fall through to default handler
    raise exc


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.warning(
        f"HTTP exception: {exc.detail}",
        extra={"request_id": request_id, "status_code": exc.status_code}
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "request_id": request_id,
            "status_code": exc.status_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={"request_id": request_id},
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "request_id": request_id,
            "status_code": 500
        }
    )

