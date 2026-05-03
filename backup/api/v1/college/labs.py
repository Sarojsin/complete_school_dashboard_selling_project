"""
College Labs API
===============
API endpoints for lab management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
from backup.core.database import get_async_college_db as get_async_db
from backup.dependencies.auth import get_current_user
from backup.models.models import User
from backup.models.college import Lab, LabEquipment, LabSchedule

router = APIRouter(prefix="/labs", tags=["Labs"])


# Lab Endpoints
@router.get("/")
async def list_labs(
    department_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all labs"""
    query = select(Lab)
    if department_id:
        query = query.filter(Lab.department_id == department_id)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    labs = res.scalars().all()
    return labs


@router.get("/{lab_id}")
async def get_lab(
    lab_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get lab details"""
    res = await db.execute(select(Lab).filter(Lab.id == lab_id))
    lab = res.scalar_one_or_none()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return lab


@router.post("/")
async def create_lab(
    name: str,
    code: str,
    department_id: int,
    capacity: int = 30,
    location: str = None,
    description: str = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create new lab"""
    lab = Lab(
        name=name,
        code=code,
        department_id=department_id,
        capacity=capacity,
        location=location,
        description=description
    )
    db.add(lab)
    await db.commit()
    await db.refresh(lab)
    return lab


# Equipment Endpoints
@router.get("/{lab_id}/equipment")
async def list_equipment(
    lab_id: int,
    condition: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List lab equipment"""
    query = select(LabEquipment).filter(LabEquipment.lab_id == lab_id)
    if condition:
        query = query.filter(LabEquipment.condition == condition)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    equipment = res.scalars().all()
    return equipment


@router.post("/{lab_id}/equipment")
async def add_equipment(
    lab_id: int,
    name: str,
    serial_number: str = None,
    quantity: int = 1,
    purchase_date: str = None,
    condition: str = "good",
    notes: str = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Add equipment to lab"""
    # Check lab exists
    res = await db.execute(select(Lab).filter(Lab.id == lab_id))
    lab = res.scalar_one_or_none()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    equipment = LabEquipment(
        lab_id=lab_id,
        name=name,
        serial_number=serial_number,
        quantity=quantity,
        purchase_date=datetime.strptime(purchase_date, "%Y-%m-%d").date() if purchase_date else None,
        condition=condition,
        notes=notes
    )
    db.add(equipment)
    
    # Update lab equipment count
    lab.equipment_count += quantity
    
    await db.commit()
    await db.refresh(equipment)
    return equipment


@router.put("/equipment/{equipment_id}")
async def update_equipment(
    equipment_id: int,
    name: str = None,
    serial_number: str = None,
    quantity: int = None,
    condition: str = None,
    notes: str = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Update equipment details"""
    res = await db.execute(select(LabEquipment).filter(LabEquipment.id == equipment_id))
    equipment = res.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    if name is not None:
        equipment.name = name
    if serial_number is not None:
        equipment.serial_number = serial_number
    if quantity is not None:
        equipment.quantity = quantity
    if condition is not None:
        equipment.condition = condition
    if notes is not None:
        equipment.notes = notes
    
    await db.commit()
    await db.refresh(equipment)
    return equipment


# Schedule Endpoints
@router.get("/{lab_id}/schedules")
async def list_schedules(
    lab_id: int,
    day_of_week: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List lab schedules"""
    query = select(LabSchedule).filter(LabSchedule.lab_id == lab_id)
    if day_of_week:
        query = query.filter(LabSchedule.day_of_week == day_of_week)
    query = query.offset(skip).limit(limit)
    res = await db.execute(query)
    schedules = res.scalars().all()
    return schedules


@router.post("/{lab_id}/schedules")
async def create_schedule(
    lab_id: int,
    course_id: int = None,
    faculty_id: int = None,
    day_of_week: str = None,
    start_time: str = None,
    end_time: str = None,
    semester_id: int = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Create lab schedule"""
    # Check lab exists
    res = await db.execute(select(Lab).filter(Lab.id == lab_id))
    lab = res.scalar_one_or_none()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    schedule = LabSchedule(
        lab_id=lab_id,
        course_id=course_id,
        faculty_id=faculty_id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        semester_id=semester_id
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule


__all__ = ["router"]
