"""
app.api.schemas.admin.users
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydantic request/response schemas for the admin user-management API.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class PasswordResetRequest(BaseModel):
    new_password: str = Field(..., min_length=8, description="New plain-text password (min 8 chars)")


class ChangeRoleRequest(BaseModel):
    """
    Request body for changing a user's role.

    Previously the endpoint accepted ``new_role`` as a raw query param,
    which is semantically wrong for a state-mutating operation and breaks
    OpenAPI documentation. This typed body schema fixes that.
    """
    new_role: str = Field(..., description="Target UserRole enum value, e.g. 'teacher'")
