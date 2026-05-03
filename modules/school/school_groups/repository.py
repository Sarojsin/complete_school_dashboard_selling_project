from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, or_, and_
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime
import secrets
# Import Group, GroupMember, GroupPost from backup for now
from backup.models.group_models import Group, GroupMember, GroupPost


class GroupRepository:
    @staticmethod
    def generate_code() -> str:
        """Generate a unique 8-character code"""
        return secrets.token_hex(4).upper()

    @staticmethod
    async def create_group(db: AsyncSession, group_data: dict) -> Group:
        """Create a new group"""
        group_data['code'] = GroupRepository.generate_code()
        group = Group(**group_data)
        db.add(group)
        await db.commit()
        await db.refresh(group)
        return group

    @staticmethod
    async def get_group_by_id(db: AsyncSession, group_id: int) -> Optional[Group]:
        """Get group by ID"""
        result = await db.execute(select(Group).filter(Group.id == group_id))
        return result.scalars().first()

    @staticmethod
    async def get_group_by_code(db: AsyncSession, code: str) -> Optional[Group]:
        """Get group by unique code"""
        result = await db.execute(select(Group).filter(Group.code == code))
        return result.scalars().first()

    @staticmethod
    async def update_group(db: AsyncSession, group: Group, **kwargs) -> Group:
        """Update group information"""
        for key, value in kwargs.items():
            if value is not None and hasattr(group, key):
                setattr(group, key, value)
        await db.commit()
        await db.refresh(group)
        return group

    @staticmethod
    async def delete_group(db: AsyncSession, group: Group):
        """Delete a group"""
        await db.delete(group)
        await db.commit()

    @staticmethod
    async def get_user_groups(db: AsyncSession, user_id: int, role: str = None) -> List[Group]:
        """Get all groups a user belongs to"""
        query = select(Group).join(GroupMember, GroupMember.group_id == Group.id).filter(
            GroupMember.user_id == user_id,
            GroupMember.is_active == True,
            Group.is_active == True
        )
        if role:
            query = query.filter(GroupMember.role == role)
        result = await db.execute(query.order_by(Group.created_at.desc()))
        return result.scalars().all()

    @staticmethod
    async def is_member(db: AsyncSession, group_id: int, user_id: int) -> bool:
        """Check if user is a member of the group"""
        result = await db.execute(
            select(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id,
                GroupMember.is_active == True
            )
        )
        return result.scalars().first() is not None

    @staticmethod
    async def get_member(db: AsyncSession, group_id: int, user_id: int) -> Optional[GroupMember]:
        """Get membership record"""
        result = await db.execute(
            select(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            )
        )
        return result.scalars().first()

    @staticmethod
    async def add_member(db: AsyncSession, member_data: dict) -> GroupMember:
        """Add a user to a group"""
        member = GroupMember(**member_data)
        db.add(member)
        await db.commit()
        await db.refresh(member)
        return member

    @staticmethod
    async def remove_member(db: AsyncSession, group_id: int, user_id: int):
        """Remove a user from a group"""
        result = await db.execute(
            select(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            )
        )
        member = result.scalars().first()
        if member:
            await db.delete(member)
            await db.commit()

    @staticmethod
    async def get_group_members(db: AsyncSession, group_id: int, role: str = None) -> List[GroupMember]:
        """Get all members of a group"""
        query = select(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.is_active == True
        )
        if role:
            query = query.filter(GroupMember.role == role)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_group_with_members(db: AsyncSession, group_id: int) -> Optional[Group]:
        """Get group with all members"""
        result = await db.execute(
            select(Group).options(
                joinedload(Group.members)
            ).filter(Group.id == group_id)
        )
        return result.scalars().first()


class GroupPostRepository:
    @staticmethod
    async def create_post(db: AsyncSession, post_data: dict) -> GroupPost:
        """Create a new group post"""
        post = GroupPost(**post_data)
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def get_post_by_id(db: AsyncSession, post_id: int) -> Optional[GroupPost]:
        """Get post by ID"""
        result = await db.execute(select(GroupPost).filter(GroupPost.id == post_id))
        return result.scalars().first()

    @staticmethod
    async def update_post(db: AsyncSession, post: GroupPost, **kwargs) -> GroupPost:
        """Update a post"""
        for key, value in kwargs.items():
            if value is not None and hasattr(post, key):
                setattr(post, key, value)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def delete_post(db: AsyncSession, post: GroupPost):
        """Delete a post"""
        await db.delete(post)
        await db.commit()

    @staticmethod
    async def get_group_posts(db: AsyncSession, group_id: int, post_type: str = None, limit: int = 20, offset: int = 0) -> List[GroupPost]:
        """Get all posts in a group"""
        query = select(GroupPost).filter(
            GroupPost.group_id == group_id,
            GroupPost.is_published == True
        )
        if post_type:
            query = query.filter(GroupPost.post_type == post_type)
        result = await db.execute(
            query.order_by(GroupPost.created_at.desc()).limit(limit).offset(offset)
        )
        return result.scalars().all()

    @staticmethod
    async def get_user_posts(db: AsyncSession, user_id: int, group_id: int = None) -> List[GroupPost]:
        """Get all posts by a user"""
        query = select(GroupPost).filter(
            GroupPost.author_id == user_id,
            GroupPost.is_published == True
        )
        if group_id:
            query = query.filter(GroupPost.group_id == group_id)
        result = await db.execute(query.order_by(GroupPost.created_at.desc()))
        return result.scalars().all()

    @staticmethod
    async def count_posts(db: AsyncSession, group_id: int) -> int:
        """Count posts in a group"""
        result = await db.execute(
            select(func.count(GroupPost.id)).filter(
                GroupPost.group_id == group_id,
                GroupPost.is_published == True
            )
        )
        return result.scalar() or 0