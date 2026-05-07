"""
College Models Package

All SQLAlchemy models for the college module.
"""

# Import all models to register them with SQLAlchemy
from .college_departments.models import CollegeDepartment
from .college_faculty.models import CollegeFaculty
from .college_programs.models import CollegeProgram
from .college_semesters.models import CollegeSemester
from .college_courses.models import CollegeCourse
from .college_students.models import CollegeStudent
from .college_enrollments.models import CollegeEnrollment
from .college_exam_section.models import CollegeExamResult, CollegeExamNotice

__all__ = [
    "CollegeDepartment",
    "CollegeFaculty",
    "CollegeProgram",
    "CollegeSemester",
    "CollegeCourse",
    "CollegeStudent",
    "CollegeEnrollment",
    "CollegeExamResult",
    "CollegeExamNotice",
]