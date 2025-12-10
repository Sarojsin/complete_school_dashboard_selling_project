from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

from dependencies import get_db, get_current_user
from models.models import UserRole
from repositories.group_post_repository import GroupPostRepository
from repositories.group_repository import GroupRepository
from services.group_post_service import GroupPostService
from schemas.group_post_schemas import GroupPostCreate, GroupPostUpdate

router = APIRouter(prefix="/groups/{group_id}/posts", tags=["group_posts"])

@router.get("/", response_class=HTMLResponse)
async def list_posts(
    request: Request,
    group_id: int,
    post_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Display all posts in a group"""
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    post_service = GroupPostService(post_repo, group_repo)
    
    limit = 20
    offset = (page - 1) * limit
    
    try:
        posts_data = post_service.get_group_posts(
            group_id, current_user.id, post_type, limit, offset
        )
        
        # Get user role for permissions
        user_role = group_repo.get_member_role(group_id, current_user.id)
        
        return request.app.state.templates.TemplateResponse(
            "groups/group_posts.html",
            {
                "request": request,
                "current_user": current_user,
                "group": {
                    "id": group_id,
                    "name": posts_data["group_name"]
                },
                "posts": posts_data["posts"],
                "post_type": post_type,
                "page": page,
                "has_more": posts_data["has_more"],
                "is_teacher": user_role == "teacher",
                "post_types": ["notice", "note", "link"]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        request.session["error"] = str(e)
        return RedirectResponse(url=f"/groups/{group_id}", status_code=303)

@router.get("/create", response_class=HTMLResponse)
async def create_post_page(
    request: Request,
    group_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Display create post form - Authority and Teachers only"""
    group_repo = GroupRepository(db)
    
    # Verify user is teacher or authority
    user_role = group_repo.get_member_role(group_id, current_user.id)
    current_role = str(current_user.role.value) if hasattr(current_user.role, 'value') else str(current_user.role)
    
    is_authority = current_role.lower() in ["authority", "admin"]
    is_teacher = user_role == "teacher"
    
    if not (is_authority or is_teacher):
        raise HTTPException(status_code=403, detail="Only Authority and Teachers can create posts")
    
    return request.app.state.templates.TemplateResponse(
        "groups/new_post.html",
        {
            "request": request,
            "current_user": current_user,
            "group_id": group_id,
            "post_types": ["notice", "note", "link"]
        }
    )

@router.post("/create", response_class=RedirectResponse)
async def create_post(
    request: Request,
    group_id: int,
    title: str = Form(...),
    content: Optional[str] = Form(None),
    post_type: str = Form(...),
    link_url: Optional[str] = Form(None),
    link_description: Optional[str] = Form(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post"""
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    post_service = GroupPostService(post_repo, group_repo)
    
    post_data = GroupPostCreate(
        group_id=group_id,
        title=title,
        content=content,
        post_type=post_type,
        link_url=link_url,
        link_description=link_description
    )
    
    try:
        result = post_service.create_post(post_data, current_user.id)
        request.session["message"] = f"Post '{result['title']}' created successfully"
        return RedirectResponse(
            url=f"/groups/{group_id}/posts",
            status_code=303
        )
    except Exception as e:
        request.session["error"] = str(e)
        return RedirectResponse(
            url=f"/groups/{group_id}/posts/create",
            status_code=303
        )

@router.get("/{post_id}", response_class=HTMLResponse)
async def view_post(
    request: Request,
    group_id: int,
    post_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """View a single post"""
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    
    # Verify user is group member
    is_member = group_repo.is_group_member(group_id, current_user.id)
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    post = post_repo.get_post_by_id(post_id)
    if not post or post.group_id != group_id:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Get user role
    user_role = group_repo.get_member_role(group_id, current_user.id)
    
    return request.app.state.templates.TemplateResponse(
        "groups/view_post.html",
        {
            "request": request,
            "current_user": current_user,
            "post": post,
            "group_id": group_id,
            "is_teacher": user_role == "teacher",
            "is_author": post.author_id == current_user.id
        }
    )

@router.post("/{post_id}/delete", response_class=RedirectResponse)
async def delete_post(
    request: Request,
    group_id: int,
    post_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a post"""
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    post_service = GroupPostService(post_repo, group_repo)
    
    try:
        post_service.delete_post(post_id, current_user.id)
        request.session["message"] = "Post deleted successfully"
    except Exception as e:
        request.session["error"] = str(e)
    
    return RedirectResponse(
        url=f"/groups/{group_id}/posts",
        status_code=303
    )

# API endpoints
@router.get("/api/posts")
async def get_posts_api(
    group_id: int,
    post_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """API endpoint for posts (for AJAX)"""
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    post_service = GroupPostService(post_repo, group_repo)
    
    limit = 10
    offset = (page - 1) * limit
    
    try:
        posts_data = post_service.get_group_posts(
            group_id, current_user.id, post_type, limit, offset
        )
        return posts_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))