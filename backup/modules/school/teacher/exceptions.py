# School Teacher Exceptions
# ======================

class TeacherError(Exception):
    """Base exception for teacher errors"""
    pass


class TeacherNotFoundError(TeacherError):
    """Raised when teacher is not found"""
    pass


class TeacherAlreadyExistsError(TeacherError):
    """Raised when teacher already exists"""
    pass


class InvalidTeacherStatusError(TeacherError):
    """Raised when teacher status is invalid"""
    pass
