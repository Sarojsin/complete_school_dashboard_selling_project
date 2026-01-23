from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GroupPostBase(BaseModel):
    title: str
    content: Optional[str] = None
    post_type: str
    link_url: Optional[str] = None
    link_description: Optional[str] = None

class GroupPostCreate(GroupPostBase):
    group_id: int

class GroupPostUpdate(GroupPostBase):
    pass

class GroupPostOut(GroupPostBase):
    id: int
    group_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_published: bool

    class Config:
        from_attributes = True
