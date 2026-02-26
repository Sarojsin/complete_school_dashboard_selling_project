from typing import Optional, List
from app.repositories.department_repository import DepartmentRepository
from app.schemas.department_schemas import DepartmentCreate, DepartmentResponse
from app.models.models import Teacher, Student, Course

class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository
    
    async def create_department(self, department_data: DepartmentCreate) -> DepartmentResponse:
        department = await self.repository.create(department_data)
        return DepartmentResponse.model_validate(department)
    
    async def get_hod_dashboard(self, user_id: int) -> dict:
        """Get HOD dashboard stats using user_id (not teacher_id)"""
        return await self.repository.get_hod_dashboard_stats(user_id)
    
    async def get_all_departments(self):
        departments = await self.repository.get_all()
        return [DepartmentResponse.model_validate(dept) for dept in departments]
    
    async def get_hod_department(self, user_id: int):
        """Get department where user is HOD"""
        return await self.repository.get_hod_department(user_id)
    
    async def get_department_teachers(self, dept_id: int) -> List[Teacher]:
        """Get all teachers in a department"""
        return await self.repository.get_department_teachers(dept_id)
    
    async def get_department_students(self, dept_id: int) -> List[Student]:
        """Get all students in a department"""
        return await self.repository.get_department_students(dept_id)
    
    async def get_department_courses(self, dept_id: int) -> List[Course]:
        """Get all courses in a department"""
        return await self.repository.get_department_courses(dept_id)
