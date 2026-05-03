"""
College Faculty Repository

Database CRUD operations for college faculty.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List

from backup.models.college.faculty import Faculty


class FacultyRepository:
    """Repository for faculty operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: int, employee_id: str, department_id: int,
                    designation: str, specialization: str = None,
                    qualification: str = None, experience_years: int = None) -> Faculty:
        """Create a new faculty"""
        faculty = Faculty(
            user_id=user_id,
            employee_id=employee_id,
            department_id=department_id,
            designation=designation,
            specialization=specialization,
            qualification=qualification,
            experience_years=experience_years
        )
        self.db.add(faculty)
        await self.db.commit()
        await self.db.refresh(faculty)
        return faculty
    
    async def get(self, faculty_id: int) -> Optional[Faculty]:
        """Get faculty by ID"""
        result = await self.db.execute(
            select(Faculty).where(Faculty.id == faculty_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> Optional[Faculty]:
        """Get faculty by user ID"""
        result = await self.db.execute(
            select(Faculty).where(Faculty.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def list(self, department_id: Optional[int] = None,
                   skip: int = 0, limit: int = 100) -> List[Faculty]:
        """List faculty with filters"""
        query = select(Faculty)
        
        if department_id:
            query = query.where(Faculty.department_id == department_id)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count(self, department_id: Optional[int] = None) -> int:
        """Count faculty"""
        query = select(func.count(Faculty.id))
        
        if department_id:
            query = query.where(Faculty.department_id == department_id)
        
        result = await self.db.execute(query)
        return result.scalar() or 0
    
    async def update(self, faculty_id: int, **kwargs) -> Optional[Faculty]:
        """Update faculty"""
        faculty = await self.get(faculty_id)
        if faculty:
            for key, value in kwargs.items():
                if value is not None and hasattr(faculty, key):
                    setattr(faculty, key, value)
            await self.db.commit()
            await self.db.refresh(faculty)
        return faculty
    
    async def delete(self, faculty_id: int) -> bool:
        """Delete faculty"""
        faculty = await self.get(faculty_id)
        if faculty:
            await self.db.delete(faculty)
            await self.db.commit()
            return True
        return False


__all__ = ["FacultyRepository"]
