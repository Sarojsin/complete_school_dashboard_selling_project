"""
College Faculty Service

Business logic for college faculty management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any

from .repository import CollegeFacultyRepository
from .schemas import FacultyCreate, FacultyUpdate


class CollegeFacultyService:
    """Service for faculty business logic"""

    def __init__(self, db: AsyncSession):
        self.repository = CollegeFacultyRepository(db)
    
    async def create_faculty(self, data: FacultyCreate) -> Dict[str, Any]:
        """Create a new faculty"""
        faculty = await self.repository.create(
            user_id=data.user_id,
            employee_id=data.employee_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            department_id=data.department_id,
            designation=data.designation,
            qualification=data.qualification,
            experience_years=data.experience_years,
            phone=data.phone
        )
        return {"faculty": faculty}
    
    async def get_faculty(self, faculty_id: int) -> Optional[Dict[str, Any]]:
        """Get faculty by ID"""
        faculty = await self.repository.get(faculty_id)
        if faculty:
            return {"faculty": faculty}
        return None
    
    async def list_faculty(self, department_id: Optional[int] = None,
                          skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List faculty"""
        faculty = await self.repository.list(department_id, skip, limit)
        total = await self.repository.count(department_id)
        return {"total": total, "faculty": faculty}
    
    async def update_faculty(self, faculty_id: int, data: FacultyUpdate) -> Dict[str, Any]:
        """Update faculty"""
        update_data = data.model_dump(exclude_unset=True)
        faculty = await self.repository.update(faculty_id, **update_data)
        if faculty:
            return {"faculty": faculty}
        return {"error": "Faculty not found"}
    
    async def soft_delete_faculty(self, faculty_id: int) -> Dict[str, Any]:
        """Soft delete faculty"""
        success = await self.repository.soft_delete(faculty_id)
        if success:
            return {"message": "Faculty deleted successfully"}
        return {"error": "Faculty not found"}

    async def delete_faculty(self, faculty_id: int) -> Dict[str, Any]:
        """Hard delete faculty (not recommended - use soft_delete instead)"""
        success = await self.repository.delete(faculty_id)
        if success:
            return {"message": "Faculty hard deleted successfully"}
        return {"error": "Faculty not found"}


__all__ = ["FacultyService"]
