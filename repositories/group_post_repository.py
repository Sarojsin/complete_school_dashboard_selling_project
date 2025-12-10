from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc
from typing import List, Optional
from models.group_models import GroupPost
from models.models import User
import logging

logger = logging.getLogger(__name__)

class GroupPostRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_post(self, post_data: dict) -> GroupPost:
        """Create a new group post"""
        post = GroupPost(**post_data)
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post
    
    def get_post_by_id(self, post_id: int) -> Optional[GroupPost]:
        """Get post by ID with author details"""
        return self.session.query(GroupPost).options(
            joinedload(GroupPost.author),
            joinedload(GroupPost.group)
        ).filter(GroupPost.id == post_id).first()
    
    def update_post(self, post_id: int, update_data: dict) -> Optional[GroupPost]:
        """Update a post"""
        post = self.get_post_by_id(post_id)
        if post:
            for key, value in update_data.items():
                setattr(post, key, value)
            self.session.commit()
            self.session.refresh(post)
        return post
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        post = self.session.query(GroupPost).filter(GroupPost.id == post_id).first()
        if post:
            self.session.delete(post)  # Hard delete since model doesn't seem to have soft delete in structure, or stick to delete()
            self.session.commit()
            return True
        return False
    
    def get_group_posts(
        self, 
        group_id: int, 
        post_type: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[GroupPost]:
        """Get all posts in a group, optionally filtered by type"""
        query = self.session.query(GroupPost).options(
            joinedload(GroupPost.author),
            joinedload(GroupPost.group)
        ).filter(
            GroupPost.group_id == group_id,
            GroupPost.is_published == True
        )
        
        if post_type:
            query = query.filter(GroupPost.post_type == post_type)
        
        return query.order_by(desc(GroupPost.created_at)).limit(limit).offset(offset).all()
    
    def get_teacher_posts(self, teacher_id: int, group_id: int = None) -> List[GroupPost]:
        """Get all posts by a teacher"""
        query = self.session.query(GroupPost).options(
            joinedload(GroupPost.group)
        ).filter(
            GroupPost.author_id == teacher_id,
            GroupPost.is_published == True
        )
        
        if group_id:
            query = query.filter(GroupPost.group_id == group_id)
            
        return query.order_by(desc(GroupPost.created_at)).all()
    
    def count_group_posts(self, group_id: int) -> int:
        """Count total posts in a group"""
        return self.session.query(GroupPost).filter(
            GroupPost.group_id == group_id,
            GroupPost.is_published == True
        ).count()