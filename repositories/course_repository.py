from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_, func
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from models.models import Course, Teacher, Student, CourseEnrollment

class CourseRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, course_id: int) -> Optional[Course]:
        result = await db.execute(
            select(Course).options(
                joinedload(Course.teacher).joinedload(Teacher.user),
                selectinload(Course.enrollments)
            ).filter(Course.id == course_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_by_code(db: AsyncSession, course_code: str) -> Optional[Course]:
        result = await db.execute(select(Course).filter(Course.course_code == course_code))
        return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100, 
                grade_level: str = None, teacher_id: int = None) -> List[Course]:
        query = select(Course).options(
            joinedload(Course.teacher).joinedload(Teacher.user),
            selectinload(Course.enrollments)
        )
        
        if grade_level:
            query = query.filter(Course.grade_level == grade_level)
        
        if teacher_id:
            query = query.filter(Course.teacher_id == teacher_id)
        
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().unique().all()
    
    @staticmethod
    async def create(db: AsyncSession, course_data: dict) -> Course:
        course = Course(**course_data)
        db.add(course)
        await db.commit()
        await db.refresh(course)
        return course
    
    @staticmethod
    async def update(db: AsyncSession, course: Course, **kwargs) -> Course:
        for key, value in kwargs.items():
            if value is not None and hasattr(course, key):
                setattr(course, key, value)
        await db.commit()
        await db.refresh(course)
        return course
    
    @staticmethod
    async def delete(db: AsyncSession, course: Course):
        await db.delete(course)
        await db.commit()
    
    @staticmethod
    async def get_enrolled_students(db: AsyncSession, course_id: int) -> List[Student]:
        result = await db.execute(
            select(Student).join(CourseEnrollment).filter(
                CourseEnrollment.course_id == course_id
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_enrollment_count(db: AsyncSession, course_id: int) -> int:
        result = await db.execute(
            select(func.count(CourseEnrollment.id)).filter(
                CourseEnrollment.course_id == course_id
            )
        )
        return result.scalar() or 0
    
    @staticmethod
    async def search(db: AsyncSession, query: str) -> List[Course]:
        search_pattern = f"%{query}%"
        result = await db.execute(
            select(Course).filter(
                or_(
                    Course.course_name.ilike(search_pattern),
                    Course.course_code.ilike(search_pattern),
                    Course.description.ilike(search_pattern)
                )
            ).limit(50)
        )
        return result.scalars().unique().all()