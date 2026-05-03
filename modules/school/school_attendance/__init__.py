"""
School Attendance Module

Module for managing school attendance.
"""

from .api import router as api_router
from .models import AttendanceSession, AttendanceRecord
from .schemas import (
    AttendanceSessionBase,
    AttendanceSessionCreate,
    AttendanceSessionUpdate,
    AttendanceSessionResponse,
    AttendanceRecordBase,
    AttendanceRecordCreate,
    AttendanceRecordUpdate,
    AttendanceRecordResponse,
    AttendanceMarkRequest,
    StudentAttendanceSummary,
    ClassAttendanceSummary,
)
from .service import AttendanceService
from .repository import AttendanceRepository
from .constants import *
from .exceptions import *
from .utils import *

__all__ = [
    # Routers
    "api_router",
    # Models
    "AttendanceSession",
    "AttendanceRecord",
    # Schemas
    "AttendanceSessionBase",
    "AttendanceSessionCreate",
    "AttendanceSessionUpdate",
    "AttendanceSessionResponse",
    "AttendanceRecordBase",
    "AttendanceRecordCreate",
    "AttendanceRecordUpdate",
    "AttendanceRecordResponse",
    "AttendanceMarkRequest",
    "StudentAttendanceSummary",
    "ClassAttendanceSummary",
    # Service
    "AttendanceService",
    # Repository
    "AttendanceRepository",
]
