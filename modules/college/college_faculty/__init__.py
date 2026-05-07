"""
College Faculty Module
"""

from .api import router as api_router

from .models import CollegeFaculty, Teacher
from .schemas import FacultyBase, FacultyCreate, FacultyUpdate, FacultyResponse, FacultyListResponse
from .service import CollegeFacultyService
from .repository import CollegeFacultyRepository
from .constants import *
from .exceptions import *
from .utils import *

__all__ = [
    "api_router",
    "CollegeFaculty",
    "Teacher",
    "FacultyBase",
    "FacultyCreate",
    "FacultyUpdate",
    "FacultyResponse",
    "FacultyListResponse",
    "CollegeFacultyService",
    "CollegeFacultyRepository",
]
