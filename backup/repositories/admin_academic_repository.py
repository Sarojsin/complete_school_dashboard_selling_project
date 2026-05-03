from typing import List, Dict, Optional, Tuple
from sqlalchemy import func, select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backup.models.models import Course, Student, Teacher, Schedule
from backup.models.department_models import Department

class AdminAcademicRepository:
    """Handles all database queries for Admin Academic endpoints."""

    @staticmethod
    async def get_courses_list(
        db: AsyncSession,
        grade_level: Optional[str] = None,
        teacher_id: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Course]:
        query = select(Course).options(selectinload(Course.teacher), selectinload(Course.enrollments))
        
        if grade_level:
            query = query.where(Course.grade_level == grade_level)
        if teacher_id:
            query = query.where(Course.teacher_id == teacher_id)
        if search:
            query = query.where(
                or_(
                    Course.name.ilike(f"%{search}%"),
                    Course.code.ilike(f"%{search}%")
                )
            )
            
        query = query.offset(skip).limit(limit).order_by(Course.name)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_course_by_code(db: AsyncSession, code: str) -> Optional[Course]:
        result = await db.execute(select(Course).where(Course.code == code))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_course_by_id(db: AsyncSession, course_id: int) -> Optional[Course]:
        result = await db.execute(select(Course).where(Course.id == course_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_departments_list(
        db: AsyncSession,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Department]:
        query = select(Department).options(
            selectinload(Department.hod),
            selectinload(Department.teachers),
            selectinload(Department.students)
        )
        
        if search:
            query = query.where(Department.name.ilike(f"%{search}%"))
            
        query = query.offset(skip).limit(limit).order_by(Department.name)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_department_by_code(db: AsyncSession, code: str) -> Optional[Department]:
        result = await db.execute(select(Department).where(Department.code == code))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_department_by_id(db: AsyncSession, dept_id: int) -> Optional[Department]:
        result = await db.execute(select(Department).where(Department.id == dept_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_academic_stats(db: AsyncSession) -> Dict[str, int]:
        total_courses_r   = await db.execute(select(func.count(Course.id)))
        active_courses_r  = await db.execute(select(func.count(Course.id)).where(Course.is_active.is_(True)))
        total_depts_r     = await db.execute(select(func.count(Department.id)))
        hod_depts_r       = await db.execute(
            select(func.count(Department.id)).where(Department.hod_teacher_id.isnot(None))
        )
        total_teachers_r  = await db.execute(select(func.count(Teacher.id)))
        total_students_r  = await db.execute(select(func.count(Student.id)))

        return {
            "total_courses": total_courses_r.scalar() or 0,
            "active_courses": active_courses_r.scalar() or 0,
            "total_departments": total_depts_r.scalar() or 0,
            "hod_departments": hod_depts_r.scalar() or 0,
            "total_teachers": total_teachers_r.scalar() or 0,
            "total_students": total_students_r.scalar() or 0,
        }

    @staticmethod
    async def get_timetable_entries(
        db: AsyncSession,
        course_id: Optional[int] = None,
        day: Optional[str] = None,
    ) -> List[Schedule]:
        query = select(Schedule)
        if course_id is not None:
            query = query.where(Schedule.course_id == course_id)
        if day:
            query = query.where(Schedule.day_of_week == day)
        query = query.order_by(Schedule.day_of_week, Schedule.start_time)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def find_timetable_conflicts(
        db: AsyncSession,
        course_id: int,
        day_of_week: str,
        start_time,
        end_time,
    ) -> List[Schedule]:
        query = select(Schedule).where(
            Schedule.day_of_week == day_of_week,
            Schedule.course_id != course_id,
            Schedule.start_time < end_time,
            Schedule.end_time > start_time,
        )
        result = await db.execute(query)
        return list(result.scalars().all())
