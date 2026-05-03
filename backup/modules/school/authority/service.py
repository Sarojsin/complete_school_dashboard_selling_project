"""
Authority Service

Business logic layer for authority.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from backup.modules.school.authority.repository import AuthorityRepository
from backup.modules.school.authority.schemas import AuthorityCreate, AuthorityUpdate


class AuthorityService:
    """Service for authority business logic"""
    
    def __init__(self):
        self.repo = AuthorityRepository()
    
    async def get_authority(self, db: AsyncSession, authority_id: int):
        """Get authority by ID"""
        return await self.repo.get_by_id(db, authority_id)
    
    async def get_authority_by_user(self, db: AsyncSession, user_id: int):
        """Get authority by user ID"""
        return await self.repo.get_by_user_id(db, user_id)
    
    async def list_authorities(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """List all authorities"""
        authorities = await self.repo.get_all(db, skip, limit)
        total = await self.repo.get_count(db)
        return {
            "authorities": authorities,
            "total": total
        }
    
    async def create_authority(self, db: AsyncSession, authority_data: AuthorityCreate):
        """Create new authority"""
        # Check if user already has authority profile
        existing = await self.repo.get_by_user_id(db, authority_data.user_id)
        if existing:
            raise ValueError("User already has authority profile")
        
        return await self.repo.create(db, authority_data.model_dump())
    
    async def update_authority(self, db: AsyncSession, authority_id: int, authority_data: AuthorityUpdate):
        """Update authority"""
        update_data = authority_data.model_dump(exclude_unset=True)
        return await self.repo.update(db, authority_id, update_data)
    
    async def delete_authority(self, db: AsyncSession, authority_id: int):
        """Delete authority"""
        return await self.repo.delete(db, authority_id)
