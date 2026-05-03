from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class DashboardStats(BaseModel):
    """Base dashboard stats"""
    total_students: int = 0
    total_teachers: int = 0
    total_parents: int = 0
    total_courses: int = 0
    total_users: int = 0
    active_users: int = 0
    total_notices: int = 0
    active_groups: int = 0

    class Config:
        from_attributes = True


class AuthorityDashboard(BaseModel):
    """Authority dashboard response"""
    stats: DashboardStats = Field(default_factory=DashboardStats)
    total_revenue: float = 0.0
    pending_fees: float = 0.0
    pending_fees_count: int = 0
    upcoming_exams: int = 0

    class Config:
        from_attributes = True


class TeacherDashboard(BaseModel):
    """Teacher dashboard response"""
    my_courses_count: int = 0
    my_assignments_count: int = 0
    pending_grading_count: int = 0
    upcoming_tests: int = 0
    recent_notices: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True


class StudentDashboard(BaseModel):
    """Student dashboard response"""
    my_courses_count: int = 0
    pending_assignments: int = 0
    upcoming_tests: int = 0
    recent_grades: List[Dict[str, Any]] = []
    attendance_summary: Dict[str, int] = {}

    class Config:
        from_attributes = True


class ParentDashboard(BaseModel):
    """Parent dashboard response"""
    children_count: int = 0
    children_info: List[Dict[str, Any]] = []
    pending_fees: float = 0.0

    class Config:
        from_attributes = True