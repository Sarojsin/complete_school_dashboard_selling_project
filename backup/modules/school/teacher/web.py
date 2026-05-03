# School Teacher Web Routes
# ========================

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backup.core.database import get_async_db
from backup.models.models import User
from backup.dependencies.auth import get_current_user

router = APIRouter(prefix="/teachers", tags=["School Teacher Web"])
templates = None


def set_templates(template_engine: Jinja2Templates):
    global templates
    templates = template_engine


@router.get("/", response_class=HTMLResponse)
async def teacher_list(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if not templates:
        raise HTTPException(status_code=500, detail="Templates not configured")
    return templates.TemplateResponse(
        "teacher/list.html",
        {"request": request, "user": current_user}
    )


@router.get("/{teacher_id}", response_class=HTMLResponse)
async def teacher_detail(
    teacher_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if not templates:
        raise HTTPException(status_code=500, detail="Templates not configured")
    return templates.TemplateResponse(
        "teacher/detail.html",
        {"request": request, "user": current_user, "teacher_id": teacher_id}
    )


__all__ = ["router", "set_templates"]
