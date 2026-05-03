"""
College Student Exceptions
"""

from fastapi import HTTPException, status


class StudentException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class StudentNotFoundError(StudentException):
    def __init__(self, student_id: int = None):
        detail = f"Student not found: {student_id}" if student_id else "Student not found"
        super().__init__(detail=detail)


class DuplicateRollNumberError(StudentException):
    def __init__(self, roll_number: str):
        super().__init__(detail=f"Roll number already exists: {roll_number}")


__all__ = ["StudentException", "StudentNotFoundError", "DuplicateRollNumberError"]
