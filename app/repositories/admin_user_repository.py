from typing import List, Dict, Optional
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User, UserRole, Student, Teacher, Parent

class AdminUserRepository:
    """Handles specialized admin queries for User management."""

    @staticmethod
    async def get_users_list(
        db: AsyncSession,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[User]:
        query = select(User)

        if role:
            try:
                query = query.where(User.role == UserRole(role))
            except ValueError:
                pass  # Ignore invalid role filters

        if is_active is not None:
            query = query.where(User.is_active == is_active)

        if search:
            query = query.where(
                or_(
                    User.full_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%")
                )
            )

        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_user_stats_by_role(db: AsyncSession) -> tuple[Dict[str, int], Dict[str, int]]:
        total_rows = await db.execute(
            select(User.role, func.count(User.id)).group_by(User.role)
        )
        active_rows = await db.execute(
            select(User.role, func.count(User.id))
            .where(User.is_active.is_(True))
            .group_by(User.role)
        )

        totals = {row[0]: row[1] for row in total_rows}
        actives = {row[0]: row[1] for row in active_rows}
        return totals, actives

    @staticmethod
    async def get_students_list(
        db: AsyncSession,
        grade: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Student]:
        query = select(Student)
        if grade:
            query = query.where(Student.grade_level == grade)
        if search:
            query = query.where(Student.full_name.ilike(f"%{search}%"))
            
        query = query.offset(skip).limit(limit).order_by(Student.full_name)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_teachers_list(
        db: AsyncSession,
        department: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Teacher]:
        query = select(Teacher)
        if department:
            query = query.where(Teacher.department == department)
        if search:
            query = query.where(Teacher.full_name.ilike(f"%{search}%"))
            
        query = query.offset(skip).limit(limit).order_by(Teacher.full_name)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_parents_list(
        db: AsyncSession,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Parent]:
        query = select(Parent)
        if search:
            query = query.where(Parent.full_name.ilike(f"%{search}%"))
            
        query = query.offset(skip).limit(limit).order_by(Parent.full_name)
        result = await db.execute(query)
        return list(result.scalars().all())
