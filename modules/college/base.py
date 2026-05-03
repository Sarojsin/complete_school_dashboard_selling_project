"""
College-specific SQLAlchemy Declarative Base.

All college models must inherit from this Base so they are
registered in the college_sell_db metadata, separate from school tables.
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from modules.shared.config import settings

# Create a separate engine for college database
def get_college_engine():
    """Get college database engine from settings"""
    from modules.shared.database import get_db_url
    college_url = getattr(settings, 'COLLEGE_DATABASE_URL', settings.DATABASE_URL_FIXED)
    async_url = get_db_url(college_url, is_async=True)
    return create_async_engine(async_url)

CollegeBase = declarative_base()

# Store the college engine reference for metadata binding
_college_engine = None

def get_college_engine_instance():
    """Get or create college engine instance"""
    global _college_engine
    if _college_engine is None:
        _college_engine = get_college_engine()
    return _college_engine

def create_college_tables():
    """Create all college tables in college database"""
    from modules.shared.database import get_db_url
    college_url = getattr(settings, 'COLLEGE_DATABASE_URL', settings.DATABASE_URL_FIXED)
    sync_url = get_db_url(college_url, is_async=False)
    engine = create_engine(sync_url)
    CollegeBase.metadata.create_all(engine)
    engine.dispose()

__all__ = [
    "CollegeBase",
    "get_college_engine_instance",
    "create_college_tables",
]

