from typing import List, Optional, Dict, Any
from repositories.group_repository import GroupRepository
from repositories.user_repository import UserRepository
from schemas.group_schemas import GroupCreate, GroupUpdate, GroupInviteRequest
from models.models import UserRole
from utils.exceptions import PermissionDeniedError, NotFoundError, ValidationError
import random
import string
import logging

logger = logging.getLogger(__name__)

class GroupService:
    def __init__(self, group_repo: GroupRepository):
        self.group_repo = group_repo
    
    def generate_group_code(self) -> str:
        """Generate a unique group code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            existing = self.group_repo.get_group_by_code(code)
            if not existing:
                return code
    
    def create_group(self, group_data: GroupCreate, creator_id: int) -> Dict[str, Any]:
        """Create a new group with the creator as a teacher"""
        # Generate unique group code
        group_code = self.generate_group_code()
        
        # Create group
        group_dict = group_data.dict()
        group_dict.update({
            "created_by": creator_id,
            "code": group_code
        })
        
        group = self.group_repo.create_group(group_dict)
        
        # Add creator as teacher member
        self.group_repo.add_member({
            "group_id": group.id,
            "user_id": creator_id,
            "role": "teacher"
        })
        
        return {
            "id": group.id,
            "name": group.name,
            "code": group.code,
            "created_at": group.created_at
        }
    
    def get_user_groups(self, user_id: int, user_role: str) -> List[Dict[str, Any]]:
        """Get all groups for a user"""
        groups = self.group_repo.get_user_groups(user_id)
        
        result = []
        for group in groups:
            # Get member counts
            all_members = self.group_repo.get_group_members(group.id)
            teachers = [m for m in all_members if m.role == "teacher"]
            students = [m for m in all_members if m.role == "student"]
            
            result.append({
                "id": group.id,
                "name": group.name,
                "description": group.description,
                "code": group.code,
                "created_at": group.created_at,
                "member_count": len(all_members),
                "teacher_count": len(teachers),
                "student_count": len(students),
                "is_teacher": any(m.user_id == user_id and m.role == "teacher" for m in all_members)
            })
        
        return result
    
    def update_group(self, group_id: int, name: Optional[str], description: Optional[str], current_user_id: int) -> dict:
        """Update group details - only creator or teachers can update"""
        group = self.group_repo.get_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        
        # Check if user is creator or teacher in the group
        is_creator = group.created_by == current_user_id
        user_role = self.group_repo.get_member_role(group_id, current_user_id)
        is_teacher = user_role == "teacher"
        
        if not (is_creator or is_teacher):
            raise HTTPException(
                status_code=403,
                detail="Only group creator or teachers can update group details"
            )
        
        updated_group = self.group_repo.update_group(group_id, name, description)
        
        return {
            "id": updated_group.id,
            "name": updated_group.name,
            "description": updated_group.description,
            "code": updated_group.code,
            "updated_at": updated_group.updated_at.isoformat() if updated_group.updated_at else None
        }
    
    def add_members_to_group(
        self, 
        group_id: int, 
        invite_data: GroupInviteRequest, 
        requester_id: int
    ) -> Dict[str, Any]:
        """Add multiple members to a group"""
        # Verify group exists
        group = self.group_repo.get_group_by_id(group_id)
        if not group:
            raise NotFoundError(f"Group {group_id} not found")
        
        # Verify requester is a teacher in the group
        requester_role = self.group_repo.get_member_role(group_id, requester_id)
        if requester_role != "teacher":
            raise PermissionDeniedError("Only teachers can add members")
        
        added = []
        failed = []
        
        for user_id in invite_data.user_ids:
            # Check if user exists using static UserRepository with session from group_repo
            user = UserRepository.get_by_id(self.group_repo.session, user_id)
            if not user or not user.is_active:
                failed.append({"user_id": user_id, "reason": "User not found or inactive"})
                continue
            
            # Check if user is already a member
            is_member = self.group_repo.is_group_member(group_id, user_id)
            if is_member:
                failed.append({"user_id": user_id, "reason": "Already a member"})
                continue
            
            # Add user to group
            self.group_repo.add_member({
                "group_id": group_id,
                "user_id": user_id,
                "role": invite_data.role
            })
            added.append({
                "user_id": user_id,
                "name": user.full_name,
                "email": user.email,
                "role": invite_data.role
            })
        
        return {
            "group_id": group_id,
            "group_name": group.name,
            "added": added,
            "failed": failed
        }
    
    def remove_member_from_group(
        self, 
        group_id: int, 
        user_id: int, 
        requester_id: int
    ) -> bool:
        """Remove a member from a group"""
        # Verify group exists
        group = self.group_repo.get_group_by_id(group_id)
        if not group:
            raise NotFoundError(f"Group {group_id} not found")
        
        # Verify requester is a teacher in the group
        requester_role = self.group_repo.get_member_role(group_id, requester_id)
        if requester_role != "teacher":
            raise PermissionDeniedError("Only teachers can remove members")
        
        # Cannot remove yourself if you're the only teacher
        if user_id == requester_id:
            teachers = self.group_repo.get_group_members(group_id, "teacher")
            if len(teachers) <= 1:
                raise ValidationError("Cannot remove the only teacher from the group")
        
        return self.group_repo.remove_member(group_id, user_id)
    
    def get_group_details(self, group_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed group information"""
        group = self.group_repo.get_group_by_id(group_id)
        if not group:
            return None
        
        # Check if user is a member
        is_member = self.group_repo.is_group_member(group_id, user_id)
        if not is_member:
            raise PermissionDeniedError("You are not a member of this group")
        
        # Get all members
        members = self.group_repo.get_group_members(group_id)
        teachers = []
        students = []
        
        for member in members:
            member_info = {
                "id": member.user.id,
                "name": member.user.full_name,
                "email": member.user.email,
                "role": member.role,
                "joined_at": member.joined_at
            }
            
            if member.role == "teacher":
                teachers.append(member_info)
            else:
                students.append(member_info)
        
        # Get user's role in group
        user_role = self.group_repo.get_member_role(group_id, user_id)
        
        return {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "code": group.code,
            "created_by": group.created_by,
            "created_at": group.created_at,
            "user_role": user_role,
            "teachers": teachers,
            "students": students,
            "total_members": len(members),
            "total_teachers": len(teachers),
            "total_students": len(students)
        }
    
    def search_users_to_invite(
        self, 
        group_id: int, 
        search_term: str, 
        requester_id: int
    ) -> List[Dict[str, Any]]:
        """Search users to invite to group"""
        # Verify requester is a teacher in the group
        requester_role = self.group_repo.get_member_role(group_id, requester_id)
        if requester_role != "teacher":
            raise PermissionDeniedError("Only teachers can invite members")
        
        # Get existing member IDs to exclude
        members = self.group_repo.get_group_members(group_id)
        exclude_ids = [member.user_id for member in members]
        
        # Search users
        users = self.group_repo.search_users_for_invite(search_term, exclude_ids)
        
        return [
            {
                "id": user.id,
                "name": user.full_name,
                "email": user.email,
                "current_role": user.role.value if hasattr(user.role, 'value') else user.role
            }
            for user in users
        ]