"""
School Modules Package

Contains school-specific role modules.
"""

from .authority import router as authority_router
from .teacher import router as teacher_router
from .student import router as student_router
from .parent import router as parent_router

__all__ = [
    "authority_router",
    "teacher_router",
    "student_router", 
    "parent_router",
]
