from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from app.models.models import Student, User, CourseEnrollment, Course, Teacher
from datetime import datetime

class StudentRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, student_id: int) -> Optional[Student]:
        result = await db.execute(
            select(Student).options(
                joinedload(Student.user),
                selectinload(Student.enrollments)
            ).filter(Student.id == student_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: int) -> Optional[Student]:
        result = await db.execute(
            select(Student).options(
                joinedload(Student.user),
                selectinload(Student.enrollments)
            ).filter(Student.user_id == user_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_by_student_id(db: AsyncSession, student_id: str) -> Optional[Student]:
        result = await db.execute(
            select(Student).options(
                joinedload(Student.user),
                selectinload(Student.enrollments)
            ).filter(Student.student_id == student_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100, 
                grade_level: str = None, section: str = None, 
                status: str = None, search: str = None) -> List[Student]:
        query = select(Student).join(User).options(joinedload(Student.user))
        
        if grade_level:
            query = query.filter(Student.grade_level == grade_level)
            
        if section:
            query = query.filter(Student.section == section)
            
        if status:
            if status == "active":
                query = query.filter(User.is_active == True)
            elif status == "inactive":
                query = query.filter(User.is_active == False)
                
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    User.full_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    Student.student_id.ilike(search_pattern)
                )
            )
        
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().unique().all()
    
    @staticmethod
    async def create(db: AsyncSession, student_data: dict) -> Student:
        student = Student(**student_data)
        db.add(student)
        await db.commit()
        await db.refresh(student)
        return student
    
    @staticmethod
    async def update(db: AsyncSession, student: Student, **kwargs) -> Student:
        for key, value in kwargs.items():
            if value is not None and hasattr(student, key):
                setattr(student, key, value)
        await db.commit()
        await db.refresh(student)
        return student
    
    @staticmethod
    async def delete(db: AsyncSession, student: Student):
        await db.delete(student)
        await db.commit()
    
    @staticmethod
    async def get_enrolled_courses(db: AsyncSession, student_id: int) -> List[Course]:
        result = await db.execute(
            select(Course).options(
                joinedload(Course.teacher).joinedload(Teacher.user),
                selectinload(Course.schedules),
                selectinload(Course.assignments)
            ).join(CourseEnrollment).filter(
                CourseEnrollment.student_id == student_id
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def enroll_in_course(db: AsyncSession, student_id: int, course_id: int):
        enrollment = CourseEnrollment(
            student_id=student_id,
            course_id=course_id,
            enrollment_date=datetime.utcnow().date()
        )
        db.add(enrollment)
        await db.commit()
        return enrollment
    
    @staticmethod
    async def unenroll_from_course(db: AsyncSession, student_id: int, course_id: int):
        result = await db.execute(
            select(CourseEnrollment).filter(
                CourseEnrollment.student_id == student_id,
                CourseEnrollment.course_id == course_id
            )
        )
        enrollment = result.scalars().first()
        
        if enrollment:
            await db.delete(enrollment)
            await db.commit()
    
    @staticmethod
    async def search(db: AsyncSession, query: str) -> List[Student]:
        search_pattern = f"%{query}%"
        result = await db.execute(
            select(Student).join(User).filter(
                or_(
                    User.full_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    Student.student_id.ilike(search_pattern)
                )
            ).limit(50)
        )
        return result.scalars().unique().all()