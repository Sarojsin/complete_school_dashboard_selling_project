from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Assignment, AssignmentSubmission
from .repository import AssignmentRepository


class AssignmentService:
    """Service layer for school assignments operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_assignment(self, assignment_data: dict) -> Assignment:
        return await AssignmentRepository.create(self.db, assignment_data)

    async def get_assignment(self, assignment_id: int) -> Optional[Assignment]:
        return await AssignmentRepository.get_by_id(self.db, assignment_id)

    async def update_assignment(self, assignment: Assignment, **kwargs) -> Assignment:
        return await AssignmentRepository.update(self.db, assignment, **kwargs)

    async def delete_assignment(self, assignment: Assignment) -> None:
        await AssignmentRepository.delete(self.db, assignment)

    async def get_teacher_assignments(self, teacher_id: int, skip: int = 0, limit: int = 100) -> List[Assignment]:
        return await AssignmentRepository.get_all(self.db, skip=skip, limit=limit, teacher_id=teacher_id)

    async def get_submissions(self, assignment_id: int) -> List[AssignmentSubmission]:
        return await AssignmentRepository.get_submissions(self.db, assignment_id)

    async def get_submission(self, submission_id: int) -> Optional[AssignmentSubmission]:
        result = await self.db.execute(select(AssignmentSubmission).filter(AssignmentSubmission.id == submission_id))
        return result.scalars().first()

    async def update_submission(self, submission: AssignmentSubmission, **kwargs) -> AssignmentSubmission:
        return await AssignmentRepository.update_submission(self.db, submission, **kwargs)

    async def create_submission(self, submission_data: dict) -> AssignmentSubmission:
        return await AssignmentRepository.create_submission(self.db, submission_data)

    async def get_submission_by_student(self, assignment_id: int, student_id: int) -> Optional[AssignmentSubmission]:
        return await AssignmentRepository.get_submission_by_student(self.db, assignment_id, student_id)

    async def get_student_assignments(self, student_id: int, course_ids: List[int], student_grade: Optional[str] = None, student_section: Optional[str] = None) -> List[dict]:
        return await AssignmentRepository.get_student_assignments(self.db, student_id, course_ids, student_grade, student_section)
