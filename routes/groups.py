from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional, List

from dependencies import get_db, get_current_user
from models.models import UserRole
from repositories.group_repository import GroupRepository
from repositories.user_repository import UserRepository
from services.group_service import GroupService
from schemas.group_schemas import (
    GroupCreate, GroupUpdate, GroupInviteRequest,
    GroupMemberRole
)

# Placeholder decorator because @require_roles usage is not clear from context if it supports sync/async
# Assuming it's a valid dependency or wrapper.
# If require_roles is a dependency yielding a user, it's fine. If it's a decorator, it might need to handle async properly.
# Looking at original code, it was used as decorator. I'll keep it as is, assuming it wraps async functions fine.
# But wait, I'm modifying functions to be "async def" still, so wrapper should be fine.

# BUT I need to remove "from dependencies import require_roles" if it is not available or standard. 
# The original code imported it. I'll keep it.

# IMPORTANT: I need to check where `require_roles` comes from. It was in `dependencies`. 
# I did not check dependencies.py for require_roles. Let's assume it exists.



router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("/", response_class=HTMLResponse)
async def list_groups(
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Display all groups user belongs to"""
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    
    groups = group_service.get_user_groups(current_user.id, current_user.role)
    
    return request.app.state.templates.TemplateResponse(
        "groups/group_list.html",
        {
            "request": request,
            "current_user": current_user,
            "groups": groups
        }
    )

@router.get("/create", response_class=HTMLResponse)
# @require_roles([UserRole.AUTHORITY, UserRole.ADMIN, UserRole.TEACHER]) # require_roles likely expects UserRole enum
async def create_group_page(
    request: Request,
    current_user = Depends(get_current_user)
):
    """Display create group form - Authority only"""
    # Only Authority can create groups
    role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    if role.lower() not in ["authority", "admin"]:
        request.session["error"] = "Only Authority can create groups"
        return RedirectResponse(url="/groups", status_code=303)

    return request.app.state.templates.TemplateResponse(
        "groups/create_group.html",
        {
            "request": request,
            "current_user": current_user
        }
    )

@router.post("/create", response_class=RedirectResponse)
async def create_group(
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new group - Authority only"""
    # Only Authority can create groups
    role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    if role.lower() not in ["authority", "admin"]:
        raise HTTPException(status_code=403, detail="Only Authority can create groups")

    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    
    group_data = GroupCreate(name=name, description=description)
    
    try:
        result = group_service.create_group(group_data, current_user.id)
        return RedirectResponse(
            url=f"/groups/{result['id']}",
            status_code=303
        )
    except Exception as e:
        request.session["error"] = str(e)
        return RedirectResponse(url="/groups/create", status_code=303)

@router.get("/{group_id}", response_class=HTMLResponse)
async def group_detail(
    request: Request,
    group_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Display group details"""
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    
    try:
        group_details = group_service.get_group_details(group_id, current_user.id)
        return request.app.state.templates.TemplateResponse(
            "groups/group_detail.html",
            {
                "request": request,
                "current_user": current_user,
                "group": group_details,
                "is_teacher": group_details["user_role"] == "teacher"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        request.session["error"] = str(e)
        return RedirectResponse(url="/groups", status_code=303)

@router.get("/{group_id}/edit", response_class=HTMLResponse)
async def edit_group_page(
    request: Request,
    group_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Display edit group form"""
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    
    try:
        group_data = group_service.get_group_details(group_id, current_user.id)
        
        # Check if user can edit (creator or teacher)
        is_creator = group_data["creator"]["id"] == current_user.id
        user_role = group_repo.get_member_role(group_id, current_user.id)
        is_teacher = user_role == "teacher"
        
        if not (is_creator or is_teacher):
            request.session["error"] = "Only group creator or teachers can edit group details"
            return RedirectResponse(url=f"/groups/{group_id}", status_code=303)
        
        return request.app.state.templates.TemplateResponse(
            "groups/edit_group.html",
            {
                "request": request,
                "current_user": current_user,
                "group": group_data
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        request.session["error"] = str(e)
        return RedirectResponse(url="/groups", status_code=303)

@router.post("/{group_id}/edit", response_class=RedirectResponse)
async def update_group(
    request: Request,
    group_id: int,
    name: str = Form(...),
    description: str = Form(""),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update group details"""
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    
    try:
        group_service.update_group(group_id, name, description, current_user.id)
        request.session["message"] = f"Group '{name}' updated successfully"
        return RedirectResponse(url=f"/groups/{group_id}", status_code=303)
    except HTTPException:
        raise
    except Exception as e:
        request.session["error"] = str(e)
        return RedirectResponse(url=f"/groups/{group_id}/edit", status_code=303)

@router.get("/{group_id}/manage", response_class=HTMLResponse)
async def manage_members_page(
    request: Request,
    group_id: int,
    search: Optional[str] = Query(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Display member management page - Authority only"""
    # Only Authority can manage members
    role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    if role.lower() not in ["authority", "admin"]:
        request.session["error"] = "Only Authority can manage group members"
        return RedirectResponse(url=f"/groups/{group_id}", status_code=303)
    
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    
    try:
        group_details = group_service.get_group_details(group_id, current_user.id)

        # Search for users to invite
        search_results = []
        if search:
            search_results = group_service.search_users_to_invite(
                group_id, search, current_user.id
            )
        
        return request.app.state.templates.TemplateResponse(
            "groups/manage_members.html",
            {
                "request": request,
                "current_user": current_user,
                "group": group_details,
                "search": search,
                "search_results": search_results,
                "roles": [role.value for role in GroupMemberRole]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        request.session["error"] = str(e)
        return RedirectResponse(url=f"/groups/{group_id}", status_code=303)

@router.post("/{group_id}/members/add", response_class=RedirectResponse)
async def add_members(
    request: Request,
    group_id: int,
    user_ids: List[int] = Form(...),
    role: str = Form(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add members to group"""
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    
    invite_data = GroupInviteRequest(user_ids=user_ids, role=role)
    
    try:
        result = group_service.add_members_to_group(
            group_id, invite_data, current_user.id
        )
        request.session["message"] = f"Added {len(result['added'])} members"
        if result['failed']:
            request.session["warning"] = f"{len(result['failed'])} users could not be added"
    except Exception as e:
        request.session["error"] = str(e)
    
    return RedirectResponse(
        url=f"/groups/{group_id}/manage",
        status_code=303
    )

@router.post("/{group_id}/members/{user_id}/remove", response_class=RedirectResponse)
async def remove_member(
    request: Request,
    group_id: int,
    user_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove member from group"""
    group_repo = GroupRepository(db)
    user_repo = UserRepository(db)
    group_service = GroupService(group_repo, user_repo)
    
    try:
        group_service.remove_member_from_group(group_id, user_id, current_user.id)
        request.session["message"] = "Member removed successfully"
    except Exception as e:
        request.session["error"] = str(e)
    
    return RedirectResponse(
        url=f"/groups/{group_id}/manage",
        status_code=303
    )

# API endpoints for AJAX calls
@router.get("/api/{group_id}/members")
async def get_group_members_api(
    group_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """API endpoint to get group members"""
    group_repo = GroupRepository(db)
    
    # Check if user is member
    is_member = group_repo.is_group_member(group_id, current_user.id)
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    members = group_repo.get_group_members(group_id)
    
    return [
        {
            "id": member.user.id,
            "name": member.user.full_name,
            "email": member.user.email,
            "role": member.role,
            "joined_at": member.joined_at.isoformat()
        }
        for member in members
    ]