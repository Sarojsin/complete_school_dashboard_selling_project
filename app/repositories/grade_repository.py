from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, desc, and_
from sqlalchemy.orm import joinedload
from typing import List, Optional, Dict
from app.models.models import Grade, Student

class GradeRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, grade_id: int) -> Optional[Grade]:
        result = await db.execute(select(Grade).filter(Grade.id == grade_id))
        return result.scalars().first()
    
    @staticmethod
    async def create(db: AsyncSession, grade_data: dict) -> Grade:
        grade = Grade(**grade_data)
        db.add(grade)
        await db.commit()
        await db.refresh(grade)
        return grade
    
    @staticmethod
    async def create_bulk(db: AsyncSession, grades_list: List[dict]) -> List[Grade]:
        """Create multiple grades at once"""
        grades = [Grade(**data) for data in grades_list]
        db.add_all(grades)
        await db.commit()
        for grade in grades:
            await db.refresh(grade)
        return grades
    
    @staticmethod
    async def update(db: AsyncSession, grade: Grade, **kwargs) -> Grade:
        for key, value in kwargs.items():
            if value is not None and hasattr(grade, key):
                setattr(grade, key, value)
        await db.commit()
        await db.refresh(grade)
        return grade
    
    @staticmethod
    async def delete(db: AsyncSession, grade: Grade):
        await db.delete(grade)
        await db.commit()
    
    @staticmethod
    async def get_student_grades(db: AsyncSession, student_id: int, 
                          course_id: int = None) -> List[Grade]:
        query = select(Grade).options(
            joinedload(Grade.course)
        ).filter(Grade.student_id == student_id)
        
        if course_id:
            query = query.filter(Grade.course_id == course_id)
        
        result = await db.execute(query.order_by(desc(Grade.date)))
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_course_grades(db: AsyncSession, course_id: int, 
                         grade_type: str = None) -> List[Grade]:
        query = select(Grade).options(
            joinedload(Grade.student)
        ).filter(Grade.course_id == course_id)
        
        if grade_type:
            query = query.filter(Grade.grade_type == grade_type)
        
        result = await db.execute(query.order_by(desc(Grade.date)))
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_grade_statistics(db: AsyncSession, student_id: int, 
                           course_id: int = None) -> Dict:
        """Calculate grade statistics for a student"""
        query = select(
            func.avg(Grade.score / Grade.max_score * 100).label('average'),
            func.max(Grade.score / Grade.max_score * 100).label('highest'),
            func.min(Grade.score / Grade.max_score * 100).label('lowest'),
            func.count(Grade.id).label('total_grades')
        ).filter(Grade.student_id == student_id)
        
        if course_id:
            query = query.filter(Grade.course_id == course_id)
        
        result = await db.execute(query)
        stats = result.first()
        
        return {
            'average': round(stats.average, 2) if stats.average else 0,
            'highest': round(stats.highest, 2) if stats.highest else 0,
            'lowest': round(stats.lowest, 2) if stats.lowest else 0,
            'total_grades': stats.total_grades or 0
        }
    
    @staticmethod
    async def get_class_statistics(db: AsyncSession, course_id: int, 
                           grade_type: str = None) -> Dict:
        """Calculate grade statistics for entire class"""
        query = select(
            func.avg(Grade.score / Grade.max_score * 100).label('average'),
            func.max(Grade.score / Grade.max_score * 100).label('highest'),
            func.min(Grade.score / Grade.max_score * 100).label('lowest'),
            func.count(func.distinct(Grade.student_id)).label('total_students')
        ).filter(Grade.course_id == course_id)
        
        if grade_type:
            query = query.filter(Grade.grade_type == grade_type)
        
        result = await db.execute(query)
        stats = result.first()
        
        return {
            'average': round(stats.average, 2) if stats.average else 0,
            'highest': round(stats.highest, 2) if stats.highest else 0,
            'lowest': round(stats.lowest, 2) if stats.lowest else 0,
            'total_students': stats.total_students or 0
        }
    
    @staticmethod
    async def get_gpa(db: AsyncSession, student_id: int) -> float:
        """Calculate GPA (simplified version)"""
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D': 1.0, 'F': 0.0
        }
        
        result = await db.execute(
            select(Grade).filter(
                Grade.student_id == student_id,
                Grade.grade.isnot(None)
            )
        )
        grades = result.scalars().all()
        
        if not grades:
            return 0.0
        
        total_points = sum(grade_points.get(g.grade, 0) for g in grades)
        return round(total_points / len(grades), 2)
    
    @staticmethod
    async def get_grade_distribution(db: AsyncSession, course_id: int) -> Dict:
        """Get distribution of letter grades for a course"""
        result = await db.execute(
            select(
                Grade.grade,
                func.count(Grade.id).label('count')
            ).filter(
                Grade.course_id == course_id,
                Grade.grade.isnot(None)
            ).group_by(Grade.grade)
        )
        results = result.all()
        
        return {grade: count for grade, count in results}
    
    @staticmethod
    async def get_top_performers(db: AsyncSession, course_id: int, limit: int = 10) -> List[Dict]:
        """Get top performing students in a course"""
        result = await db.execute(
            select(
                Grade.student_id,
                func.avg(Grade.score / Grade.max_score * 100).label('average')
            ).filter(
                Grade.course_id == course_id
            ).group_by(
                Grade.student_id
            ).order_by(
                desc(func.avg(Grade.score / Grade.max_score * 100))
            ).limit(limit)
        )
        results = result.all()
        
        top_performers = []
        for student_id, average in results:
            s_res = await db.execute(select(Student).filter(Student.id == student_id))
            student = s_res.scalars().first()
            
            if student:
                top_performers.append({
                    'student': student,
                    'average': round(average, 2)
                })
        
        return top_performers