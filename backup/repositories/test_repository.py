from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from datetime import datetime
from backup.models.test_models import Test, TestQuestion, TestSubmission

class TestRepository:
    @staticmethod
    async def create(db: AsyncSession, test_data: Dict[str, Any], questions_data: List[Dict[str, Any]]) -> Test:
        # Calculate total points
        total_points = sum(q.get('points', 1.0) for q in questions_data)
        test_data['total_points'] = total_points
        
        test = Test(**test_data)
        db.add(test)
        await db.flush()  # Get ID
        
        for q_data in questions_data:
            question = TestQuestion(**q_data, test_id=test.id)
            db.add(question)
            
        await db.commit()
        await db.refresh(test)
        return test

    @staticmethod
    async def get_all(db: AsyncSession, teacher_id: Optional[int] = None) -> List[Test]:
        query = select(Test).options(selectinload(Test.questions))
        if teacher_id:
            query = query.filter(Test.teacher_id == teacher_id)
        result = await db.execute(query.order_by(desc(Test.created_at)))
        return result.scalars().unique().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, test_id: int) -> Optional[Test]:
        result = await db.execute(
            select(Test).options(selectinload(Test.questions)).filter(Test.id == test_id)
        )
        return result.scalars().first()

    @staticmethod
    async def update(db: AsyncSession, test: Test, **kwargs) -> Test:
        for key, value in kwargs.items():
            if hasattr(test, key):
                setattr(test, key, value)
        await db.commit()
        await db.refresh(test)
        return test

    @staticmethod
    async def delete(db: AsyncSession, test: Test):
        await db.delete(test)
        await db.commit()

    @staticmethod
    async def get_available_tests_for_student(db: AsyncSession, student_id: int, section: Optional[str] = None, grade_level: Optional[str] = None) -> List[Test]:
        now = datetime.now()
        # Base query: active tests within time window
        query = select(Test).options(selectinload(Test.questions)).filter(
            Test.is_active == True,
            Test.start_time <= now,
            Test.end_time >= now
        )
        
        # Filter by Grade/Section targeting as requested (e.g., "9A")
        if grade_level and section:
            # Show tests matching this grade AND (this section OR "All")
            query = query.filter(
                Test.grade_level == grade_level,
                or_(
                    Test.target_section == section,
                    Test.target_section == "All",
                    Test.target_section.is_(None)
                )
            )
            
        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def get_submission(db: AsyncSession, test_id: int, student_id: int) -> Optional[TestSubmission]:
        result = await db.execute(
            select(TestSubmission).filter(
                TestSubmission.test_id == test_id,
                TestSubmission.student_id == student_id
            )
        )
        return result.scalars().first()

    @staticmethod
    async def update_submission(db: AsyncSession, submission: TestSubmission, **kwargs) -> TestSubmission:
        for key, value in kwargs.items():
            if hasattr(submission, key):
                setattr(submission, key, value)
        await db.commit()
        await db.refresh(submission)
        return submission

    @staticmethod
    async def get_student_results(db: AsyncSession, student_id: int) -> List[TestSubmission]:
        result = await db.execute(
            select(TestSubmission).filter(
                TestSubmission.student_id == student_id,
                TestSubmission.submitted_at.isnot(None)
            ).order_by(desc(TestSubmission.submitted_at))
        )
        return result.scalars().all()

    @staticmethod
    async def get_test_results(db: AsyncSession, test_id: int) -> List[TestSubmission]:
        result = await db.execute(
            select(TestSubmission).filter(
                TestSubmission.test_id == test_id,
                TestSubmission.submitted_at.isnot(None)
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_teacher(db: AsyncSession, teacher_id: int) -> List[Test]:
        result = await db.execute(
            select(Test).filter(Test.teacher_id == teacher_id).order_by(desc(Test.created_at))
        )
        return result.scalars().unique().all()
