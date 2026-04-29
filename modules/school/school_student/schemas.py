from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime

class StudentBase(BaseModel):
    user_id: int
    student_id: str
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_id: Optional[int] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None
    roll_number: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_id: Optional[int] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None
    roll_number: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    enrollment_date: Optional[date] = None
    
    model_config = ConfigDict(from_attributes=True)
