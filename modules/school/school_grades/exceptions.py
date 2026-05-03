# School Grades Exceptions
# ====================

class GradeException(Exception):
    """Base exception for grades module"""
    pass


class GradeNotFoundException(GradeException):
    """Grade not found exception"""
    def __init__(self, grade_id: int):
        self.grade_id = grade_id
        super().__init__(f"Grade with ID {grade_id} not found")


class DuplicateGradeException(GradeException):
    """Duplicate grade exception"""
    def __init__(self, student_id: int, course_id: int):
        self.student_id = student_id
        self.course_id = course_id
        super().__init__(f"Grade already exists for student {student_id} in course {course_id}")


class InvalidGradeException(GradeException):
    """Invalid grade exception"""
    def __init__(self, grade: str):
        self.grade = grade
        super().__init__(f"Invalid grade: {grade}")


class GradeAccessDeniedException(GradeException):
    """Access denied exception"""
    def __init__(self, grade_id: int, user_id: int):
        self.grade_id = grade_id
        self.user_id = user_id
        super().__init__(f"User {user_id} cannot modify grade {grade_id}")


class GradeAlreadyPublishedException(GradeException):
    """Grade already published"""
    def __init__(self, grade_id: int):
        self.grade_id = grade_id
        super().__init__(f"Grade {grade_id} is already published and cannot be modified")


class AssessmentNotFoundException(GradeException):
    """Assessment not found exception"""
    def __init__(self, assessment_id: int):
        self.assessment_id = assessment_id
        super().__init__(f"Assessment with ID {assessment_id} not found")


__all__ = [
    "GradeException",
    "GradeNotFoundException",
    "DuplicateGradeException",
    "InvalidGradeException",
    "GradeAccessDeniedException",
    "GradeAlreadyPublishedException",
    "AssessmentNotFoundException"
]