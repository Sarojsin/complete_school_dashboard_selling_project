# School Exam Section Repository
# ===========================

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from .models import SchoolExamSchedule, ExamGrade
from .schemas import (
    ExamScheduleCreate,
    ExamScheduleUpdate,
    GradeCreate,
    GradeUpdate,
)


class ExamSectionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Exam Schedule methods
    async def create_exam(self, data: ExamScheduleCreate) -> SchoolExamSchedule:
        exam = SchoolExamSchedule(**data.model_dump())
        self.db.add(exam)
        await self.db.commit()
        await self.db.refresh(exam)
        return exam

    async def get_exam(self, exam_id: int) -> Optional[SchoolExamSchedule]:
        result = await self.db.execute(
            select(SchoolExamSchedule).where(SchoolExamSchedule.id == exam_id)
        )
        return result.scalar_one_or_none()

    async def get_exams_by_class(self, class_id: int) -> List[SchoolExamSchedule]:
        result = await self.db.execute(
            select(SchoolExamSchedule).where(SchoolExamSchedule.class_id == class_id)
        )
        return list(result.scalars().all())

    async def get_all_exams(self, skip: int = 0, limit: int = 100) -> List[SchoolExamSchedule]:
        result = await self.db.execute(
            select(SchoolExamSchedule).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update_exam(self, exam_id: int, data: ExamScheduleUpdate) -> Optional[SchoolExamSchedule]:
        from sqlalchemy import update
        stmt = update(SchoolExamSchedule).where(SchoolExamSchedule.id == exam_id).values(**data.model_dump(exclude_unset=True))
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_exam(exam_id)

    async def delete_exam(self, exam_id: int) -> bool:
        exam = await self.get_exam(exam_id)
        if exam:
            await self.db.delete(exam)
            await self.db.commit()
            return True
        return False

    # Grade methods
    async def create_grade(self, data: GradeCreate) -> ExamGrade:
        grade = ExamGrade(**data.model_dump())
        self.db.add(grade)
        await self.db.commit()
        await self.db.refresh(grade)
        return grade

    async def get_grade(self, grade_id: int) -> Optional[ExamGrade]:
        result = await self.db.execute(
            select(ExamGrade).where(ExamGrade.id == grade_id)
        )
        return result.scalar_one_or_none()

    async def get_grades_by_student(self, student_id: int) -> List[ExamGrade]:
        result = await self.db.execute(
            select(ExamGrade).where(ExamGrade.student_id == student_id)
        )
        return list(result.scalars().all())

    async def get_grades_by_exam(self, exam_id: int) -> List[ExamGrade]:
        result = await self.db.execute(
            select(ExamGrade).where(ExamGrade.exam_id == exam_id)
        )
        return list(result.scalars().all())

    async def get_all_grades(self, skip: int = 0, limit: int = 100) -> List[ExamGrade]:
        result = await self.db.execute(
            select(ExamGrade).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update_grade(self, grade_id: int, data: GradeUpdate) -> Optional[ExamGrade]:
        from sqlalchemy import update
        stmt = update(ExamGrade).where(ExamGrade.id == grade_id).values(**data.model_dump(exclude_unset=True))
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_grade(grade_id)

    async def delete_grade(self, grade_id: int) -> bool:
        grade = await self.get_grade(grade_id)
        if grade:
            await self.db.delete(grade)
            await self.db.commit()
            return True
        return False


__all__ = ["ExamSectionRepository"]