from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from .models import GroupPostType, GroupMemberRole


class GroupMemberRole(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    AUTHORITY = "authority"
    PARENT = "parent"


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class GroupOut(GroupBase):
    id: int
    code: str
    created_by: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class GroupMemberBase(BaseModel):
    user_id: int
    role: GroupMemberRole


class GroupMemberCreate(GroupMemberBase):
    pass


class GroupMemberOut(BaseModel):
    id: int
    group_id: int
    user_id: int
    role: GroupMemberRole
    is_active: bool
    joined_at: datetime

    class Config:
        from_attributes = True


class GroupWithMembers(GroupOut):
    member_count: int = 0


class GroupInviteRequest(BaseModel):
    user_ids: List[int]
    role: GroupMemberRole


# Group Post Schemas
class GroupPostBase(BaseModel):
    title: str
    content: Optional[str] = None
    post_type: GroupPostType = GroupPostType.DISCUSSION
    link_url: Optional[str] = None


class GroupPostCreate(GroupPostBase):
    group_id: int


class GroupPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    post_type: Optional[GroupPostType] = None
    link_url: Optional[str] = None


class GroupPostOut(GroupPostBase):
    id: int
    group_id: int
    author_id: int
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True