"""
College HOD Models

HOD is a faculty role; no separate model needed.
This module re-exports backup models for type hints.
"""

# Import models used by HOD module
from backup.models.college import Department, Faculty, CollegeCourse

__all__ = ["Department", "Faculty", "CollegeCourse"]
