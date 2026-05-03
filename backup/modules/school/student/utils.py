# School Student Utilities
# ====================

from typing import Optional


def generate_student_id(prefix: str = "S", year: int = None, sequence: int = 1) -> str:
    """Generate student ID"""
    year_str = str(year)[-2:] if year else "00"
    return f"{prefix}{year_str}{sequence:04d}"


__all__ = ["generate_student_id"]
