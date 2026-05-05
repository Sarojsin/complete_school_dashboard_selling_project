"""
School HOD Module

Provides HOD (Head of Department) dashboard and department management.
"""

from .router import router as hod_router
from .service import HODService
from .repository import HODRepository
from .models import Teacher
from .schemas import (
    HODDashboardSchema,
    DepartmentListResponse,
    TeacherListResponse,
    CourseListResponse,
)

__all__ = [
    "router",
    "HODService",
    "HODRepository",
    "Teacher",
    "HODDashboardSchema",
    "DepartmentListResponse",
    "TeacherListResponse",
    "CourseListResponse",
]
