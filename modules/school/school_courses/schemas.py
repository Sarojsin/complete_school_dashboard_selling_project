from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseBase(BaseModel):
    course_code: str
    course_name: str
    description: Optional[str] = None
    credits: Optional[int] = None
    grade_level: Optional[str] = None
    semester: Optional[str] = None


class CourseCreate(CourseBase):
    teacher_id: Optional[int] = None


class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    teacher_id: Optional[int] = None
    grade_level: Optional[str] = None
    semester: Optional[str] = None


class CourseResponse(CourseBase):
    id: int
    teacher_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True