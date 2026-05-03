"""
School Models Package

Contains school-specific models (Student, Teacher, Parent, Authority, Class, Fee).
"""

from .student import SchoolStudent
from .teacher import SchoolTeacher
from .parent import SchoolParent
from .authority import SchoolAuthority
from .class_model import SchoolClass
from .fee import SchoolFee

__all__ = [
    "SchoolStudent",
    "SchoolTeacher", 
    "SchoolParent",
    "SchoolAuthority",
    "SchoolClass",
    "SchoolFee",
]
