"""
College Faculty Exceptions
"""

from fastapi import HTTPException, status


class FacultyException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class FacultyNotFoundError(FacultyException):
    def __init__(self, faculty_id: int = None):
        detail = f"Faculty not found: {faculty_id}" if faculty_id else "Faculty not found"
        super().__init__(detail=detail)


class DuplicateEmployeeIdError(FacultyException):
    def __init__(self, employee_id: str):
        super().__init__(detail=f"Employee ID already exists: {employee_id}")


__all__ = ["FacultyException", "FacultyNotFoundError", "DuplicateEmployeeIdError"]
