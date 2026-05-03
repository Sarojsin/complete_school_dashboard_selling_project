"""
Auth API Routes - Authentication endpoints

Contains login, logout, refresh, change password, and user info endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.shared.database import get_db
from modules.auth.service import AuthService
from modules.auth.schemas import LoginRequest, TokenResponse, RefreshRequest, ChangePasswordRequest
from modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return access and refresh tokens.
    
    Args:
        data: LoginRequest with username and password
        db: Database session
    
    Returns:
        TokenResponse with access_token, refresh_token, token_type, and role
    """
    return AuthService(db).login(data)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using a valid refresh token.
    
    Args:
        data: RefreshRequest with refresh_token
        db: Database session
    
    Returns:
        TokenResponse with new access and refresh tokens
    """
    return AuthService(db).refresh_access_token(data.refresh_token)


@router.post("/logout")
def logout(current_user=Depends(get_current_user)):
    """
    Logout user (stateless - client discards tokens).
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Success message
    """
    return {"message": "Logged out successfully"}


@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password.
    
    Args:
        data: ChangePasswordRequest with current and new password
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Success message
    """
    return AuthService(db).change_password(
        current_user.id, 
        data.current_password, 
        data.new_password
    )


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        User information (id, username, email, role, is_active)
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role),
        "is_active": current_user.is_active
    }


__all__ = ["router"]