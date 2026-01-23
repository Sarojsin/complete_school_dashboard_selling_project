from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_, and_, func, desc
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from app.models.group_models import Group, GroupMember
from app.models.models import User
import logging

logger = logging.getLogger(__name__)

class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_group(self, group_data: dict) -> Group:
        """Create a new group"""
        group = Group(**group_data)
        self.session.add(group)
        await self.session.commit()
        await self.session.refresh(group)
        return group
    
    async def get_group_by_id(self, group_id: int) -> Optional[Group]:
        """Get group by ID"""
        result = await self.session.execute(select(Group).filter(Group.id == group_id))
        return result.scalars().first()
    
    async def get_group_by_code(self, code: str) -> Optional[Group]:
        """Get group by unique code"""
        result = await self.session.execute(select(Group).filter(Group.code == code))
        return result.scalars().first()
    
    async def update_group(self, group_id: int, update_data: dict) -> Optional[Group]:
        """Update group information"""
        group = await self.get_group_by_id(group_id)
        if group:
            for key, value in update_data.items():
                setattr(group, key, value)
            await self.session.commit()
            await self.session.refresh(group)
        return group
    
    async def delete_group(self, group_id: int) -> bool:
        """Delete a group (soft delete)"""
        group = await self.get_group_by_id(group_id)
        if group:
            group.is_active = False
            await self.session.commit()
            return True
        return False
    
    async def get_user_groups(self, user_id: int, role: str = None) -> List[Group]:
        """Get all groups a user belongs to, optionally filtered by role"""
        query = select(Group).join(GroupMember, GroupMember.group_id == Group.id).filter(
            GroupMember.user_id == user_id,
            GroupMember.is_active == True,
            Group.is_active == True
        )
        
        if role:
            query = query.filter(GroupMember.role == role)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def is_group_member(self, group_id: int, user_id: int) -> bool:
        """Check if user is a member of the group"""
        result = await self.session.execute(
            select(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id,
                GroupMember.is_active == True
            )
        )
        member = result.scalars().first()
        return member is not None
    
    async def get_member_role(self, group_id: int, user_id: int) -> Optional[str]:
        """Get user's role in a group"""
        result = await self.session.execute(
            select(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id,
                GroupMember.is_active == True
            )
        )
        member = result.scalars().first()
        return member.role if member else None
    
    async def add_member(self, member_data: dict) -> GroupMember:
        """Add a user to a group"""
        member = GroupMember(**member_data)
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member
    
    async def remove_member(self, group_id: int, user_id: int) -> bool:
        """Remove a user from a group"""
        result = await self.session.execute(
            select(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            )
        )
        member = result.scalars().first()
        
        if member:
            member.is_active = False
            await self.session.commit()
            return True
        return False
    
    async def get_group_members(self, group_id: int, role: str = None) -> List[GroupMember]:
        """Get all members of a group"""
        query = select(GroupMember).options(joinedload(GroupMember.user)).filter(
            GroupMember.group_id == group_id,
            GroupMember.is_active == True
        )
        
        if role:
            query = query.filter(GroupMember.role == role)
        
        result = await self.session.execute(query)
        return result.scalars().unique().all()
    
    async def get_group_with_members(self, group_id: int) -> Optional[Group]:
        """Get group with all members"""
        result = await self.session.execute(
            select(Group).options(
                selectinload(Group.members).selectinload(GroupMember.user)
            ).filter(Group.id == group_id)
        )
        return result.scalars().first()
    
    async def search_users_for_invite(self, search_term: str, exclude_ids: List[int] = None) -> List[User]:
        """Search users to invite to group"""
        query = select(User).filter(
            and_(
                or_(
                    User.email.ilike(f"%{search_term}%"),
                    User.full_name.ilike(f"%{search_term}%")
                ),
                User.is_active == True
            )
        )
        
        if exclude_ids:
            query = query.filter(User.id.notin_(exclude_ids))
        
        result = await self.session.execute(query.limit(20))
        return result.scalars().all()