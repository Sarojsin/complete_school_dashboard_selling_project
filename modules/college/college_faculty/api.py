"""
College Faculty API Routes

API endpoints for managing college faculty members.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from modules.shared.database import get_db
from modules.shared.models import User
from backup.models.college.faculty import Faculty
from modules.auth.dependencies import get_current_user, require_college_portal

router = APIRouter(prefix="/faculty", tags=["College Faculty"], dependencies=[Depends(require_college_portal)])


@router.get("/dashboard")
async def get_faculty_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get faculty dashboard with overview stats"""
    total_faculty = await db.execute(select(func.count(Faculty.id)))
    
    return {
        "total_faculty": total_faculty.scalar() or 0
    }


@router.get("/list")
async def list_faculty(
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all faculty members"""
    query = select(Faculty)
    
    if department_id:
        query = query.where(Faculty.department_id == department_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    faculty = result.scalars().all()
    
    return {"faculty": [
        {
            "id": f.id,
            "user_id": f.user_id,
            "employee_id": f.employee_id,
            "department_id": f.department_id,
            "designation": f.designation,
            "specialization": f.specialization,
            "qualification": f.qualification
        }
        for f in faculty
    ]}


@router.get("/{faculty_id}")
async def get_faculty(
    faculty_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get faculty details by ID"""
    result = await db.execute(select(Faculty).where(Faculty.id == faculty_id))
    faculty = result.scalar_one_or_none()
    
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    return {
        "id": faculty.id,
        "user_id": faculty.user_id,
        "employee_id": faculty.employee_id,
        "department_id": faculty.department_id,
        "designation": faculty.designation,
        "specialization": faculty.specialization,
        "qualification": faculty.qualification,
        "experience_years": faculty.experience_years,
        "joining_date": str(faculty.joining_date) if faculty.joining_date else None
    }


@router.post("/")
async def create_faculty(
    user_id: int,
    employee_id: str,
    department_id: int,
    designation: str,
    specialization: Optional[str] = None,
    qualification: Optional[str] = None,
    experience_years: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new faculty member"""
    faculty = Faculty(
        user_id=user_id,
        employee_id=employee_id,
        department_id=department_id,
        designation=designation,
        specialization=specialization,
        qualification=qualification,
        experience_years=experience_years
    )
    db.add(faculty)
    await db.commit()
    await db.refresh(faculty)
    
    return {"faculty": faculty, "message": "Faculty created successfully"}


__all__ = ["router"]
