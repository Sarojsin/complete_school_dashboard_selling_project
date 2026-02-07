from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.templates import templates
from app.dependencies import get_async_db, get_current_user_web
from app.models.models import User, UserRole
from app.repositories.department_repository import DepartmentRepository
from app.services.department_service import DepartmentService

router = APIRouter()

@router.get("/dashboard")
async def hod_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.HOD:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    stats = await service.get_hod_dashboard(current_user.id)
    
    return templates.TemplateResponse("hod/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "stats": stats
    })
