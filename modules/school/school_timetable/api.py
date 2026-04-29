from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal
from modules.shared.models import User

# Import from backup for now
from modules.auth.dependencies import require_school_authority

from .repository import TimetableRepository, PeriodRepository
from .schemas import (
    TimetableEntryCreate,
    TimetableEntryUpdate,
    TimetableEntryResponse,
    PeriodCreate,
    PeriodUpdate,
    PeriodResponse,
    TimetableConflictCheck,
    TimetableResponse
)

router = APIRouter(dependencies=[Depends(require_school_portal)])


# ==================== Timetable Entry Endpoints ====================

@router.get("/entries", response_model=List[TimetableEntryResponse])
async def get_all_timetable_entries(
    skip: int = 0,
    limit: int = 100,
    course_id: int = None,
    class_id: int = None,
    day_of_week: str = None,
    academic_year: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all timetable entries"""
    entries = await TimetableRepository.get_all(
        db, skip=skip, limit=limit,
        course_id=course_id, class_id=class_id,
        day_of_week=day_of_week, academic_year=academic_year
    )
    return entries


@router.get("/entries/{entry_id}", response_model=TimetableEntryResponse)
async def get_timetable_entry(
    entry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get timetable entry by ID"""
    entry = await TimetableRepository.get_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Timetable entry not found")
    return entry


@router.post("/entries", response_model=TimetableEntryResponse)
async def create_timetable_entry(
    entry: TimetableEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_school_authority)
):
    """Create new timetable entry (Authority only)"""
    # Check for conflicts
    conflicts = await TimetableRepository.check_conflicts(
        db,
        day_of_week=entry.day_of_week,
        start_time=entry.start_time,
        end_time=entry.end_time,
        class_id=entry.class_id,
        course_id=entry.course_id
    )
    if conflicts:
        raise HTTPException(
            status_code=400,
            detail="Schedule conflict detected with existing entries"
        )

    created_entry = await TimetableRepository.create(db, entry.model_dump())
    return created_entry


@router.put("/entries/{entry_id}", response_model=TimetableEntryResponse)
async def update_timetable_entry(
    entry_id: int,
    entry_update: TimetableEntryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_school_authority)
):
    """Update timetable entry (Authority only)"""
    entry = await TimetableRepository.get_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Timetable entry not found")

    # Check for conflicts if times are being changed
    update_data = entry_update.model_dump(exclude_unset=True)
    if 'day_of_week' in update_data or 'start_time' in update_data or 'end_time' in update_data:
        day = update_data.get('day_of_week', entry.day_of_week)
        start = update_data.get('start_time', str(entry.start_time))
        end = update_data.get('end_time', str(entry.end_time))

        conflicts = await TimetableRepository.check_conflicts(
            db,
            day_of_week=day,
            start_time=start,
            end_time=end,
            class_id=entry.class_id,
            course_id=entry.course_id,
            exclude_entry_id=entry_id
        )
        if conflicts:
            raise HTTPException(
                status_code=400,
                detail="Schedule conflict detected with existing entries"
            )

    updated_entry = await TimetableRepository.update(db, entry, **update_data)
    return updated_entry


@router.delete("/entries/{entry_id}")
async def delete_timetable_entry(
    entry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_school_authority)
):
    """Delete timetable entry (Authority only)"""
    entry = await TimetableRepository.get_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Timetable entry not found")

    await TimetableRepository.delete(db, entry)
    return {"message": "Timetable entry deleted successfully"}


@router.post("/entries/check-conflicts")
async def check_timetable_conflicts(
    conflict_check: TimetableConflictCheck,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_school_authority)
):
    """Check for scheduling conflicts"""
    conflicts = await TimetableRepository.check_conflicts(
        db,
        day_of_week=conflict_check.day_of_week,
        start_time=conflict_check.start_time,
        end_time=conflict_check.end_time,
        class_id=None,
        course_id=conflict_check.course_id,
        exclude_entry_id=conflict_check.exclude_entry_id
    )
    return {
        "has_conflicts": len(conflicts) > 0,
        "conflicts": conflicts
    }


# ==================== Teacher Timetable Endpoints ====================

@router.get("/teacher/me", response_model=List[TimetableEntryResponse])
async def get_my_timetable(
    day_of_week: str = None,
    academic_year: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's (teacher) timetable"""
    # Get teacher_id from user - need to check how to get it
    # For now, return empty list
    return []


@router.get("/teacher/{teacher_id}", response_model=List[TimetableEntryResponse])
async def get_teacher_timetable(
    teacher_id: int,
    day_of_week: str = None,
    academic_year: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get timetable for a specific teacher"""
    entries = await TimetableRepository.get_by_teacher(
        db, teacher_id, day_of_week=day_of_week, academic_year=academic_year
    )
    return entries


# ==================== Class Timetable Endpoints ====================

@router.get("/class/{class_id}", response_model=List[TimetableEntryResponse])
async def get_class_timetable(
    class_id: int,
    day_of_week: str = None,
    academic_year: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get timetable for a specific class"""
    entries = await TimetableRepository.get_by_class(
        db, class_id, day_of_week=day_of_week, academic_year=academic_year
    )
    return entries


# ==================== Period Endpoints ====================

@router.get("/periods", response_model=List[PeriodResponse])
async def get_all_periods(
    skip: int = 0,
    limit: int = 100,
    class_id: int = None,
    academic_year: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all periods"""
    periods = await PeriodRepository.get_all(
        db, skip=skip, limit=limit, class_id=class_id, academic_year=academic_year
    )
    return periods


@router.get("/periods/{period_id}", response_model=PeriodResponse)
async def get_period(
    period_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get period by ID"""
    period = await PeriodRepository.get_by_id(db, period_id)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    return period


@router.post("/periods", response_model=PeriodResponse)
async def create_period(
    period: PeriodCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_school_authority)
):
    """Create new period (Authority only)"""
    created_period = await PeriodRepository.create(db, period.model_dump())
    return created_period


@router.put("/periods/{period_id}", response_model=PeriodResponse)
async def update_period(
    period_id: int,
    period_update: PeriodUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_school_authority)
):
    """Update period (Authority only)"""
    period = await PeriodRepository.get_by_id(db, period_id)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")

    updated_period = await PeriodRepository.update(
        db, period, **period_update.model_dump(exclude_unset=True)
    )
    return updated_period


@router.delete("/periods/{period_id}")
async def delete_period(
    period_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_school_authority)
):
    """Delete period (Authority only)"""
    period = await PeriodRepository.get_by_id(db, period_id)
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")

    await PeriodRepository.delete(db, period)
    return {"message": "Period deleted successfully"}


@router.get("/class/{class_id}/periods", response_model=List[PeriodResponse])
async def get_class_periods(
    class_id: int,
    academic_year: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get periods for a specific class (ordered by period number)"""
    periods = await PeriodRepository.get_by_class_ordered(db, class_id, academic_year)
    return periods