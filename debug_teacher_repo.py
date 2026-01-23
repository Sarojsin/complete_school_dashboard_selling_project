
import asyncio
from app.core.database import async_engine
from app.repositories.teacher_repository import TeacherRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def debug_teachers_route():
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as db:
        teachers = await TeacherRepository.get_all(db)
        print(f"Total teachers from repo: {len(teachers)}")
        for t in teachers:
            print(f"Teacher ID: {t.id}, User ID: {t.user_id}, Name: {t.user.full_name if t.user else 'N/A'}")

if __name__ == "__main__":
    asyncio.run(debug_teachers_route())
