from typing import List, Dict, Optional, Tuple, Any
from sqlalchemy import select, func, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta, datetime

from backup.models.models import Grade, Student
from backup.models.exam_models import ExamResult, ExamNotice

class AdminExamRepository:
    """Handles database queries for the Admin Exams endpoints."""

    @staticmethod
    async def get_exam_results(
        db: AsyncSession,
        course_id: Optional[int] = None,
        exam_type: Optional[str] = None,
        is_published: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ExamResult]:
        query = select(ExamResult).options(
            selectinload(ExamResult.student).selectinload(Student.user),
            selectinload(ExamResult.course)
        )
        
        if course_id:
            query = query.where(ExamResult.course_id == course_id)
        if exam_type:
            query = query.where(ExamResult.exam_type == exam_type)
        if is_published is not None:
            query = query.where(ExamResult.is_published == is_published)
            
        query = query.offset(skip).limit(limit).order_by(ExamResult.id.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def set_results_published_status(
        db: AsyncSession,
        course_id: int,
        exam_type: str,
        is_published: bool,
        published_by: Optional[int] = None
    ) -> None:
        values = {"is_published": is_published}
        if is_published:
            values["published_by"] = published_by
            values["published_at"] = datetime.utcnow()
            
        await db.execute(
            update(ExamResult)
            .where(
                ExamResult.course_id == course_id,
                ExamResult.exam_type == exam_type
            )
            .values(**values)
        )

    @staticmethod
    async def get_exam_notices(
        db: AsyncSession,
        notice_type: Optional[str] = None,
        upcoming: bool = False,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ExamNotice]:
        query = select(ExamNotice).options(selectinload(ExamNotice.creator))
        
        if notice_type:
            query = query.where(ExamNotice.notice_type == notice_type)
        if upcoming:
            query = query.where(ExamNotice.exam_date >= date.today())
            
        query = query.offset(skip).limit(limit).order_by(ExamNotice.exam_date.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_exam_stats_raw(db: AsyncSession) -> Dict[str, Any]:
        total_r = await db.execute(select(func.count(ExamResult.id)))
        published_r = await db.execute(select(func.count(ExamResult.id)).where(ExamResult.is_published == True))
        
        by_type = {}
        for exam_type in ["midterm", "final", "quiz", "assignment", "project"]:
            count_r = await db.execute(select(func.count(ExamResult.id)).where(ExamResult.exam_type == exam_type))
            by_type[exam_type] = count_r.scalar() or 0
            
        today = date.today()
        upcoming_r = await db.execute(
            select(func.count(ExamNotice.id)).where(
                ExamNotice.exam_date >= today,
                ExamNotice.exam_date <= today + timedelta(days=30)
            )
        )
        
        avg_r = await db.execute(select(func.avg(ExamResult.marks)))
        
        return {
            "total_results": total_r.scalar() or 0,
            "published_results": published_r.scalar() or 0,
            "by_exam_type": by_type,
            "upcoming_count": upcoming_r.scalar() or 0,
            "average_marks": float(avg_r.scalar() or 0)
        }

    @staticmethod
    async def get_student_for_report(db: AsyncSession, student_id: int) -> Optional[Student]:
        result = await db.execute(select(Student).where(Student.id == student_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_student_grades(db: AsyncSession, student_id: int, semester: Optional[str] = None) -> List[Grade]:
        query = select(Grade).options(selectinload(Grade.course)).where(Grade.student_id == student_id)
        if semester:
            query = query.where(Grade.grade_type == semester)
        result = await db.execute(query)
        return list(result.scalars().all())
