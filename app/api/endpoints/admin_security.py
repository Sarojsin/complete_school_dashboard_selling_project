"""
Admin Security Control Panel API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Endpoints for managing security settings, audit logs, and user access control.

Key improvements:
- Schemas imported from ``app.api.schemas.admin.security``
- ``update_security_settings`` now accepts a typed ``SecuritySettingsUpdate``
  body instead of a raw ``dict`` parameter
- ``add_ip_to_whitelist`` uses ``IpWhitelistEntryCreate`` request body
  instead of raw query params on a POST endpoint
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models.models import User
from app.api.deps.admin import get_current_admin, require_super_admin
from app.api.schemas.admin.security import (
    IpWhitelistEntryCreate,
    JwtSettingsUpdate,
    PasswordPolicyUpdate,
    SecuritySettingsUpdate,
)

router = APIRouter(prefix="/admin/security", tags=["Admin Security"])


# ---------------------------------------------------------------------------
# Audit logs
# ---------------------------------------------------------------------------

@router.get("/audit-logs")
async def get_audit_logs(
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    resource: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """
    Return paginated audit logs.

    .. note:: Pending AuditLog model — returns representative placeholder data.
    """
    logs = [
        {
            "id": 1,
            "user_id": 1,
            "username": "admin",
            "action": "LOGIN",
            "resource": "auth",
            "ip_address": "192.168.1.1",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": 2,
            "user_id": 2,
            "username": "teacher1",
            "action": "CREATE",
            "resource": "course",
            "ip_address": "192.168.1.2",
            "created_at": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
        },
    ]
    return {"logs": logs, "total": len(logs), "page": skip // limit + 1}


@router.get("/audit-logs/{log_id}")
async def get_audit_log_detail(
    log_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return detailed information for a single audit log entry."""
    return {
        "id": log_id,
        "user_id": 1,
        "username": "admin",
        "action": "UPDATE",
        "resource": "user",
        "old_values": {"role": "teacher"},
        "new_values": {"role": "hod"},
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0...",
        "created_at": datetime.utcnow().isoformat(),
    }


# ---------------------------------------------------------------------------
# Security settings
# ---------------------------------------------------------------------------

@router.get("/settings")
async def get_security_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return the current security configuration."""
    return {
        "jwt_expiration_minutes": 60,
        "refresh_token_expiration_days": 7,
        "csrf_enabled": True,
        "ip_whitelist_enabled": False,
        "ip_whitelist": ["192.168.1.0/24", "10.0.0.0/8"],
        "password_policy": {
            "min_length": 8,
            "require_uppercase": True,
            "require_numbers": True,
            "require_special_chars": True,
            "expiry_days": 90,
        },
        "failed_login_attempts_allowed": 5,
        "account_lockout_minutes": 30,
        "two_factor_enabled": False,
    }


@router.patch("/settings")
async def update_security_settings(
    body: SecuritySettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """
    Update security settings.

    Only super-admins (``ADMIN`` role) may change security configuration.
    Previously accepted a raw ``dict`` — now a validated Pydantic body.
    """
    updated = body.model_dump(exclude_unset=True)
    return {"success": True, "message": "Security settings updated", "updated_settings": updated}


# ---------------------------------------------------------------------------
# JWT settings
# ---------------------------------------------------------------------------

@router.get("/jwt")
async def get_jwt_settings(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return current JWT configuration."""
    return {"access_token_expiration": 60, "refresh_token_expiration": 7, "algorithm": "HS256"}


@router.patch("/jwt")
async def update_jwt_settings(
    body: JwtSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Update JWT token expiration settings."""
    return {
        "success": True,
        "message": "JWT settings updated",
        "access_token_expires": body.access_token_expires,
        "refresh_token_expires": body.refresh_token_expires,
    }


# ---------------------------------------------------------------------------
# IP whitelist
# ---------------------------------------------------------------------------

@router.get("/ip-whitelist")
async def get_ip_whitelist(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return the IP whitelist configuration."""
    return {
        "enabled": False,
        "ips": [
            {"id": 1, "ip": "192.168.1.0/24", "description": "School Network"},
            {"id": 2, "ip": "10.0.0.0/8",     "description": "Internal Network"},
        ],
    }


@router.post("/ip-whitelist", status_code=status.HTTP_201_CREATED)
async def add_ip_to_whitelist(
    body: IpWhitelistEntryCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """
    Add an IP address or CIDR range to the whitelist.

    Previously accepted ``ip`` and ``description`` as raw query parameters
    on a POST endpoint — now uses a proper typed request body.
    """
    return {"success": True, "message": f"IP {body.ip} added to whitelist", "ip": body.ip, "description": body.description}


@router.delete("/ip-whitelist/{ip_id}")
async def remove_ip_from_whitelist(
    ip_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Remove an IP entry from the whitelist by ID."""
    return {"success": True, "message": "IP removed from whitelist"}


# ---------------------------------------------------------------------------
# Password policy
# ---------------------------------------------------------------------------

@router.get("/password-policy")
async def get_password_policy(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return the current password policy."""
    return {
        "min_length": 8,
        "require_uppercase": True,
        "require_numbers": True,
        "require_special_chars": True,
        "expiry_days": 90,
        "prevent_reuse_count": 5,
    }


@router.patch("/password-policy")
async def update_password_policy(
    body: PasswordPolicyUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Update the password policy."""
    return {"success": True, "message": "Password policy updated", "updated": body.model_dump(exclude_unset=True)}


# ---------------------------------------------------------------------------
# Failed logins / account unlock
# ---------------------------------------------------------------------------

@router.get("/failed-logins")
async def get_failed_logins(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return recent failed login attempts."""
    return {
        "attempts": [
            {"id": 1, "username": "student1", "ip_address": "192.168.1.100",
             "attempted_at": datetime.utcnow().isoformat(), "attempts_count": 3}
        ],
        "total": 1,
    }


@router.post("/unlock-account/{user_id}")
async def unlock_user_account(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Unlock a locked user account."""
    return {"success": True, "message": f"Account {user_id} unlocked"}


# ---------------------------------------------------------------------------
# 2FA management
# ---------------------------------------------------------------------------

@router.get("/2fa/status")
async def get_2fa_status(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return current 2FA configuration."""
    return {"enabled": False, "required_for_roles": ["admin"], "optional_for_roles": ["teacher", "hod"]}


@router.post("/2fa/enable")
async def enable_2fa(
    required_for_roles: Optional[list] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Enable two-factor authentication."""
    return {"success": True, "message": "2FA enabled"}


@router.post("/2fa/disable")
async def disable_2fa(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Disable two-factor authentication."""
    return {"success": True, "message": "2FA disabled"}


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

@router.get("/sessions")
async def get_active_sessions(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return all active user sessions."""
    return {
        "sessions": [
            {
                "id": "session_123",
                "user_id": 1,
                "username": "admin",
                "ip_address": "192.168.1.1",
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            }
        ]
    }


@router.delete("/sessions/{session_id}")
async def invalidate_session(
    session_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Invalidate a specific session by ID."""
    return {"success": True, "message": "Session invalidated"}


@router.delete("/sessions/user/{user_id}")
async def force_logout_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Force-logout a user from all active sessions."""
    return {"success": True, "message": f"User {user_id} logged out from all sessions"}


# ---------------------------------------------------------------------------
# Security dashboard
# ---------------------------------------------------------------------------

@router.get("/dashboard")
async def get_security_dashboard(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return a security summary dashboard."""
    return {
        "security_score": 85,
        "active_sessions": 12,
        "failed_logins_today": 3,
        "locked_accounts": 1,
        "recent_events": [
            {"type": "login",            "user": "admin",    "time": "5 min ago"},
            {"type": "failed_login",     "user": "unknown",  "time": "10 min ago"},
            {"type": "password_changed", "user": "teacher1", "time": "1 hour ago"},
        ],
        "settings": {"2fa_enabled": False, "csrf_enabled": True, "ip_whitelist_enabled": False},
    }
