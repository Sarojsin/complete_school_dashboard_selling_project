# College Exam Section Repository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from backup.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date


class ExamSchedule(Base):
    __tablename__ = "exam_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    exam_type = Column(String(50))
    exam_date = Column(Date)
    start_time = Column(String(20))
    end_time = Column(String(20))
    room = Column(String(50))


from backup.modules.college.exam_section.schemas import ExamScheduleCreate, ExamScheduleUpdate


class ExamScheduleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: ExamScheduleCreate) -> ExamSchedule:
        exam = ExamSchedule(**data.model_dump())
        self.db.add(exam)
        await self.db.commit()
        await self.db.refresh(exam)
        return exam

    async def get(self, exam_id: int) -> Optional[ExamSchedule]:
        result = await self.db.execute(select(ExamSchedule).where(ExamSchedule.id == exam_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ExamSchedule]:
        result = await self.db.execute(select(ExamSchedule).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update(self, exam_id: int, data: ExamScheduleUpdate) -> Optional[ExamSchedule]:
        await self.db.execute(
            select(ExamSchedule).where(ExamSchedule.id == exam_id).values(**data.model_dump(exclude_unset=True))
        )
        await self.db.commit()
        return await self.get(exam_id)

    async def delete(self, exam_id: int) -> bool:
        exam = await self.get(exam_id)
        if exam:
            await self.db.delete(exam)
            await self.db.commit()
            return True
        return False


__all__ = ["ExamSchedule", "ExamScheduleRepository"]
