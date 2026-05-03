"""
School Attendance Exceptions

Module-specific exceptions for school attendance.
"""

from fastapi import HTTPException, status


class AttendanceException(HTTPException):
    """Base exception for attendance errors"""
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class SessionNotFoundError(AttendanceException):
    """Raised when attendance session is not found"""
    def __init__(self, session_id: int = None):
        detail = f"Attendance session not found: {session_id}" if session_id else "Attendance session not found"
        super().__init__(detail=detail)


class RecordNotFoundError(AttendanceException):
    """Raised when attendance record is not found"""
    def __init__(self, record_id: int = None):
        detail = f"Attendance record not found: {record_id}" if record_id else "Attendance record not found"
        super().__init__(detail=detail)


class DuplicateAttendanceError(AttendanceException):
    """Raised when trying to mark attendance that's already marked"""
    def __init__(self, student_id: int):
        super().__init__(detail=f"Attendance already marked for student {student_id}")


class InvalidStatusError(AttendanceException):
    """Raised when attendance status is invalid"""
    def __init__(self, status: str):
        super().__init__(detail=f"Invalid attendance status: {status}")


class SessionAlreadyExistsError(AttendanceException):
    """Raised when trying to create a session that already exists"""
    def __init__(self):
        super().__init__(detail="Attendance session already exists for this class, date, and subject")


class PermissionDeniedError(AttendanceException):
    """Raised when user doesn't have permission"""
    def __init__(self, action: str = "perform this action"):
        super().__init__(detail=f"Permission denied: Cannot {action}")


class ClassNotFoundError(AttendanceException):
    """Raised when class is not found"""
    def __init__(self, class_id: int):
        super().__init__(detail=f"Class not found: {class_id}")


class StudentNotFoundError(AttendanceException):
    """Raised when student is not found"""
    def __init__(self, student_id: int):
        super().__init__(detail=f"Student not found: {student_id}")


__all__ = [
    "AttendanceException",
    "SessionNotFoundError",
    "RecordNotFoundError",
    "DuplicateAttendanceError",
    "InvalidStatusError",
    "SessionAlreadyExistsError",
    "PermissionDeniedError",
    "ClassNotFoundError",
    "StudentNotFoundError",
]
