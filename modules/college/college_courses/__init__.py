"""
College Courses Module

Module for managing college courses, departments, programs, semesters, enrollments.
"""

from .router import router
from .models import CollegeCourse, Department, Program, Semester, Enrollment

__all__ = [
    "router",
    "CollegeCourse", "Department", "Program", "Semester", "Enrollment"
]