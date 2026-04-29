# School Teacher Exceptions

from fastapi import HTTPException, status


class TeacherException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class TeacherNotFoundError(TeacherException):
    def __init__(self):
        super().__init__(detail="Teacher not found")


__all__ = ["TeacherException", "TeacherNotFoundError"]
