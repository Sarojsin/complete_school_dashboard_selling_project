"""
College HOD Module

Handles department head (HOD) operations and department oversight.
"""

from .router import router as hod_router
from .service import HodService
from .repository import HodRepository
from .models import Department, Faculty, CollegeCourse
from .schemas import (
    HODDashboardResponse,
    DepartmentDetailResponse,
    FacultySchema,
    CourseSchema,
)

__all__ = [
    "router",
    "HodService",
    "HodRepository",
    "Department",
    "Faculty",
    "CollegeCourse",
    "HODDashboardResponse",
    "DepartmentDetailResponse",
    "FacultySchema",
    "CourseSchema",
]
