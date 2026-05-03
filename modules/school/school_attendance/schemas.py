"""
School Attendance Schemas

Pydantic schemas for school attendance API validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# Attendance Session Schemas
class AttendanceSessionBase(BaseModel):
    """Base schema for attendance session"""
    class_id: int
    date: date
    subject_id: Optional[int] = None


class AttendanceSessionCreate(AttendanceSessionBase):
    """Schema for creating an attendance session"""
    pass


class AttendanceSessionUpdate(BaseModel):
    """Schema for updating an attendance session"""
    subject_id: Optional[int] = None


class AttendanceSessionResponse(AttendanceSessionBase):
    """Schema for attendance session response"""
    id: int
    taken_by: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Attendance Record Schemas
class AttendanceRecordBase(BaseModel):
    """Base schema for attendance record"""
    student_id: int
    status: str = Field(..., pattern="^(present|absent|late|excused)$")
    remarks: Optional[str] = None


class AttendanceRecordCreate(AttendanceRecordBase):
    """Schema for creating an attendance record"""
    session_id: int


class AttendanceRecordUpdate(BaseModel):
    """Schema for updating an attendance record"""
    status: Optional[str] = Field(None, pattern="^(present|absent|late|excused)$")
    remarks: Optional[str] = None


class AttendanceRecordResponse(AttendanceRecordBase):
    """Schema for attendance record response"""
    id: int
    session_id: int
    marked_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Combined Schemas
class AttendanceMarkRequest(BaseModel):
    """Schema for marking attendance"""
    student_id: int
    status: str = Field(..., pattern="^(present|absent|late|excused)$")
    remarks: Optional[str] = None


class AttendanceSessionWithRecords(AttendanceSessionResponse):
    """Schema for attendance session with all records"""
    attendance_records: List[AttendanceRecordResponse] = []

    class Config:
        from_attributes = True


class StudentAttendanceSummary(BaseModel):
    """Schema for student attendance summary"""
    student_id: int
    student_name: Optional[str] = None
    present: int = 0
    absent: int = 0
    late: int = 0
    excused: int = 0
    total: int = 0
    percentage: float = 0.0


class ClassAttendanceSummary(BaseModel):
    """Schema for class attendance summary"""
    class_id: int
    date: date
    total_students: int = 0
    present: int = 0
    absent: int = 0
    late: int = 0
    excused: int = 0
    attendance_percentage: float = 0.0


__all__ = [
    "AttendanceSessionBase",
    "AttendanceSessionCreate",
    "AttendanceSessionUpdate",
    "AttendanceSessionResponse",
    "AttendanceSessionWithRecords",
    "AttendanceRecordBase",
    "AttendanceRecordCreate",
    "AttendanceRecordUpdate",
    "AttendanceRecordResponse",
    "AttendanceMarkRequest",
    "StudentAttendanceSummary",
    "ClassAttendanceSummary",
]
