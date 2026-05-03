"""
Feature Repository

Handles database operations for system features, role permissions, and audit logs.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from datetime import datetime

from backup.models.admin_models import SystemFeature, FeatureRolePermission, AdminAuditLog
from backup.models.models import UserRole


class FeatureRepository:
    """Repository for managing system features"""
    
    @staticmethod
    async def create(db: AsyncSession, feature_data: Dict[str, Any]) -> SystemFeature:
        """Create a new feature"""
        feature = SystemFeature(**feature_data)
        db.add(feature)
        await db.commit()
        await db.refresh(feature)
        return feature
    
    @staticmethod
    async def get_by_id(db: AsyncSession, feature_id: int) -> Optional[SystemFeature]:
        """Get feature by ID"""
        result = await db.execute(
            select(SystemFeature)
            .options(selectinload(SystemFeature.role_permissions))
            .filter(SystemFeature.id == feature_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_by_code(db: AsyncSession, feature_code: str) -> Optional[SystemFeature]:
        """Get feature by code"""
        result = await db.execute(
            select(SystemFeature)
            .options(selectinload(SystemFeature.role_permissions))
            .filter(SystemFeature.feature_code == feature_code)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_all(
        db: AsyncSession, 
        category: Optional[str] = None,
        enabled_only: bool = False,
        skip: int = 0, 
        limit: int = 100
    ) -> List[SystemFeature]:
        """Get all features with optional filtering"""
        query = select(SystemFeature).options(selectinload(SystemFeature.role_permissions))
        
        if category:
            query = query.filter(SystemFeature.feature_category == category)
        
        if enabled_only:
            query = query.filter(SystemFeature.is_enabled == True)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def get_categories(db: AsyncSession) -> List[str]:
        """Get all unique feature categories"""
        result = await db.execute(
            select(SystemFeature.feature_category)
            .distinct()
            .where(SystemFeature.feature_category.isnot(None))
        )
        return [row[0] for row in result.all() if row[0]]
    
    @staticmethod
    async def update(
        db: AsyncSession, 
        feature_code: str, 
        updates: Dict[str, Any]
    ) -> Optional[SystemFeature]:
        """Update a feature"""
        feature = await FeatureRepository.get_by_code(db, feature_code)
        if not feature:
            return None
        
        for key, value in updates.items():
            if hasattr(feature, key):
                setattr(feature, key, value)
        
        feature.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(feature)
        return feature
    
    @staticmethod
    async def delete(db: AsyncSession, feature_code: str) -> bool:
        """Delete a feature"""
        feature = await FeatureRepository.get_by_code(db, feature_code)
        if not feature:
            return False
        
        await db.delete(feature)
        await db.commit()
        return True
    
    @staticmethod
    async def toggle(db: AsyncSession, feature_code: str) -> Optional[SystemFeature]:
        """Toggle feature enabled/disabled"""
        feature = await FeatureRepository.get_by_code(db, feature_code)
        if not feature:
            return None
        
        # Get actual boolean value from the column
        is_enabled = bool(feature.is_enabled) if feature.is_enabled is not None else False
        feature.is_enabled = not is_enabled
        feature.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(feature)
        return feature
    
    @staticmethod
    async def get_enabled_count(db: AsyncSession) -> int:
        """Get count of enabled features"""
        from sqlalchemy import func
        result = await db.execute(
            select(func.count(SystemFeature.id)).where(SystemFeature.is_enabled == True)
        )
        return result.scalar() or 0
    
    @staticmethod
    async def get_total_count(db: AsyncSession) -> int:
        """Get total count of features"""
        from sqlalchemy import func
        result = await db.execute(
            select(func.count(SystemFeature.id))
        )
        return result.scalar() or 0


class FeatureRolePermissionRepository:
    """Repository for managing role permissions on features"""
    
    @staticmethod
    async def create(db: AsyncSession, permission_data: Dict[str, Any]) -> FeatureRolePermission:
        """Create a new role permission"""
        permission = FeatureRolePermission(**permission_data)
        db.add(permission)
        await db.commit()
        await db.refresh(permission)
        return permission
    
    @staticmethod
    async def get(
        db: AsyncSession, 
        feature_id: int, 
        role: UserRole
    ) -> Optional[FeatureRolePermission]:
        """Get permission for a feature and role"""
        result = await db.execute(
            select(FeatureRolePermission).filter(
                and_(
                    FeatureRolePermission.feature_id == feature_id,
                    FeatureRolePermission.role == role
                )
            )
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_by_feature(db: AsyncSession, feature_id: int) -> List[FeatureRolePermission]:
        """Get all permissions for a feature"""
        result = await db.execute(
            select(FeatureRolePermission).filter(
                FeatureRolePermission.feature_id == feature_id
            )
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def upsert(
        db: AsyncSession,
        feature_id: int,
        role: UserRole,
        permissions: Dict[str, bool]
    ) -> FeatureRolePermission:
        """Create or update permission"""
        existing = await FeatureRolePermissionRepository.get(db, feature_id, role)
        
        if existing:
            for key, value in permissions.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            await db.commit()
            await db.refresh(existing)
            return existing
        else:
            permission_data = {
                "feature_id": feature_id,
                "role": role,
                **permissions
            }
            return await FeatureRolePermissionRepository.create(db, permission_data)
    
    @staticmethod
    async def delete(db: AsyncSession, feature_id: int, role: UserRole) -> bool:
        """Delete a role permission"""
        permission = await FeatureRolePermissionRepository.get(db, feature_id, role)
        if not permission:
            return False
        
        await db.delete(permission)
        await db.commit()
        return True


class AdminAuditLogRepository:
    """Repository for managing admin audit logs"""
    
    @staticmethod
    async def create(db: AsyncSession, log_data: Dict[str, Any]) -> AdminAuditLog:
        """Create a new audit log entry"""
        log_entry = AdminAuditLog(**log_data)
        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        return log_entry
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        admin_user_id: Optional[int] = None,
        feature_code: Optional[str] = None,
        action: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AdminAuditLog]:
        """Get audit logs with optional filtering"""
        query = select(AdminAuditLog).order_by(AdminAuditLog.timestamp.desc())
        
        if admin_user_id:
            query = query.filter(AdminAuditLog.admin_user_id == admin_user_id)
        
        if feature_code:
            query = query.filter(AdminAuditLog.feature_code == feature_code)
        
        if action:
            query = query.filter(AdminAuditLog.action == action)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def get_by_feature(
        db: AsyncSession, 
        feature_code: str,
        limit: int = 50
    ) -> List[AdminAuditLog]:
        """Get audit logs for a specific feature"""
        result = await db.execute(
            select(AdminAuditLog)
            .filter(AdminAuditLog.feature_code == feature_code)
            .order_by(AdminAuditLog.timestamp.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def log_action(
        db: AsyncSession,
        admin_user_id: int,
        action: str,
        feature_code: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> AdminAuditLog:
        """Helper to log an admin action"""
        log_data = {
            "admin_user_id": admin_user_id,
            "action": action,
            "feature_code": feature_code,
            "old_value": old_value,
            "new_value": new_value,
            "ip_address": ip_address
        }
        return await AdminAuditLogRepository.create(db, log_data)
