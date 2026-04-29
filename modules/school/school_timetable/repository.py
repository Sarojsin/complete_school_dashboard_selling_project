from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_, and_, func
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import time

from modules.school.school_timetable.models import TimetableEntry, Period, DayOfWeek


class TimetableRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, entry_id: int) -> Optional[TimetableEntry]:
        result = await db.execute(
            select(TimetableEntry).options(
                joinedload(TimetableEntry.course),
                joinedload(TimetableEntry.teacher)
            ).filter(TimetableEntry.id == entry_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        course_id: int = None,
        class_id: int = None,
        day_of_week: str = None,
        academic_year: str = None
    ) -> List[TimetableEntry]:
        query = select(TimetableEntry).options(
            joinedload(TimetableEntry.course),
            joinedload(TimetableEntry.teacher)
        )

        if course_id:
            query = query.filter(TimetableEntry.course_id == course_id)

        if class_id:
            query = query.filter(TimetableEntry.class_id == class_id)

        if day_of_week:
            try:
                day = DayOfWeek(day_of_week.lower())
                query = query.filter(TimetableEntry.day_of_week == day)
            except ValueError:
                pass

        if academic_year:
            query = query.filter(TimetableEntry.academic_year == academic_year)

        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().unique().all()

    @staticmethod
    async def create(db: AsyncSession, entry_data: dict) -> TimetableEntry:
        # Convert day_of_week to enum if needed
        if 'day_of_week' in entry_data and isinstance(entry_data['day_of_week'], str):
            entry_data['day_of_week'] = DayOfWeek(entry_data['day_of_week'].lower())

        entry = TimetableEntry(**entry_data)
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry

    @staticmethod
    async def update(db: AsyncSession, entry: TimetableEntry, **kwargs) -> TimetableEntry:
        for key, value in kwargs.items():
            if value is not None and hasattr(entry, key):
                if key == 'day_of_week' and isinstance(value, str):
                    value = DayOfWeek(value.lower())
                setattr(entry, key, value)
        await db.commit()
        await db.refresh(entry)
        return entry

    @staticmethod
    async def delete(db: AsyncSession, entry: TimetableEntry):
        await db.delete(entry)
        await db.commit()

    @staticmethod
    async def check_conflicts(
        db: AsyncSession,
        day_of_week: str,
        start_time: str,
        end_time: str,
        class_id: int = None,
        course_id: int = None,
        exclude_entry_id: int = None
    ) -> List[TimetableEntry]:
        """Check for scheduling conflicts"""
        try:
            day = DayOfWeek(day_of_week.lower())
        except ValueError:
            return []

        # Parse times
        start = time.fromisoformat(start_time)
        end = time.fromisoformat(end_time)

        query = select(TimetableEntry).filter(
            TimetableEntry.day_of_week == day,
            TimetableEntry.is_active == 1,
            or_(
                and_(
                    TimetableEntry.start_time <= start,
                    TimetableEntry.end_time > start
                ),
                and_(
                    TimetableEntry.start_time < end,
                    TimetableEntry.end_time >= end
                ),
                and_(
                    TimetableEntry.start_time >= start,
                    TimetableEntry.end_time <= end
                )
            )
        )

        if class_id:
            query = query.filter(TimetableEntry.class_id == class_id)

        if course_id:
            query = query.filter(TimetableEntry.course_id == course_id)

        if exclude_entry_id:
            query = query.filter(TimetableEntry.id != exclude_entry_id)

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_teacher(
        db: AsyncSession,
        teacher_id: int,
        day_of_week: str = None,
        academic_year: str = None
    ) -> List[TimetableEntry]:
        query = select(TimetableEntry).filter(
            TimetableEntry.teacher_id == teacher_id,
            TimetableEntry.is_active == 1
        )

        if day_of_week:
            try:
                day = DayOfWeek(day_of_week.lower())
                query = query.filter(TimetableEntry.day_of_week == day)
            except ValueError:
                pass

        if academic_year:
            query = query.filter(TimetableEntry.academic_year == academic_year)

        result = await db.execute(query.order_by(TimetableEntry.start_time))
        return result.scalars().all()

    @staticmethod
    async def get_by_class(
        db: AsyncSession,
        class_id: int,
        day_of_week: str = None,
        academic_year: str = None
    ) -> List[TimetableEntry]:
        query = select(TimetableEntry).filter(
            TimetableEntry.class_id == class_id,
            TimetableEntry.is_active == 1
        )

        if day_of_week:
            try:
                day = DayOfWeek(day_of_week.lower())
                query = query.filter(TimetableEntry.day_of_week == day)
            except ValueError:
                pass

        if academic_year:
            query = query.filter(TimetableEntry.academic_year == academic_year)

        result = await db.execute(query.order_by(TimetableEntry.start_time))
        return result.scalars().all()


class PeriodRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, period_id: int) -> Optional[Period]:
        result = await db.execute(
            select(Period).filter(Period.id == period_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        class_id: int = None,
        academic_year: str = None
    ) -> List[Period]:
        query = select(Period)

        if class_id:
            query = query.filter(Period.class_id == class_id)

        if academic_year:
            query = query.filter(Period.academic_year == academic_year)

        result = await db.execute(query.order_by(Period.period_number).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, period_data: dict) -> Period:
        period = Period(**period_data)
        db.add(period)
        await db.commit()
        await db.refresh(period)
        return period

    @staticmethod
    async def update(db: AsyncSession, period: Period, **kwargs) -> Period:
        for key, value in kwargs.items():
            if value is not None and hasattr(period, key):
                setattr(period, key, value)
        await db.commit()
        await db.refresh(period)
        return period

    @staticmethod
    async def delete(db: AsyncSession, period: Period):
        await db.delete(period)
        await db.commit()

    @staticmethod
    async def get_by_class_ordered(
        db: AsyncSession,
        class_id: int,
        academic_year: str = None
    ) -> List[Period]:
        query = select(Period).filter(Period.class_id == class_id)

        if academic_year:
            query = query.filter(Period.academic_year == academic_year)

        result = await db.execute(query.order_by(Period.period_number))
        return result.scalars().all()