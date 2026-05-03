"""
School Authority Module

This module handles authority-related functionality for the school system.
"""

from .models import SchoolAuthority
from .schemas import (
    AuthorityBase,
    AuthorityCreate,
    AuthorityUpdate,
    AuthorityResponse,
    AuthorityListResponse,
)
from .service import AuthorityService
from .repository import AuthorityRepository

__all__ = [
    "SchoolAuthority",
    "AuthorityBase",
    "AuthorityCreate",
    "AuthorityUpdate",
    "AuthorityResponse",
    "AuthorityListResponse",
    "AuthorityService",
    "AuthorityRepository",
]
