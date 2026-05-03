"""
Auth Router - FastAPI endpoints for authentication

Contains all authentication endpoints: login, signup, refresh, logout
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from modules.shared.database import get_db
from modules.college.database import get_college_async_db # NEW
from modules.shared.config import settings
from modules.auth.dependencies import get_current_user

from modules.auth.service import AuthService
from modules.auth.schemas import (
    LoginRequest,
    TokenResponse,
    AuthSessionResponse,
    UserResponse,
    StudentCreate,
    TeacherCreate,
    AuthorityCreate,
    AdminCreate,
    ParentCreate,
    SignupResponse,
    LogoutResponse,
    RefreshRequest,
)
from modules.shared.models import PortalType


router = APIRouter(tags=["Authentication"])


# ====================
# Login Endpoints
# ====================

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return access token (OAuth2 form)"""
    service = AuthService(db)
    return await service.authenticate_user(
        LoginRequest(username=form_data.username, password=form_data.password)
    )


@router.post("/login-json", response_model=AuthSessionResponse)
async def login_json(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return access token (JSON body)"""
    service = AuthService(db)
    result = await service.authenticate_user_json(login_data)
    return result


# ====================
# Refresh Token
# ====================

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token"""
    # Get refresh token from cookie or header
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        # Check header if not in cookie
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            refresh_token = authorization.split(" ")[1]
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    service = AuthService(db)
    return await service.refresh_token(refresh_token)


# ====================
# Signup Endpoints
# ====================

@router.post("/signup/student", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new student"""
    service = AuthService(db)
    try:
        return await service.signup_student(student_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/teacher", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_teacher(
    teacher_data: TeacherCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new teacher"""
    service = AuthService(db)
    try:
        return await service.signup_teacher(teacher_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/admin", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_admin(
    admin_data: AdminCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new admin (requires secret key)"""
    service = AuthService(db)
    try:
        return await service.signup_admin(admin_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/authority", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_authority(
    authority_data: AuthorityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new authority (requires secret key)"""
    service = AuthService(db)
    try:
        return await service.signup_authority(authority_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/parent", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_parent(
    parent_data: ParentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new parent"""
    service = AuthService(db)
    try:
        return await service.signup_parent(parent_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/hod", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_hod(
    hod_data: TeacherCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new HOD"""
    service = AuthService(db)
    try:
        return await service.signup_hod(hod_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/exam-section", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_exam_section(
    exam_data: AuthorityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new exam section (requires secret key)"""
    service = AuthService(db)
    try:
        return await service.signup_exam_section(exam_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/library", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_library(
    library_data: AuthorityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new library manager (requires secret key)"""
    service = AuthService(db)
    try:
        return await service.signup_library(library_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/account", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_account(
    account_data: AuthorityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new account section (requires secret key)"""
    service = AuthService(db)
    try:
        return await service.signup_account(account_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ====================
# College Signup Endpoints
# ====================

@router.post("/signup/college/student", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_college_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db),
    college_db: AsyncSession = Depends(get_college_async_db) # NEW
):
    """Register a new college student"""
    # Validate portal_type is college
    if student_data.portal_type != PortalType.COLLEGE:
        raise HTTPException(status_code=400, detail="This endpoint is for college students only. Use portal_type='college'")
    
    service = AuthService(db, college_db=college_db) # Updated
    try:
        return await service.signup_college_student(student_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/college/teacher", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_college_teacher(
    teacher_data: TeacherCreate,
    db: AsyncSession = Depends(get_db),
    college_db: AsyncSession = Depends(get_college_async_db) # NEW
):
    """Register a new college faculty/teacher"""
    if teacher_data.portal_type != PortalType.COLLEGE:
        raise HTTPException(status_code=400, detail="This endpoint is for college faculty only. Use portal_type='college'")
    
    service = AuthService(db, college_db=college_db) # Updated
    try:
        return await service.signup_college_teacher(teacher_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup/college/authority", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup_college_authority(
    authority_data: AuthorityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a college authority (HOD, Dean, Registrar, Exam Section, Account Section, etc.)"""
    if authority_data.portal_type != PortalType.COLLEGE:
        raise HTTPException(status_code=400, detail="This endpoint is for college authorities only. Use portal_type='college'")
    
    # For college authorities, secret key might be required depending on role
    service = AuthService(db)
    try:
        return await service.signup_college_authority(authority_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ====================
# Logout Endpoint
# ====================

@router.post("/logout", response_model=LogoutResponse)
async def logout(response: Response):
    """Logout user and clear tokens"""
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return LogoutResponse(message="Logged out successfully")


# ====================
# Current User Endpoint
# ====================

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


__all__ = ["router"]
