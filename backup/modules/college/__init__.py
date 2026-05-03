"""
College Modules Package

Modular structure for college management system.
Each submodule contains: api.py, repository.py, service.py, schemas.py
"""

# Import routers from each module
# Each module exports a 'router' object from its api.py

try:
    from .faculty import router as faculty_router
except ImportError:
    faculty_router = None

try:
    from .student import router as student_router
except ImportError:
    student_router = None

try:
    from .program import router as program_router
except ImportError:
    program_router = None

try:
    from .placement import router as placement_router
except ImportError:
    placement_router = None

try:
    from .research import router as research_router
except ImportError:
    research_router = None

try:
    from .hostel import router as hostel_router
except ImportError:
    hostel_router = None

# Export available routers
__all__ = [
    "faculty_router",
    "student_router", 
    "program_router",
    "placement_router",
    "research_router",
    "hostel_router",
]
