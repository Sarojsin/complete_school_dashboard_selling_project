from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User, UserRole, Student, Teacher, Parent
from app.models.admin_models import LoginHistory, FailedLoginAttempt, UserSecurityState

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

    @staticmethod
    async def get_user_security_state(
        db: AsyncSession,
        user_id: int,
        create_if_missing: bool = False,
    ) -> Optional[UserSecurityState]:
        result = await db.execute(
            select(UserSecurityState).where(UserSecurityState.user_id == user_id)
        )
        state = result.scalar_one_or_none()
        if state or not create_if_missing:
            return state

        state = UserSecurityState(user_id=user_id)
        db.add(state)
        await db.flush()
        return state

    @staticmethod
    async def set_user_lock(
        db: AsyncSession,
        user_id: int,
        lock: bool,
        admin_user_id: int,
        reason: Optional[str] = None,
    ) -> UserSecurityState:
        state = await AdminUserRepository.get_user_security_state(
            db, user_id, create_if_missing=True
        )
        state.is_locked = lock
        state.lock_reason = reason if lock else None
        state.locked_by = admin_user_id if lock else None
        state.locked_at = datetime.utcnow() if lock else None
        state.updated_at = datetime.utcnow()
        return state

    @staticmethod
    async def mark_force_logout(
        db: AsyncSession,
        user_id: int,
        admin_user_id: int,
    ) -> UserSecurityState:
        state = await AdminUserRepository.get_user_security_state(
            db, user_id, create_if_missing=True
        )
        state.force_logout_after = datetime.utcnow()
        state.force_logout_by = admin_user_id
        state.updated_at = datetime.utcnow()
        return state

    @staticmethod
    async def create_login_history(
        db: AsyncSession,
        username: str,
        success: bool,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        failure_reason: Optional[str] = None,
        token_issued_at: Optional[datetime] = None,
    ) -> LoginHistory:
        entry = LoginHistory(
            user_id=user_id,
            username=username,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason=failure_reason,
            token_issued_at=token_issued_at,
        )
        db.add(entry)
        await db.flush()
        return entry

    @staticmethod
    async def increment_failed_login_attempt(
        db: AsyncSession,
        username: str,
        ip_address: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> FailedLoginAttempt:
        result = await db.execute(
            select(FailedLoginAttempt).where(
                FailedLoginAttempt.username == username,
                FailedLoginAttempt.ip_address == ip_address,
            )
        )
        row = result.scalar_one_or_none()
        if row:
            row.attempts_count += 1
            row.last_failure_reason = reason
            row.last_attempt_at = datetime.utcnow()
            return row

        row = FailedLoginAttempt(
            username=username,
            ip_address=ip_address,
            attempts_count=1,
            last_failure_reason=reason,
            last_attempt_at=datetime.utcnow(),
        )
        db.add(row)
        await db.flush()
        return row

    @staticmethod
    async def clear_failed_login_attempts(
        db: AsyncSession,
        username: str,
        ip_address: Optional[str] = None,
    ) -> None:
        result = await db.execute(
            select(FailedLoginAttempt).where(
                FailedLoginAttempt.username == username,
                FailedLoginAttempt.ip_address == ip_address,
            )
        )
        row = result.scalar_one_or_none()
        if row:
            await db.delete(row)

    @staticmethod
    async def get_login_history_for_user(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
    ) -> List[LoginHistory]:
        result = await db.execute(
            select(LoginHistory)
            .where(LoginHistory.user_id == user_id)
            .order_by(LoginHistory.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
