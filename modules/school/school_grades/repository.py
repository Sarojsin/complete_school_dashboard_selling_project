from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from .models import Grade, Assessment


class GradeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, grade_data: dict) -> Grade:
        grade = Grade(**grade_data)
        self.db.add(grade)
        await self.db.commit()
        await self.db.refresh(grade)
        return grade
    
    async def get(self, grade_id: int) -> Optional[Grade]:
        result = await self.db.execute(
            select(Grade).filter(Grade.id == grade_id)
        )
        return result.scalars().first()
    
    async def get_by_student(self, student_id: int) -> List[Grade]:
        result = await self.db.execute(
            select(Grade).filter(Grade.student_id == student_id).order_by(desc(Grade.date))
        )
        return result.scalars().all()
    
    async def get_by_course(self, course_id: int) -> List[Grade]:
        result = await self.db.execute(
            select(Grade).filter(Grade.course_id == course_id).order_by(desc(Grade.date))
        )
        return result.scalars().all()
    
    async def get_all(self, student_id: Optional[int] = None, course_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Grade]:
        query = select(Grade).order_by(desc(Grade.date))
        if student_id:
            query = query.filter(Grade.student_id == student_id)
        if course_id:
            query = query.filter(Grade.course_id == course_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update(self, grade_id: int, grade_data: dict) -> Optional[Grade]:
        grade = await self.get(grade_id)
        if grade:
            for key, value in grade_data.items():
                if value is not None and hasattr(grade, key):
                    setattr(grade, key, value)
            await self.db.commit()
            await self.db.refresh(grade)
        return grade
    
    async def delete(self, grade_id: int) -> bool:
        grade = await self.get(grade_id)
        if grade:
            await self.db.delete(grade)
            await self.db.commit()
            return True
        return False
    
    async def get_top_performers(self, course_id: int, limit: int = 10) -> List[Grade]:
        """Get top performing students in a course by score percentage"""
        # First get all grades for the course
        result = await self.db.execute(
            select(Grade).filter(Grade.course_id == course_id)
        )
        grades = result.scalars().all()
        
        # Calculate percentage and sort
        graded_list = [(g, (g.score / g.max_score * 100) if g.max_score > 0 else 0) for g in grades]
        graded_list.sort(key=lambda x: x[1], reverse=True)
        
        # Return top performers
        return [g[0] for g in graded_list[:limit]]


class AssessmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, assessment_data: dict) -> Assessment:
        assessment = Assessment(**assessment_data)
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment
    
    async def get(self, assessment_id: int) -> Optional[Assessment]:
        result = await self.db.execute(
            select(Assessment).filter(Assessment.id == assessment_id)
        )
        return result.scalars().first()
    
    async def get_by_course(self, course_id: int) -> List[Assessment]:
        result = await self.db.execute(
            select(Assessment).filter(Assessment.course_id == course_id, Assessment.is_active == True)
        )
        return result.scalars().all()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Assessment]:
        result = await self.db.execute(
            select(Assessment).offset(skip).limit(limit)
        )
        return result.scalars().all()