from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from typing import AsyncGenerator, Generator
from modules.shared.config import settings

from modules.shared.base import Base

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

sync_url = get_db_url(settings.DATABASE_URL_FIXED, is_async=False)
async_url = get_db_url(settings.DATABASE_URL_FIXED, is_async=True)

# Sync Engine
engine = create_engine(sync_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async Engine
async_engine = create_async_engine(async_url)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Alias for backward compatibility with other modules
get_async_db = get_db

def get_sync_db() -> Generator[Session, None, None]:
    """Get sync database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
