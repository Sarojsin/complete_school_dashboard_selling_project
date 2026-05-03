"""
School Attendance Utilities

Helper functions for school attendance module.
"""

from typing import List, Dict, Any
from datetime import date, datetime, timedelta
from .constants import (
    ATTENDANCE_STATUS_PRESENT,
    ATTENDANCE_STATUS_ABSENT,
    ATTENDANCE_STATUS_LATE,
    ATTENDANCE_STATUS_EXCUSED,
    MINIMUM_ATTENDANCE_PERCENTAGE,
)


def calculate_attendance_percentage(present: int, total: int) -> float:
    """Calculate attendance percentage"""
    if total == 0:
        return 0.0
    return round((present / total) * 100, 2)


def is_attendance_low(percentage: float) -> bool:
    """Check if attendance is below minimum threshold"""
    return percentage < MINIMUM_ATTENDANCE_PERCENTAGE


def is_attendance_warning(percentage: float) -> bool:
    """Check if attendance is in warning zone"""
    return MINIMUM_ATTENDANCE_PERCENTAGE <= percentage < 80.0


def get_status_color(status: str) -> str:
    """Get color for attendance status"""
    colors = {
        ATTENDANCE_STATUS_PRESENT: "green",
        ATTENDANCE_STATUS_ABSENT: "red",
        ATTENDANCE_STATUS_LATE: "orange",
        ATTENDANCE_STATUS_EXCUSED: "blue",
    }
    return colors.get(status, "gray")


def format_attendance_summary(summary: Dict[str, Any]) -> str:
    """Format attendance summary as readable string"""
    total = summary.get("total", 0)
    present = summary.get("present", 0)
    percentage = summary.get("percentage", 0.0)
    
    return f"{present}/{total} ({percentage}%)"


def get_date_range(period: str) -> tuple:
    """Get date range for common periods"""
    today = date.today()
    
    if period == "today":
        return today, today
    elif period == "week":
        return today - timedelta(days=7), today
    elif period == "month":
        return today - timedelta(days=30), today
    elif period == "term":
        return today - timedelta(days=90), today
    elif period == "year":
        return today - timedelta(days=365), today
    
    return today, today


def prepare_bulk_attendance_records(
    student_ids: List[int],
    default_status: str = ATTENDANCE_STATUS_ABSENT
) -> List[Dict[str, Any]]:
    """Prepare bulk attendance records with default values"""
    return [
        {
            "student_id": student_id,
            "status": default_status,
            "remarks": None
        }
        for student_id in student_ids
    ]


def validate_attendance_status(status: str) -> bool:
    """Validate if attendance status is valid"""
    valid_statuses = [
        ATTENDANCE_STATUS_PRESENT,
        ATTENDANCE_STATUS_ABSENT,
        ATTENDANCE_STATUS_LATE,
        ATTENDANCE_STATUS_EXCUSED,
    ]
    return status in valid_statuses


__all__ = [
    "calculate_attendance_percentage",
    "is_attendance_low",
    "is_attendance_warning",
    "get_status_color",
    "format_attendance_summary",
    "get_date_range",
    "prepare_bulk_attendance_records",
    "validate_attendance_status",
]
