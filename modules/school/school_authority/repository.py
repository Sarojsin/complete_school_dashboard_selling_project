"""
Authority Repository

Data access layer for authority.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Union
from sqlalchemy import Column
from .models import SchoolAuthority
from .schemas import AuthorityCreate, AuthorityUpdate


class AuthorityRepository:
    """Repository for authority data access"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, authority_id: int) -> Optional[SchoolAuthority]:
        """Get authority by ID"""
        result = await self.db.execute(
            select(SchoolAuthority).where(SchoolAuthority.id == authority_id)
        )
        return result.scalars().first()
    
    async def get_by_user_id(self, user_id: Union[int, Column[int]]) -> Optional[SchoolAuthority]:
        """Get authority by user ID"""
        result = await self.db.execute(
            select(SchoolAuthority).where(SchoolAuthority.user_id == user_id)
        )
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[SchoolAuthority]:
        """Get all authorities"""
        result = await self.db.execute(
            select(SchoolAuthority).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_count(self) -> int:
        """Get total count of authorities"""
        result = await self.db.execute(select(SchoolAuthority))
        return len(result.scalars().all())
    
    async def create(self, authority_data: dict) -> SchoolAuthority:
        """Create new authority"""
        authority = SchoolAuthority(**authority_data)
        self.db.add(authority)
        await self.db.commit()
        await self.db.refresh(authority)
        return authority
    
    async def update(self, authority_id: int, authority_data: dict) -> Optional[SchoolAuthority]:
        """Update authority"""
        authority = await self.get_by_id(authority_id)
        if authority:
            for key, value in authority_data.items():
                if value is not None:
                    setattr(authority, key, value)
            await self.db.commit()
            await self.db.refresh(authority)
        return authority
    
    async def delete(self, authority_id: int) -> Optional[SchoolAuthority]:
        """Delete authority"""
        authority = await self.get_by_id(authority_id)
        if authority:
            await self.db.delete(authority)
            await self.db.commit()
        return authority
