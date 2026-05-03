"""
School API Router
=================
Contains all school-specific API endpoints.
"""
from fastapi import APIRouter

router = APIRouter()

# Import school endpoints
# Note: Importing after router definition to avoid circular imports
from backup.api.v1.school import (
    students,
    teachers,
    authorities,
    parents,
)

# Include routers with tags
router.include_router(students.router, tags=["School Students"])
router.include_router(teachers.router, tags=["School Teachers"])
router.include_router(authorities.router, tags=["School Authorities"])
router.include_router(parents.router, tags=["School Parents"])

__all__ = ["router"]
