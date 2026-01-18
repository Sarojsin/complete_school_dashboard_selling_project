from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from models.models import Teacher, User, Course, Student

class TeacherRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, teacher_id: int) -> Optional[Teacher]:
        result = await db.execute(
            select(Teacher).options(
                joinedload(Teacher.user),
                selectinload(Teacher.courses)
            ).filter(Teacher.id == teacher_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: int) -> Optional[Teacher]:
        result = await db.execute(
            select(Teacher).options(
                joinedload(Teacher.user),
                selectinload(Teacher.courses)
            ).filter(Teacher.user_id == user_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_by_employee_id(db: AsyncSession, employee_id: str) -> Optional[Teacher]:
        result = await db.execute(
            select(Teacher).options(
                joinedload(Teacher.user),
                selectinload(Teacher.courses)
            ).filter(Teacher.employee_id == employee_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100, 
                department: str = None, status: str = None, 
                search: str = None) -> List[Teacher]:
        query = select(Teacher).join(User).options(joinedload(Teacher.user))
        
        if department:
            query = query.filter(Teacher.department == department)
            
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
                    Teacher.employee_id.ilike(search_pattern),
                    Teacher.department.ilike(search_pattern)
                )
            )
        
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().unique().all()
    
    @staticmethod
    async def create(db: AsyncSession, teacher_data: dict) -> Teacher:
        teacher = Teacher(**teacher_data)
        db.add(teacher)
        await db.commit()
        await db.refresh(teacher)
        return teacher
    
    @staticmethod
    async def update(db: AsyncSession, teacher: Teacher, **kwargs) -> Teacher:
        for key, value in kwargs.items():
            if value is not None and hasattr(teacher, key):
                setattr(teacher, key, value)
        await db.commit()
        await db.refresh(teacher)
        return teacher
    
    @staticmethod
    async def delete(db: AsyncSession, teacher: Teacher):
        await db.delete(teacher)
        await db.commit()
    
    @staticmethod
    async def get_teaching_courses(db: AsyncSession, teacher_id: int) -> List[Course]:
        result = await db.execute(select(Course).filter(Course.teacher_id == teacher_id))
        return result.scalars().all()
    
    @staticmethod
    async def search(db: AsyncSession, query: str) -> List[Teacher]:
        search_pattern = f"%{query}%"
        result = await db.execute(
            select(Teacher).join(User).filter(
                or_(
                    User.full_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    Teacher.department.ilike(search_pattern)
                )
            ).limit(50)
        )
        return result.scalars().unique().all()
    
    @staticmethod
    async def get_my_students(db: AsyncSession, teacher_id: int, 
                        grade: str = None, section: str = None, 
                        search: str = None) -> List[Student]:
        from models.models import CourseEnrollment
        
        query = select(Student).join(CourseEnrollment).join(Course).filter(
            Course.teacher_id == teacher_id
        ).join(User).options(joinedload(Student.user))
        
        if grade:
            query = query.filter(Student.grade_level == grade)
        if section:
            query = query.filter(Student.section == section)
            
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    User.full_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    Student.student_id.ilike(search_pattern)
                )
            )
            
        result = await db.execute(query.distinct())
        return result.scalars().unique().all()