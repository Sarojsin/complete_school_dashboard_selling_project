# College Lab Utils
# ==============

from typing import Dict, Any


def format_time_range(start_time: str, end_time: str) -> str:
    """Format time range for display"""
    return f"{start_time} - {end_time}"


def calculate_lab_utilization(schedules: list, capacity: int) -> float:
    """Calculate lab utilization percentage"""
    if not schedules or capacity == 0:
        return 0.0
    return (len(schedules) / capacity) * 100


__all__ = [
    "format_time_range",
    "calculate_lab_utilization",
]
