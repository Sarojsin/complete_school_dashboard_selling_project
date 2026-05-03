"""
College Faculty Utilities
"""

from typing import Optional


def format_employee_id(prefix: str, number: int) -> str:
    """Format employee ID"""
    return f"{prefix}{number:04d}"


def get_designation_order(designation: str) -> int:
    """Get order for sorting designations"""
    order = {
        "Professor": 1,
        "Associate Professor": 2,
        "Assistant Professor": 3,
        "Lecturer": 4,
        "Teaching Assistant": 5,
    }
    return order.get(designation, 999)


__all__ = ["format_employee_id", "get_designation_order"]
