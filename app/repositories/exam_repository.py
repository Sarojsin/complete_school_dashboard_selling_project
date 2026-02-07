from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from app.models.models import Student, Course, User
from app.models.exam_models import ExamResult
from app.schemas.exam_schemas import ExamResultCreate
from datetime import datetime

class ExamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_result(self, result_data: ExamResultCreate, user_id: int) -> ExamResult:
        # Calculate grade based on marks
        marks = result_data.marks
        if marks >= 90:
            grade = "A"
        elif marks >= 80:
            grade = "B"
        elif marks >= 70:
            grade = "C"
        elif marks >= 60:
            grade = "D"
        else:
            grade = "F"
        
        db_result = ExamResult(
            **result_data.dict(),
            grade=grade,
            published_by=user_id,
            published_at=datetime.utcnow()
        )
        
        self.session.add(db_result)
        await self.session.commit()
        await self.session.refresh(db_result)
        return db_result
    
    async def get_student_results(self, student_id: int) -> List[ExamResult]:
        result = await self.session.execute(
            select(ExamResult)
            .where(ExamResult.student_id == student_id)
            .order_by(ExamResult.semester.desc())
        )
        return result.scalars().all()
    
    async def get_all_results(self) -> List[ExamResult]:
        result = await self.session.execute(
            select(ExamResult)
            .join(Student, ExamResult.student_id == Student.id)
            .join(Course, ExamResult.course_id == Course.id)
            .order_by(ExamResult.published_at.desc())
        )
        return result.scalars().all()
