"""
College Department API Endpoints
================================

Department endpoints for college mode.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from backup.core.database import get_async_college_db as get_async_db
from backup.models.models import User
from backup.models.college import Department
from backup.dependencies.auth import get_current_user

router = APIRouter(prefix="/departments", tags=["College Departments"])


@router.get("")
async def get_departments(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get all departments in the college"""
    query = select(Department)
    
    if search:
        query = query.where(Department.name.ilike(f"%{search}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    departments = result.scalars().all()
    
    return {
        "departments": [
            {
                "id": dept.id,
                "name": dept.name,
                "code": dept.code,
                "description": dept.description,
                "hod_teacher_id": dept.hod_teacher_id
            }
            for dept in departments
        ]
    }


@router.get("/{department_id}")
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get department by ID"""
    result = await db.execute(
        select(Department).where(Department.id == department_id)
    )
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return {
        "id": department.id,
        "name": department.name,
        "code": department.code,
        "description": department.description,
        "hod_teacher_id": department.hod_teacher_id
    }


@router.post("")
async def create_department(
    name: str,
    code: str,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new department"""
    # Check if code already exists
    result = await db.execute(
        select(Department).where(Department.code == code)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Department code already exists")
    
    department = Department(
        name=name,
        code=code,
        description=description
    )
    
    db.add(department)
    await db.commit()
    await db.refresh(department)
    
    return {
        "id": department.id,
        "name": department.name,
        "code": department.code,
        "message": "Department created successfully"
    }


@router.patch("/{department_id}")
async def update_department(
    department_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Update a department"""
    result = await db.execute(
        select(Department).where(Department.id == department_id)
    )
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    if name:
        department.name = name
    if description:
        department.description = description
    
    await db.commit()
    await db.refresh(department)
    
    return {
        "id": department.id,
        "name": department.name,
        "code": department.code,
        "message": "Department updated successfully"
    }


@router.delete("/{department_id}")
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a department"""
    result = await db.execute(
        select(Department).where(Department.id == department_id)
    )
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    await db.delete(department)
    await db.commit()
    
    return {"message": "Department deleted successfully"}
