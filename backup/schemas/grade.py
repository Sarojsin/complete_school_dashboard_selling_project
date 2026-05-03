from pydantic import BaseModel
from typing import Optional
from datetime import date

class GradeBase(BaseModel):
    grade_type: Optional[str] = None
    score: float
    max_score: float
    grade: Optional[str] = None
    remarks: Optional[str] = None

class GradeCreate(GradeBase):
    student_id: int
    course_id: int

class GradeUpdate(BaseModel):
    score: Optional[float] = None
    max_score: Optional[float] = None
    grade: Optional[str] = None
    remarks: Optional[str] = None

class GradeResponse(GradeBase):
    id: int
    student_id: int
    course_id: int
    date: date
    
    class Config:
        from_attributes = True
