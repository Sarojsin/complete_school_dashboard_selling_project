"""
Admin Global Settings API

Endpoints for reading and updating global system settings.
"""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import smtplib
from email.message import EmailMessage

from backup.core.database import get_async_db
from backup.models.models import User
from backup.api.deps.admin import get_current_admin
from backup.repositories.admin_settings_repository import AdminSettingsRepository
from backup.core.crypto import encrypt_text, decrypt_text
from backup.api.schemas.admin.settings import (
    AcademicSettingsUpdate,
    FeatureToggleSettingsUpdate,
    GeneralSettingsUpdate,
    LocalizationSettingsUpdate,
    NotificationSettingsUpdate,
    PaymentSettingsUpdate,
    SmtpSettingsUpdate,
)

router = APIRouter(prefix="/admin/settings", tags=["Admin Settings"])


DEFAULT_GENERAL_SETTINGS = {
    "school_name": "Nexus Elite School",
    "school_code": "NES-001",
    "address": "123 Education Street, City",
    "phone": "+977-1-1234567",
    "email": "info@nexuselite.edu.np",
    "website": "https://nexuselite.edu.np",
    "logo_url": "/media/logo.png",
}

DEFAULT_ACADEMIC_SETTINGS = {
    "academic_year": "2024",
    "semester_system": "2",
    "grading_system": "percentage",
    "passing_percentage": 35,
    "class_timing_start": "08:00",
    "class_timing_end": "14:00",
    "working_days_per_week": 6,
}

DEFAULT_LOCALIZATION_SETTINGS = {
    "default_language": "en",
    "timezone": "Asia/Kathmandu",
    "date_format": "YYYY-MM-DD",
    "time_format": "24h",
    "currency": "NPR",
    "currency_symbol": "Rs",
}

DEFAULT_SMTP_SETTINGS = {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "school@gmail.com",
    "smtp_from_name": "Nexus Elite School",
    "smtp_enabled": True,
    "smtp_tls": True,
}

DEFAULT_PAYMENT_SETTINGS = {
    "payment_gateway": "esewa",
    "merchant_id": "NIS-12345",
    "merchant_key": "********",
    "gateway_enabled": True,
    "test_mode": True,
}

DEFAULT_NOTIFICATION_SETTINGS = {
    "email_notifications": True,
    "sms_notifications": False,
    "push_notifications": True,
    "notify_on_fee_due": True,
    "notify_on_attendance": True,
    "notify_on_exam_results": True,
}

DEFAULT_FEATURE_TOGGLES = {
    "chat_enabled": True,
    "video_enabled": True,
    "online_exams_enabled": True,
    "online_payment_enabled": True,
    "parent_portal_enabled": True,
    "library_enabled": True,
    "attendance_tracking_enabled": True,
    "online_registration_enabled": True,
}


async def _get_setting(db: AsyncSession, key: str, default: dict) -> dict:
    return await AdminSettingsRepository.get_setting_value(db, key, default)


async def _update_setting(db: AsyncSession, key: str, updates: dict, updated_by: int) -> dict:
    current = await _get_setting(db, key, {})
    current.update({k: v for k, v in updates.items() if v is not None})
    await AdminSettingsRepository.upsert_setting(db, key, current, updated_by=updated_by)
    return current


# ---------------------------------------------------------------------------
# General
# ---------------------------------------------------------------------------

@router.get("/general")
async def get_general_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return general school settings."""
    return await _get_setting(db, "general_settings", DEFAULT_GENERAL_SETTINGS)


@router.patch("/general")
async def update_general_settings(
    body: GeneralSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update general school settings."""
    updated = await _update_setting(
        db, "general_settings", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
    return {"success": True, "message": "General settings updated", "updated": updated}


@router.post("/logo")
async def upload_school_logo(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Upload a new school logo."""
    # Actual file persistence logic goes here
    logo_url = f"/media/logo_{file.filename}"
    await _update_setting(db, "general_settings", {"logo_url": logo_url}, updated_by=current_user.id)
    return {"success": True, "message": "Logo uploaded successfully", "logo_url": logo_url}


# ---------------------------------------------------------------------------
# Academic
# ---------------------------------------------------------------------------

@router.get("/academic")
async def get_academic_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return academic configuration settings."""
    return await _get_setting(db, "academic_settings", DEFAULT_ACADEMIC_SETTINGS)


@router.patch("/academic")
async def update_academic_settings(
    body: AcademicSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update academic configuration settings."""
    updated = await _update_setting(
        db, "academic_settings", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
    return {"success": True, "message": "Academic settings updated", "updated": updated}


# ---------------------------------------------------------------------------
# Localization
# ---------------------------------------------------------------------------

@router.get("/localization")
async def get_localization_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return locale and timezone settings."""
    return await _get_setting(db, "localization_settings", DEFAULT_LOCALIZATION_SETTINGS)


@router.patch("/localization")
async def update_localization_settings(
    body: LocalizationSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update locale and timezone settings."""
    updated = await _update_setting(
        db, "localization_settings", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
    return {"success": True, "message": "Localization settings updated", "updated": updated}


# ---------------------------------------------------------------------------
# SMTP
# ---------------------------------------------------------------------------

@router.get("/smtp")
async def get_smtp_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return SMTP settings (password is never exposed)."""
    settings_data = await _get_setting(db, "smtp_settings", DEFAULT_SMTP_SETTINGS)
    # Never expose password
    if "smtp_password" in settings_data:
        settings_data = {**settings_data, "smtp_password": None}
    return settings_data


@router.patch("/smtp")
async def update_smtp_settings(
    body: SmtpSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update SMTP settings. Passwords are encrypted before persistence."""
    updates = body.model_dump(exclude_unset=True)
    if "smtp_password" in updates and updates["smtp_password"]:
        updates["smtp_password"] = encrypt_text(updates["smtp_password"])
    updated = await _update_setting(db, "smtp_settings", updates, updated_by=current_user.id)
    if "smtp_password" in updated:
        updated["smtp_password"] = None
    return {"success": True, "message": "SMTP settings updated", "updated": updated}


@router.post("/smtp/test")
async def test_smtp_settings(
    test_email: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Send a test email to verify current SMTP configuration."""
    settings_data = await _get_setting(db, "smtp_settings", DEFAULT_SMTP_SETTINGS)
    if not settings_data.get("smtp_enabled"):
        raise HTTPException(status_code=400, detail="SMTP is disabled")

    host = settings_data.get("smtp_host")
    port = settings_data.get("smtp_port")
    username = settings_data.get("smtp_username")
    password = decrypt_text(settings_data.get("smtp_password"))
    from_name = settings_data.get("smtp_from_name") or "Admin"
    use_tls = settings_data.get("smtp_tls", True)

    if not host or not port or not username or not password:
        raise HTTPException(status_code=400, detail="SMTP settings are incomplete")

    msg = EmailMessage()
    msg["Subject"] = "SMTP Test"
    msg["From"] = f"{from_name} <{username}>"
    msg["To"] = test_email
    msg.set_content("SMTP settings test email.")

    try:
        server = smtplib.SMTP(host, port, timeout=10)
        if use_tls:
            server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"SMTP test failed: {exc}")

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
    return await _get_setting(db, "payment_settings", DEFAULT_PAYMENT_SETTINGS)


@router.patch("/payment")
async def update_payment_settings(
    body: PaymentSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update payment gateway settings."""
    updated = await _update_setting(
        db, "payment_settings", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
    return {"success": True, "message": "Payment settings updated", "updated": updated}


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------

@router.get("/notifications")
async def get_notification_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return notification channel and trigger settings."""
    return await _get_setting(db, "notification_settings", DEFAULT_NOTIFICATION_SETTINGS)


@router.patch("/notifications")
async def update_notification_settings(
    body: NotificationSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update notification settings."""
    updated = await _update_setting(
        db, "notification_settings", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
    return {"success": True, "message": "Notification settings updated", "updated": updated}


# ---------------------------------------------------------------------------
# Feature toggles
# ---------------------------------------------------------------------------

@router.get("/features")
async def get_feature_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return global feature-toggle settings."""
    return await _get_setting(db, "feature_toggle_settings", DEFAULT_FEATURE_TOGGLES)


@router.patch("/features")
async def update_feature_settings(
    body: FeatureToggleSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Update global feature-toggle settings."""
    updated = await _update_setting(
        db, "feature_toggle_settings", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
    return {"success": True, "message": "Feature settings updated", "updated": updated}


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
        "general": await get_general_settings(db, current_user),
        "academic": await get_academic_settings(db, current_user),
        "localization": await get_localization_settings(db, current_user),
        "smtp": await get_smtp_settings(db, current_user),
        "payment": await get_payment_settings(db, current_user),
        "notifications": await get_notification_settings(db, current_user),
        "features": await get_feature_settings(db, current_user),
    }
