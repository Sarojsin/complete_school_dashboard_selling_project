"""
Authentication Dependencies - Backward Compatibility Layer

This file now imports from app.shared.auth for backward compatibility.
New code should import directly from app.shared.auth
"""

# Re-export from shared location for backward compatibility
from backup.shared.auth.dependencies import (
    get_current_user,
    get_current_student,
    get_current_teacher,
    get_current_authority,
    get_current_teacher_or_authority,
    get_current_parent,
    get_current_user_web,
    oauth2_scheme,
)

__all__ = [
    "get_current_user",
    "get_current_student",
    "get_current_teacher",
    "get_current_authority",
    "get_current_teacher_or_authority",
    "get_current_parent",
    "get_current_user_web",
    "oauth2_scheme",
]
