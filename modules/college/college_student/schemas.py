"""
College Student Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date


class CollegeStudentBase(BaseModel):
    user_id: int
    roll_number: str
    program_id: Optional[int] = None
    semester_id: Optional[int] = None


class CollegeStudentCreate(CollegeStudentBase):
    pass


class CollegeStudentUpdate(BaseModel):
    program_id: Optional[int] = None
    semester_id: Optional[int] = None
    cgpa: Optional[float] = None


class CollegeStudentResponse(CollegeStudentBase):
    id: int
    cgpa: float
    total_credits_completed: int
    enrollment_date: Optional[date] = None
    full_name: str  # from user relationship

    class Config:
        from_attributes = True


class StudentCourseResponse(BaseModel):
    id: Optional[int] = None
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    credits: Optional[int] = None
    enrollment_id: Optional[int] = None
    
    class Config:
        from_attributes = False  # We're constructing dicts manually


class StudentGradeResponse(BaseModel):
    enrollment_id: Optional[int] = None
    course_id: Optional[int] = None
    grade: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = False


class StudentEnrollmentResponse(BaseModel):
    id: Optional[int] = None
    course_id: Optional[int] = None
    status: Optional[str] = None
    grade: Optional[str] = None
    enrolled_at: Optional[date] = None
    
    class Config:
        from_attributes = False


class HostelAllocationResponse(BaseModel):
    id: int
    hostel_id: int
    room_id: int
    allocation_date: Optional[date] = None
    status: str
    
    class Config:
        from_attributes = False


__all__ = ["CollegeStudentBase", "CollegeStudentCreate", "CollegeStudentUpdate", "CollegeStudentResponse"]
