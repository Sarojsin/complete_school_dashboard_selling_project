from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# --- Synchronous Database Setup (Legacy) ---
if settings.DATABASE_URL_FIXED.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL_FIXED,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )
else:
    engine = create_engine(
        settings.DATABASE_URL_FIXED,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=settings.DEBUG
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Asynchronous Database Setup (New) ---
# Convert the URL for asyncpg or aiosqlite
ASYNC_DATABASE_URL = settings.DATABASE_URL_FIXED
if ASYNC_DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
elif ASYNC_DATABASE_URL.startswith("sqlite:///"):
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True if not ASYNC_DATABASE_URL.startswith("sqlite") else False
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_async_db():
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
        from app.models.admin_models import (
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
