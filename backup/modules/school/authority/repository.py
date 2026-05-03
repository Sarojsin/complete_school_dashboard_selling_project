"""
Authority Repository

Data access layer for authority.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backup.models.school.authority import SchoolAuthority


class AuthorityRepository:
    """Repository for authority data access"""
    
    async def get_by_id(self, db: AsyncSession, authority_id: int):
        """Get authority by ID"""
        result = await db.execute(
            select(SchoolAuthority).where(SchoolAuthority.id == authority_id)
        )
        return result.scalars().first()
    
    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        """Get authority by user ID"""
        result = await db.execute(
            select(SchoolAuthority).where(SchoolAuthority.user_id == user_id)
        )
        return result.scalars().first()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get all authorities"""
        result = await db.execute(
            select(SchoolAuthority).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_count(self, db: AsyncSession):
        """Get total count of authorities"""
        result = await db.execute(select(SchoolAuthority))
        return len(result.scalars().all())
    
    async def create(self, db: AsyncSession, authority_data: dict):
        """Create new authority"""
        authority = SchoolAuthority(**authority_data)
        db.add(authority)
        await db.commit()
        await db.refresh(authority)
        return authority
    
    async def update(self, db: AsyncSession, authority_id: int, authority_data: dict):
        """Update authority"""
        authority = await self.get_by_id(db, authority_id)
        if authority:
            for key, value in authority_data.items():
                if value is not None:
                    setattr(authority, key, value)
            await db.commit()
            await db.refresh(authority)
        return authority
    
    async def delete(self, db: AsyncSession, authority_id: int):
        """Delete authority"""
        authority = await self.get_by_id(db, authority_id)
        if authority:
            await db.delete(authority)
            await db.commit()
        return authority
