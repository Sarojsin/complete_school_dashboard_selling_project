"""
College API Router
==================
Contains all college-specific API endpoints.
"""
from fastapi import APIRouter

router = APIRouter()

# Import college endpoints
# Note: Importing after router definition to avoid circular imports
from backup.api.v1.college import (
    students,
    faculty,
    departments,
    courses,
    enrollments,
    programs,
    semesters,
    placements,
    research,
    hostels,
    labs,
)

# Include routers with tags
router.include_router(students.router, tags=["College Students"])
router.include_router(faculty.router, tags=["Faculty"])
router.include_router(departments.router, tags=["Departments"])
router.include_router(courses.router, tags=["Courses"])
router.include_router(enrollments.router, tags=["Enrollments"])
router.include_router(programs.router, tags=["Programs"])
router.include_router(semesters.router, tags=["Semesters"])
router.include_router(placements.router, tags=["Placements"])
router.include_router(research.router, tags=["Research"])
router.include_router(hostels.router, tags=["Hostels"])
router.include_router(labs.router, tags=["Labs"])

__all__ = ["router"]
