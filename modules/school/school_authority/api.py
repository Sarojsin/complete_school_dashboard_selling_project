"""
School Authority API Routes

API routes for school authority/administration management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_db, get_async_db, get_db, get_sync_db
from modules.shared.auth import get_current_user
from modules.shared.models import User

router = APIRouter(prefix="/authority", tags=["School Authority"])


@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get authority dashboard data"""
    return {"message": "Authority dashboard - migrate from app/api/endpoints/authority.py"}


@router.get("/students")
async def list_students(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all students (authority view)"""
    return {"message": "List students - migrate from app/api/endpoints/authority.py"}


@router.get("/teachers")
async def list_teachers(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all teachers (authority view)"""
    return {"message": "List teachers - migrate from app/api/endpoints/authority.py"}
