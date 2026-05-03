from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backup.core.config import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# --- Synchronous Database Setup (School - Default) ---
if settings.DATABASE_URL_FIXED.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL_FIXED,
        connect_args={"check_same_thread": False},
        echo=settings.is_debug
    )
else:
    engine = create_engine(
        settings.DATABASE_URL_FIXED,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=settings.is_debug
    )

# --- Synchronous Database Setup (College - Separate DB) ---
college_engine = None
if settings.use_separate_databases:
    college_db_url = settings.COLLEGE_DATABASE_URL_FIXED
    if college_db_url.startswith("sqlite"):
        college_engine = create_engine(
            college_db_url,
            connect_args={"check_same_thread": False},
            echo=settings.DEBUG
        )
    else:
        college_engine = create_engine(
            college_db_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            echo=settings.is_debug
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
CollegeSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=college_engine) if college_engine else None


def get_db():
    """Get school database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_college_db():
    """Get college database session (if separate)"""
    if not college_engine:
        # Fall back to school database
        logger.warning(
            "COLLEGE_DB_REQUESTED: No separate college database configured. "
            "Falling back to school database. Set DATABASE_MODE=separate and "
            "COLLEGE_DATABASE_URL to enable college database isolation."
        )
        db = SessionLocal()
    else:
        db = CollegeSessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Asynchronous Database Setup (School) ---
ASYNC_DATABASE_URL = settings.DATABASE_URL_FIXED
if ASYNC_DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
elif ASYNC_DATABASE_URL.startswith("sqlite:///"):
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.is_debug,
    future=True,
    pool_pre_ping=True if not ASYNC_DATABASE_URL.startswith("sqlite") else False
)

# --- Asynchronous Database Setup (College - Separate DB) ---
async_college_engine = None
if settings.use_separate_databases:
    college_async_url = settings.COLLEGE_DATABASE_URL_FIXED
    if college_async_url.startswith("postgresql://"):
        college_async_url = college_async_url.replace("postgresql://", "postgresql+asyncpg://")
    elif college_async_url.startswith("sqlite:///"):
        college_async_url = college_async_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    
    async_college_engine = create_async_engine(
        college_async_url,
        echo=settings.is_debug,
        future=True,
        pool_pre_ping=True if not college_async_url.startswith("sqlite") else False
    )

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

AsyncCollegeSessionLocal = async_sessionmaker(
    bind=async_college_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
) if async_college_engine else None


async def get_async_db():
    """Get school async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_async_college_db():
    """Get college async database session (if separate)"""
    if async_college_engine:
        async with AsyncCollegeSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    else:
        # Fall back to school database
        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()


# Base class for models
Base = declarative_base()


def ensure_admin_tables() -> None:
    """
    Ensure admin/security/setting tables exist.

    This is a lightweight safety net for environments where migrations
    haven't been applied yet.
    """
    try:
        from backup.models.admin_models import (
            SystemSetting,
            LoginHistory,
            FailedLoginAttempt,
            UserSecurityState,
            BackupRecord,
        )
        Base.metadata.create_all(
            bind=engine,
            tables=[
                SystemSetting.__table__,
                LoginHistory.__table__,
                FailedLoginAttempt.__table__,
                UserSecurityState.__table__,
                BackupRecord.__table__,
            ],
        )
    except Exception:
        # Fail open; the app should still start even if bootstrap fails.
        pass
