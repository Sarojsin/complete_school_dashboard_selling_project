from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
from models.group_models import Group, GroupMember
from models.models import User
import logging

logger = logging.getLogger(__name__)

class GroupRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_group(self, group_data: dict) -> Group:
        """Create a new group"""
        group = Group(**group_data)
        self.session.add(group)
        self.session.commit()
        self.session.refresh(group)
        return group
    
    def get_group_by_id(self, group_id: int) -> Optional[Group]:
        """Get group by ID"""
        return self.session.query(Group).filter(Group.id == group_id).first()
    
    def get_group_by_code(self, code: str) -> Optional[Group]:
        """Get group by unique code"""
        return self.session.query(Group).filter(Group.code == code).first()
    
    def update_group(self, group_id: int, update_data: dict) -> Optional[Group]:
        """Update group information"""
        group = self.get_group_by_id(group_id)
        if group:
            for key, value in update_data.items():
                setattr(group, key, value)
            self.session.commit()
            self.session.refresh(group)
        return group
    
    def delete_group(self, group_id: int) -> bool:
        """Delete a group (soft delete)"""
        group = self.get_group_by_id(group_id)
        if group:
            group.is_active = False
            self.session.commit()
            return True
        return False
    
    def get_user_groups(self, user_id: int, role: str = None) -> List[Group]:
        """Get all groups a user belongs to, optionally filtered by role"""
        query = self.session.query(Group).join(GroupMember, GroupMember.group_id == Group.id).filter(
            GroupMember.user_id == user_id,
            GroupMember.is_active == True,
            Group.is_active == True
        )
        
        if role:
            query = query.filter(GroupMember.role == role)
        
        return query.all()
    
    def is_group_member(self, group_id: int, user_id: int) -> bool:
        """Check if user is a member of the group"""
        member = self.session.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
            GroupMember.is_active == True
        ).first()
        return member is not None
    
    def get_member_role(self, group_id: int, user_id: int) -> Optional[str]:
        """Get user's role in a group"""
        member = self.session.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id,
            GroupMember.is_active == True
        ).first()
        return member.role if member else None
    
    def update_group(self, group_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Group]:
        """Update group details"""
        group = self.get_by_id(group_id)
        if not group:
            return None
        
        if name:
            group.name = name
        if description is not None:  # Allow empty string
            group.description = description
        
        self.session.commit()
        self.session.refresh(group)
        return group
    
    def add_member(self, member_data: dict) -> GroupMember:
        """Add a user to a group"""
        member = GroupMember(**member_data)
        self.session.add(member)
        self.session.commit()
        self.session.refresh(member)
        return member
    
    def remove_member(self, group_id: int, user_id: int) -> bool:
        """Remove a user from a group"""
        member = self.session.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        
        if member:
            member.is_active = False
            self.session.commit()
            return True
        return False
    
    def get_group_members(self, group_id: int, role: str = None) -> List[GroupMember]:
        """Get all members of a group"""
        query = self.session.query(GroupMember).options(joinedload(GroupMember.user)).filter(
            GroupMember.group_id == group_id,
            GroupMember.is_active == True
        )
        
        if role:
            query = query.filter(GroupMember.role == role)
        
        return query.all()
    
    def get_group_with_members(self, group_id: int) -> Optional[Group]:
        """Get group with all members"""
        return self.session.query(Group).options(
            selectinload(Group.members).selectinload(GroupMember.user)
        ).filter(Group.id == group_id).first()
    
    def search_users_for_invite(self, search_term: str, exclude_ids: List[int] = None) -> List[User]:
        """Search users to invite to group"""
        query = self.session.query(User).filter(
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
        
        return query.limit(20).all()