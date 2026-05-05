"""
College Dean Module

Provides high-level oversight and analytics for college dean.
"""

from .router import router as dean_router
from .service import DeanService
from .repository import DeanRepository
from .models import Department, Program, Faculty, CollegeStudent
from .schemas import (
    DeanDashboardResponse,
    DepartmentListSchema,
    ProgramListSchema,
    FacultySummarySchema,
    StudentSummarySchema,
)

__all__ = [
    "router",
    "DeanService",
    "DeanRepository",
    "Department",
    "Program",
    "Faculty",
    "CollegeStudent",
    "DeanDashboardResponse",
    "DepartmentListSchema",
    "ProgramListSchema",
    "FacultySummarySchema",
    "StudentSummarySchema",
]
