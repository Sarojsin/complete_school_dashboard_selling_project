# College HOD Web Routes

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backup.core.database import get_async_db
from backup.models.models import User
from backup.dependencies.auth import get_current_user

router = APIRouter(prefix="/hods", tags=["College HOD Web"])
templates = None


def set_templates(template_engine):
    global templates
    templates = template_engine


@router.get("/", response_class=HTMLResponse)
async def hod_list(request: Request, current_user: User = Depends(get_current_user)):
    if not templates:
        raise HTTPException(status_code=500, detail="Templates not configured")
    return templates.TemplateResponse("hod/list.html", {"request": request, "user": current_user})


__all__ = ["router", "set_templates"]
