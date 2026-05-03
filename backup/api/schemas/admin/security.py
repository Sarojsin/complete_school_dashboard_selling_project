"""
app.api.schemas.admin.security
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydantic request/response schemas for the admin security-control API.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, IPvAnyNetwork


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    username: Optional[str]
    action: str
    resource: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    details: Optional[Dict[str, Any]]
    created_at: str


class SecuritySettingsUpdate(BaseModel):
    """
    Typed body schema for PATCH /security/settings.

    Previously the endpoint accepted ``dict`` directly, which provides no
    validation, no IDE auto-completion, and no OpenAPI documentation.
    """
    jwt_expiration_minutes: Optional[int] = Field(None, gt=0)
    refresh_token_expiration_days: Optional[int] = Field(None, gt=0)
    csrf_enabled: Optional[bool] = None
    ip_whitelist_enabled: Optional[bool] = None
    failed_login_attempts_allowed: Optional[int] = Field(None, ge=1)
    account_lockout_minutes: Optional[int] = Field(None, ge=1)
    two_factor_enabled: Optional[bool] = None


class PasswordPolicyUpdate(BaseModel):
    min_length: Optional[int] = Field(None, ge=6, le=64)
    require_uppercase: Optional[bool] = None
    require_numbers: Optional[bool] = None
    require_special_chars: Optional[bool] = None
    expiry_days: Optional[int] = Field(None, ge=0)
    prevent_reuse_count: Optional[int] = Field(None, ge=0)


class JwtSettingsUpdate(BaseModel):
    access_token_expires: Optional[int] = Field(None, gt=0, description="Minutes")
    refresh_token_expires: Optional[int] = Field(None, gt=0, description="Days")


class IpWhitelistEntryCreate(BaseModel):
    """
    Request body for POST /security/ip-whitelist.

    Previously ``ip`` and ``description`` were raw query params on a POST
    endpoint — incorrect HTTP semantics for resource creation.
    """
    ip: str = Field(..., description="IP address or CIDR range, e.g. '192.168.1.0/24'")
    description: str = Field("", description="Human-readable label for this entry")
