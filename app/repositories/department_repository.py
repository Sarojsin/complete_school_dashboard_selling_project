from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.models.models import Teacher, Student
from app.models.department_models import Department
from app.schemas.department_schemas import DepartmentCreate

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
    
    async def get_hod_dashboard_stats(self, hod_id: int) -> dict:
        # Get department of HOD
        dept_result = await self.session.execute(
            select(Department).where(Department.hod_teacher_id == hod_id)
        )
        dept = dept_result.scalar_one_or_none()
        
        if not dept:
            return {"error": "No department assigned"}
        
        # Count teachers in department
        teachers_count = await self.session.execute(
            select(func.count(Teacher.id)).where(Teacher.department_id == dept.id)
        )
        
        # Count students in department
        students_count = await self.session.execute(
            select(func.count(Student.id)).where(Student.department_id == dept.id)
        )
        
        return {
            "total_teachers": teachers_count.scalar(),
            "total_students": students_count.scalar(),
            "department_name": dept.name
        }
