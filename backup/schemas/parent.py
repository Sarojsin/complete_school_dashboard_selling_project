from pydantic import BaseModel
from typing import Optional
from .user import UserCreate, UserResponse

class ParentBase(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None

class ParentCreate(UserCreate, ParentBase):
    student_id: str  # Link to existing student

class ParentUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None

class ParentResponse(ParentBase):
    id: int
    user_id: int
    user: UserResponse
    
    class Config:
        from_attributes = True
