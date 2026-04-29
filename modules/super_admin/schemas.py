"""
Super Admin Schemas - Pydantic models for admin operations

Contains request/response schemas for admin functionality.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime


class SystemSettingUpdate(BaseModel):
    """Update system setting request"""
    value: str


class SystemSettingResponse(BaseModel):
    """System setting response"""
    key: str
    value: Optional[str]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class FeatureToggle(BaseModel):
    """Feature toggle request"""
    is_enabled: bool


class FeatureCreate(BaseModel):
    """Create feature request"""
    feature_code: str = Field(..., min_length=1, max_length=100)
    feature_name: str = Field(..., min_length=1, max_length=200)
    feature_category: str
    description: Optional[str] = None
    is_global: bool = False


class FeatureUpdate(BaseModel):
    """Update feature request"""
    feature_name: Optional[str] = None
    description: Optional[str] = None
    is_global: Optional[bool] = None


class FeatureResponse(BaseModel):
    """Feature response"""
    id: int
    feature_code: str
    feature_name: str
    feature_category: str
    is_enabled: bool
    is_global: bool
    description: Optional[str]
    
    class Config:
        from_attributes = True


class RolePermissionUpdate(BaseModel):
    """Update role permission"""
    role: str
    can_create: bool = False
    can_read: bool = True
    can_update: bool = False
    can_delete: bool = False


class FeatureWithPermissionsResponse(FeatureResponse):
    """Feature with permissions"""
    role_permissions: List[Dict[str, Any]] = []


class AuditLogResponse(BaseModel):
    """Audit log response"""
    id: int
    user_id: Optional[int]
    action: str
    details: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class BackupResponse(BaseModel):
    """Backup response"""
    id: int
    filename: str
    size_bytes: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_schools: int = 0
    total_colleges: int = 0
    total_users: int = 0
    total_students: int = 0
    total_teachers: int = 0
    active_sessions: int = 0
    system_health: str = "healthy"


class UserCountByRole(BaseModel):
    """User count by role"""
    role: str
    count: int


class OverviewResponse(BaseModel):
    """Dashboard overview"""
    users: int
    students: int
    teachers: int
    courses: int
    notices: int
    assignments: int


class FeaturesSummaryResponse(BaseModel):
    """Features summary"""
    total: int
    enabled: int
    disabled: int
    categories: List[str]


class AnalyticsResponse(BaseModel):
    """Analytics response"""
    period: str
    data: Dict[str, Any]


class UserManageResponse(BaseModel):
    """User management response"""
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True


class UserDeactivateRequest(BaseModel):
    """User deactivation request"""
    reason: Optional[str] = None