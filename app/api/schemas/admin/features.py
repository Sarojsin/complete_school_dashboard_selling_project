"""
app.api.schemas.admin.features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydantic request/response schemas for the admin feature-management API.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class FeatureCreate(BaseModel):
    feature_code: str = Field(..., description="Unique machine-readable identifier, e.g. 'CHAT_ENABLED'")
    feature_name: str = Field(..., description="Human-readable display name")
    feature_category: Optional[str] = Field(None, description="Grouping category")
    description: Optional[str] = None
    is_enabled: bool = True
    is_global: bool = True


class FeatureUpdate(BaseModel):
    feature_name: Optional[str] = None
    feature_category: Optional[str] = None
    description: Optional[str] = None
    is_enabled: Optional[bool] = None
    is_global: Optional[bool] = None


class RolePermissionUpdate(BaseModel):
    role: str = Field(..., description="UserRole enum value string, e.g. 'teacher'")
    can_create: bool = True
    can_read: bool = True
    can_update: bool = True
    can_delete: bool = True


class RolePermissionsBatchUpdate(BaseModel):
    """
    Batch payload for updating multiple role permissions in a single request.

    Example::

        {
            "roles": {
                "teacher": {"can_create": true, "can_read": true, ...},
                "student": {"can_create": false, "can_read": true, ...}
            }
        }
    """
    roles: dict[str, dict[str, bool]]


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class FeatureResponse(BaseModel):
    id: int
    feature_code: str
    feature_name: str
    feature_category: Optional[str]
    description: Optional[str]
    is_enabled: bool
    is_global: bool

    model_config = {"from_attributes": True}


class FeatureDetailResponse(FeatureResponse):
    """Feature response with its associated role permissions."""
    role_permissions: List[dict] = []
