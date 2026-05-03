"""
College Faculty Module
"""

from .api import router as api_router

from .models import Faculty, Teacher
from .schemas import FacultyBase, FacultyCreate, FacultyUpdate, FacultyResponse, FacultyListResponse
from .service import FacultyService
from .repository import FacultyRepository
from .constants import *
from .exceptions import *
from .utils import *

__all__ = [
    "api_router",
    "Faculty",
    "Teacher",
    "FacultyBase",
    "FacultyCreate",
    "FacultyUpdate",
    "FacultyResponse",
    "FacultyListResponse",
    "FacultyService",
    "FacultyRepository",
]
