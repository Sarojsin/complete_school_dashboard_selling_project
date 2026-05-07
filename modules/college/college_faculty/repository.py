"""
College Faculty Repository

Database CRUD operations for college faculty.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List

from modules.college.college_faculty.models import CollegeFaculty


class CollegeFacultyRepository:
    """Repository for faculty operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: int, employee_id: str, first_name: str, last_name: str,
                    email: str, department_id: Optional[int] = None,
                    designation: str = None, qualification: str = None,
                    experience_years: int = None, phone: str = None) -> CollegeFaculty:
        """Create a new faculty"""
        faculty = CollegeFaculty(
            user_id=user_id,
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            department_id=department_id,
            designation=designation,
            qualification=qualification,
            experience_years=experience_years,
            phone=phone
        )
        self.db.add(faculty)
        await self.db.commit()
        await self.db.refresh(faculty)
        return faculty
    
    async def get(self, faculty_id: int) -> Optional[CollegeFaculty]:
        """Get faculty by ID (excludes soft-deleted)"""
        result = await self.db.execute(
            select(CollegeFaculty).where(
                CollegeFaculty.id == faculty_id,
                CollegeFaculty.is_deleted == False
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int) -> Optional[CollegeFaculty]:
        """Get faculty by user ID"""
        result = await self.db.execute(
            select(CollegeFaculty).where(CollegeFaculty.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def list(self, department_id: Optional[int] = None,
                   skip: int = 0, limit: int = 100) -> List[CollegeFaculty]:
        """List faculty with filters (excludes soft-deleted)"""
        query = select(CollegeFaculty).where(CollegeFaculty.is_deleted == False)

        if department_id:
            query = query.where(CollegeFaculty.department_id == department_id)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def count(self, department_id: Optional[int] = None) -> int:
        """Count faculty (excludes soft-deleted)"""
        query = select(func.count(CollegeFaculty.id)).where(CollegeFaculty.is_deleted == False)

        if department_id:
            query = query.where(CollegeFaculty.department_id == department_id)

        result = await self.db.execute(query)
        return result.scalar() or 0
    
    async def update(self, faculty_id: int, **kwargs) -> Optional[CollegeFaculty]:
        """Update faculty"""
        faculty = await self.get(faculty_id)
        if faculty:
            for key, value in kwargs.items():
                if value is not None and hasattr(faculty, key):
                    setattr(faculty, key, value)
            await self.db.commit()
            await self.db.refresh(faculty)
        return faculty
    
    async def soft_delete(self, faculty_id: int) -> bool:
        """Soft delete faculty"""
        faculty = await self.get(faculty_id)
        if faculty:
            await faculty.soft_delete(self.db)
            return True
        return False

    async def delete(self, faculty_id: int) -> bool:
        """Hard delete faculty (not recommended)"""
        faculty = await self.get(faculty_id)
        if faculty:
            await self.db.delete(faculty)
            await self.db.commit()
            return True
        return False


__all__ = ["CollegeFacultyRepository"]
