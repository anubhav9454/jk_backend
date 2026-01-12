"""Custom exception classes for the application."""


class BookNotFoundError(Exception):
    """Raised when a book is not found."""
    pass


class AuthorNotFoundError(Exception):
    """Raised when an author is not found."""
    pass


class GenreNotFoundError(Exception):
    """Raised when a genre is not found."""
    pass


class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    pass


class DocumentNotFoundError(Exception):
    """Raised when a document is not found."""
    pass


class AuthorAlreadyExistsError(Exception):
    """Raised when trying to create an author that already exists."""
    pass


class GenreAlreadyExistsError(Exception):
    """Raised when trying to create a genre that already exists."""
    pass


class UserAlreadyExistsError(Exception):
    """Raised when trying to create a user that already exists."""
    pass


class InvalidCredentialsError(Exception):
    """Raised when authentication credentials are invalid."""
    pass


class InsufficientPermissionsError(Exception):
    """Raised when user lacks required permissions."""
    pass

