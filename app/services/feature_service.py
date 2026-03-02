"""
Feature Service

Business logic for managing system features and permissions.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from app.models.admin_models import SystemFeature, FeatureRolePermission
from app.models.models import User, UserRole
from app.repositories.feature_repository import (
    FeatureRepository,
    FeatureRolePermissionRepository,
    AdminAuditLogRepository
)


class FeatureService:
    """Service for feature management operations"""
    
    @staticmethod
    async def check_feature_enabled(db: AsyncSession, feature_code: str) -> bool:
        """
        Check if a feature is globally enabled.
        
        Args:
            db: Database session
            feature_code: The feature code to check
            
        Returns:
            True if feature is enabled, False if disabled
            
        Note:
            If feature doesn't exist in database, returns True for backward compatibility.
            This allows new features to work without explicit database configuration,
            while existing features must be explicitly enabled.
        """
        feature = await FeatureRepository.get_by_code(db, feature_code)
        if not feature:
            # Feature not found in database - assume enabled for backward compatibility
            # New features work automatically; old features need explicit enablement
            return True
        return feature.is_enabled
    
    @staticmethod
    async def check_role_permission(
        db: AsyncSession, 
        feature_code: str, 
        role: UserRole, 
        action: str
    ) -> bool:
        """
        Check if a role has permission for a specific action on a feature.
        
        Args:
            db: Database session
            feature_code: The feature code
            role: The user role
            action: Action to check (create, read, update, delete)
            
        Returns:
            True if role has permission, False otherwise
        """
        feature = await FeatureRepository.get_by_code(db, feature_code)
        if not feature:
            # Feature not found - assume enabled
            return True
        
        # If feature is global and enabled, allow all roles
        if feature.is_global and feature.is_enabled:
            return True
        
        # Check role-specific permission
        permission = await FeatureRolePermissionRepository.get(db, feature.id, role)
        if not permission:
            # No specific permission - default to read-only
            return action == "read"
        
        return permission.has_permission(action)
    
    @staticmethod
    async def can_access_feature(
        db: AsyncSession,
        feature_code: str,
        user: User,
        action: str = "read"
    ) -> bool:
        """
        Combined check: Is feature enabled AND does user have permission?
        
        Args:
            db: Database session
            feature_code: The feature code
            user: The user trying to access
            action: The action (create, read, update, delete)
            
        Returns:
            True if user can access, False otherwise
        """
        # First check if feature is globally enabled
        if not await FeatureService.check_feature_enabled(db, feature_code):
            return False
        
        # Then check if user's role has permission
        return await FeatureService.check_role_permission(
            db, feature_code, user.role, action
        )
    
    @staticmethod
    async def enforce_feature_access(
        db: AsyncSession,
        feature_code: str,
        user: User,
        action: str = "read"
    ) -> None:
        """
        Enforce feature access - raises exception if not allowed.
        Use this in endpoints to block unauthorized access.
        
        Args:
            db: Database session
            feature_code: The feature code
            user: The user trying to access
            action: The action
            
        Raises:
            HTTPException: If access is denied
        """
        from fastapi import HTTPException, status
        
        can_access = await FeatureService.can_access_feature(db, feature_code, user, action)
        
        if not can_access:
            feature = await FeatureRepository.get_by_code(db, feature_code)
            if feature and not feature.is_enabled:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Feature '{feature_code}' is currently disabled. Contact administrator for access."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You don't have permission to perform this action on '{feature_code}'"
                )
    
    @staticmethod
    async def toggle_feature(
        db: AsyncSession,
        feature_code: str,
        admin_user_id: int,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Toggle a feature on/off.
        
        Args:
            db: Database session
            feature_code: The feature code to toggle
            admin_user_id: ID of admin performing the action
            ip_address: IP address of admin
            
        Returns:
            Dict with success status and new state
        """
        feature = await FeatureRepository.get_by_code(db, feature_code)
        if not feature:
            return {"success": False, "message": "Feature not found"}
        
        old_value = feature.is_enabled
        new_value = not old_value
        
        # Toggle the feature
        await FeatureRepository.toggle(db, feature_code)
        
        # Log the action
        await AdminAuditLogRepository.log_action(
            db=db,
            admin_user_id=admin_user_id,
            action="toggle_feature",
            feature_code=feature_code,
            old_value=str(old_value),
            new_value=str(new_value),
            ip_address=ip_address
        )
        
        return {
            "success": True,
            "message": f"Feature {feature_code} has been {'disabled' if new_value else 'enabled'}",
            "is_enabled": new_value
        }
    
    @staticmethod
    async def get_all_features(
        db: AsyncSession,
        category: Optional[str] = None,
        enabled_only: bool = False
    ) -> List[SystemFeature]:
        """Get all features with optional filtering"""
        return await FeatureRepository.get_all(
            db, 
            category=category,
            enabled_only=enabled_only
        )
    
    @staticmethod
    async def get_feature_by_code(
        db: AsyncSession, 
        feature_code: str
    ) -> Optional[SystemFeature]:
        """Get a single feature by code"""
        return await FeatureRepository.get_by_code(db, feature_code)
    
    @staticmethod
    async def create_feature(
        db: AsyncSession,
        feature_data: Dict[str, Any],
        admin_user_id: int,
        ip_address: Optional[str] = None
    ) -> SystemFeature:
        """Create a new feature"""
        feature = await FeatureRepository.create(db, feature_data)
        
        # Log the action
        await AdminAuditLogRepository.log_action(
            db=db,
            admin_user_id=admin_user_id,
            action="create_feature",
            feature_code=feature.feature_code,
            new_value=str(feature_data),
            ip_address=ip_address
        )
        
        return feature
    
    @staticmethod
    async def update_feature(
        db: AsyncSession,
        feature_code: str,
        updates: Dict[str, Any],
        admin_user_id: int,
        ip_address: Optional[str] = None
    ) -> Optional[SystemFeature]:
        """Update a feature"""
        old_feature = await FeatureRepository.get_by_code(db, feature_code)
        if not old_feature:
            return None
        
        old_value = {
            "is_enabled": old_feature.is_enabled,
            "is_global": old_feature.is_global,
            "description": old_feature.description
        }
        
        feature = await FeatureRepository.update(db, feature_code, updates)
        
        # Log the action
        await AdminAuditLogRepository.log_action(
            db=db,
            admin_user_id=admin_user_id,
            action="update_feature",
            feature_code=feature_code,
            old_value=str(old_value),
            new_value=str(updates),
            ip_address=ip_address
        )
        
        return feature
    
    @staticmethod
    async def delete_feature(
        db: AsyncSession,
        feature_code: str,
        admin_user_id: int,
        ip_address: Optional[str] = None
    ) -> bool:
        """Delete a feature"""
        result = await FeatureRepository.delete(db, feature_code)
        
        if result:
            # Log the action
            await AdminAuditLogRepository.log_action(
                db=db,
                admin_user_id=admin_user_id,
                action="delete_feature",
                feature_code=feature_code,
                old_value="feature_exists",
                new_value=None,
                ip_address=ip_address
            )
        
        return result
    
    @staticmethod
    async def set_role_permission(
        db: AsyncSession,
        feature_code: str,
        role: UserRole,
        permissions: Dict[str, bool],
        admin_user_id: int,
        ip_address: Optional[str] = None
    ) -> Optional[FeatureRolePermission]:
        """Set permissions for a role on a feature"""
        feature = await FeatureRepository.get_by_code(db, feature_code)
        if not feature:
            return None
        
        old_permission = await FeatureRolePermissionRepository.get(db, feature.id, role)
        old_value = None
        if old_permission:
            old_value = {
                "can_create": old_permission.can_create,
                "can_read": old_permission.can_read,
                "can_update": old_permission.can_update,
                "can_delete": old_permission.can_delete
            }
        
        permission = await FeatureRolePermissionRepository.upsert(
            db, feature.id, role, permissions
        )
        
        # Log the action
        await AdminAuditLogRepository.log_action(
            db=db,
            admin_user_id=admin_user_id,
            action="set_role_permission",
            feature_code=feature_code,
            old_value=str(old_value) if old_value else None,
            new_value=str(permissions),
            ip_address=ip_address
        )
        
        return permission
    
    @staticmethod
    async def get_features_by_category(db: AsyncSession) -> Dict[str, List[SystemFeature]]:
        """Get features grouped by category"""
        features = await FeatureRepository.get_all(db)
        categories: Dict[str, List[SystemFeature]] = {}
        
        for feature in features:
            category = feature.feature_category or "uncategorized"
            if category not in categories:
                categories[category] = []
            categories[category].append(feature)
        
        return categories
    
    @staticmethod
    async def get_audit_logs(
        db: AsyncSession,
        feature_code: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List:
        """Get audit logs"""
        if feature_code:
            return await AdminAuditLogRepository.get_by_feature(db, feature_code, limit)
        return await AdminAuditLogRepository.get_all(db, skip=skip, limit=limit)
