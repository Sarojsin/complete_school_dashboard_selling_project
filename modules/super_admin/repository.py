"""
Super Admin Repository - Database operations for admin functions

Contains merged repository classes from 11 admin repository files.
Converted to async pattern.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from typing import Optional, List
from modules.super_admin.models import SystemSetting, Feature, SystemFeature, FeatureRolePermission, AuditLog, SystemBackup
from modules.shared.models import User


class UserManagementRepository:
    """User management repository - async"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def deactivate_user(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        if user:
            user.is_active = False
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def count_users_by_role(self):
        result = await self.db.execute(
            select(User.role, func.count(User.id)).group_by(User.role)
        )
        return result.all()

    async def get_user_stats_by_role(self):
        """Get user statistics by role"""
        result = await self.db.execute(
            select(User.role, func.count(User.id)).group_by(User.role)
        )
        rows = result.all()
        return [{"role": r[0].value if hasattr(r[0], 'value') else str(r[0]), "count": r[1]} for r in rows]

    async def get_students_list(self, skip: int = 0, limit: int = 100):
        """Get students list"""
        from modules.school.school_student.models import SchoolStudent
        result = await self.db.execute(
            select(SchoolStudent).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_teachers_list(self, skip: int = 0, limit: int = 100):
        """Get teachers list"""
        from modules.school.school_teacher.models import Teacher
        result = await self.db.execute(
            select(Teacher).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_parents_list(self, skip: int = 0, limit: int = 100):
        """Get parents list"""
        from modules.school.school_parent.models import Parent
        result = await self.db.execute(
            select(Parent).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def toggle_user_active(self, user_id: int):
        """Toggle user active status"""
        user = await self.get_user_by_id(user_id)
        if user:
            user.is_active = not user.is_active
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def reset_password(self, user_id: int):
        """Reset user password to default"""
        from modules.shared.auth_utils import get_password_hash
        user = await self.get_user_by_id(user_id)
        if user:
            # Default password: "password123" - in production, send reset email
            user.hashed_password = get_password_hash("password123")
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def lock_user(self, user_id: int):
        """Lock user account"""
        user = await self.get_user_by_id(user_id)
        if user:
            user.is_active = False
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def change_user_role(self, user_id: int, new_role: str):
        """Change user role"""
        from modules.shared.models import UserRole
        user = await self.get_user_by_id(user_id)
        if user:
            user.role = UserRole(new_role)
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def count_total_users(self):
        result = await self.db.execute(
            select(func.count(User.id))
        )
        return result.scalar()


class SettingsRepository:
    """Settings repository - async"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_setting(self, key: str):
        result = await self.db.execute(
            select(SystemSetting).where(SystemSetting.key == key)
        )
        return result.scalar_one_or_none()

    async def set_setting(self, key: str, value: str):
        setting = await self.get_setting(key)
        if setting:
            setting.value = value
        else:
            setting = SystemSetting(key=key, value=value)
            self.db.add(setting)
        await self.db.commit()
        await self.db.refresh(setting)
        return setting

    async def get_all_settings(self):
        result = await self.db.execute(
            select(SystemSetting)
        )
        return result.scalars().all()


class FeatureRepository:
    """Feature toggle repository - async"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_features(self):
        result = await self.db.execute(
            select(Feature)
        )
        return result.scalars().all()

    async def get_feature(self, name: str):
        result = await self.db.execute(
            select(Feature).where(Feature.name == name)
        )
        return result.scalar_one_or_none()

    async def toggle_feature(self, feature_name: str, enabled: bool):
        feature = await self.get_feature(feature_name)
        if feature:
            feature.is_enabled = enabled
            await self.db.commit()
            await self.db.refresh(feature)
        return feature

    # === Extended System Feature Methods ===
    async def get_all_system_features(self, category: str = None, enabled_only: bool = False):
        """Get all system features with optional filters"""
        query = select(SystemFeature)
        if category:
            query = query.where(SystemFeature.feature_category == category)
        if enabled_only:
            query = query.where(SystemFeature.is_enabled == True)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_system_feature(self, feature_code: str):
        """Get a system feature by code"""
        result = await self.db.execute(
            select(SystemFeature).where(SystemFeature.feature_code == feature_code)
        )
        return result.scalar_one_or_none()

    async def create_system_feature(self, feature_code: str, feature_name: str, feature_category: str, 
                                    description: str = None, is_global: bool = False):
        """Create a new system feature"""
        feature = SystemFeature(
            feature_code=feature_code,
            feature_name=feature_name,
            feature_category=feature_category,
            description=description,
            is_enabled=True,
            is_global=is_global
        )
        self.db.add(feature)
        await self.db.commit()
        await self.db.refresh(feature)
        return feature

    async def update_system_feature(self, feature_code: str, **kwargs):
        """Update a system feature"""
        feature = await self.get_system_feature(feature_code)
        if feature:
            for key, value in kwargs.items():
                if hasattr(feature, key) and value is not None:
                    setattr(feature, key, value)
            await self.db.commit()
            await self.db.refresh(feature)
        return feature

    async def delete_system_feature(self, feature_code: str):
        """Delete a system feature"""
        feature = await self.get_system_feature(feature_code)
        if feature:
            await self.db.delete(feature)
            await self.db.commit()
        return feature

    async def get_feature_categories(self):
        """Get all distinct feature categories"""
        result = await self.db.execute(
            select(SystemFeature.feature_category).distinct()
        )
        return [row[0] for row in result.all()]

    async def get_feature_permissions(self, feature_code: str):
        """Get permissions for a feature"""
        feature = await self.get_system_feature(feature_code)
        if not feature:
            return []
        result = await self.db.execute(
            select(FeatureRolePermission).where(FeatureRolePermission.feature_id == feature.id)
        )
        return result.scalars().all()

    async def update_feature_permission(self, feature_code: str, role: str, 
                                         can_create: bool = False, can_read: bool = True,
                                         can_update: bool = False, can_delete: bool = False):
        """Update or create role permission for a feature"""
        feature = await self.get_system_feature(feature_code)
        if not feature:
            return None
        
        result = await self.db.execute(
            select(FeatureRolePermission).where(
                FeatureRolePermission.feature_id == feature.id,
                FeatureRolePermission.role == role
            )
        )
        permission = result.scalar_one_or_none()
        
        if permission:
            permission.can_create = can_create
            permission.can_read = can_read
            permission.can_update = can_update
            permission.can_delete = can_delete
        else:
            permission = FeatureRolePermission(
                feature_id=feature.id,
                role=role,
                can_create=can_create,
                can_read=can_read,
                can_update=can_update,
                can_delete=can_delete
            )
            self.db.add(permission)
        
        await self.db.commit()
        await self.db.refresh(permission)
        return permission


class AuditRepository:
    """Audit log repository - async"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_action(self, user_id: int, action: str, details: Optional[dict] = None, ip: Optional[str] = None):
        log = AuditLog(user_id=user_id, action=action, details=details, ip_address=ip)
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    async def get_recent_logs(self, limit: int = 100):
        result = await self.db.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        )
        return result.scalars().all()

    async def get_user_login_history(self, user_id: int, limit: int = 50):
        """Get login history for a specific user"""
        result = await self.db.execute(
            select(AuditLog).where(
                AuditLog.action.like("%LOGIN%")
            ).order_by(AuditLog.created_at.desc()).limit(limit)
        )
        return result.scalars().all()


class BackupRepository:
    """Backup repository - async"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_backup(self, filename: str, size: int, status: str = "completed"):
        backup = SystemBackup(filename=filename, size_bytes=size, status=status)
        self.db.add(backup)
        await self.db.commit()
        await self.db.refresh(backup)
        return backup

    async def get_all_backups(self):
        result = await self.db.execute(
            select(SystemBackup).order_by(SystemBackup.created_at.desc())
        )
        return result.scalars().all()


class DashboardRepository:
    """Dashboard statistics repository - async"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_stats(self) -> dict:
        # Total users
        result = await self.db.execute(
            select(func.count(User.id))
        )
        total_users = result.scalar() or 0
        
        # Count by role
        role_result = await self.db.execute(
            select(User.role, func.count(User.id)).group_by(User.role)
        )
        role_dict = {}
        for role, count in role_result.all():
            role_key = str(role.value) if hasattr(role, 'value') else str(role)
            role_dict[role_key] = count
        
        return {
            "total_users": total_users,
            "total_students": role_dict.get("school_student", 0) + role_dict.get("college_student", 0),
            "total_teachers": role_dict.get("school_teacher", 0) + role_dict.get("college_faculty", 0),
            "total_schools": role_dict.get("school_authority", 0),
            "total_colleges": role_dict.get("college_hod", 0) + role_dict.get("college_dean", 0),
            "active_sessions": 0,
            "system_health": "healthy"
        }