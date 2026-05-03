"""
College Library Utilities
"""

from datetime import date, timedelta


def calculate_fine(due_date: date, return_date: date, fine_per_day: float = 10.0) -> float:
    """Calculate fine for late return"""
    if return_date <= due_date:
        return 0.0
    days_late = (return_date - due_date).days
    return days_late * fine_per_day


def is_overdue(due_date: date) -> bool:
    """Check if book is overdue"""
    return date.today() > due_date


__all__ = ["calculate_fine", "is_overdue"]
