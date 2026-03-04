"""
Admin Features API
~~~~~~~~~~~~~~~~~~

Endpoints for managing system features, role permissions, and audit logs.

All schemas live in ``app.api.schemas.admin.features``.
Authentication is handled by the shared ``get_current_admin`` dependency.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_async_db
from app.models.models import User, UserRole
from app.models.admin_models import AdminAuditLog
from app.services.feature_service import FeatureService
from app.repositories.feature_repository import (
    FeatureRepository,
    FeatureRolePermissionRepository,
    AdminAuditLogRepository,
)
from app.api.deps.admin import get_current_admin
from app.api.schemas.admin.features import (
    FeatureCreate,
    FeatureUpdate,
    RolePermissionUpdate,
    RolePermissionsBatchUpdate,
)

router = APIRouter(prefix="/features", tags=["Admin Features"])


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _feature_to_dict(f) -> dict:
    """Serialize a SystemFeature ORM object to a plain dict."""
    return {
        "id": f.id,
        "feature_code": f.feature_code,
        "feature_name": f.feature_name,
        "feature_category": f.feature_category,
        "description": f.description,
        "is_enabled": f.is_enabled,
        "is_global": f.is_global,
    }


def _permission_to_dict(p) -> dict:
    """Serialize a FeatureRolePermission ORM object to a plain dict."""
    return {
        "role": p.role.value if hasattr(p.role, "value") else str(p.role),
        "can_create": p.can_create,
        "can_read": p.can_read,
        "can_update": p.can_update,
        "can_delete": p.can_delete,
    }


# ---------------------------------------------------------------------------
# Feature CRUD
# ---------------------------------------------------------------------------

@router.get("", response_model=dict)
async def get_all_features(
    category: Optional[str] = None,
    enabled_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all system features with optional filtering and pagination."""
    features = await FeatureService.get_all_features(
        db, category=category, enabled_only=enabled_only
    )
    items = features[skip : skip + limit]  # noqa: E203
    return {
        "features": [
            {**_feature_to_dict(f), "role_permissions_count": len(f.role_permissions) if f.role_permissions else 0}
            for f in items
        ],
        "total": len(features),
        "page": skip // limit + 1,
        "per_page": limit,
    }


@router.get("/categories")
async def get_feature_categories(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all distinct feature category names."""
    categories = await FeatureRepository.get_categories(db)
    return {"categories": categories}


@router.get("/category/{category}")
async def get_features_by_category(
    category: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return features filtered by category."""
    features = await FeatureService.get_all_features(db, category=category)
    return {
        "category": category,
        "features": [_feature_to_dict(f) for f in features],
    }


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_feature(
    feature: FeatureCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Create a new system feature."""
    existing = await FeatureRepository.get_by_code(db, feature.feature_code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Feature with code '{feature.feature_code}' already exists",
        )

    client_ip = request.client.host if request.client else None
    new_feature = await FeatureService.create_feature(
        db, feature.model_dump(), current_user.id, ip_address=client_ip
    )
    return {
        "id": new_feature.id,
        "feature_code": new_feature.feature_code,
        "feature_name": new_feature.feature_name,
        "message": "Feature created successfully",
    }


@router.get("/{feature_code}")
async def get_feature(
    feature_code: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return a single feature by its code, including role permissions."""
    feature = await FeatureRepository.get_by_code(db, feature_code)
    if not feature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Feature '{feature_code}' not found")

    return {
        **_feature_to_dict(feature),
        "role_permissions": [_permission_to_dict(p) for p in (feature.role_permissions or [])],
    }


@router.put("/{feature_code}")
async def update_feature(
    feature_code: str,
    updates: FeatureUpdate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update one or more fields of an existing feature."""
    update_data = updates.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid update data provided")

    client_ip = request.client.host if request.client else None
    feature = await FeatureService.update_feature(
        db, feature_code, update_data, current_user.id, ip_address=client_ip
    )
    if not feature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Feature '{feature_code}' not found")

    return {
        "message": "Feature updated successfully",
        "feature": {
            "id": feature.id,
            "feature_code": feature.feature_code,
            "feature_name": feature.feature_name,
            "is_enabled": feature.is_enabled,
            "is_global": feature.is_global,
        },
    }


@router.delete("/{feature_code}")
async def delete_feature(
    feature_code: str,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Permanently delete a feature and its associated permissions."""
    client_ip = request.client.host if request.client else None
    deleted = await FeatureService.delete_feature(
        db, feature_code, current_user.id, ip_address=client_ip
    )
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Feature '{feature_code}' not found")

    return {"message": f"Feature '{feature_code}' deleted successfully"}


# ---------------------------------------------------------------------------
# Toggle
# ---------------------------------------------------------------------------

@router.post("/{feature_code}/toggle")
async def toggle_feature(
    feature_code: str,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Toggle a feature on/off and return the new state."""
    client_ip = request.client.host if request.client else None
    result = await FeatureService.toggle_feature(
        db, feature_code, current_user.id, ip_address=client_ip
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Feature not found"),
        )
    return result


# ---------------------------------------------------------------------------
# Role Permissions
# ---------------------------------------------------------------------------

@router.get("/{feature_code}/permissions")
async def get_feature_permissions(
    feature_code: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all role permissions for a specific feature."""
    feature = await FeatureRepository.get_by_code(db, feature_code)
    if not feature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Feature '{feature_code}' not found")

    permissions = await FeatureRolePermissionRepository.get_by_feature(db, feature.id)
    return {
        "feature_code": feature_code,
        "feature_name": feature.feature_name,
        "permissions": [_permission_to_dict(p) for p in permissions],
    }


@router.put("/{feature_code}/permissions")
async def update_role_permissions(
    feature_code: str,
    permissions: List[RolePermissionUpdate],
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update permissions for a list of roles on a specific feature."""
    feature = await FeatureRepository.get_by_code(db, feature_code)
    if not feature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Feature '{feature_code}' not found")

    client_ip = request.client.host if request.client else None
    updated = []

    for perm in permissions:
        try:
            role = UserRole(perm.role)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role: '{perm.role}'",
            )
        perm_data = {"can_create": perm.can_create, "can_read": perm.can_read,
                     "can_update": perm.can_update, "can_delete": perm.can_delete}
        result = await FeatureService.set_role_permission(
            db, feature_code, role, perm_data, current_user.id, ip_address=client_ip
        )
        if result:
            updated.append({"role": perm.role, "status": "updated"})

    return {"message": f"Updated permissions for {len(updated)} roles", "permissions": updated}


@router.post("/{feature_code}/permissions")
async def batch_update_role_permissions(
    feature_code: str,
    update_data: RolePermissionsBatchUpdate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Batch-update role permissions for a feature (UI-compatible endpoint)."""
    feature = await FeatureRepository.get_by_code(db, feature_code)
    if not feature:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Feature '{feature_code}' not found")

    client_ip = request.client.host if request.client else None
    updated_count = 0

    for role_name, perms in update_data.roles.items():
        try:
            role = UserRole(role_name)
        except ValueError:
            continue  # skip unknown roles silently in batch mode

        await FeatureService.set_role_permission(
            db, feature_code, role, perms, current_user.id, ip_address=client_ip
        )
        updated_count += 1

    return {"message": f"Updated permissions for {updated_count} roles", "status": "success"}


# ---------------------------------------------------------------------------
# Audit Logs
# ---------------------------------------------------------------------------

@router.get("/audit-logs")
async def get_audit_logs(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return paginated admin audit logs."""
    logs = await AdminAuditLogRepository.get_all(db, skip=skip, limit=limit)
    return {
        "logs": [
            {
                "id": log.id,
                "admin_user_id": log.admin_user_id,
                "action": log.action,
                "feature_code": log.feature_code,
                "old_value": log.old_value,
                "new_value": log.new_value,
                "ip_address": log.ip_address,
                "timestamp": log.timestamp.isoformat() if log.timestamp else None,
            }
            for log in logs
        ],
        "total": len(logs),
    }


@router.get("/audit-logs/feature/{feature_code}")
async def get_feature_audit_logs(
    feature_code: str,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return audit logs scoped to a specific feature code."""
    logs = await AdminAuditLogRepository.get_by_feature(db, feature_code, limit)
    return {
        "feature_code": feature_code,
        "logs": [
            {
                "id": log.id,
                "admin_user_id": log.admin_user_id,
                "action": log.action,
                "old_value": log.old_value,
                "new_value": log.new_value,
                "ip_address": log.ip_address,
                "timestamp": log.timestamp.isoformat() if log.timestamp else None,
            }
            for log in logs
        ],
    }
