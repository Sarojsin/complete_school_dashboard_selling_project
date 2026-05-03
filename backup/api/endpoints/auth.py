from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from datetime import datetime
import os
from backup.core.database import get_async_db
from backup.repositories.user_repository import UserRepository
from backup.services.auth_service import AuthService
from backup.repositories.admin_settings_repository import AdminSettingsRepository
from backup.repositories.admin_user_repository import AdminUserRepository
from backup.schemas.misc import LoginRequest, UserResponse, StudentCreate, TeacherCreate, AuthorityCreate, ParentCreate
from backup.schemas.auth import AuthSessionResponse
from backup.schemas.admin import AdminCreate
from backup.models.models import User, UserRole
from backup.core.config import settings
from backup.services.password_policy_service import PasswordPolicyService

router = APIRouter()


async def _record_login_event(
    db: AsyncSession,
    username: str,
    success: bool,
    user_id: int = None,
    ip_address: str = None,
    user_agent: str = None,
    failure_reason: str = None,
):
    """
    Best-effort login auditing.

    This should never break authentication flow if audit tables are not yet deployed.
    """
    from datetime import datetime

    try:
        await AdminUserRepository.create_login_history(
            db=db,
            username=username,
            success=success,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason=failure_reason,
            token_issued_at=datetime.utcnow() if success else None,
        )

        # Failed-attempt aggregation is best-effort; absence of its table
        # should not roll back login_history persistence.
        try:
            if success:
                await AdminUserRepository.clear_failed_login_attempts(db, username, ip_address)
            else:
                row = await AdminUserRepository.increment_failed_login_attempt(
                    db, username=username, ip_address=ip_address, reason=failure_reason
                )
                security_settings = await AdminSettingsRepository.get_setting_value(
                    db,
                    "security_settings",
                    {
                        "failed_login_attempts_allowed": 5,
                        "account_lockout_minutes": 30,
                    },
                )
                max_attempts = security_settings.get("failed_login_attempts_allowed", 5)
                if user_id and row and row.attempts_count >= max_attempts:
                    await AdminUserRepository.set_user_lock(
                        db=db,
                        user_id=user_id,
                        lock=True,
                        admin_user_id=user_id,
                        reason="Too many failed login attempts",
                    )
        except Exception:
            pass

        await db.commit()
    except Exception:
        await db.rollback()


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        secure=not settings.DEBUG,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=not settings.DEBUG,
        path="/",
    )

@router.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    user = await UserRepository.get_by_username(db, form_data.username)
    if user:
        # Auto-unlock if lockout duration passed
        try:
            state = await AdminUserRepository.get_user_security_state(db, user.id)
            if state and state.is_locked and state.locked_at:
                security_settings = await AdminSettingsRepository.get_setting_value(
                    db, "security_settings", {"account_lockout_minutes": 30}
                )
                lockout_minutes = security_settings.get("account_lockout_minutes", 30)
                if lockout_minutes and (datetime.utcnow() - state.locked_at).total_seconds() >= lockout_minutes * 60:
                    await AdminUserRepository.set_user_lock(db, user.id, lock=False, admin_user_id=user.id)
                    await db.commit()
                else:
                    await _record_login_event(
                        db=db,
                        username=form_data.username,
                        success=False,
                        user_id=user.id,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        failure_reason="account_locked",
                    )
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Account is locked",
                    )
        except HTTPException:
            raise
        except Exception:
            pass

    user = await UserRepository.authenticate(db, form_data.username, form_data.password)
    if not user:
        await _record_login_event(
            db=db,
            username=form_data.username,
            success=False,
            user_id=user.id if user else None,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason="invalid_credentials",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        await _record_login_event(
            db=db,
            username=form_data.username,
            success=False,
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason="account_inactive",
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    jwt_settings = await AdminSettingsRepository.get_setting_value(
        db, "jwt_settings", {"access_token_expiration": settings.ACCESS_TOKEN_EXPIRE_MINUTES, "refresh_token_expiration": settings.REFRESH_TOKEN_EXPIRE_DAYS}
    )
    tokens = AuthService.create_token_for_user(
        user,
        access_expires_minutes=jwt_settings.get("access_token_expiration"),
        refresh_expires_days=jwt_settings.get("refresh_token_expiration"),
    )
    
    response = JSONResponse(content={
        "token_type": "bearer",
        "user": UserResponse.model_validate(user).model_dump(mode='json')
    })
    
    # Set as session cookies (no max_age/expires means delete on browser close)
    _set_auth_cookies(response, tokens["access_token"], tokens["refresh_token"])
    await _record_login_event(
        db=db,
        username=form_data.username,
        success=True,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    return response

@router.post("/login-json", response_model=AuthSessionResponse)
async def login_json(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_async_db)
):
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    user = await UserRepository.get_by_username(db, login_data.username)
    if user:
        try:
            state = await AdminUserRepository.get_user_security_state(db, user.id)
            if state and state.is_locked and state.locked_at:
                security_settings = await AdminSettingsRepository.get_setting_value(
                    db, "security_settings", {"account_lockout_minutes": 30}
                )
                lockout_minutes = security_settings.get("account_lockout_minutes", 30)
                if lockout_minutes and (datetime.utcnow() - state.locked_at).total_seconds() >= lockout_minutes * 60:
                    await AdminUserRepository.set_user_lock(db, user.id, lock=False, admin_user_id=user.id)
                    await db.commit()
                else:
                    await _record_login_event(
                        db=db,
                        username=login_data.username,
                        success=False,
                        user_id=user.id,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        failure_reason="account_locked",
                    )
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is locked")
        except HTTPException:
            raise
        except Exception:
            pass

    user = await UserRepository.authenticate(db, login_data.username, login_data.password)
    if not user:
        await _record_login_event(
            db=db,
            username=login_data.username,
            success=False,
            user_id=user.id if user else None,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason="invalid_credentials",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        await _record_login_event(
            db=db,
            username=login_data.username,
            success=False,
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason="account_inactive",
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    jwt_settings = await AdminSettingsRepository.get_setting_value(
        db, "jwt_settings", {"access_token_expiration": settings.ACCESS_TOKEN_EXPIRE_MINUTES, "refresh_token_expiration": settings.REFRESH_TOKEN_EXPIRE_DAYS}
    )
    tokens = AuthService.create_token_for_user(
        user,
        access_expires_minutes=jwt_settings.get("access_token_expiration"),
        refresh_expires_days=jwt_settings.get("refresh_token_expiration"),
    )
    await _record_login_event(
        db=db,
        username=login_data.username,
        success=True,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    response = JSONResponse(content={
        "token_type": "bearer",
        "user": UserResponse.model_validate(user).model_dump(mode='json')
    })
    _set_auth_cookies(response, tokens["access_token"], tokens["refresh_token"])
    return response

@router.post("/refresh")
async def refresh_token(
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        # Check header if not in cookie
        authorization: str = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            refresh_token = authorization.split(" ")[1]

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    user_id = AuthService.verify_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = await UserRepository.get_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    # Enforce lock/force-logout on refresh tokens
    try:
        state = await AdminUserRepository.get_user_security_state(db, user.id)
        if state and state.is_locked:
            raise HTTPException(status_code=403, detail="Account is locked")
        if state and state.force_logout_after:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_iat = payload.get("iat")
            if token_iat is not None:
                token_issued_at = datetime.utcfromtimestamp(int(token_iat))
                if token_issued_at <= state.force_logout_after:
                    raise HTTPException(status_code=401, detail="Refresh token revoked")
    except HTTPException:
        raise
    except Exception:
        pass

    jwt_settings = await AdminSettingsRepository.get_setting_value(
        db, "jwt_settings", {"access_token_expiration": settings.ACCESS_TOKEN_EXPIRE_MINUTES, "refresh_token_expiration": settings.REFRESH_TOKEN_EXPIRE_DAYS}
    )
    tokens = AuthService.create_token_for_user(
        user,
        access_expires_minutes=jwt_settings.get("access_token_expiration"),
        refresh_expires_days=jwt_settings.get("refresh_token_expiration"),
    )
    
    response = JSONResponse(content={
        "token_type": "bearer"
    })
    
    _set_auth_cookies(response, tokens["access_token"], tokens["refresh_token"])
    return response

@router.post("/signup/student")
async def signup_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public student registration"""
    # Check if user already exists
    existing_user = await UserRepository.get_by_email(db, student_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, student_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if student_id exists
    from backup.repositories.student_repository import StudentRepository
    existing_student = await StudentRepository.get_by_student_id(db, student_data.student_id)
    if existing_student:
        raise HTTPException(status_code=400, detail="Student ID already exists")

    await PasswordPolicyService.enforce(db, student_data.password)
    
    # Create user
    user = await UserRepository.create(
        db=db,
        email=student_data.email,
        username=student_data.username,
        password=student_data.password,
        full_name=student_data.full_name,
        role=UserRole.STUDENT
    )
    
    # Create student profile
    student_profile_data = {
        "user_id": user.id,
        "student_id": student_data.student_id,
        "full_name": student_data.full_name,
        "date_of_birth": student_data.date_of_birth,
        "phone": student_data.phone,
        "address": student_data.address,
        "parent_name": student_data.parent_name,
        "parent_phone": student_data.parent_phone,
        "grade_level": student_data.grade_level,
        "section": student_data.section
    }
    
    await StudentRepository.create(db, student_profile_data)
    
    return {
        "message": "Student account created successfully",
        "user": UserResponse.model_validate(user)
    }

@router.post("/signup/teacher")
async def signup_teacher(
    teacher_data: TeacherCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public teacher registration"""
    # Check if user already exists
    existing_user = await UserRepository.get_by_email(db, teacher_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, teacher_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if employee_id exists
    from backup.repositories.teacher_repository import TeacherRepository
    existing_teacher = await TeacherRepository.get_by_employee_id(db, teacher_data.employee_id)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    await PasswordPolicyService.enforce(db, teacher_data.password)
    
    # Create user
    user = await UserRepository.create(
        db=db,
        email=teacher_data.email,
        username=teacher_data.username,
        password=teacher_data.password,
        full_name=teacher_data.full_name,
        role=UserRole.TEACHER
    )
    
    # Create teacher profile
    teacher_profile_data = {
        "user_id": user.id,
        "employee_id": teacher_data.employee_id,
        "full_name": teacher_data.full_name,
        "phone": teacher_data.phone,
        "department": teacher_data.department,
        "qualification": teacher_data.qualification,
        "specialization": teacher_data.specialization
    }
    
    await TeacherRepository.create(db, teacher_profile_data)
    
    return {
        "message": "Teacher account created successfully",
        "user": UserResponse.model_validate(user)
    }

@router.post("/signup/admin", status_code=status.HTTP_201_CREATED)
async def signup_admin(
    admin_data: AdminCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public admin registration - requires special secret key"""
    # Check if ADMIN_SECRET_KEY is configured
    if not settings.is_admin_secret_configured:
        raise HTTPException(
            status_code=500,
            detail="Admin registration is not configured. Please set ADMIN_SECRET_KEY environment variable."
        )
    
    # Verify secret key
    if admin_data.secret_key != settings.ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin secret key")

    # Check if user already exists
    existing_user = await UserRepository.get_by_email(db, admin_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, admin_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    await PasswordPolicyService.enforce(db, admin_data.password)
    
    # Create user with ADMIN role
    user = await UserRepository.create(
        db=db,
        email=admin_data.email,
        username=admin_data.username,
        password=admin_data.password,
        full_name=admin_data.full_name,
        role=UserRole.ADMIN
    )
    
    return {
        "message": "Admin account created successfully",
        "user": UserResponse.model_validate(user)
    }

@router.post("/signup/authority")
async def signup_authority(
    authority_data: AuthorityCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public authority registration"""
    # Verify secret key
    if authority_data.secret_key != settings.AUTHORITY_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid authority secret key")

    # Check if user already exists
    existing_user = await UserRepository.get_by_email(db, authority_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, authority_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    await PasswordPolicyService.enforce(db, authority_data.password)
    
    # Create user
    user = await UserRepository.create(
        db=db,
        email=authority_data.email,
        username=authority_data.username,
        password=authority_data.password,
        full_name=authority_data.full_name,
        role=UserRole.AUTHORITY
    )
    
    # Create authority profile
    from backup.models.models import Authority
    
    authority_profile = Authority(
        user_id=user.id,
        position=authority_data.position,
        department=authority_data.department,
        phone=authority_data.phone
    )
    db.add(authority_profile)
    await db.commit()
    await db.refresh(authority_profile)
    
    return {
        "message": "Authority account created successfully",
        "user": UserResponse.model_validate(user)
    }

@router.post("/signup/parent")
async def signup_parent(
    parent_data: ParentCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public parent registration"""
    # Check if user already exists
    existing_user = await UserRepository.get_by_email(db, parent_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, parent_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Verify student exists
    from backup.repositories.student_repository import StudentRepository
    student = await StudentRepository.get_by_student_id(db, parent_data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if student already has a parent
    if student.parent_id:
        raise HTTPException(status_code=400, detail="Student already has a linked parent")

    await PasswordPolicyService.enforce(db, parent_data.password)
    
    # Create user
    user = await UserRepository.create(
        db=db,
        email=parent_data.email,
        username=parent_data.username,
        password=parent_data.password,
        full_name=parent_data.full_name,
        role=UserRole.PARENT
    )
    
    # Create parent profile
    from backup.repositories.parent_repository import ParentRepository
    parent_profile_data = {
        "user_id": user.id,
        "phone": parent_data.phone,
        "full_name": parent_data.full_name,
        "address": parent_data.address,
        "occupation": parent_data.occupation
    }
    
    created_parent = await ParentRepository.create(db, parent_profile_data)
    
    # Link student to parent
    await ParentRepository.link_child(db, created_parent.id, student.id)
    
    return {
        "message": "Parent account created successfully",
        "user": UserResponse.model_validate(user)
    }

@router.post("/signup/hod")
async def signup_hod(
    teacher_data: TeacherCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public HOD registration"""
    # Check if user already exists
    existing_user = await UserRepository.get_by_email(db, teacher_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, teacher_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if employee_id exists
    from backup.repositories.teacher_repository import TeacherRepository
    existing_teacher = await TeacherRepository.get_by_employee_id(db, teacher_data.employee_id)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    await PasswordPolicyService.enforce(db, teacher_data.password)
    
    # Create user
    user = await UserRepository.create(
        db=db,
        email=teacher_data.email,
        username=teacher_data.username,
        password=teacher_data.password,
        full_name=teacher_data.full_name,
        role=UserRole.HOD
    )
    
    # Create teacher profile
    teacher_profile_data = {
        "user_id": user.id,
        "employee_id": teacher_data.employee_id,
        "full_name": teacher_data.full_name,
        "phone": teacher_data.phone,
        "department": teacher_data.department,
        "qualification": teacher_data.qualification,
        "specialization": teacher_data.specialization
    }
    
    await TeacherRepository.create(db, teacher_profile_data)
    
    return {
        "message": "HOD account created successfully",
        "user": UserResponse.model_validate(user)
    }

@router.post("/signup/exam-section")
async def signup_exam_section(
    authority_data: AuthorityCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public exam section registration"""
    if authority_data.secret_key != settings.AUTHORITY_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid secret key")

    existing_user = await UserRepository.get_by_email(db, authority_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, authority_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    await PasswordPolicyService.enforce(db, authority_data.password)
    
    user = await UserRepository.create(
        db=db,
        email=authority_data.email,
        username=authority_data.username,
        password=authority_data.password,
        full_name=authority_data.full_name,
        role=UserRole.EXAM_SECTION
    )
    
    from backup.models.models import Authority
    authority_profile = Authority(
        user_id=user.id,
        position=authority_data.position,
        department=authority_data.department,
        phone=authority_data.phone
    )
    db.add(authority_profile)
    await db.commit()
    
    return {
        "message": "Exam Section account created successfully",
        "user": UserResponse.model_validate(user)
    }

@router.post("/signup/library")
async def signup_library(
    authority_data: AuthorityCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public library registration"""
    if authority_data.secret_key != settings.AUTHORITY_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid secret key")

    existing_user = await UserRepository.get_by_email(db, authority_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, authority_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    await PasswordPolicyService.enforce(db, authority_data.password)
    
    user = await UserRepository.create(
        db=db,
        email=authority_data.email,
        username=authority_data.username,
        password=authority_data.password,
        full_name=authority_data.full_name,
        role=UserRole.LIBRARY_MANAGER
    )
    
    from backup.models.models import Authority
    authority_profile = Authority(
        user_id=user.id,
        position=authority_data.position,
        department=authority_data.department,
        phone=authority_data.phone
    )
    db.add(authority_profile)
    await db.commit()
    
    return {
        "message": "Library account created successfully",
        "user": UserResponse.model_validate(user)
    }

@router.post("/signup/account")
async def signup_account(
    authority_data: AuthorityCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Public account section registration"""
    if authority_data.secret_key != settings.AUTHORITY_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid secret key")

    existing_user = await UserRepository.get_by_email(db, authority_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = await UserRepository.get_by_username(db, authority_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    await PasswordPolicyService.enforce(db, authority_data.password)
    
    user = await UserRepository.create(
        db=db,
        email=authority_data.email,
        username=authority_data.username,
        password=authority_data.password,
        full_name=authority_data.full_name,
        role=UserRole.ACCOUNT_SECTION
    )
    
    from backup.models.models import Authority
    authority_profile = Authority(
        user_id=user.id,
        position=authority_data.position,
        department=authority_data.department,
        phone=authority_data.phone
    )
    db.add(authority_profile)
    await db.commit()
    
    return {
        "message": "Account Section account created successfully",
        "user": UserResponse.model_validate(user)
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"message": "Logged out successfully"}
