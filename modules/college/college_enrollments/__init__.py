"""
College Enrollment Module

Handles student course enrollment management.
"""

from .router import router as enrollment_router
from .service import CollegeEnrollmentService
from .repository import CollegeEnrollmentRepository
from .models import CollegeEnrollment
from .schemas import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    EnrollmentDetail,
)

__all__ = [
    "router",
    "CollegeEnrollmentService",
    "CollegeEnrollmentRepository",
    "CollegeEnrollment",
    "EnrollmentCreate",
    "EnrollmentUpdate",
    "EnrollmentResponse",
    "EnrollmentDetail",
]
