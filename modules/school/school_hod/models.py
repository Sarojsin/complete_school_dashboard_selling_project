"""
School HOD Models

HOD is a teacher role; no separate model required.
This module primarily re-exports the Teacher model for type safety and
provides a clear marker for HOD-specific operations.
"""

from modules.school.school_teacher.models import Teacher

# HOD is a teacher who is head of a department.
# The department attribute on Teacher determines HOD status.
# In the future, a separate HODProfile table could be added for
# additional HOD-specific fields (appointment date, tenure, etc.)

__all__ = ["Teacher"]
