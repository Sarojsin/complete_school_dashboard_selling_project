"""
School Authority Exceptions
"""

from fastapi import HTTPException, status


class AuthorityException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class AuthorityNotFoundError(AuthorityException):
    def __init__(self):
        super().__init__(detail="Authority not found")


__all__ = ["AuthorityException", "AuthorityNotFoundError"]
