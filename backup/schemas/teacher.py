from pydantic import BaseModel
from typing import Optional
from datetime import date
from .user import UserCreate, UserResponse

class TeacherBase(BaseModel):
    employee_id: str
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None

class TeacherCreate(UserCreate, TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None

class TeacherResponse(TeacherBase):
    id: int
    user_id: int
    joining_date: date
    user: UserResponse
    
    class Config:
        from_attributes = True
