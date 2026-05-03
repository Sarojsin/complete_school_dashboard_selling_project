# School Groups Utils
# ================

from typing import List, Dict, Optional
from datetime import datetime
from .constants import GROUP_TYPE_PRIVATE, MEMBER_ROLE_ADMIN, MAX_MEMBERS_DEFAULT


def can_join_group(group_type: str, is_member: bool) -> bool:
    """Check if user can join group"""
    if group_type == GROUP_TYPE_PRIVATE and is_member:
        return False
    return True


def can_moderate(user_role: str) -> bool:
    """Check if user can moderate group"""
    return user_role in [MEMBER_ROLE_ADMIN, "moderator"]


def format_group_size(member_count: int) -> str:
    """Format group size for display"""
    if member_count == 0:
        return "No members"
    elif member_count == 1:
        return "1 member"
    elif member_count < 1000:
        return f"{member_count} members"
    else:
        thousands = member_count / 1000
        return f"{thousands:.1f}k members"


def is_group_full(current_count: int, capacity: Optional[int]) -> bool:
    """Check if group is at capacity"""
    max_members = capacity or MAX_MEMBERS_DEFAULT
    return current_count >= max_members


def get_member_permissions(user_role: str) -> Dict[str, bool]:
    """Get permissions for member role"""
    permissions = {
        "can_post": user_role in ["admin", "moderator", "member"],
        "can_comment": user_role in ["admin", "moderator", "member"],
        "can_delete_own_post": user_role in ["admin", "moderator", "member"],
        "can_delete_any_post": user_role in ["admin", "moderator"],
        "can_invite": user_role in ["admin", "moderator"],
        "can_remove_member": user_role in ["admin", "moderator"],
        "can_update_group": user_role == "admin"
    }
    return permissions


def format_post_time(created_at: datetime) -> str:
    """Format post time for display"""
    now = datetime.utcnow()
    delta = now - created_at
    
    if delta.total_seconds() < 60:
        return "Just now"
    elif delta.total_seconds() < 3600:
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes}m ago"
    elif delta.total_seconds() < 86400:
        hours = int(delta.total_seconds() / 3600)
        return f"{hours}h ago"
    elif delta.days < 7:
        return f"{delta.days}d ago"
    else:
        return created_at.strftime("%Y-%m-%d")


def calculate_engagement_score(likes: int, comments: int, shares: int) -> int:
    """Calculate engagement score"""
    return likes + (comments * 2) + (shares * 3)


__all__ = [
    "can_join_group",
    "can_moderate",
    "format_group_size",
    "is_group_full",
    "get_member_permissions",
    "format_post_time",
    "calculate_engagement_score"
]