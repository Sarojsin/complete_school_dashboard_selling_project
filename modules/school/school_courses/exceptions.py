# School Courses Exceptions
# ===================

class CourseException(Exception):
    """Base exception for courses module"""
    pass


class CourseNotFoundException(CourseException):
    """Course not found exception"""
    def __init__(self, course_id: int):
        self.course_id = course_id
        super().__init__(f"Course with ID {course_id} not found")


class DuplicateCourseException(CourseException):
    """Duplicate course exception"""
    def __init__(self, course_name: str):
        self.course_name = course_name
        super().__init__(f"Course '{course_name}' already exists")


class CourseFullException(CourseException):
    """Course is at capacity"""
    def __init__(self, course_id: int, capacity: int):
        self.course_id = course_id
        self.capacity = capacity
        super().__init__(f"Course {course_id} has reached capacity of {capacity}")


class EnrollmentNotFoundException(CourseException):
    """Enrollment not found exception"""
    def __init__(self, enrollment_id: int):
        self.enrollment_id = enrollment_id
        super().__init__(f"Enrollment {enrollment_id} not found")


class DuplicateEnrollmentException(CourseException):
    """Duplicate enrollment exception"""
    def __init__(self, student_id: int, course_id: int):
        self.student_id = student_id
        self.course_id = course_id
        super().__init__(f"Student {student_id} already enrolled in course {course_id}")


class InvalidCourseCapacityException(CourseException):
    """Invalid course capacity"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        super().__init__(f"Invalid capacity: {capacity}. Must be positive.")


__all__ = [
    "CourseException",
    "CourseNotFoundException",
    "DuplicateCourseException",
    "CourseFullException",
    "EnrollmentNotFoundException",
    "DuplicateEnrollmentException",
    "InvalidCourseCapacityException"
]