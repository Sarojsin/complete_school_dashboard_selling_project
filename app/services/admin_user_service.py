from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User, UserRole, Student, Teacher, Parent
from app.repositories.user_repository import UserRepository
from app.repositories.admin_user_repository import AdminUserRepository
from app.core.exceptions import NotFoundError, ValidationError, ForbiddenError
from app.api.deps.admin import hash_password
from app.api.schemas.admin.users import ChangeRoleRequest, PasswordResetRequest, UserResponse


class AdminUserService:
    """Business logic for admin user management."""

    @staticmethod
    async def get_user_or_404(db: AsyncSession, user_id: int) -> User:
        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    @staticmethod
    async def get_all_users(
        db: AsyncSession, role: Optional[str], is_active: Optional[bool],
        search: Optional[str], skip: int, limit: int
    ) -> List[User]:
        return await AdminUserRepository.get_users_list(db, role, is_active, search, skip, limit)

    @staticmethod
    async def toggle_user_active(db: AsyncSession, user_id: int, current_user_id: int) -> Dict[str, Any]:
        if user_id == current_user_id:
            raise ValidationError("Cannot deactivate your own account")

        user = await AdminUserService.get_user_or_404(db, user_id)
        user.is_active = not user.is_active
        await db.commit()

        action = "activated" if user.is_active else "deactivated"
        return {"success": True, "message": f"User {action} successfully", "is_active": user.is_active}

    @staticmethod
    async def reset_user_password(db: AsyncSession, user_id: int, request: PasswordResetRequest) -> Dict[str, Any]:
        user = await AdminUserService.get_user_or_404(db, user_id)
        user.hashed_password = hash_password(request.new_password)
        await db.commit()
        return {"success": True, "message": "Password reset successfully"}

    @staticmethod
    async def change_user_role(db: AsyncSession, user_id: int, request: ChangeRoleRequest) -> Dict[str, Any]:
        user = await AdminUserService.get_user_or_404(db, user_id)
        try:
            user.role = UserRole(request.new_role)
        except ValueError:
            raise ValidationError(f"Invalid role '{request.new_role}'")

        await db.commit()
        return {"success": True, "message": f"Role changed to '{request.new_role}'", "new_role": request.new_role}

    @staticmethod
    async def lock_user_account(
        db: AsyncSession,
        user_id: int,
        current_admin_id: int,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        if user_id == current_admin_id:
            raise ValidationError("Cannot lock your own account")

        user = await AdminUserService.get_user_or_404(db, user_id)
        await AdminUserRepository.set_user_lock(
            db=db,
            user_id=user_id,
            lock=True,
            admin_user_id=current_admin_id,
            reason=reason,
        )
        # Keep existing auth behavior consistent by marking locked user inactive.
        user.is_active = False
        await db.commit()
        return {"success": True, "message": "Account locked successfully", "user_id": user_id}

    @staticmethod
    async def force_logout_user(
        db: AsyncSession,
        user_id: int,
        current_admin_id: int,
    ) -> Dict[str, Any]:
        await AdminUserService.get_user_or_404(db, user_id)
        await AdminUserRepository.mark_force_logout(
            db=db,
            user_id=user_id,
            admin_user_id=current_admin_id,
        )
        await db.commit()
        return {"success": True, "message": "User has been force logged out", "user_id": user_id}

    @staticmethod
    async def get_login_history(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
    ) -> Dict[str, Any]:
        await AdminUserService.get_user_or_404(db, user_id)
        logs = await AdminUserRepository.get_login_history_for_user(db, user_id, skip, limit)
        return {
            "user_id": user_id,
            "items": [
                {
                    "id": entry.id,
                    "username": entry.username,
                    "success": entry.success,
                    "ip_address": entry.ip_address,
                    "user_agent": entry.user_agent,
                    "failure_reason": entry.failure_reason,
                    "token_issued_at": entry.token_issued_at.isoformat() if entry.token_issued_at else None,
                    "created_at": entry.created_at.isoformat() if entry.created_at else None,
                }
                for entry in logs
            ],
            "count": len(logs),
        }

    @staticmethod
    async def get_user_stats_by_role(db: AsyncSession) -> Dict[str, Any]:
        totals, actives = await AdminUserRepository.get_user_stats_by_role(db)
        return {
            role.value: {
                "total":    totals.get(role, 0),
                "active":   actives.get(role, 0),
                "inactive": totals.get(role, 0) - actives.get(role, 0),
            }
            for role in UserRole
        }

    @staticmethod
    async def get_students_list(
        db: AsyncSession, grade: Optional[str], search: Optional[str], skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        students = await AdminUserRepository.get_students_list(db, grade, search, skip, limit)
        return [
            {
                "id": s.id,
                "student_id": s.student_id,
                "full_name": s.full_name,
                "grade_level": s.grade_level,
                "section": s.section,
                "parent_name": s.parent_name,
                "enrollment_date": s.enrollment_date.isoformat() if s.enrollment_date else None,
            }
            for s in students
        ]

    @staticmethod
    async def get_teachers_list(
        db: AsyncSession, department: Optional[str], search: Optional[str], skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        teachers = await AdminUserRepository.get_teachers_list(db, department, search, skip, limit)
        return [
            {
                "id": t.id,
                "employee_id": t.employee_id,
                "full_name": t.full_name,
                "department": t.department,
                "qualification": t.qualification,
                "status": t.status,
            }
            for t in teachers
        ]

    @staticmethod
    async def get_parents_list(
        db: AsyncSession, search: Optional[str], skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        parents = await AdminUserRepository.get_parents_list(db, search, skip, limit)
        return [
            {
                "id": p.id,
                "full_name": p.full_name,
                "phone": p.phone,
                "occupation": p.occupation,
                "children_count": len(p.children) if p.children else 0,
            }
            for p in parents
        ]
