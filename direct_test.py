"""
Simple test to reproduce the college signup error and capture traceback
"""
import asyncio
import traceback
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from modules.auth.service import AuthService
from modules.auth.schemas import StudentCreate
from modules.shared.config import settings

# Fix URL
def get_async_url(url):
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "sqlite+aiosqlite:///")
    return url

async def test():
    school_engine = create_async_engine(get_async_url(settings.DATABASE_URL_FIXED))
    college_engine = create_async_engine(get_async_url(settings.COLLEGE_DATABASE_URL))
    SchoolSession = sessionmaker(school_engine, class_=AsyncSession, expire_on_commit=False)
    CollegeSession = sessionmaker(college_engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SchoolSession() as db, CollegeSession() as college_db:
        service = AuthService(db, college_db=college_db)
        data = StudentCreate(
            username="testcollegestudent",
            email="testcollege@example.com",
            password="TestPass123!",
            full_name="Test College Student",
            student_id="TCS001",
            portal_type="college"
        )
        try:
            result = await service.signup_college_student(data)
            print("SUCCESS:", result)
        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()

asyncio.run(test())
