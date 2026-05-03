"""
College Student Utilities
"""

from typing import Optional


def calculate_cgpa(grades: list) -> float:
    """Calculate CGPA from grades"""
    if not grades:
        return 0.0
    return round(sum(grades) / len(grades), 2)


def is_good_standing(cgpa: float, min_cgpa: float = 5.0) -> bool:
    """Check if student is in good standing"""
    return cgpa >= min_cgpa


__all__ = ["calculate_cgpa", "is_good_standing"]
