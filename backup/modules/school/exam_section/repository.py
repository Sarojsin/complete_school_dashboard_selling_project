# School Exam Section Repository
# ===========================

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from backup.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time


class SchoolExamSchedule(Base):
    __tablename__ = "school_exam_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("school_classes.id"), nullable=False)
    subject = Column(String(200), nullable=False)
    exam_date = Column(Date, nullable=False)
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)
    total_marks = Column(Integer, default=100)
    passing_marks = Column(Integer, default=35)


class SchoolGrade(Base):
    __tablename__ = "school_grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("school_exam_schedules.id"), nullable=False)
    marks = Column(Integer, nullable=False)
    grade = Column(String(5), nullable=False)
    remarks = Column(String(500))


from backup.modules.school.exam_section.schemas import (
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
        result = await self.db.execute(select(SchoolExamSchedule).where(SchoolExamSchedule.id == exam_id))
        return result.scalar_one_or_none()

    async def get_exams_by_class(self, class_id: int) -> List[SchoolExamSchedule]:
        result = await self.db.execute(select(SchoolExamSchedule).where(SchoolExamSchedule.class_id == class_id))
        return list(result.scalars().all())

    async def get_all_exams(self, skip: int = 0, limit: int = 100) -> List[SchoolExamSchedule]:
        result = await self.db.execute(select(SchoolExamSchedule).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_exam(self, exam_id: int, data: ExamScheduleUpdate) -> Optional[SchoolExamSchedule]:
        await self.db.execute(
            select(SchoolExamSchedule).where(SchoolExamSchedule.id == exam_id).values(**data.model_dump(exclude_unset=True))
        )
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
    async def create_grade(self, data: GradeCreate) -> SchoolGrade:
        grade = SchoolGrade(**data.model_dump())
        self.db.add(grade)
        await self.db.commit()
        await self.db.refresh(grade)
        return grade

    async def get_grade(self, grade_id: int) -> Optional[SchoolGrade]:
        result = await self.db.execute(select(SchoolGrade).where(SchoolGrade.id == grade_id))
        return result.scalar_one_or_none()

    async def get_grades_by_student(self, student_id: int) -> List[SchoolGrade]:
        result = await self.db.execute(select(SchoolGrade).where(SchoolGrade.student_id == student_id))
        return list(result.scalars().all())

    async def get_grades_by_exam(self, exam_id: int) -> List[SchoolGrade]:
        result = await self.db.execute(select(SchoolGrade).where(SchoolGrade.exam_id == exam_id))
        return list(result.scalars().all())

    async def get_all_grades(self, skip: int = 0, limit: int = 100) -> List[SchoolGrade]:
        result = await self.db.execute(select(SchoolGrade).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_grade(self, grade_id: int, data: GradeUpdate) -> Optional[SchoolGrade]:
        await self.db.execute(
            select(SchoolGrade).where(SchoolGrade.id == grade_id).values(**data.model_dump(exclude_unset=True))
        )
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
