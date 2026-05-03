"""
College Courses Module

Module for managing college courses, departments, programs, semesters, enrollments.
"""

from .router import router
from .models import CollegeCourse
# Import other models from backup for re-export
from backup.models.college import Department, Program, Semester, Enrollment

__all__ = [
    "router",
    "CollegeCourse", "Department", "Program", "Semester", "Enrollment"
]
