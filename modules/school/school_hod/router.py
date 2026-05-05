"""
School HOD Router

FastAPI endpoints for HOD dashboard and department oversight.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal, require_hod
from modules.shared.models import User
from .service import HODService
from .schemas import HODDashboardSchema, DepartmentListResponse, TeacherListResponse, CourseListResponse

router = APIRouter(
    prefix="/hod",
    tags=["School HOD"],
    dependencies=[Depends(require_school_portal)]
)


@router.get("/dashboard", response_model=HODDashboardSchema)
async def get_hod_dashboard(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_db)
):
    """Get HOD dashboard with department overview"""
    service = HODService(db)
    return await service.get_dashboard(current_user.id)


@router.get("/departments", response_model=DepartmentListResponse)
async def get_all_departments(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_db)
):
    """Get list of all departments in the school"""
    service = HODService(db)
    return await service.get_departments()


@router.get("/teachers", response_model=TeacherListResponse)
async def get_department_teachers(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_db)
):
    """Get teachers in the HOD's department"""
    service = HODService(db)
    return await service.get_department_teachers(current_user.id)


@router.get("/courses", response_model=CourseListResponse)
async def get_department_courses(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_db)
):
    """Get courses in the HOD's department"""
    service = HODService(db)
    return await service.get_department_courses(current_user.id)


__all__ = ["router"]
