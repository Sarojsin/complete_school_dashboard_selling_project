from pydantic import BaseModel
from typing import Optional
from datetime import date

class AttendanceBase(BaseModel):
    date: date
    status: str  # present, absent, late
    remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    student_id: int
    course_id: int

class AttendanceResponse(AttendanceBase):
    id: int
    student_id: int
    course_id: int
    
    class Config:
        from_attributes = True
