from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_async_db
from app.core.templates import templates
from dependencies import get_current_user
from models.models import User
from models.group_models import Group, GroupMember, GroupPost
from repositories.group_repository import GroupRepository
from repositories.group_post_repository import GroupPostRepository

router = APIRouter()

@router.get("/groups")
async def groups_list(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Display all groups the user is a member of or can join"""
    # Get all public groups and groups user is a member of
    result = await db.execute(
        select(Group).options(
            selectinload(Group.members),
            joinedload(Group.creator)
        ).order_by(Group.created_at.desc())
    )
    all_groups = result.scalars().unique().all()
    
    # Separate into user's groups and available groups
    user_groups = []
    available_groups = []
    
    for group in all_groups:
        is_member = any(m.user_id == current_user.id for m in group.members)
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
        elif group.is_active:  # Show active groups as available
            available_groups.append(group_data)
    
    return templates.TemplateResponse(
        "groups/group_list.html",
        {
            "request": request,
            "current_user": current_user,
            "user_groups": user_groups,
            "available_groups": available_groups
        }
    )

@router.get("/groups/{group_id}")
async def group_detail(
    request: Request,
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Display group details and posts"""
    # Get group with members and posts
    result = await db.execute(
        select(Group).options(
            selectinload(Group.members).joinedload(GroupMember.user),
            joinedload(Group.creator)
        ).filter(Group.id == group_id)
    )
    group = result.scalars().first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if user is a member or creator
    is_member = any(m.user_id == current_user.id for m in group.members)
    is_creator = group.creator and group.creator.id == current_user.id
    
    # Get recent posts
    posts_result = await db.execute(
        select(GroupPost).options(
            joinedload(GroupPost.author)
        ).filter(
            GroupPost.group_id == group_id
        ).order_by(GroupPost.created_at.desc()).limit(20)
    )
    posts = posts_result.scalars().unique().all()
    
    formatted_posts = []
    for post in posts:
        formatted_posts.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_name": post.author.full_name if post.author else "Unknown",
            "created_at": post.created_at,
            "updated_at": post.updated_at
        })
    
    return templates.TemplateResponse(
        "groups/group_detail.html",
        {
            "request": request,
            "current_user": current_user,
            "group": group,
            "is_member": is_member,
            "is_creator": is_creator,
            "posts": formatted_posts,
            "member_count": len(group.members)
        }
    )

@router.get("/groups/{group_id}/posts/create")
async def create_post_form(
    request: Request,
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Display form to create a new post"""
    # Verify user is a member
    result = await db.execute(
        select(Group).options(
            selectinload(Group.members)
        ).filter(Group.id == group_id)
    )
    group = result.scalars().first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    is_member = any(m.user_id == current_user.id for m in group.members)
    if not is_member:
        raise HTTPException(status_code=403, detail="Must be a group member to post")
    
    return templates.TemplateResponse(
        "groups/new_post.html",
        {
            "request": request,
            "current_user": current_user,
            "group": group
        }
    )

@router.post("/groups/{group_id}/posts/create")
async def create_post(
    group_id: int,
    title: str = Form(...),
    content: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new post in the group"""
    # Verify membership
    result = await db.execute(
        select(Group).options(
            selectinload(Group.members)
        ).filter(Group.id == group_id)
    )
    group = result.scalars().first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    is_member = any(m.user_id == current_user.id for m in group.members)
    if not is_member:
        raise HTTPException(status_code=403, detail="Must be a group member to post")
    
    # Create post
    post = GroupPost(
        group_id=group_id,
        author_id=current_user.id,
        title=title,
        content=content
    )
    db.add(post)
    await db.commit()
    
    return RedirectResponse(url=f"/groups/{group_id}", status_code=303)

@router.post("/groups/{group_id}/join")
async def join_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Join a public group"""
    # Get group
    result = await db.execute(
        select(Group).options(
            selectinload(Group.members)
        ).filter(Group.id == group_id)
    )
    group = result.scalars().first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if group is active
    if not group.is_active:
        raise HTTPException(status_code=403, detail="Group is not active")
    
    # Check if already a member
    is_member = any(m.user_id == current_user.id for m in group.members)
    if is_member:
        return RedirectResponse(url=f"/groups/{group_id}", status_code=303)
    
    # Add member
    member = GroupMember(
        group_id=group_id,
        user_id=current_user.id,
        role="member"
    )
    db.add(member)
    await db.commit()
    
    return RedirectResponse(url=f"/groups/{group_id}", status_code=303)

@router.post("/groups/{group_id}/leave")
async def leave_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Leave a group"""
    # Get group
    result = await db.execute(
        select(Group).options(joinedload(Group.creator)).filter(Group.id == group_id)
    )
    group = result.scalars().first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Can't leave if you're the creator - check using the creator relationship
    is_creator = group.creator and group.creator.id == current_user.id
    if is_creator:
        raise HTTPException(status_code=403, detail="Creator cannot leave the group")
    
    # Remove membership
    result = await db.execute(
        select(GroupMember).filter(
            and_(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user.id
            )
        )
    )
    member = result.scalars().first()
    
    if member:
        await db.delete(member)
        await db.commit()
    
    return RedirectResponse(url="/groups", status_code=303)
