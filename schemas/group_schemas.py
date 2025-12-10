from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class GroupMemberRole(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(GroupBase):
    pass

class GroupInviteRequest(BaseModel):
    user_ids: List[int]
    role: str

class GroupOut(GroupBase):
    id: int
    code: str
    created_by: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
