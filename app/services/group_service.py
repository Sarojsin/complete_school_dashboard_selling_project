from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from app.models.group_models import Group, GroupMember, GroupPost
from app.repositories.group_repository import GroupRepository

class GroupService:
    def __init__(self, group_repo: GroupRepository):
        self.group_repo = group_repo

    async def get_groups_list(self, user_id: int):
        result = await self.group_repo.session.execute(
            select(Group).options(
                selectinload(Group.members),
                joinedload(Group.creator)
            ).order_by(Group.created_at.desc())
        )
        all_groups = result.scalars().unique().all()
        
        user_groups = []
        available_groups = []
        
        for group in all_groups:
            is_member = any(m.user_id == user_id for m in group.members)
            group_data = {
                "id": group.id,
                "name": group.name,
                "description": group.description,
                "is_active": group.is_active,
                "member_count": len(group.members),
                "creator_name": group.creator.full_name if group.creator else "Unknown",
                "created_at": group.created_at
            }
            if is_member:
                user_groups.append(group_data)
            elif group.is_active:
                available_groups.append(group_data)
                
        return {
            "user_groups": user_groups,
            "available_groups": available_groups
        }

    async def get_user_groups(self, user_id: int, role: str = None):
        """Get all groups a user belongs to"""
        return await self.group_repo.get_user_groups(user_id, role)

    async def get_group_detail(self, group_id: int, user_id: int):
        group = await self.group_repo.get_group_with_members(group_id)
        if not group:
            return None
            
        is_member = any(m.user_id == user_id for m in group.members)
        is_creator = group.created_by == user_id
        
        # Get recent posts
        posts_result = await self.group_repo.session.execute(
            select(GroupPost).options(
                joinedload(GroupPost.author)
            ).filter(GroupPost.group_id == group_id)
            .order_by(GroupPost.created_at.desc()).limit(20)
        )
        posts = posts_result.scalars().unique().all()
        
        formatted_posts = []
        for post in posts:
            formatted_posts.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author_name": post.author.full_name if post.author else "Unknown",
                "created_at": post.created_at
            })
            
        return {
            "group": group,
            "is_member": is_member,
            "is_creator": is_creator,
            "posts": formatted_posts,
            "member_count": len(group.members)
        }

    async def join_group(self, group_id: int, user_id: int):
        group = await self.group_repo.get_group_by_id(group_id)
        if not group or not group.is_active:
            return False
            
        is_member = await self.group_repo.is_group_member(group_id, user_id)
        if is_member:
            return True
            
        await self.group_repo.add_member({
            "group_id": group_id,
            "user_id": user_id,
            "role": "member"
        })
        return True