from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from backup.models.models import Teacher, Student, Course
from backup.models.department_models import Department
from backup.schemas.department_schemas import DepartmentCreate

class DepartmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, department: DepartmentCreate) -> Department:
        db_department = Department(**department.dict())
        self.session.add(db_department)
        await self.session.commit()
        await self.session.refresh(db_department)
        return db_department
    
    async def get_all(self) -> List[Department]:
        result = await self.session.execute(select(Department))
        return result.scalars().all()
    
    async def get_by_id(self, dept_id: int) -> Optional[Department]:
        result = await self.session.execute(
            select(Department).where(Department.id == dept_id)
        )
        return result.scalar_one_or_none()
    
    async def get_hod_department(self, user_id: int) -> Optional[Department]:
        """Find department where user is HOD (via Teacher profile)"""
        # First get the Teacher profile for this user
        teacher_result = await self.session.execute(
            select(Teacher).where(Teacher.user_id == user_id)
        )
        teacher = teacher_result.scalar_one_or_none()
        
        if not teacher:
            return None
        
        # Then find department where this teacher is HOD
        dept_result = await self.session.execute(
            select(Department).where(Department.hod_teacher_id == teacher.id)
        )
        return dept_result.scalar_one_or_none()
    
    async def get_department_teachers(self, dept_id: int) -> List[Teacher]:
        """Get all teachers in a department with their user info"""
        result = await self.session.execute(
            select(Teacher)
            .where(Teacher.department_id == dept_id)
            .order_by(Teacher.full_name)
        )
        return result.scalars().all()
    
    async def get_department_students(self, dept_id: int) -> List[Student]:
        """Get all students in a department"""
        result = await self.session.execute(
            select(Student)
            .where(Student.department_id == dept_id)
            .order_by(Student.full_name)
        )
        return result.scalars().all()
    
    async def get_department_courses(self, dept_id: int) -> List[Course]:
        """Get all courses taught by teachers in a department"""
        result = await self.session.execute(
            select(Course)
            .join(Teacher, Course.teacher_id == Teacher.id)
            .where(Teacher.department_id == dept_id)
            .order_by(Course.name)
        )
        return result.scalars().all()
    
    async def get_hod_dashboard_stats(self, user_id: int) -> dict:
        """Get dashboard stats for HOD (using user_id, not teacher_id)"""
        # Get department for this HOD user
        dept = await self.get_hod_department(user_id)
        
        if not dept:
            return {
                "error": "No department assigned",
                "department_name": "",
                "department_id": 0,
                "total_teachers": 0,
                "total_students": 0,
                "total_courses": 0
            }
        
        # Count teachers in department
        teachers_count = await self.session.execute(
            select(func.count(Teacher.id)).where(Teacher.department_id == dept.id)
        )
        
        # Count students in department
        students_count = await self.session.execute(
            select(func.count(Student.id)).where(Student.department_id == dept.id)
        )
        
        # Count courses in department
        courses_count = await self.session.execute(
            select(func.count(Course.id))
            .join(Teacher, Course.teacher_id == Teacher.id)
            .where(Teacher.department_id == dept.id)
        )
        
        return {
            "department_name": dept.name,
            "department_id": dept.id,
            "total_teachers": teachers_count.scalar(),
            "total_students": students_count.scalar(),
            "total_courses": courses_count.scalar()
        }
