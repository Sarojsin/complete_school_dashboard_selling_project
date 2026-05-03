"""
College Faculty Models

SQLAlchemy models for college faculty management.
"""

# Import from existing app models
from backup.models.college.faculty import Faculty
from modules.school.school_teacher.models import Teacher

__all__ = ["Faculty", "Teacher"]
