from pydantic import BaseModel
from typing import Optional
from .user import UserCreate

class AdminBase(BaseModel):
    position: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None

class AdminCreate(UserCreate, AdminBase):
    secret_key: str

class AdminResponse(AdminBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True
