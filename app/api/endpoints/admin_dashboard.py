"""
Admin Dashboard API
~~~~~~~~~~~~~~~~~~~

Endpoints for admin dashboard overview and system statistics.

Strict Layered Architecture enforced:
- Only Pydantic models (validation) and Router bindings.
- Zero direct Database ORM queries.
- Business queries and logic flow through DashboardService exclusively.
"""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models.models import User
from app.api.deps.admin import get_current_admin
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@router.get("/dashboard")
async def get_dashboard(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return combined dashboard statistics."""
    return await DashboardService.get_dashboard_summary(db, current_user)


@router.get("/stats")
async def get_system_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return concise system-wide user statistics."""
    return await DashboardService.get_system_stats(db)


@router.get("/users/count")
async def get_users_by_role(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return user counts grouped by role."""
    return await DashboardService.get_users_by_role(db)


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

@router.get("/overview")
async def get_dashboard_overview(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return comprehensive dashboard overview with all key metrics."""
    return await DashboardService.get_dashboard_overview(db)


# ---------------------------------------------------------------------------
# Features summary
# ---------------------------------------------------------------------------

@router.get("/features/summary")
async def get_features_summary(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return feature counts broken down by status and category."""
    return await DashboardService.get_features_summary(db)


@router.get("/features/enabled")
async def get_enabled_features(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all currently enabled features, optionally filtered by category."""
    return await DashboardService.get_enabled_features(db, category)


@router.get("/features/disabled")
async def get_disabled_features(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all currently disabled features, optionally filtered by category."""
    return await DashboardService.get_disabled_features(db, category)


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

@router.get("/analytics/enrollment")
async def get_enrollment_analytics(
    period: str = "yearly",
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return student enrollment counts, grouped by month or day."""
    return await DashboardService.get_enrollment_analytics(db, period)


@router.get("/analytics/fees")
async def get_fee_analytics(
    period: str = "yearly",
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return fee collection analytics for charts."""
    return await DashboardService.get_fee_analytics(db, period)


@router.get("/analytics/attendance")
async def get_attendance_analytics(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return attendance percentage overview."""
    return await DashboardService.get_attendance_analytics()


@router.get("/analytics/exams")
async def get_exam_analytics(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return exam performance analytics grouped by exam type and grade."""
    return await DashboardService.get_exam_analytics(db)


@router.get("/analytics/summary")
async def get_analytics_summary(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all analytics segments in a single aggregated response."""
    return await DashboardService.get_analytics_summary(db)
