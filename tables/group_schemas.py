from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class GroupPostType(str, Enum):
    NOTICE = "notice"
    NOTE = "note"
    LINK = "link"

class GroupMemberRole(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"

class GroupBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None

class GroupInDB(GroupBase):
    id: int
    code: str
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

class GroupWithMembers(GroupInDB):
    member_count: int
    teacher_count: int
    student_count: int

class GroupMemberBase(BaseModel):
    user_id: int
    role: GroupMemberRole

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMemberInDB(GroupMemberBase):
    id: int
    group_id: int
    joined_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class GroupMemberWithUser(GroupMemberInDB):
    user_name: str
    user_email: str

class GroupInviteRequest(BaseModel):
    user_ids: List[int]
    role: GroupMemberRole