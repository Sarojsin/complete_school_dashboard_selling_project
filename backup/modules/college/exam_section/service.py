# College Exam Section Service

from typing import Optional, List

from backup.modules.college.exam_section.repository import ExamScheduleRepository
from backup.modules.college.exam_section.schemas import ExamScheduleCreate, ExamScheduleUpdate, ExamSchedule


class ExamScheduleService:
    def __init__(self, repository: ExamScheduleRepository):
        self.repository = repository

    async def create(self, data: ExamScheduleCreate) -> ExamSchedule:
        return await self.repository.create(data)

    async def get(self, exam_id: int) -> Optional[ExamSchedule]:
        return await self.repository.get(exam_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ExamSchedule]:
        return await self.repository.get_all(skip, limit)

    async def update(self, exam_id: int, data: ExamScheduleUpdate) -> Optional[ExamSchedule]:
        return await self.repository.update(exam_id, data)

    async def delete(self, exam_id: int) -> bool:
        return await self.repository.delete(exam_id)


__all__ = ["ExamScheduleService"]
