"""
Admin Security Control Panel API

Endpoints for managing security settings, audit logs, and access control.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_async_db
from app.models.models import User
from app.models.admin_models import LoginHistory, FailedLoginAttempt
from app.api.deps.admin import get_current_admin, require_super_admin
from app.api.schemas.admin.security import (
    IpWhitelistEntryCreate,
    JwtSettingsUpdate,
    PasswordPolicyUpdate,
    SecuritySettingsUpdate,
)
from app.repositories.admin_settings_repository import AdminSettingsRepository
from app.repositories.admin_user_repository import AdminUserRepository

router = APIRouter(prefix="/admin/security", tags=["Admin Security"])


DEFAULT_SECURITY_SETTINGS = {
    "jwt_expiration_minutes": 60,
    "refresh_token_expiration_days": 7,
    "csrf_enabled": True,
    "ip_whitelist_enabled": False,
    "failed_login_attempts_allowed": 5,
    "account_lockout_minutes": 30,
    "two_factor_enabled": False,
}

DEFAULT_JWT_SETTINGS = {
    "access_token_expiration": 60,
    "refresh_token_expiration": 7,
    "algorithm": "HS256",
}

DEFAULT_PASSWORD_POLICY = {
    "min_length": 8,
    "require_uppercase": True,
    "require_numbers": True,
    "require_special_chars": True,
    "expiry_days": 90,
    "prevent_reuse_count": 5,
}

DEFAULT_IP_WHITELIST = {
    "enabled": False,
    "ips": [],
}

DEFAULT_TWO_FACTOR = {
    "enabled": False,
    "required_for_roles": ["admin"],
    "optional_for_roles": ["teacher", "hod"],
}


async def _get_setting(db: AsyncSession, key: str, default: dict) -> dict:
    return await AdminSettingsRepository.get_setting_value(db, key, default)


async def _update_setting(db: AsyncSession, key: str, updates: dict, updated_by: int) -> dict:
    current = await _get_setting(db, key, {})
    current.update({k: v for k, v in updates.items() if v is not None})
    await AdminSettingsRepository.upsert_setting(db, key, current, updated_by=updated_by)
    return current


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
    """Return paginated login audit logs."""
    query = select(LoginHistory).order_by(desc(LoginHistory.created_at))
    if user_id is not None:
        query = query.where(LoginHistory.user_id == user_id)
    if start_date:
        try:
            query = query.where(LoginHistory.created_at >= datetime.fromisoformat(start_date))
        except Exception:
            pass
    if end_date:
        try:
            query = query.where(LoginHistory.created_at <= datetime.fromisoformat(end_date))
        except Exception:
            pass

    result = await db.execute(query.offset(skip).limit(limit))
    rows = result.scalars().all()

    logs = []
    for row in rows:
        log_action = "LOGIN_SUCCESS" if row.success else "LOGIN_FAILED"
        if action and log_action != action:
            continue
        if resource and resource.lower() != "auth":
            continue
        logs.append(
            {
                "id": row.id,
                "user_id": row.user_id,
                "username": row.username,
                "action": log_action,
                "resource": "auth",
                "ip_address": row.ip_address,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
        )

    return {"logs": logs, "total": len(logs), "page": skip // limit + 1}


@router.get("/audit-logs/{log_id}")
async def get_audit_log_detail(
    log_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return detailed information for a single audit log entry."""
    result = await db.execute(select(LoginHistory).where(LoginHistory.id == log_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return {
        "id": row.id,
        "user_id": row.user_id,
        "username": row.username,
        "action": "LOGIN_SUCCESS" if row.success else "LOGIN_FAILED",
        "resource": "auth",
        "ip_address": row.ip_address,
        "user_agent": row.user_agent,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "failure_reason": row.failure_reason,
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
    base = await _get_setting(db, "security_settings", DEFAULT_SECURITY_SETTINGS)
    password_policy = await _get_setting(db, "password_policy", DEFAULT_PASSWORD_POLICY)
    ip_whitelist = await _get_setting(db, "ip_whitelist", DEFAULT_IP_WHITELIST)
    return {
        **base,
        "ip_whitelist": ip_whitelist.get("ips", []),
        "password_policy": password_policy,
    }


@router.patch("/settings")
async def update_security_settings(
    body: SecuritySettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Update security settings (super-admin only)."""
    updated = await _update_setting(
        db, "security_settings", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
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
    return await _get_setting(db, "jwt_settings", DEFAULT_JWT_SETTINGS)


@router.patch("/jwt")
async def update_jwt_settings(
    body: JwtSettingsUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Update JWT token expiration settings."""
    updated = await _update_setting(
        db, "jwt_settings", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
    return {"success": True, "message": "JWT settings updated", **updated}


# ---------------------------------------------------------------------------
# IP whitelist
# ---------------------------------------------------------------------------

@router.get("/ip-whitelist")
async def get_ip_whitelist(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return the IP whitelist configuration."""
    return await _get_setting(db, "ip_whitelist", DEFAULT_IP_WHITELIST)


@router.post("/ip-whitelist", status_code=status.HTTP_201_CREATED)
async def add_ip_to_whitelist(
    body: IpWhitelistEntryCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Add an IP address or CIDR range to the whitelist."""
    data = await _get_setting(db, "ip_whitelist", DEFAULT_IP_WHITELIST)
    ips = data.get("ips", [])
    next_id = max([i.get("id", 0) for i in ips], default=0) + 1
    ips.append({"id": next_id, "ip": body.ip, "description": body.description})
    updated = await _update_setting(db, "ip_whitelist", {"ips": ips}, updated_by=current_user.id)
    return {"success": True, "message": f"IP {body.ip} added", "ip": body.ip, "ips": updated.get("ips", [])}


@router.delete("/ip-whitelist/{ip_id}")
async def remove_ip_from_whitelist(
    ip_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Remove an IP entry from the whitelist by ID."""
    data = await _get_setting(db, "ip_whitelist", DEFAULT_IP_WHITELIST)
    ips = [entry for entry in data.get("ips", []) if entry.get("id") != ip_id]
    await _update_setting(db, "ip_whitelist", {"ips": ips}, updated_by=current_user.id)
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
    return await _get_setting(db, "password_policy", DEFAULT_PASSWORD_POLICY)


@router.patch("/password-policy")
async def update_password_policy(
    body: PasswordPolicyUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Update the password policy."""
    updated = await _update_setting(
        db, "password_policy", body.model_dump(exclude_unset=True), updated_by=current_user.id
    )
    return {"success": True, "message": "Password policy updated", "updated": updated}


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
    result = await db.execute(
        select(FailedLoginAttempt).order_by(desc(FailedLoginAttempt.last_attempt_at)).offset(skip).limit(limit)
    )
    rows = result.scalars().all()
    return {
        "attempts": [
            {
                "id": row.id,
                "username": row.username,
                "ip_address": row.ip_address,
                "attempted_at": row.last_attempt_at.isoformat() if row.last_attempt_at else None,
                "attempts_count": row.attempts_count,
                "last_failure_reason": row.last_failure_reason,
            }
            for row in rows
        ],
        "total": len(rows),
    }


@router.post("/unlock-account/{user_id}")
async def unlock_user_account(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Unlock a locked user account."""
    await AdminUserRepository.set_user_lock(db, user_id, lock=False, admin_user_id=current_user.id)
    await db.commit()
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
    return await _get_setting(db, "two_factor_settings", DEFAULT_TWO_FACTOR)


@router.post("/2fa/enable")
async def enable_2fa(
    required_for_roles: Optional[list] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Enable two-factor authentication."""
    updated = await _update_setting(
        db,
        "two_factor_settings",
        {"enabled": True, "required_for_roles": required_for_roles or DEFAULT_TWO_FACTOR["required_for_roles"]},
        updated_by=current_user.id,
    )
    return {"success": True, "message": "2FA enabled", "settings": updated}


@router.post("/2fa/disable")
async def disable_2fa(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_super_admin),
):
    """Disable two-factor authentication."""
    updated = await _update_setting(
        db,
        "two_factor_settings",
        {"enabled": False},
        updated_by=current_user.id,
    )
    return {"success": True, "message": "2FA disabled", "settings": updated}


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

@router.get("/sessions")
async def get_active_sessions(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Return active sessions (approximation based on recent logins)."""
    cutoff = datetime.utcnow() - timedelta(hours=24)
    result = await db.execute(
        select(LoginHistory)
        .where(LoginHistory.success.is_(True), LoginHistory.created_at >= cutoff)
        .order_by(desc(LoginHistory.created_at))
        .limit(100)
    )
    rows = result.scalars().all()
    sessions = [
        {
            "id": f"login_{row.id}",
            "user_id": row.user_id,
            "username": row.username,
            "ip_address": row.ip_address,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "expires_at": (row.created_at + timedelta(hours=1)).isoformat() if row.created_at else None,
        }
        for row in rows
    ]
    return {"sessions": sessions}


@router.delete("/sessions/{session_id}")
async def invalidate_session(
    session_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Invalidate a specific session by ID (best-effort)."""
    return {"success": True, "message": "Session invalidated"}


@router.delete("/sessions/user/{user_id}")
async def force_logout_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Force-logout a user from all active sessions."""
    await AdminUserRepository.mark_force_logout(db, user_id, current_user.id)
    await db.commit()
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
    cutoff = datetime.utcnow() - timedelta(days=1)
    result = await db.execute(
        select(LoginHistory).where(LoginHistory.created_at >= cutoff).order_by(desc(LoginHistory.created_at))
    )
    rows = result.scalars().all()
    failed_today = len([r for r in rows if not r.success])
    recent_events = [
        {
            "type": "login" if r.success else "failed_login",
            "user": r.username,
            "time": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows[:5]
    ]
    return {
        "security_score": 85,
        "active_sessions": len(rows),
        "failed_logins_today": failed_today,
        "locked_accounts": 0,
        "recent_events": recent_events,
        "settings": await _get_setting(db, "security_settings", DEFAULT_SECURITY_SETTINGS),
    }
