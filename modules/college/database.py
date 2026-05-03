"""
College-specific Database Configuration.

All college operations use this separate database connection.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from typing import AsyncGenerator, Generator
from modules.shared.config import settings

# Import CollegeBase to bind its metadata
from modules.college.base import CollegeBase

def get_db_url(url: str, is_async: bool = False) -> str:
    """Fix database URL for async/sync compatibility"""
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    
    if is_async:
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("sqlite:///"):
            return url.replace("sqlite:///", "sqlite+aiosqlite:///")
    return url

# Get college database URL from settings
college_db_url = getattr(settings, 'COLLEGE_DATABASE_URL', settings.DATABASE_URL_FIXED)

# Sync Engine for College (for table creation, migrations)
sync_url = get_db_url(college_db_url, is_async=False)
college_sync_engine = create_engine(sync_url)

# Async Engine for College (for runtime operations)
async_url = get_db_url(college_db_url, is_async=True)
college_async_engine = create_async_engine(async_url)

# Session factories
CollegeSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=college_sync_engine)
CollegeAsyncSessionLocal = async_sessionmaker(college_async_engine, expire_on_commit=False, class_=AsyncSession)

def get_college_db() -> Generator[Session, None, None]:
    """Get sync college database session (for legacy sync code)"""
    db = CollegeSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_college_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async college database session (recommended)"""
    async with CollegeAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Bind CollegeBase metadata to college engine - THIS IS CRITICAL
CollegeBase.metadata.bind = college_sync_engine

def create_college_tables():
    """Create all college tables in college database"""
    CollegeBase.metadata.create_all(college_sync_engine)

def drop_college_tables():
    """Drop all college tables (use with caution)"""
    CollegeBase.metadata.drop_all(college_sync_engine)

__all__ = [
    "college_sync_engine",
    "college_async_engine",
    "CollegeSessionLocal",
    "CollegeAsyncSessionLocal",
    "get_college_db",
    "get_college_async_db",
    "CollegeBase",
    "create_college_tables",
    "drop_college_tables",
]
