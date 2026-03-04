"""
app.api.schemas.admin.academic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydantic request schemas for the admin academic-management API
(courses, departments, timetable).
"""

from typing import Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Course schemas
# ---------------------------------------------------------------------------

class CourseCreateRequest(BaseModel):
    name: str
    code: str = Field(..., description="Unique course code, e.g. 'CS101'")
    description: Optional[str] = None
    teacher_id: Optional[int] = None
    grade_level: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)


class CourseUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    teacher_id: Optional[int] = None
    grade_level: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


# ---------------------------------------------------------------------------
# Department schemas
# ---------------------------------------------------------------------------

class DepartmentCreateRequest(BaseModel):
    name: str
    code: str = Field(..., description="Unique department code, e.g. 'SCI'")
    description: Optional[str] = None
    hod_teacher_id: Optional[int] = None


class DepartmentUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    hod_teacher_id: Optional[int] = None
    is_active: Optional[bool] = None


# ---------------------------------------------------------------------------
# Timetable schemas
# ---------------------------------------------------------------------------

class TimetableEntryRequest(BaseModel):
    course_id: int
    day_of_week: str = Field(
        ...,
        description="Day of week in lowercase English, e.g. 'monday'",
    )
    start_time: str = Field(..., description="HH:MM 24-hour format")
    end_time: str = Field(..., description="HH:MM 24-hour format")
    room: Optional[str] = None
