from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_async_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.misc import Token, LoginRequest, UserResponse, StudentCreate, TeacherCreate, AuthorityCreate, ParentCreate
from app.models.models import User, UserRole
from app.core.config import settings

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    user = await UserRepository.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    tokens = AuthService.create_token_for_user(user)
    
    response = JSONResponse(content={
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user": UserResponse.from_orm(user).model_dump(mode='json')
    })
    
    # Set as session cookies (no max_age/expires means delete on browser close)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {tokens['access_token']}",
        httponly=True,
        samesite="lax",
        secure=not settings.DEBUG,
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        samesite="lax",
        secure=not settings.DEBUG,
        path="/"
    )
    return response

@router.post("/login-json", response_model=Token)
async def login_json(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_async_db)
):
    user = await UserRepository.authenticate(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    tokens = AuthService.create_token_for_user(user)
    
    return Token(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

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

    tokens = AuthService.create_token_for_user(user)
    
    response = JSONResponse(content={
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    })
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {tokens['access_token']}",
        httponly=True,
        samesite="lax",
        secure=not settings.DEBUG,
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        samesite="lax",
        secure=not settings.DEBUG,
        path="/"
    )
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
    from app.repositories.student_repository import StudentRepository
    existing_student = await StudentRepository.get_by_student_id(db, student_data.student_id)
    if existing_student:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
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
        "user": UserResponse.from_orm(user)
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
    from app.repositories.teacher_repository import TeacherRepository
    existing_teacher = await TeacherRepository.get_by_employee_id(db, teacher_data.employee_id)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
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
        "user": UserResponse.from_orm(user)
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
    from app.models.models import Authority
    
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
        "user": UserResponse.from_orm(user)
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
    from app.repositories.student_repository import StudentRepository
    student = await StudentRepository.get_by_student_id(db, parent_data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if student already has a parent
    if student.parent_id:
        raise HTTPException(status_code=400, detail="Student already has a linked parent")
    
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
    from app.repositories.parent_repository import ParentRepository
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
        "user": UserResponse.from_orm(user)
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
    from app.repositories.teacher_repository import TeacherRepository
    existing_teacher = await TeacherRepository.get_by_employee_id(db, teacher_data.employee_id)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
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
        "user": UserResponse.from_orm(user)
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
    
    user = await UserRepository.create(
        db=db,
        email=authority_data.email,
        username=authority_data.username,
        password=authority_data.password,
        full_name=authority_data.full_name,
        role=UserRole.EXAM_SECTION
    )
    
    from app.models.models import Authority
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
        "user": UserResponse.from_orm(user)
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
    
    user = await UserRepository.create(
        db=db,
        email=authority_data.email,
        username=authority_data.username,
        password=authority_data.password,
        full_name=authority_data.full_name,
        role=UserRole.LIBRARY_MANAGER
    )
    
    from app.models.models import Authority
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
        "user": UserResponse.from_orm(user)
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
    
    user = await UserRepository.create(
        db=db,
        email=authority_data.email,
        username=authority_data.username,
        password=authority_data.password,
        full_name=authority_data.full_name,
        role=UserRole.ACCOUNT_SECTION
    )
    
    from app.models.models import Authority
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
        "user": UserResponse.from_orm(user)
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"message": "Logged out successfully"}
