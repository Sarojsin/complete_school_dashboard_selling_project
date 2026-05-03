# College Dean Web Routes

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from backup.models.models import User
from backup.dependencies.auth import get_current_user

router = APIRouter(prefix="/deans", tags=["College Dean Web"])
templates = None


def set_templates(template_engine):
    global templates
    templates = template_engine


@router.get("/", response_class=HTMLResponse)
async def dean_list(request: Request, current_user: User = Depends(get_current_user)):
    if not templates:
        raise HTTPException(status_code=500, detail="Templates not configured")
    return templates.TemplateResponse("dean/list.html", {"request": request, "user": current_user})


__all__ = ["router", "set_templates"]
