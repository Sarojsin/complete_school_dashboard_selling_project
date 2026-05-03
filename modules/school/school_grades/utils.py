# School Grades Utils
# ================

from typing import List, Dict, Optional
from .constants import GRADE_POINTS, GRADE_LETTERS


def calculate_letter_grade(score: float) -> str:
    """Calculate letter grade from score percentage"""
    if score >= 97:
        return "A+"
    elif score >= 93:
        return "A"
    elif score >= 90:
        return "A-"
    elif score >= 87:
        return "B+"
    elif score >= 83:
        return "B"
    elif score >= 80:
        return "B-"
    elif score >= 77:
        return "C+"
    elif score >= 73:
        return "C"
    elif score >= 70:
        return "C-"
    elif score >= 67:
        return "D+"
    elif score >= 63:
        return "D"
    elif score >= 60:
        return "D-"
    else:
        return "F"


def calculate_grade_points(letter_grade: str) -> float:
    """Get grade points for a letter grade"""
    return GRADE_POINTS.get(letter_grade, 0.0)


def calculate_gpa(grades: List[Dict]) -> float:
    """Calculate GPA from list of grades"""
    if not grades:
        return 0.0
    
    total_points = 0.0
    total_credits = 0
    
    for grade in grades:
        letter = grade.get("letter_grade", "F")
        credits = grade.get("credit_hours", 3)
        points = calculate_grade_points(letter)
        
        total_points += points * credits
        total_credits += credits
    
    if total_credits == 0:
        return 0.0
    
    return round(total_points / total_credits, 2)


def calculate_weighted_score(assessments: List[Dict]) -> float:
    """Calculate weighted score from assessments"""
    if not assessments:
        return 0.0
    
    total_weight = 0
    weighted_score = 0
    
    for assessment in assessments:
        score = assessment.get("score", 0)
        weight = assessment.get("weight", 0)
        
        weighted_score += score * weight
        total_weight += weight
    
    if total_weight == 0:
        return 0.0
    
    return round(weighted_score / total_weight, 2)


def get_grade_color(letter_grade: str) -> str:
    """Get color representation for grade"""
    if letter_grade.startswith("A"):
        return "green"
    elif letter_grade.startswith("B"):
        return "blue"
    elif letter_grade.startswith("C"):
        return "yellow"
    elif letter_grade.startswith("D"):
        return "orange"
    else:
        return "red"


def calculate_class_average(grades: List[Dict]) -> float:
    """Calculate class average"""
    if not grades:
        return 0.0
    
    total = sum(g.get("score", 0) for g in grades)
    return round(total / len(grades), 2)


def get_top_performers(grades: List[Dict], limit: int = 10) -> List[Dict]:
    """Get top performing students"""
    sorted_grades = sorted(
        grades, 
        key=lambda x: x.get("score", 0), 
        reverse=True
    )
    return sorted_grades[:limit]


__all__ = [
    "calculate_letter_grade",
    "calculate_grade_points",
    "calculate_gpa",
    "calculate_weighted_score",
    "get_grade_color",
    "calculate_class_average",
    "get_top_performers"
]