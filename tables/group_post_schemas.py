from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
from .group_schemas import GroupPostType

class GroupPostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    post_type: GroupPostType
    link_url: Optional[HttpUrl] = None
    link_description: Optional[str] = None

class GroupPostCreate(GroupPostBase):
    group_id: int

class GroupPostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    link_url: Optional[HttpUrl] = None
    link_description: Optional[str] = None
    is_published: Optional[bool] = None

class GroupPostInDB(GroupPostBase):
    id: int
    group_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_published: bool
    
    class Config:
        from_attributes = True

class GroupPostWithAuthor(GroupPostInDB):
    author_name: str
    author_email: str
    group_name: str