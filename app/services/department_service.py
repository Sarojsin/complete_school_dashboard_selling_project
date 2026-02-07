from typing import Optional
from app.repositories.department_repository import DepartmentRepository
from app.schemas.department_schemas import DepartmentCreate, DepartmentResponse

class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository
    
    async def create_department(self, department_data: DepartmentCreate) -> DepartmentResponse:
        department = await self.repository.create(department_data)
        return DepartmentResponse.from_orm(department)
    
    async def get_hod_dashboard(self, hod_id: int) -> dict:
        return await self.repository.get_hod_dashboard_stats(hod_id)
    
    async def get_all_departments(self):
        departments = await self.repository.get_all()
        return [DepartmentResponse.from_orm(dept) for dept in departments]
