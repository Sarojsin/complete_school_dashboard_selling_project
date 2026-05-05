"""
College Programs Module

Provides academic program information for college.
"""

from .router import router as programs_router
from .service import ProgramService
from .repository import ProgramRepository
from .models import ProgramModel
from .schemas import ProgramBase, ProgramResponse

__all__ = [
    "router",
    "ProgramService",
    "ProgramRepository",
    "ProgramModel",
    "ProgramBase",
    "ProgramResponse",
]
