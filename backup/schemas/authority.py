from pydantic import BaseModel
from typing import Optional
from datetime import date
from .user import UserCreate, UserResponse

class AuthorityBase(BaseModel):
    position: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None

class AuthorityCreate(UserCreate, AuthorityBase):
    secret_key: str

class AuthorityUpdate(BaseModel):
    position: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None

class AuthorityResponse(AuthorityBase):
    id: int
    user_id: int
    user: UserResponse
    
    class Config:
        from_attributes = True
