"""
College Registrar Module

Manages academic records, student enrollment oversight, and transcripts.
"""

from .router import router as registrar_router
from .service import RegistrarService
from .repository import RegistrarRepository
from .models import CollegeStudent, Enrollment, Program
from .schemas import (
    RegistrarDashboardResponse,
    StudentDetailSchema,
    EnrollmentDetailSchema,
    StudentAcademicRecord,
)

__all__ = [
    "router",
    "RegistrarService",
    "RegistrarRepository",
    "CollegeStudent",
    "Enrollment",
    "Program",
    "RegistrarDashboardResponse",
    "StudentDetailSchema",
    "EnrollmentDetailSchema",
    "StudentAcademicRecord",
]
