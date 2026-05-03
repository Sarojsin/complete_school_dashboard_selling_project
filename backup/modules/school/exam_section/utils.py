# School Exam Section Utils
# ======================

def calculate_grade(marks: float, total_marks: int = 100) -> str:
    """Calculate grade based on marks"""
    percentage = (marks / total_marks) * 100
    
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C+"
    elif percentage >= 40:
        return "C"
    elif percentage >= 30:
        return "D"
    else:
        return "F"


__all__ = ["calculate_grade"]
