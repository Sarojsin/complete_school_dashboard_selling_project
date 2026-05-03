"""
Auth Repository - Async Database operations for authentication

Contains user lookup, creation, password update operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from modules.shared.models import User
from modules.shared.auth_utils import get_password_hash


class AuthRepository:
    """Repository for authentication-related database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str,
        role: str,
        portal_type: str  # NEW
    ) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            portal_type=portal_type  # NEW
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_password(self, user_id: int, new_password: str) -> Optional[User]:
        """Update user password"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()
        if user:
            user.hashed_password = get_password_hash(new_password)
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user by username and password"""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        
        from modules.shared.auth_utils import verify_password
        if not verify_password(password, user.hashed_password):
            return None
        
        return user


__all__ = ["AuthRepository"]