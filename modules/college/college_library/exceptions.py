"""
College Library Exceptions
"""

from fastapi import HTTPException, status


class LibraryException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class BookNotFoundError(LibraryException):
    def __init__(self, book_id: int = None):
        detail = f"Book not found: {book_id}" if book_id else "Book not found"
        super().__init__(detail=detail)


class BookNotAvailableError(LibraryException):
    def __init__(self):
        super().__init__(detail="Book not available for loan")


__all__ = ["LibraryException", "BookNotFoundError", "BookNotAvailableError"]
