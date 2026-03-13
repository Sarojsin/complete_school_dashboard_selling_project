"""
Admin System Monitoring API
~~~~~~~~~~~~~~~~~~~~~~~~~~~

API endpoints for monitoring server status, database health, active users, and performance.

Strict Layered Architecture enforced:
- Validation is handled by Pydantic models.
- Core business logic flows exclusively through `AdminSystemService`.
- No direct database manipulations in the routing layer.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models.models import User
from app.api.deps.admin import get_current_admin
from app.services.admin_system_service import AdminSystemService

router = APIRouter(prefix="/admin/system", tags=["Admin System"])


@router.get("/status")
async def get_server_status(current_user: User = Depends(get_current_admin)):
    """Get server status and health metrics"""
    return await AdminSystemService.get_server_status()


@router.get("/database/health")
async def get_database_health(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Check database health"""
    return await AdminSystemService.get_database_health(db)


@router.get("/users/online")
async def get_active_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get currently active users (logged in recently)"""
    return await AdminSystemService.get_active_users(db)


@router.get("/performance")
async def get_performance_metrics(current_user: User = Depends(get_current_admin)):
    """Get API performance metrics"""
    return await AdminSystemService.get_performance_metrics()


@router.get("/backup/status")
async def get_backup_status(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get backup status"""
    return await AdminSystemService.get_backup_status(db)


@router.get("/security/status")
async def get_security_status(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get security status"""
    return await AdminSystemService.get_security_status(db)


@router.get("/dashboard")
async def get_system_dashboard(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get comprehensive system dashboard"""
    return await AdminSystemService.get_system_dashboard(db)
