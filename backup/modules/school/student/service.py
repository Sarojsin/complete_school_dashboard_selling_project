# School Student Service
# ====================

from typing import Optional, List

from backup.modules.school.student.repository import StudentRepository
from backup.modules.school.student.schemas import StudentCreate, StudentUpdate, Student


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def create(self, data: StudentCreate) -> Student:
        return await self.repository.create(data)

    async def get(self, student_id: int) -> Optional[Student]:
        return await self.repository.get(student_id)

    async def get_by_user_id(self, user_id: int) -> Optional[Student]:
        return await self.repository.get_by_user_id(user_id)

    async def get_all(
        self,
        grade_level: Optional[str] = None,
        section: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Student]:
        return await self.repository.get_all(grade_level, section, skip, limit)

    async def update(self, student_id: int, data: StudentUpdate) -> Optional[Student]:
        return await self.repository.update(student_id, data)

    async def delete(self, student_id: int) -> bool:
        return await self.repository.delete(student_id)


__all__ = ["StudentService"]
