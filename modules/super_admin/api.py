"""
Super Admin API Routes - System-wide administrative endpoints

Contains all admin routes merged from 15 admin endpoint files.
Converted to async pattern.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_super_admin
from modules.shared.models import User
from modules.super_admin.service import SuperAdminService
from modules.super_admin.schemas import (
    SystemSettingUpdate, FeatureToggle, DashboardStats, 
    FeatureCreate, FeatureUpdate, FeatureResponse, FeatureWithPermissionsResponse,
    RolePermissionUpdate, OverviewResponse, FeaturesSummaryResponse, AnalyticsResponse
)

router = APIRouter(prefix="/admin", tags=["Super Admin"])


async def get_service(db: AsyncSession = Depends(get_db)):
    return SuperAdminService(db)


# ── Dashboard ─────────────────────────────────────────
@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get dashboard statistics"""
    return await service.get_dashboard_stats()


@router.get("/users/stats/by-role")
async def get_user_stats_by_role(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get user statistics by role"""
    return await service.get_user_stats_by_role()


@router.get("/users/students/list")
async def get_students_list(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get students list"""
    return await service.get_students_list(skip, limit)


@router.get("/users/teachers/list")
async def get_teachers_list(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get teachers list"""
    return await service.get_teachers_list(skip, limit)


@router.get("/users/parents/list")
async def get_parents_list(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get parents list"""
    return await service.get_parents_list(skip, limit)


@router.patch("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Toggle user active status"""
    return await service.toggle_user_active(user_id, current_user.id)


@router.post("/users/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Reset user password"""
    return await service.reset_user_password(user_id, current_user.id)


@router.post("/users/{user_id}/lock")
async def lock_user_account(
    user_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Lock user account"""
    return await service.lock_user_account(user_id, current_user.id)


@router.post("/users/{user_id}/force-logout")
async def force_logout_user(
    user_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Force logout user"""
    return await service.force_logout_user(user_id, current_user.id)


@router.get("/users/{user_id}/login-history")
async def get_user_login_history(
    user_id: int,
    limit: int = 50,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get user login history"""
    return await service.get_user_login_history(user_id, limit)


@router.post("/users/{user_id}/change-role")
async def change_user_role(
    user_id: int,
    new_role: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Change user role"""
    return await service.change_user_role(user_id, new_role, current_user.id)


# ── User Management ───────────────────────────────────
@router.get("/users")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """List all users"""
    return await service.list_all_users(skip, limit)


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get user by ID"""
    return await service.get_user(user_id)


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Deactivate a user"""
    return await service.deactivate_user(user_id, current_user.id)


@router.get("/users-by-role")
async def get_users_by_role(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get user count by role"""
    return await service.get_users_by_role()


# ── Settings ──────────────────────────────────────────
@router.get("/settings")
async def list_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """List all system settings"""
    return await service.get_all_settings()


@router.get("/settings/{key}")
async def get_setting(
    key: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get a specific setting"""
    return await service.get_setting(key)


@router.put("/settings/{key}")
async def update_setting(
    key: str,
    data: SystemSettingUpdate,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update a system setting"""
    return await service.update_setting(key, data.value, current_user.id)


# ── Features ───────────────────────────────────────────
@router.get("/features")
async def list_features(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """List all features"""
    return await service.list_features()


@router.put("/features/{name}/toggle")
async def toggle_feature(
    name: str,
    data: FeatureToggle,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Toggle a feature"""
    return await service.toggle_feature(name, data.is_enabled, int(current_user.id))


# ── System Features (Extended) ─────────────────────────────
@router.get("/system-features", response_model=dict)
async def list_system_features(
    category: Optional[str] = None,
    enabled_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Return all system features with optional filtering and pagination."""
    features = await service.list_system_features(category, enabled_only)
    items = features[skip : skip + limit]
    return {
        "features": [
            {
                "id": f.id,
                "feature_code": f.feature_code,
                "feature_name": f.feature_name,
                "feature_category": f.feature_category,
                "description": f.description,
                "is_enabled": f.is_enabled,
                "is_global": f.is_global,
            }
            for f in items
        ],
        "total": len(features),
        "page": skip // limit + 1,
        "per_page": limit,
    }


@router.get("/system-features/categories")
async def get_feature_categories(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Return all distinct feature category names."""
    categories = await service.get_feature_categories()
    return {"categories": categories}


@router.get("/system-features/{feature_code}", response_model=FeatureResponse)
async def get_system_feature(
    feature_code: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get a system feature by code"""
    feature = await service.get_system_feature(feature_code)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature


@router.post("/system-features", response_model=FeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_system_feature(
    data: FeatureCreate,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Create a new system feature"""
    feature = await service.create_system_feature(
        data=data.model_dump(),
        admin_id=int(current_user.id)
    )
    return feature


@router.put("/system-features/{feature_code}", response_model=FeatureResponse)
async def update_system_feature(
    feature_code: str,
    data: FeatureUpdate,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update a system feature"""
    feature = await service.update_system_feature(
        feature_code, 
        data.model_dump(exclude_unset=True),
        int(current_user.id)
    )
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature


@router.delete("/system-features/{feature_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_feature(
    feature_code: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Delete a system feature"""
    await service.delete_system_feature(feature_code, int(current_user.id))


@router.get("/system-features/{feature_code}/permissions")
async def get_feature_permissions(
    feature_code: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get permissions for a feature"""
    permissions = await service.get_feature_permissions(feature_code)
    return {
        "permissions": [
            {
                "role": p.role,
                "can_create": p.can_create,
                "can_read": p.can_read,
                "can_update": p.can_update,
                "can_delete": p.can_delete,
            }
            for p in permissions
        ]
    }


@router.put("/system-features/{feature_code}/permissions")
async def update_feature_permission(
    feature_code: str,
    data: RolePermissionUpdate,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update role permission for a feature"""
    result = await service.update_feature_permission(
        feature_code,
        data.role,
        data.can_create,
        data.can_read,
        data.can_update,
        data.can_delete,
        int(current_user.id)
    )
    return {"message": "Permission updated", "feature_code": feature_code}


# ── Audit Logs ────────────────────────────────────────
@router.get("/audit-logs")
async def audit_logs(
    limit: int = Query(100, le=500),
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get audit logs"""
    return await service.get_audit_logs(limit)


# ── Backups ───────────────────────────────────────────
@router.get("/backups")
async def list_backups(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """List all backups"""
    return await service.list_backups()


@router.post("/backups")
async def create_backup(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Create a new backup"""
    return await service.create_backup(current_user.id)


__all__ = ["router"]


# ── Admin Settings Extended ─────────────────────────────


@router.get("/settings/general")
async def get_general_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get general settings"""
    return await service.get_general_settings()


@router.patch("/settings/general")
async def update_general_settings(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update general settings"""
    return await service.update_general_settings(settings, current_user.id)


@router.get("/settings/academic")
async def get_academic_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get academic settings"""
    return await service.get_academic_settings()


@router.patch("/settings/academic")
async def update_academic_settings(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update academic settings"""
    return await service.update_academic_settings(settings, current_user.id)


@router.get("/settings/localization")
async def get_localization_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get localization settings"""
    return await service.get_localization_settings()


@router.patch("/settings/localization")
async def update_localization_settings(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update localization settings"""
    return await service.update_localization_settings(settings, current_user.id)


@router.get("/settings/smtp")
async def get_smtp_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get SMTP settings"""
    return await service.get_smtp_settings()


@router.patch("/settings/smtp")
async def update_smtp_settings(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update SMTP settings"""
    return await service.update_smtp_settings(settings, current_user.id)



@router.post("/settings/smtp/test")
async def test_smtp_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Test SMTP settings"""
    return await service.test_smtp_settings(current_user.id)


@router.get("/settings/payment")
async def get_payment_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get payment settings"""
    return await service.get_payment_settings()


@router.patch("/settings/payment")
async def update_payment_settings(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update payment settings"""
    return await service.update_payment_settings(settings, current_user.id)


@router.get("/settings/notifications")
async def get_notification_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get notification settings"""
    return await service.get_notification_settings()


@router.patch("/settings/notifications")
async def update_notification_settings(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update notification settings"""
    return await service.update_notification_settings(settings, current_user.id)


@router.get("/settings/features")
async def get_feature_toggles(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get feature toggles"""
    return await service.get_feature_toggles()



@router.patch("/settings/features")
async def update_feature_toggles(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update feature toggles"""
    return await service.update_feature_toggles(settings, current_user.id)


# ── Admin Security Extended ───────────────────────────────


@router.get("/security/settings")
async def get_security_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get security settings"""
    return await service.get_security_settings()


@router.patch("/security/settings")
async def update_security_settings(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update security settings"""
    return await service.update_security_settings(settings, current_user.id)


@router.get("/security/jwt")
async def get_jwt_settings(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get JWT settings"""
    return await service.get_jwt_settings()



@router.patch("/security/jwt")
async def update_jwt_settings(
    settings: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update JWT settings"""
    return await service.update_jwt_settings(settings, current_user.id)


@router.get("/security/ip-whitelist")
async def get_ip_whitelist(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get IP whitelist"""
    return await service.get_ip_whitelist()


@router.post("/security/ip-whitelist")
async def add_ip_to_whitelist(
    ip_address: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Add IP to whitelist"""
    return await service.add_ip_to_whitelist(ip_address, current_user.id)


@router.delete("/security/ip-whitelist/{ip_id}")
async def remove_ip_from_whitelist(
    ip_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Remove IP from whitelist"""
    return await service.remove_ip_from_whitelist(ip_id, current_user.id)


@router.get("/security/password-policy")
async def get_password_policy(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get password policy"""
    return await service.get_password_policy()



@router.patch("/security/password-policy")
async def update_password_policy(
    policy: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update password policy"""
    return await service.update_password_policy(policy, current_user.id)


@router.get("/security/failed-logins")
async def get_failed_logins(
    limit: int = Query(50, le=200),
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get failed login attempts"""
    return await service.get_failed_logins(limit)


@router.post("/security/unlock-account/{user_id}")
async def unlock_user_account(
    user_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Unlock user account"""
    return await service.unlock_user_account(user_id, current_user.id)


@router.get("/security/2fa/status")
async def get_2fa_status(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get 2FA status"""
    return await service.get_2fa_status()


@router.post("/security/2fa/enable")
async def enable_2fa(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Enable 2FA"""
    return await service.enable_2fa(current_user.id)


@router.post("/security/2fa/disable")
async def disable_2fa(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Disable 2FA"""
    return await service.disable_2fa(current_user.id)


@router.get("/security/sessions")
async def get_active_sessions(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get active sessions"""
    return await service.get_active_sessions()


@router.delete("/security/sessions/{session_id}")
async def invalidate_session(
    session_id: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Invalidate session"""
    return await service.invalidate_session(session_id, current_user.id)


@router.delete("/security/sessions/user/{user_id}")
async def force_logout_user(
    user_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Force logout user"""
    return await service.force_logout_user(user_id, current_user.id)


@router.get("/security/dashboard")
async def get_security_dashboard(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get security dashboard"""
    return await service.get_security_dashboard(current_user.id)


# ── Admin Reports Extended ───────────────────────────────


@router.get("/reports/attendance/students")
async def get_attendance_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get student attendance report"""
    return await service.get_attendance_report(start_date, end_date)


@router.get("/reports/fees/due")
async def get_fee_due_report(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get fee due report"""
    return await service.get_fee_due_report()


@router.get("/reports/teachers/performance")
async def get_teacher_performance_report(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get teacher performance report"""
    return await service.get_teacher_performance_report()


@router.get("/reports/exams/performance")
async def get_exam_performance_report(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get exam performance report"""
    return await service.get_exam_performance_report()


@router.get("/reports/library/overdue")
async def get_library_overdue_report(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get library overdue report"""
    return await service.get_library_overdue_report()



@router.get("/reports/finance/summary")
async def get_finance_report(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get financial report"""
    return await service.get_finance_report()


@router.get("/reports/export/csv")
async def export_report_csv(
    report_type: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Export report as CSV"""
    return await service.export_report_csv(report_type)


@router.get("/reports/export/pdf")
async def export_report_pdf(
    report_type: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Export report as PDF"""
    return await service.export_report_pdf(report_type)


@router.get("/reports/comprehensive")
async def get_comprehensive_report(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get comprehensive report"""
    return await service.get_comprehensive_report()


# ── Admin Backup Extended ────────────────────────────────


@router.get("/backups/{backup_id}/download")
async def download_backup(
    backup_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Download backup"""
    return await service.download_backup(backup_id, current_user.id)


@router.post("/backups/{backup_id}/restore")
async def restore_backup(
    backup_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Restore backup"""
    return await service.restore_backup(backup_id, current_user.id)


@router.delete("/backups/{backup_id}")
async def delete_backup(
    backup_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Delete backup"""
    return await service.delete_backup(backup_id, current_user.id)


@router.get("/backups/schedule")
async def get_backup_schedule(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get backup schedule"""
    return await service.get_backup_schedule()


@router.patch("/backups/schedule")
async def update_backup_schedule(
    schedule: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update backup schedule"""
    return await service.update_backup_schedule(schedule, current_user.id)


@router.get("/backups/status")
async def get_backup_status(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get backup status"""
    return await service.get_backup_status()


@router.post("/backups/export")
async def export_data(
    export_type: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Export data"""
    return await service.export_data(export_type, current_user.id)


@router.post("/backups/import")
async def import_data(
    import_type: str,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Import data"""
    return await service.import_data(import_type, current_user.id)


# ── Exam Management (Admin) ─────────────────────────────


@router.get("/exam/types")
async def get_exam_types(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get available exam types"""
    return await service.get_exam_types()


@router.get("/exam/grading-scale")
async def get_grading_scale(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get grading scale"""
    return await service.get_grading_scale()


@router.get("/exam/results")
async def get_exam_results(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get exam results"""
    return await service.get_exam_results(skip, limit)


@router.post("/exam/results/publish")
async def publish_results(
    exam_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Publish exam results"""
    return await service.publish_exam_results(exam_id, current_user.id)


@router.post("/exam/results/unpublish")
async def unpublish_results(
    exam_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Unpublish exam results"""
    return await service.unpublish_exam_results(exam_id, current_user.id)


@router.get("/exam/notices")
async def get_exam_notices(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get exam notices"""
    return await service.get_exam_notices()


@router.post("/exam/notices")
async def create_exam_notice(
    notice_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Create exam notice"""
    return await service.create_exam_notice(notice_data, current_user.id)


@router.get("/exam/stats")
async def get_exam_stats(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get exam statistics"""
    return await service.get_exam_stats()


@router.get("/exam/report-card/{student_id}")
async def generate_report_card(
    student_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Generate report card for student"""
    return await service.generate_report_card(student_id)


# ── Finance Management (Admin) ─────────────────────────


@router.get("/finance/structures")
async def get_fee_structures(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get fee structures"""
    return await service.get_fee_structures(skip, limit)


@router.post("/finance/structures")
async def create_fee_structure(
    structure_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Create fee structure"""
    return await service.create_fee_structure(structure_data, current_user.id)


@router.patch("/finance/structures/{structure_id}")
async def update_fee_structure(
    structure_id: int,
    structure_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update fee structure"""
    return await service.update_fee_structure(structure_id, structure_data, current_user.id)


@router.get("/finance/records")
async def get_fee_records(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get fee records"""
    return await service.get_fee_records(skip, limit)


@router.post("/finance/records/pay")
async def record_payment(
    payment_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Record payment"""
    return await service.record_payment(payment_data, current_user.id)


@router.post("/finance/records/refund")
async def refund_payment(
    record_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Refund payment"""
    return await service.refund_payment(record_id, current_user.id)


@router.post("/finance/penalty/apply")
async def apply_late_penalty(
    student_id: int,
    penalty_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Apply late penalty"""
    return await service.apply_late_penalty(student_id, penalty_data, current_user.id)


@router.get("/finance/reports/summary")
async def get_financial_summary(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get financial summary"""
    return await service.get_financial_summary()


@router.get("/finance/reports/export")
async def export_financial_report(
    format: str = "csv",
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Export financial report"""
    return await service.export_financial_report(format)



@router.get("/finance/invoice/{record_id}")
async def generate_invoice(
    record_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Generate invoice"""
    return await service.generate_invoice(record_id)


@router.get("/finance/stats")
async def get_finance_stats(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get finance statistics"""
    return await service.get_finance_stats()


# ── Academic Management ────────────────────────────────
# Course management endpoints (admin)


@router.get("/courses")
async def get_all_courses_admin(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get all courses (admin view)"""
    return await service.get_all_courses(skip, limit)


@router.post("/courses")
async def create_course_admin(
    course_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Create a new course (admin)"""
    return await service.create_course(course_data, current_user.id)


@router.patch("/courses/{course_id}")
async def update_course_admin(
    course_id: int,
    course_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update a course (admin)"""
    return await service.update_course(course_id, course_data, current_user.id)


@router.delete("/courses/{course_id}")
async def delete_course_admin(
    course_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Delete a course (admin)"""
    return await service.delete_course(course_id, current_user.id)


# Department management endpoints (admin)


@router.get("/departments")
async def get_all_departments_admin(
    skip: int = 0,
    limit: int = 100,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get all departments (admin view)"""
    return await service.get_all_departments(skip, limit)


@router.post("/departments")
async def create_department_admin(
    dept_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Create a new department (admin)"""
    return await service.create_department(dept_data, current_user.id)


@router.patch("/departments/{dept_id}")
async def update_department_admin(
    dept_id: int,
    dept_data: dict,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Update a department (admin)"""
    return await service.update_department(dept_id, dept_data, current_user.id)


@router.delete("/departments/{dept_id}")
async def delete_department_admin(
    dept_id: int,
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Delete a department (admin)"""
    return await service.delete_department(dept_id, current_user.id)


# Timetable management endpoints (admin)


@router.get("/timetable")
async def get_timetable_admin(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get timetable (admin view)"""
    return await service.get_timetable()


@router.get("/timetable/conflicts")
async def check_timetable_conflicts(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Check timetable conflicts"""
    return await service.check_timetable_conflicts()


# Academic stats


@router.get("/academic/stats")
async def get_academic_stats(
    service: SuperAdminService = Depends(get_service),
    current_user: User = Depends(require_super_admin)
):
    """Get academic statistics"""
    return await service.get_academic_stats()