"""
Faculty Service

Business logic layer for faculty.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from backup.modules.college.faculty.repository import FacultyRepository
from backup.modules.college.faculty.schemas import FacultyCreate, FacultyUpdate


class FacultyService:
    """Service for faculty business logic"""
    
    def __init__(self):
        self.repo = FacultyRepository()
    
    async def get_faculty(self, db: AsyncSession, faculty_id: int):
        """Get faculty by ID"""
        return await self.repo.get_by_id(db, faculty_id)
    
    async def get_faculty_by_user(self, db: AsyncSession, user_id: int):
        """Get faculty by user ID"""
        return await self.repo.get_by_user_id(db, user_id)
    
    async def get_faculty_by_employee(self, db: AsyncSession, employee_id: str):
        """Get faculty by employee ID"""
        return await self.repo.get_by_employee_id(db, employee_id)
    
    async def list_faculty(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """List all faculty"""
        faculty = await self.repo.get_all(db, skip, limit)
        total = await self.repo.get_count(db)
        return {
            "faculty": faculty,
            "total": total
        }
    
    async def list_faculty_by_department(self, db: AsyncSession, department_id: int, skip: int = 0, limit: int = 100):
        """List faculty by department"""
        faculty = await self.repo.get_by_department(db, department_id, skip, limit)
        return faculty
    
    async def create_faculty(self, db: AsyncSession, faculty_data: FacultyCreate):
        """Create new faculty"""
        # Check if user already has faculty profile
        existing = await self.repo.get_by_user_id(db, faculty_data.user_id)
        if existing:
            raise ValueError("User already has faculty profile")
        
        # Check if employee ID is unique
        existing_emp = await self.repo.get_by_employee_id(db, faculty_data.employee_id)
        if existing_emp:
            raise ValueError("Employee ID already exists")
        
        return await self.repo.create(db, faculty_data.model_dump())
    
    async def update_faculty(self, db: AsyncSession, faculty_id: int, faculty_data: FacultyUpdate):
        """Update faculty"""
        update_data = faculty_data.model_dump(exclude_unset=True)
        return await self.repo.update(db, faculty_id, update_data)
    
    async def delete_faculty(self, db: AsyncSession, faculty_id: int):
        """Delete faculty"""
        return await self.repo.delete(db, faculty_id)
