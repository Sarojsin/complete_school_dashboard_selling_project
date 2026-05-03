
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from backup.models.models import Teacher, User
from backup.core.config import settings

ASYNC_DATABASE_URL = settings.DATABASE_URL_FIXED.replace("postgresql://", "postgresql+asyncpg://")

async def check_integrity():
    engine = create_async_engine(ASYNC_DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as db:
        # Check for teachers with same user_id
        res = await db.execute(
            select(Teacher.user_id, func.count(Teacher.id))
            .group_by(Teacher.user_id)
            .having(func.count(Teacher.id) > 1)
        )
        dupes = res.all()
        if dupes:
            print(f"Found {len(dupes)} user_ids with multiple teachers!")
            for user_id, count in dupes:
                print(f"User ID {user_id} has {count} teachers.")
        else:
            print("No duplicate teacher-user mappings found.")
            
        # Check for teachers with same employee_id
        res = await db.execute(
            select(Teacher.employee_id, func.count(Teacher.id))
            .group_by(Teacher.employee_id)
            .having(func.count(Teacher.id) > 1)
        )
        dupes = res.all()
        if dupes:
            print(f"Found {len(dupes)} employee_ids with multiple teachers!")
            for emp_id, count in dupes:
                print(f"Employee ID {emp_id} has {count} teachers.")
        else:
            print("No duplicate employee IDs found.")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_integrity())
