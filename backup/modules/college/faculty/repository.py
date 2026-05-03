"""
Faculty Repository

Data access layer for faculty.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backup.models.college import Faculty


class FacultyRepository:
    """Repository for faculty data access"""
    
    async def get_by_id(self, db: AsyncSession, faculty_id: int):
        """Get faculty by ID"""
        result = await db.execute(
            select(Faculty).where(Faculty.id == faculty_id)
        )
        return result.scalars().first()
    
    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        """Get faculty by user ID"""
        result = await db.execute(
            select(Faculty).where(Faculty.user_id == user_id)
        )
        return result.scalars().first()
    
    async def get_by_employee_id(self, db: AsyncSession, employee_id: str):
        """Get faculty by employee ID"""
        result = await db.execute(
            select(Faculty).where(Faculty.employee_id == employee_id)
        )
        return result.scalars().first()
    
    async def get_by_department(self, db: AsyncSession, department_id: int, skip: int = 0, limit: int = 100):
        """Get faculty by department"""
        result = await db.execute(
            select(Faculty)
            .where(Faculty.department_id == department_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get all faculty"""
        result = await db.execute(
            select(Faculty).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_count(self, db: AsyncSession):
        """Get total count of faculty"""
        result = await db.execute(select(Faculty))
        return len(result.scalars().all())
    
    async def create(self, db: AsyncSession, faculty_data: dict):
        """Create new faculty"""
        faculty = Faculty(**faculty_data)
        db.add(faculty)
        await db.commit()
        await db.refresh(faculty)
        return faculty
    
    async def update(self, db: AsyncSession, faculty_id: int, faculty_data: dict):
        """Update faculty"""
        faculty = await self.get_by_id(db, faculty_id)
        if faculty:
            for key, value in faculty_data.items():
                if value is not None:
                    setattr(faculty, key, value)
            await db.commit()
            await db.refresh(faculty)
        return faculty
    
    async def delete(self, db: AsyncSession, faculty_id: int):
        """Delete faculty"""
        faculty = await self.get_by_id(db, faculty_id)
        if faculty:
            await db.delete(faculty)
            await db.commit()
        return faculty
