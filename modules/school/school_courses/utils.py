# School Courses Utils
# =================

from typing import List, Dict, Any
from .constants import MIN_CREDIT_HOURS, MAX_CREDIT_HOURS


def validate_credit_hours(credits: int) -> bool:
    """Validate credit hours are within range"""
    return MIN_CREDIT_HOURS <= credits <= MAX_CREDIT_HOURS


def calculate_enrollment_percentage(enrolled: int, capacity: int) -> float:
    """Calculate enrollment percentage"""
    if capacity == 0:
        return 0.0
    return (enrolled / capacity) * 100


def is_course_full(enrolled: int, capacity: int) -> bool:
    """Check if course is at capacity"""
    return enrolled >= capacity


def format_course_code(department: str, course_number: str) -> str:
    """Format course code"""
    return f"{department.upper()}-{course_number}"


def calculate_gpa(grades: List[Dict[str, Any]]) -> float:
    """Calculate GPA from grades"""
    if not grades:
        return 0.0
    
    grade_points = {
        "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0, "F": 0.0
    }
    
    total_points = 0.0
    total_credits = 0
    
    for grade in grades:
        letter = grade.get("grade", "F")
        credits = grade.get("credits", 3)
        points = grade_points.get(letter, 0.0)
        
        total_points += points * credits
        total_credits += credits
    
    if total_credits == 0:
        return 0.0
    
    return round(total_points / total_credits, 2)


__all__ = [
    "validate_credit_hours",
    "calculate_enrollment_percentage",
    "is_course_full",
    "format_course_code",
    "calculate_gpa"
]