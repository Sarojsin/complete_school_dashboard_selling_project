from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backup.core.database import get_async_db
from backup.core.templates import templates
from backup.dependencies.auth import get_current_user
from backup.models.models import User
from backup.models.group_models import Group, GroupMember, GroupPost
from backup.repositories.group_repository import GroupRepository
from backup.repositories.group_post_repository import GroupPostRepository
from backup.services.group_service import GroupService

router = APIRouter()

@router.get("/groups")
async def groups_list(request: Request, current_user: User = Depends(get_current_user)):
    role = current_user.role.value.lower()
    if role not in ['authority', 'teacher', 'student']:
         role = 'student' # default or common
    return RedirectResponse(url=f"/{role}/groups", status_code=302)

# Keep other specialized routes if needed, or redirect them too
@router.get("/groups/create")
async def create_group_redirect(current_user: User = Depends(get_current_user)):
    role = current_user.role.value.lower()
    if role in ['authority', 'admin']:
        return RedirectResponse(url="/authority/groups/create", status_code=302)
    return RedirectResponse(url="/groups", status_code=302)

@router.get("/groups/{group_id}")
async def group_detail(group_id: int, current_user: User = Depends(get_current_user)):
    role = current_user.role.value.lower()
    return RedirectResponse(url=f"/{role}/groups/{group_id}", status_code=302)

@router.get("/groups/{group_id}/posts/create")
async def create_post_form(group_id: int, current_user: User = Depends(get_current_user)):
    role = current_user.role.value.lower()
    return RedirectResponse(url=f"/{role}/groups/{group_id}/posts/create", status_code=302)
@router.get("/groups/{group_id}/posts")
async def group_posts_redirect(group_id: int, current_user: User = Depends(get_current_user)):
    role = current_user.role.value.lower()
    return RedirectResponse(url=f"/{role}/groups/{group_id}/posts", status_code=302)

@router.get("/groups/{group_id}/edit")
async def edit_group_redirect(group_id: int, current_user: User = Depends(get_current_user)):
    role = current_user.role.value.lower()
    return RedirectResponse(url=f"/{role}/groups/{group_id}/edit", status_code=302)
