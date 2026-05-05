"""
College Enrollment Module

Handles student course enrollment management.
"""

from .router import router as enrollment_router
from .service import EnrollmentService
from .repository import EnrollmentRepository
from .models import EnrollmentModel
from .schemas import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    EnrollmentDetail,
)

__all__ = [
    "router",
    "EnrollmentService",
    "EnrollmentRepository",
    "EnrollmentModel",
    "EnrollmentCreate",
    "EnrollmentUpdate",
    "EnrollmentResponse",
    "EnrollmentDetail",
]
