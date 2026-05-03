from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, desc, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from backup.models.group_models import GroupPost
from backup.models.models import User
import logging

logger = logging.getLogger(__name__)

class GroupPostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_post(self, post_data: dict) -> GroupPost:
        """Create a new group post"""
        post = GroupPost(**post_data)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post
    
    async def get_post_by_id(self, post_id: int) -> Optional[GroupPost]:
        """Get post by ID with author details"""
        result = await self.session.execute(
            select(GroupPost).options(
                joinedload(GroupPost.author),
                joinedload(GroupPost.group)
            ).filter(GroupPost.id == post_id)
        )
        return result.scalars().first()
    
    async def update_post(self, post_id: int, update_data: dict) -> Optional[GroupPost]:
        """Update a post"""
        post = await self.get_post_by_id(post_id)
        if post:
            for key, value in update_data.items():
                setattr(post, key, value)
            await self.session.commit()
            await self.session.refresh(post)
        return post
    
    async def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        result = await self.session.execute(select(GroupPost).filter(GroupPost.id == post_id))
        post = result.scalars().first()
        if post:
            await self.session.delete(post)
            await self.session.commit()
            return True
        return False
    
    async def get_group_posts(
        self, 
        group_id: int, 
        post_type: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[GroupPost]:
        """Get all posts in a group, optionally filtered by type"""
        query = select(GroupPost).options(
            joinedload(GroupPost.author),
            joinedload(GroupPost.group)
        ).filter(
            GroupPost.group_id == group_id,
            GroupPost.is_published == True
        )
        
        if post_type:
            query = query.filter(GroupPost.post_type == post_type)
        
        result = await self.session.execute(
            query.order_by(desc(GroupPost.created_at)).limit(limit).offset(offset)
        )
        return result.scalars().unique().all()
    
    async def get_teacher_posts(self, teacher_id: int, group_id: int = None) -> List[GroupPost]:
        """Get all posts by a teacher"""
        query = select(GroupPost).options(
            joinedload(GroupPost.group)
        ).filter(
            GroupPost.author_id == teacher_id,
            GroupPost.is_published == True
        )
        
        if group_id:
            query = query.filter(GroupPost.group_id == group_id)
            
        result = await self.session.execute(query.order_by(desc(GroupPost.created_at)))
        return result.scalars().unique().all()
    
    async def count_group_posts(self, group_id: int) -> int:
        """Count total posts in a group"""
        result = await self.session.execute(
            select(func.count(GroupPost.id)).filter(
                GroupPost.group_id == group_id,
                GroupPost.is_published == True
            )
        )
        return result.scalar() or 0