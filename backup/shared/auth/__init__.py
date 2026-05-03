"""
Shared Authentication Module

Contains authentication dependencies and JWT utilities.
"""

from .dependencies import (
    get_current_user,
    get_current_student,
    get_current_teacher,
    get_current_authority,
    get_current_teacher_or_authority,
    get_current_parent,
    get_current_user_web,
    oauth2_scheme,
)
from .jwt import create_access_token, verify_token

__all__ = [
    "get_current_user",
    "get_current_student",
    "get_current_teacher",
    "get_current_authority",
    "get_current_teacher_or_authority",
    "get_current_parent",
    "get_current_user_web",
    "oauth2_scheme",
    "create_access_token",
    "verify_token",
]
