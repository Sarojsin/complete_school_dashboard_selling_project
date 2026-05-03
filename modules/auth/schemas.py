from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from modules.shared.models import UserRole, PortalType


# ====================
# Login Schemas
# ====================

class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str
    portal_type: Optional[PortalType] = None  # Optional portal hint


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    portal_type: PortalType


class AuthSessionResponse(BaseModel):
    """Auth session response with user info"""
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class RefreshRequest(BaseModel):
    refresh_token: str


# ====================
# User Response
# ====================

class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    portal_type: PortalType
    is_active: bool

    class Config:
        from_attributes = True


# ====================
# Password Schemas
# ====================

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


# ====================
# Signup Schemas
# ====================

class StudentCreate(BaseModel):
    """Student signup schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str
    student_id: str = Field(..., min_length=1, max_length=50)
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None
    portal_type: PortalType


class TeacherCreate(BaseModel):
    """Teacher signup schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str
    employee_id: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    portal_type: PortalType


class AuthorityCreate(BaseModel):
    """Authority signup schema (used for authority, exam-section, library, account)"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str
    secret_key: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    portal_type: PortalType


class AdminCreate(BaseModel):
    """Admin signup schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str
    secret_key: str
    portal_type: PortalType


class ParentCreate(BaseModel):
    """Parent signup schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: str
    student_id: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None
    portal_type: PortalType


# ====================
# Signup Response
# ====================

class SignupResponse(BaseModel):
    """Signup response schema"""
    message: str
    user: UserResponse


# ====================
# Logout Response
# ====================

class LogoutResponse(BaseModel):
    message: str


# Update forward reference
AuthSessionResponse.model_rebuild()

__all__ = [
    "LoginRequest",
    "TokenResponse",
    "AuthSessionResponse",
    "RefreshRequest",
    "UserResponse",
    "ChangePasswordRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "StudentCreate",
    "TeacherCreate",
    "AuthorityCreate",
    "AdminCreate",
    "ParentCreate",
    "SignupResponse",
    "LogoutResponse",
]
