"""
app.api.schemas.admin.settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydantic request schemas for the admin settings API.  Each sub-section of
settings gets its own class so PATCH endpoints accept a typed request body
rather than a flat list of individual query parameters.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class GeneralSettingsUpdate(BaseModel):
    school_name: Optional[str] = None
    school_code: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None


class AcademicSettingsUpdate(BaseModel):
    academic_year: Optional[str] = None
    semester_system: Optional[str] = None
    grading_system: Optional[str] = None
    passing_percentage: Optional[int] = Field(None, ge=0, le=100)
    class_timing_start: Optional[str] = None  # HH:MM
    class_timing_end: Optional[str] = None    # HH:MM


class LocalizationSettingsUpdate(BaseModel):
    default_language: Optional[str] = None
    timezone: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
    currency: Optional[str] = None


class SmtpSettingsUpdate(BaseModel):
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = Field(None, gt=0, le=65535)
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = Field(None, description="Will be encrypted at rest")
    smtp_from_name: Optional[str] = None
    smtp_enabled: Optional[bool] = None
    smtp_tls: Optional[bool] = None


class PaymentSettingsUpdate(BaseModel):
    payment_gateway: Optional[str] = None
    merchant_id: Optional[str] = None
    merchant_key: Optional[str] = None
    gateway_enabled: Optional[bool] = None
    test_mode: Optional[bool] = None


class NotificationSettingsUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    notify_on_fee_due: Optional[bool] = None
    notify_on_attendance: Optional[bool] = None
    notify_on_exam_results: Optional[bool] = None


class FeatureToggleSettingsUpdate(BaseModel):
    chat_enabled: Optional[bool] = None
    video_enabled: Optional[bool] = None
    online_exams_enabled: Optional[bool] = None
    online_payment_enabled: Optional[bool] = None
    parent_portal_enabled: Optional[bool] = None
    library_enabled: Optional[bool] = None
    attendance_tracking_enabled: Optional[bool] = None
    online_registration_enabled: Optional[bool] = None
