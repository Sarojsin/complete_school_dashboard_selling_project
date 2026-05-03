from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple

from backup.models.models import User, Student

class AdminSystemRepository:
    """Repository for system health and diagnostic queries."""

    @staticmethod
    async def check_db_connection(db: AsyncSession) -> None:
        await db.execute(text("SELECT 1"))

    @staticmethod
    async def get_table_counts(db: AsyncSession) -> Tuple[int, int]:
        users_count = await db.execute(select(func.count(User.id)))
        students_count = await db.execute(select(func.count(Student.id)))
        return users_count.scalar() or 0, students_count.scalar() or 0

    @staticmethod
    async def get_user_activity_stats(db: AsyncSession) -> Tuple[int, int]:
        total_users = await db.execute(select(func.count(User.id)))
        active_users = await db.execute(select(func.count(User.id)).where(User.is_active.is_(True)))
        return total_users.scalar() or 0, active_users.scalar() or 0
