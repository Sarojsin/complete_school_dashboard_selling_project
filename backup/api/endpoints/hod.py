from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backup.dependencies import get_async_db, get_current_user
from backup.models.models import User, UserRole
from backup.models import models # Fallback if needed / or explicit mapping
from backup.repositories.department_repository import DepartmentRepository
from backup.services.department_service import DepartmentService
from backup.schemas.department_schemas import DepartmentCreate, DepartmentResponse

router = APIRouter(prefix="/api/hod", tags=["HOD"])

@router.get("/dashboard", response_model=dict)
async def get_hod_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.HOD:
        raise HTTPException(status_code=403, detail="Only HOD can access")
    
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    return await service.get_hod_dashboard(current_user.id)

@router.get("/departments", response_model=List[DepartmentResponse])
async def get_all_departments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    return await service.get_all_departments()