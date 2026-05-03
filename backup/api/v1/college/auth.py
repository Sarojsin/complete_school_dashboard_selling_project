"""
College Authorization Dependencies
===================================
Dependency functions for ensuring only college users can access college endpoints.
"""

from fastapi import Depends, HTTPException, status
from backup.models.models import User, UserRole


# Define roles that are allowed to access college endpoints
# In a real implementation, you might add COLLEGE_STUDENT, COLLEGE_TEACHER to UserRole
COLLEGE_ALLOWED_ROLES = [
    UserRole.STUDENT,
    UserRole.TEACHER,
    UserRole.AUTHORITY,
    UserRole.ADMIN,
    UserRole.HOD,
    UserRole.EXAM_SECTION,
]


def create_college_auth_dependency(get_current_user_func):
    """
    Factory to create a college-authenticated dependency.
    
    Usage:
        get_current_college_user = create_college_auth_dependency(get_current_user)
        
        @router.get("/students")
        async def list_students(
            current_user: User = Depends(get_current_college_user),
            ...
        ):
            ...
    """
    async def college_auth(current_user: User = Depends(get_current_user_func)) -> User:
        # Check if user's role allows college access
        if current_user.role not in COLLEGE_ALLOWED_ROLES:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="College access denied. Your role does not have permission to access college endpoints."
            )
        return current_user
    
    return college_auth


# Pre-configured dependency for common use cases
# Usage: add `current_user: User = Depends(require_college_user)` to endpoint
from backup.dependencies.auth import get_current_user as _get_current_user
require_college_user = create_college_auth_dependency(_get_current_user)

__all__ = [
    "require_college_user",
    "create_college_auth_dependency",
    "COLLEGE_ALLOWED_ROLES",
]
