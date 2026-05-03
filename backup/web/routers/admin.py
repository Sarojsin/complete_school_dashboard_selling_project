"""
Admin Web Routes

Web routes for serving admin HTML templates.
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import httpx
from datetime import datetime

from backup.core.database import get_async_db
from backup.dependencies import get_current_user_web
from backup.models.models import User, UserRole
from backup.core.templates import templates


router = APIRouter()


# Define admin roles
ADMIN_ROLES = [UserRole.ADMIN, UserRole.HOD]
SECTION_ADMIN_ROLES = [UserRole.EXAM_SECTION, UserRole.LIBRARY_MANAGER, UserRole.ACCOUNT_SECTION, UserRole.AUTHORITY]


async def get_current_admin(
    request: Request,
    current_user: User = Depends(get_current_user_web)
) -> User:
    """Require admin or authority role"""
    if current_user.role not in ADMIN_ROLES + SECTION_ADMIN_ROLES:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    return current_user


def get_api_base_url() -> str:
    """Get the API base URL for internal API calls"""
    import os
    return os.getenv("API_BASE_URL", "http://localhost:8000")


async def call_admin_api(endpoint: str, method: str = "GET", data: dict = None, cookies: dict = None):
    """Helper to call admin API endpoints"""
    base_url = get_api_base_url()
    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(f"{base_url}{endpoint}", cookies=cookies)
        elif method == "POST":
            response = await client.post(f"{base_url}{endpoint}", json=data, cookies=cookies)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        if response.status_code >= 400:
            return None
        return response.json()


async def _get_admin_stats(db: AsyncSession):
    """Helper to get common admin statistics"""
    from sqlalchemy import select, func
    from backup.models.models import Student, Teacher, User as UserModel, Parent, Course, FeeRecord, Notice
    from backup.models.group_models import Group
    from backup.models.exam_models import ExamNotice
    from backup.repositories.feature_repository import FeatureRepository
    from datetime import date, timedelta
    try:
        # Count users by role
        total_students = await db.scalar(select(func.count(Student.id))) or 0
        total_teachers = await db.scalar(select(func.count(Teacher.id))) or 0
        total_parents = await db.scalar(select(func.count(Parent.id))) or 0
        total_courses = await db.scalar(select(func.count(Course.id))) or 0
        total_users = await db.scalar(select(func.count(UserModel.id))) or 0
        
        # Total Revenue (Fees Collected)
        total_revenue = await db.scalar(
            select(func.sum(FeeRecord.paid_amount)).where(FeeRecord.status == "paid")
        ) or 0.0
        
        # Pending Fees
        pending_fees = await db.scalar(
            select(func.sum(FeeRecord.amount - FeeRecord.paid_amount)).where(
                FeeRecord.status.in_(["pending", "overdue", "partial"])
            )
        ) or 0.0
        
        # Upcoming Exams (next 30 days)
        today = date.today()
        thirty_days_later = today + timedelta(days=30)
        upcoming_exams = await db.scalar(
            select(func.count(ExamNotice.id)).where(
                ExamNotice.exam_date >= today,
                ExamNotice.exam_date <= thirty_days_later
            )
        ) or 0
        
        # Active Groups
        active_groups = await db.scalar(
            select(func.count(Group.id)).where(Group.is_active == True)
        ) or 0
        
        # Total Notices
        total_notices = await db.scalar(select(func.count(Notice.id))) or 0
        
        # Get feature counts
        enabled_features = await FeatureRepository.get_enabled_count(db) or 0
        total_features = await FeatureRepository.get_total_count(db) or 0
        
        # Calculate percentages
        features_enabled_pct = int((enabled_features / total_features * 100)) if total_features > 0 else 0
        
        return {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_parents": total_parents,
            "total_courses": total_courses,
            "total_users": total_users,
            "total_revenue": round(float(total_revenue), 2),
            "pending_fees": round(float(pending_fees), 2),
            "upcoming_exams": upcoming_exams,
            "active_groups": active_groups,
            "total_notices": total_notices,
            "enabled_features": enabled_features,
            "total_features": total_features,
            "features_enabled_pct": features_enabled_pct
        }
    except Exception as e:
        print(f"Error getting admin stats: {e}")
        return {
            "total_students": 0, "total_teachers": 0, "total_parents": 0,
            "total_courses": 0, "total_users": 0, "total_revenue": 0,
            "pending_fees": 0, "upcoming_exams": 0, "active_groups": 0,
            "total_notices": 0, "enabled_features": 0, "total_features": 0,
            "features_enabled_pct": 0
        }


# ------------------ ADMIN PAGES ------------------

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Admin dashboard page with system statistics and audit logs.
    """
    # Get stats using helper
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats,
            "now": datetime.now()
        }
    )


@router.get("/features", response_class=HTMLResponse)
async def admin_features(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db),
    category: Optional[str] = None
):
    """
    Features management page to enable/disable system features.
    """
    from backup.services.feature_service import FeatureService
    from backup.repositories.feature_repository import FeatureRepository
    
    # Get all features
    features = await FeatureService.get_all_features(db, category=category)
    
    # Get all categories
    categories = await FeatureRepository.get_categories(db)
    
    # Organize features by category
    features_by_category = {}
    for feature in features:
        cat = feature.feature_category or "Other"
        if cat not in features_by_category:
            features_by_category[cat] = []
        features_by_category[cat].append({
            "id": feature.id,
            "feature_code": feature.feature_code,
            "feature_name": feature.feature_name,
            "description": feature.description,
            "is_enabled": feature.is_enabled,
            "is_global": feature.is_global,
            "role_permissions_count": len(feature.role_permissions) if feature.role_permissions else 0
        })
    
    # Get stats for sidebar
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/features.html",
        {
            "request": request,
            "current_user": current_user,
            "features": features,
            "features_by_category": features_by_category,
            "categories": categories,
            "selected_category": category,
            "stats": stats
        }
    )


# Duplicate feature detail route removed




@router.get("/features/{feature_code}", response_class=HTMLResponse)
async def admin_feature_detail(
    feature_code: str,
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Individual feature detail and permission management page.
    """
    from backup.repositories.feature_repository import FeatureRepository, FeatureRolePermissionRepository, AdminAuditLogRepository
    from backup.models.models import UserRole
    
    feature = await FeatureRepository.get_by_code(db, feature_code)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
        
    permissions = await FeatureRolePermissionRepository.get_by_feature(db, feature.id)
    # Organize permissions by role for easy template access
    permissions_map = {p.role.value if hasattr(p.role, 'value') else str(p.role): p for p in permissions}
    
    logs = await AdminAuditLogRepository.get_by_feature(db, feature_code, limit=10)
    
    # Get all possible roles from the enum
    roles = [role.value for role in UserRole]
    
    # Get stats for sidebar
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/feature_detail.html",
        {
            "request": request,
            "current_user": current_user,
            "feature": feature,
            "permissions": permissions_map,
            "roles": roles,
            "logs": logs,
            "stats": stats
        }
    )


@router.get("/audit", response_class=HTMLResponse)
async def admin_audit_logs(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db),
    feature_code: Optional[str] = None,
    limit: int = 50
):
    """
    Audit logs page showing all admin actions.
    """
    from backup.repositories.feature_repository import AdminAuditLogRepository
    
    if feature_code:
        logs = await AdminAuditLogRepository.get_by_feature(db, feature_code, limit=limit)
    else:
        logs = await AdminAuditLogRepository.get_all(db, limit=limit)
    
    # Get stats for sidebar
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/audit_logs.html",
        {
            "request": request,
            "current_user": current_user,
            "logs": logs,
            "feature_code": feature_code,
            "stats": stats
        }
    )


@router.get("/settings", response_class=HTMLResponse)
async def admin_settings(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    System settings page.
    """
    # Get stats for sidebar
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/settings.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats
        }
    )


# ------------------ ADDITIONAL ADMIN PAGES ------------------

@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    User management page - lists all users with management options.
    """
    from backup.models.models import User as UserModel
    from sqlalchemy import select
    
    # Get all users
    result = await db.execute(select(UserModel).order_by(UserModel.created_at.desc()))
    users = result.scalars().all()
    
    # Get stats for sidebar
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/users.html",
        {
            "request": request,
            "current_user": current_user,
            "users": users,
            "stats": stats
        }
    )


@router.get("/academic", response_class=HTMLResponse)
async def admin_academic(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Academic management page - courses, departments, timetable.
    """
    from backup.models.models import Course
    from backup.models.department_models import Department
    from sqlalchemy import select
    
    # Get courses
    courses_result = await db.execute(select(Course))
    courses = courses_result.scalars().all()
    
    # Get departments
    depts_result = await db.execute(select(Department))
    departments = depts_result.scalars().all()
    
    # Get stats for sidebar
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/academic.html",
        {
            "request": request,
            "current_user": current_user,
            "courses": courses,
            "departments": departments,
            "stats": stats
        }
    )


@router.get("/finance", response_class=HTMLResponse)
async def admin_finance(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Finance management page - fees, payments, reports.
    """
    from backup.models.models import FeeRecord, FeeStructure
    from sqlalchemy import select
    
    # Get fee records
    fees_result = await db.execute(select(FeeRecord).order_by(FeeRecord.due_date.desc()))
    fee_records = fees_result.scalars().all()
    
    # Get fee structures
    structures_result = await db.execute(select(FeeStructure))
    fee_structures = structures_result.scalars().all()
    
    # Get stats for sidebar
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/finance.html",
        {
            "request": request,
            "current_user": current_user,
            "fee_records": fee_records,
            "fee_structures": fee_structures,
            "stats": stats
        }
    )


# ------------------ SYSTEM MONITORING ------------------

@router.get("/system", response_class=HTMLResponse)
async def admin_system(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    System monitoring page - server status, database health, active users.
    """
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/system.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats
        }
    )


# ------------------ SECURITY CONTROL ------------------

@router.get("/security", response_class=HTMLResponse)
async def admin_security(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Security control panel - JWT settings, IP whitelist, audit logs.
    """
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/security.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats
        }
    )


# ------------------ BACKUP & RESTORE ------------------

@router.get("/backup", response_class=HTMLResponse)
async def admin_backup(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Backup and restore page.
    """
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/backup.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats
        }
    )


# ------------------ REPORTS ------------------

@router.get("/reports", response_class=HTMLResponse)
async def admin_reports(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Reports generation page.
    """
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/reports.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats
        }
    )


# ------------------ NOTICES ------------------

@router.get("/notices", response_class=HTMLResponse)
async def admin_notices(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Notice management page.
    """
    from backup.models.models import Notice
    from sqlalchemy import select
    
    notices_result = await db.execute(select(Notice).order_by(Notice.created_at.desc()))
    notices = notices_result.scalars().all()
    
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/notices.html",
        {
            "request": request,
            "current_user": current_user,
            "notices": notices,
            "stats": stats
        }
    )


# ------------------ COMMUNICATION ------------------

@router.get("/communication", response_class=HTMLResponse)
async def admin_communication(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Communication monitoring page.
    """
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/communication.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats
        }
    )


# ------------------ MEDIA ------------------

@router.get("/media", response_class=HTMLResponse)
async def admin_media(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Media management page.
    """
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/media.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats
        }
    )


# ------------------ ADVANCED FEATURES ------------------

@router.get("/advanced", response_class=HTMLResponse)
async def admin_advanced(
    request: Request,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Advanced features page - AI predictions, alerts, multi-school.
    """
    stats = await _get_admin_stats(db)
    
    return templates.TemplateResponse(
        "admin/advanced.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats
        }
    )
