# School Library Utils
# ================

from datetime import date, timedelta
from typing import Optional


def validate_isbn(isbn: str) -> bool:
    """Validate ISBN format"""
    # Remove hyphens and spaces
    isbn = isbn.replace("-", "").replace(" ", "")
    
    # Check ISBN-10 or ISBN-13
    if len(isbn) == 10:
        return isbn[:9].isdigit() and (isbn[9].isdigit() or isbn[9] == 'X')
    elif len(isbn) == 13:
        return isbn.isdigit()
    
    return False


def calculate_due_date(issue_date: date, loan_period: int = 14) -> date:
    """Calculate due date for a book loan"""
    return issue_date + timedelta(days=loan_period)


def is_overdue(due_date: date) -> bool:
    """Check if a book is overdue"""
    return date.today() > due_date


def days_until_due(due_date: date) -> int:
    """Calculate days until due date"""
    delta = due_date - date.today()
    return delta.days


def days_overdue(due_date: date) -> int:
    """Calculate days overdue"""
    if not is_overdue(due_date):
        return 0
    delta = date.today() - due_date
    return delta.days


def calculate_late_fee(days_overdue: int, rate_per_day: float = 5.0) -> float:
    """Calculate late fee"""
    if days_overdue <= 0:
        return 0.0
    return days_overdue * rate_per_day


__all__ = [
    "validate_isbn",
    "calculate_due_date",
    "is_overdue",
    "days_until_due",
    "days_overdue",
    "calculate_late_fee"
]
