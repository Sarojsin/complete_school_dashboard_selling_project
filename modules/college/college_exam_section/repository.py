"""
College Exam Section Repository

Async CRUD operations for exam results and notices.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from datetime import datetime
from .models import CollegeExamResult, CollegeExamNotice
from .schemas import CollegeExamResultCreate, CollegeExamResultUpdate


class ExamSectionRepository:
    """Repository for exam section database operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Exam Results ────────────────────────────────────────────────

    async def create_result(self, data: CollegeExamResultCreate, published_by: int) -> CollegeExamResult:
        """Create a new exam result (initially unpublished)"""
        # Calculate grade based on marks
        marks = data.marks or 0
        max_marks = data.max_marks if data.max_marks and data.max_marks > 0 else 100
        if marks > max_marks:
            raise ValueError(f"Marks ({marks}) cannot exceed max_marks ({max_marks})")

        percentage = (marks / max_marks) * 100
        if percentage >= 90:
            grade = "A"
        elif percentage >= 80:
            grade = "B"
        elif percentage >= 70:
            grade = "C"
        elif percentage >= 60:
            grade = "D"
        else:
            grade = "F"

        result = CollegeExamResult(
            **data.model_dump(),
            grade=grade,
            published_by=published_by,
            published_at=datetime.utcnow() if data.is_published else None,
            is_published=data.is_published if hasattr(data, 'is_published') else False
        )
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def get_result(self, result_id: int) -> Optional[CollegeExamResult]:
        """Get exam result by ID"""
        result = await self.db.execute(
            select(CollegeExamResult).where(CollegeExamResult.id == result_id)
        )
        return result.scalar_one_or_none()

    async def get_student_results(self, student_id: int) -> List[CollegeExamResult]:
        """Get all results for a student (ordered by semester desc)"""
        result = await self.db.execute(
            select(CollegeExamResult)
            .where(CollegeExamResult.student_id == student_id)
            .order_by(CollegeExamResult.semester_id.desc(), CollegeExamResult.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_course_results(self, course_id: int) -> List[CollegeExamResult]:
        """Get all results for a course"""
        result = await self.db.execute(
            select(CollegeExamResult)
            .where(CollegeExamResult.course_id == course_id)
            .order_by(CollegeExamResult.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_all_results(
        self,
        semester_id: Optional[int] = None,
        exam_type: Optional[str] = None,
        is_published: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CollegeExamResult]:
        """Get all results with filters"""
        query = select(CollegeExamResult)

        if semester_id is not None:
            query = query.where(CollegeExamResult.semester_id == semester_id)
        if exam_type:
            query = query.where(CollegeExamResult.exam_type == exam_type)
        if is_published is not None:
            query = query.where(CollegeExamResult.is_published == is_published)

        query = query.order_by(CollegeExamResult.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_result(self, result_id: int, data: CollegeExamResultUpdate) -> Optional[CollegeExamResult]:
        """Update exam result"""
        result = await self.get_result(result_id)
        if not result:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(result, key, value)

        # If publishing now, set published_at
        if data.is_published and not result.is_published:
            result.published_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def publish_result(self, result_id: int, published_by: int) -> Optional[CollegeExamResult]:
        """Publish a result (makes it visible to students)"""
        result = await self.get_result(result_id)
        if not result:
            return None
        result.is_published = True
        result.published_by = published_by
        result.published_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def unpublish_result(self, result_id: int) -> Optional[CollegeExamResult]:
        """Unpublish a result"""
        result = await self.get_result(result_id)
        if not result:
            return None
        result.is_published = False
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def delete_result(self, result_id: int) -> bool:
        """Delete exam result"""
        result = await self.get_result(result_id)
        if result:
            await self.db.delete(result)
            await self.db.commit()
            return True
        return False

    async def get_stats(self) -> dict:
        """Get exam section statistics"""
        total = await self.db.execute(select(func.count(CollegeExamResult.id)))
        published = await self.db.execute(
            select(func.count(CollegeExamResult.id)).where(CollegeExamResult.is_published == True)
        )
        return {
            "total_results": total.scalar() or 0,
            "published_count": published.scalar() or 0,
            "unpublished_count": (total.scalar() or 0) - (published.scalar() or 0)
        }

    # ── Exam Notices ────────────────────────────────────────────────

    async def create_notice(self, title: str, content: str, notice_type: str, created_by: int,
                           exam_date: Optional[datetime] = None, semester_id: Optional[int] = None) -> CollegeExamNotice:
        """Create exam notice"""
        notice = CollegeExamNotice(
            title=title,
            content=content,
            notice_type=notice_type,
            exam_date=exam_date,
            semester_id=semester_id,
            created_by=created_by
        )
        self.db.add(notice)
        await self.db.commit()
        await self.db.refresh(notice)
        return notice

    async def get_notices(self, is_active: bool = True, semester_id: Optional[int] = None) -> List[CollegeExamNotice]:
        """Get exam notices"""
        query = select(CollegeExamNotice).where(CollegeExamNotice.is_active == is_active)
        if semester_id is not None:
            query = query.where(CollegeExamNotice.semester_id == semester_id)
        query = query.order_by(CollegeExamNotice.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_notice(self, notice_id: int) -> Optional[CollegeExamNotice]:
        """Get notice by ID"""
        result = await self.db.execute(
            select(CollegeExamNotice).where(CollegeExamNotice.id == notice_id)
        )
        return result.scalar_one_or_none()


__all__ = ["ExamSectionRepository"]
