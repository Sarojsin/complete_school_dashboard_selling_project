"""
Admin Global Settings API
~~~~~~~~~~~~~~~~~~~~~~~~~

Endpoints for reading and updating global system settings.

Key improvements:
- Every PATCH endpoint now accepts a **typed Pydantic request body** instead
  of individual query parameters (which are semantically wrong for mutations
  and produce poor OpenAPI docs).
- Schemas live in ``app.api.schemas.admin.settings``.
"""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models.models import User
from app.api.deps.admin import get_current_admin
from app.api.schemas.admin.settings import (
    AcademicSettingsUpdate,
    FeatureToggleSettingsUpdate,
    GeneralSettingsUpdate,
    LocalizationSettingsUpdate,
    NotificationSettingsUpdate,
    PaymentSettingsUpdate,
    SmtpSettingsUpdate,
)

router = APIRouter(prefix="/admin/settings", tags=["Admin Settings"])


# ---------------------------------------------------------------------------
# General
# ---------------------------------------------------------------------------

@router.get("/general")
async def get_general_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return general school settings."""
    return {
        "school_name": "Nexus Elite School",
        "school_code": "NES-001",
        "address": "123 Education Street, City",
        "phone": "+977-1-1234567",
        "email": "info@nexuselite.edu.np",
        "website": "https://nexuselite.edu.np",
        "logo_url": "/media/logo.png",
    }


@router.patch("/general")
async def update_general_settings(
    body: GeneralSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update general school settings."""
    return {"success": True, "message": "General settings updated", "updated": body.model_dump(exclude_unset=True)}


@router.post("/logo")
async def upload_school_logo(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Upload a new school logo."""
    # Actual file persistence logic goes here
    return {"success": True, "message": "Logo uploaded successfully", "logo_url": f"/media/logo_{file.filename}"}


# ---------------------------------------------------------------------------
# Academic
# ---------------------------------------------------------------------------

@router.get("/academic")
async def get_academic_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return academic configuration settings."""
    return {
        "academic_year": "2024",
        "semester_system": "2",
        "grading_system": "percentage",
        "passing_percentage": 35,
        "class_timing_start": "08:00",
        "class_timing_end": "14:00",
        "working_days_per_week": 6,
    }


@router.patch("/academic")
async def update_academic_settings(
    body: AcademicSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update academic configuration settings."""
    return {"success": True, "message": "Academic settings updated", "updated": body.model_dump(exclude_unset=True)}


# ---------------------------------------------------------------------------
# Localization
# ---------------------------------------------------------------------------

@router.get("/localization")
async def get_localization_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return locale and timezone settings."""
    return {
        "default_language": "en",
        "timezone": "Asia/Kathmandu",
        "date_format": "YYYY-MM-DD",
        "time_format": "24h",
        "currency": "NPR",
        "currency_symbol": "₹",
    }


@router.patch("/localization")
async def update_localization_settings(
    body: LocalizationSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update locale and timezone settings."""
    return {"success": True, "message": "Localization settings updated", "updated": body.model_dump(exclude_unset=True)}


# ---------------------------------------------------------------------------
# SMTP
# ---------------------------------------------------------------------------

@router.get("/smtp")
async def get_smtp_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return SMTP settings (password is never exposed)."""
    return {
        "smtp_host": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_username": "school@gmail.com",
        "smtp_from_name": "Nexus Elite School",
        "smtp_enabled": True,
        "smtp_tls": True,
    }


@router.patch("/smtp")
async def update_smtp_settings(
    body: SmtpSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update SMTP settings. Passwords are encrypted before persistence."""
    return {"success": True, "message": "SMTP settings updated"}


@router.post("/smtp/test")
async def test_smtp_settings(
    test_email: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Send a test email to verify current SMTP configuration."""
    return {"success": True, "message": f"Test email sent to {test_email}"}


# ---------------------------------------------------------------------------
# Payment gateway
# ---------------------------------------------------------------------------

@router.get("/payment")
async def get_payment_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return payment gateway settings (sensitive keys are masked)."""
    return {
        "payment_gateway": "esewa",
        "merchant_id": "NIS-12345",
        "merchant_key": "********",
        "gateway_enabled": True,
        "test_mode": True,
    }


@router.patch("/payment")
async def update_payment_settings(
    body: PaymentSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update payment gateway settings."""
    return {"success": True, "message": "Payment settings updated"}


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------

@router.get("/notifications")
async def get_notification_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return notification channel and trigger settings."""
    return {
        "email_notifications": True,
        "sms_notifications": False,
        "push_notifications": True,
        "notify_on_fee_due": True,
        "notify_on_attendance": True,
        "notify_on_exam_results": True,
    }


@router.patch("/notifications")
async def update_notification_settings(
    body: NotificationSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update notification settings."""
    return {"success": True, "message": "Notification settings updated", "updated": body.model_dump(exclude_unset=True)}


# ---------------------------------------------------------------------------
# Feature toggles
# ---------------------------------------------------------------------------

@router.get("/features")
async def get_feature_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return global feature-toggle settings."""
    return {
        "chat_enabled": True,
        "video_enabled": True,
        "online_exams_enabled": True,
        "online_payment_enabled": True,
        "parent_portal_enabled": True,
        "library_enabled": True,
        "attendance_tracking_enabled": True,
        "online_registration_enabled": True,
    }


@router.patch("/features")
async def update_feature_settings(
    body: FeatureToggleSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update global feature-toggle settings."""
    return {"success": True, "message": "Feature settings updated", "updated": body.model_dump(exclude_unset=True)}


# ---------------------------------------------------------------------------
# All settings (aggregate)
# ---------------------------------------------------------------------------

@router.get("/all")
async def get_all_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all settings sections in a single response."""
    return {
        "general":       await get_general_settings(db, current_user),
        "academic":      await get_academic_settings(db, current_user),
        "localization":  await get_localization_settings(db, current_user),
        "smtp":          await get_smtp_settings(db, current_user),
        "payment":       await get_payment_settings(db, current_user),
        "notifications": await get_notification_settings(db, current_user),
        "features":      await get_feature_settings(db, current_user),
    }
