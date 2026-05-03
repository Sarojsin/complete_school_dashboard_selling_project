from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal, require_school_teacher, require_school_authority
from modules.shared.models import User
from .repository import GroupRepository, GroupPostRepository
from .schemas import (
    GroupCreate, GroupUpdate, GroupOut, GroupWithMembers,
    GroupMemberCreate, GroupMemberOut, GroupInviteRequest,
    GroupPostCreate, GroupPostUpdate, GroupPostOut
)

router = APIRouter(dependencies=[Depends(require_school_portal)])


# GROUP ENDPOINTS

@router.get("/", response_model=List[GroupOut])
async def get_my_groups(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all groups user belongs to"""
    groups = await GroupRepository.get_user_groups(db, current_user.id)
    return groups


@router.post("/", response_model=GroupOut)
async def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Create a new group (Teacher only)"""
    new_group = await GroupRepository.create_group(
        db,
        {
            "name": group_data.name,
            "description": group_data.description,
            "created_by": current_user.id
        }
    )
    # Add creator as admin member
    await GroupRepository.add_member(db, {
        "group_id": new_group.id,
        "user_id": current_user.id,
        "role": "teacher"
    })
    return new_group


@router.get("/{group_id}", response_model=GroupWithMembers)
async def get_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get group details"""
    group = await GroupRepository.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check membership
    is_member = await GroupRepository.is_member(db, group_id, current_user.id)
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    members = await GroupRepository.get_group_members(db, group_id)
    return GroupWithMembers(
        **group.__dict__,
        member_count=len(members)
    )


@router.put("/{group_id}", response_model=GroupOut)
async def update_group(
    group_id: int,
    group_update: GroupUpdate,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Update group (Creator only)"""
    group = await GroupRepository.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_group = await GroupRepository.update_group(
        db, group, **group_update.model_dump(exclude_unset=True)
    )
    return updated_group


@router.delete("/{group_id}")
async def delete_group(
    group_id: int,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Delete group (Creator only)"""
    group = await GroupRepository.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await GroupRepository.delete_group(db, group)
    return {"message": "Group deleted successfully"}


@router.post("/join")
async def join_group(
    code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Join a group using code"""
    group = await GroupRepository.get_group_by_code(db, code)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if already member
    is_member = await GroupRepository.is_member(db, group.id, current_user.id)
    if is_member:
        raise HTTPException(status_code=400, detail="Already a member")
    
    role = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    await GroupRepository.add_member(db, {
        "group_id": group.id,
        "user_id": current_user.id,
        "role": role
    })
    return {"message": "Joined group successfully", "group": group}


@router.post("/{group_id}/leave")
async def leave_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Leave a group"""
    group = await GroupRepository.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    is_member = await GroupRepository.is_member(db, group_id, current_user.id)
    if not is_member:
        raise HTTPException(status_code=400, detail="Not a member")
    
    # Can't leave if creator
    if group.created_by == current_user.id:
        raise HTTPException(status_code=400, detail="Creator cannot leave group")
    
    await GroupRepository.remove_member(db, group_id, current_user.id)
    return {"message": "Left group successfully"}


@router.post("/{group_id}/members", response_model=GroupMemberOut)
async def add_member(
    group_id: int,
    member_data: GroupMemberCreate,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Add member to group (Teacher/Authority only)"""
    group = await GroupRepository.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if already member
    existing = await GroupRepository.get_member(db, group_id, member_data.user_id)
    if existing:
        raise HTTPException(status_code=400, detail="User already a member")
    
    member = await GroupRepository.add_member(db, {
        "group_id": group_id,
        "user_id": member_data.user_id,
        "role": member_data.role.value
    })
    return member


@router.get("/{group_id}/members", response_model=List[GroupMemberOut])
async def get_members(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get group members"""
    group = await GroupRepository.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    members = await GroupRepository.get_group_members(db, group_id)
    return members


# GROUP POST ENDPOINTS

@router.get("/{group_id}/posts", response_model=List[GroupPostOut])
async def get_group_posts(
    group_id: int,
    post_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get posts in a group"""
    group = await GroupRepository.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    posts = await GroupPostRepository.get_group_posts(db, group_id, post_type, limit, offset)
    return posts


@router.post("/{group_id}/posts", response_model=GroupPostOut)
async def create_post(
    group_id: int,
    post_data: GroupPostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a post in a group"""
    group = await GroupRepository.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    is_member = await GroupRepository.is_member(db, group_id, current_user.id)
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    post = await GroupPostRepository.create_post(db, {
        "group_id": group_id,
        "author_id": current_user.id,
        "title": post_data.title,
        "content": post_data.content,
        "post_type": post_data.post_type.value,
        "link_url": post_data.link_url
    })
    return post


@router.put("/posts/{post_id}", response_model=GroupPostOut)
async def update_post(
    post_id: int,
    post_update: GroupPostUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a post"""
    post = await GroupPostRepository.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_post = await GroupPostRepository.update_post(
        db, post, **post_update.model_dump(exclude_unset=True)
    )
    return updated_post


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a post"""
    post = await GroupPostRepository.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await GroupPostRepository.delete_post(db, post)
    return {"message": "Post deleted successfully"}