"""
Authority Service

Business logic layer for authority.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .repository import AuthorityRepository
from .schemas import AuthorityCreate, AuthorityUpdate, AuthorityResponse, AuthorityListResponse


class AuthorityService:
    """Service for authority business logic"""
    
    def __init__(self, db: AsyncSession):
        self.repo = AuthorityRepository(db)
    
    async def get_authority(self, authority_id: int) -> Optional[AuthorityResponse]:
        """Get authority by ID"""
        return await self.repo.get_by_id(authority_id)
    
    async def get_authority_by_user(self, user_id: any) -> Optional[AuthorityResponse]:
        """Get authority by user ID"""
        return await self.repo.get_by_user_id(user_id)
    
    async def list_authorities(self, skip: int = 0, limit: int = 100) -> AuthorityListResponse:
        """List all authorities"""
        authorities = await self.repo.get_all(skip, limit)
        total = await self.repo.get_count()
        return {
            "authorities": authorities,
            "total": total
        }
    
    async def create_authority(self, authority_data: AuthorityCreate) -> AuthorityResponse:
        """Create new authority"""
        # Check if user already has authority profile
        existing = await self.repo.get_by_user_id(authority_data.user_id)
        if existing:
            raise ValueError("User already has authority profile")
        
        return await self.repo.create(authority_data.model_dump())
    
    async def update_authority(self, authority_id: int, authority_data: AuthorityUpdate) -> Optional[AuthorityResponse]:
        """Update authority"""
        update_data = authority_data.model_dump(exclude_unset=True)
        return await self.repo.update(authority_id, update_data)
    
    async def delete_authority(self, authority_id: int) -> bool:
        """Delete authority"""
        authority = await self.repo.delete(authority_id)
        return authority is not None
