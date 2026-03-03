"""
Core Custom Domain Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These exceptions are raised by the Service layer instead of FastAPI HTTPExceptions.
This enforces strict decoupling between the web/HTTP layer (FastAPI) and the
business logic layer (Services).

The API/Web routing layer defines exception handlers to map these pure Python
exceptions into appropriate HTTP responses.
"""

class BaseAppException(Exception):
    """Base exception for all application-level errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundError(BaseAppException):
    """Raised when a requested resource is not found (maps to HTTP 404)."""
    pass


class ValidationError(BaseAppException):
    """Raised when input data violates business rules (maps to HTTP 400)."""
    pass


class ForbiddenError(BaseAppException):
    """Raised when a user attempts to access a forbidden resource (maps to HTTP 403)."""
    pass


class UnauthorizedError(BaseAppException):
    """Raised when authentication fails or is missing (maps to HTTP 401)."""
    pass


class ConflictError(BaseAppException):
    """Raised when an action conflicts with existing state, e.g., duplicates (maps to HTTP 409)."""
    pass
