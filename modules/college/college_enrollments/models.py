"""
College Enrollment Models

Imports enrollment models from backup (single source of truth).
"""

from backup.models.college.enrollment import Enrollment as EnrollmentModel

__all__ = ["EnrollmentModel"]
