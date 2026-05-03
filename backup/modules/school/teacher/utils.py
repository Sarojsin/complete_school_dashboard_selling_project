# School Teacher Utilities
# ======================

from typing import Optional


def generate_employee_id(prefix: str = "T", sequence: int = 1) -> str:
    """Generate employee ID for teachers"""
    return f"{prefix}{sequence:05d}"


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if not phone:
        return True
    # Simple validation - should be digits, possibly with + or -
    return len(phone) >= 7 and len(phone) <= 20


__all__ = ["generate_employee_id", "validate_phone"]
