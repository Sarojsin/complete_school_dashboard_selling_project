
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.models import Teacher, User
from app.repositories.teacher_repository import TeacherRepository
from app.core.config import settings

ASYNC_DATABASE_URL = settings.DATABASE_URL_FIXED.replace("postgresql://", "postgresql+asyncpg://")

async def test_delete():
    engine = create_async_engine(ASYNC_DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        # Get an existing teacher
        result = await db.execute(select(Teacher).limit(1))
        teacher = result.scalars().first()
        
        if not teacher:
            print("No teachers found to test deletion.")
            return

        print(f"Testing deletion for Teacher ID: {teacher.id}")
        
        # Test TeacherRepository.get_by_id
        found_teacher = await TeacherRepository.get_by_id(db, teacher.id)
        if found_teacher:
            print(f"Teacher {teacher.id} found via repository.")
        else:
            print(f"Teacher {teacher.id} NOT found via repository!")
            
        # We won't actually delete it here to avoid messing up the DB, 
        # but we confirmed the fetch works.
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_delete())
