# update main.py to include home page route

# update main.py to include home page route

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from tables.tables import Token, LoginRequest, UserResponse, StudentCreate, TeacherCreate, AuthorityCreate
from models.models import User, UserRole
from config.config import settings

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = UserRepository.authenticate(db, form_data.username, form_data.password)
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
    
    access_token = AuthService.create_token_for_user(user)
    
    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user).model_dump(mode='json')
    })
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return response

@router.post("/login-json", response_model=Token)
async def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = UserRepository.authenticate(db, login_data.username, login_data.password)
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
    
    access_token = AuthService.create_token_for_user(user)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@router.post("/signup/student")
async def signup_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    """Public student registration"""
    # Check if user already exists
    existing_user = UserRepository.get_by_email(db, student_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = UserRepository.get_by_username(db, student_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if student_id exists
    from repositories.student_repository import StudentRepository
    existing_student = StudentRepository.get_by_student_id(db, student_data.student_id)
    if existing_student:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
    # Create user
    user = UserRepository.create(
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
        "date_of_birth": student_data.date_of_birth,
        "phone": student_data.phone,
        "address": student_data.address,
        "parent_name": student_data.parent_name,
        "parent_phone": student_data.parent_phone,
        "grade_level": student_data.grade_level,
        "section": student_data.section
    }
    
    created_student = StudentRepository.create(db, student_profile_data)
    
    return {
        "message": "Student account created successfully",
        "user": UserResponse.from_orm(user)
    }

@router.post("/signup/teacher")
async def signup_teacher(
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db)
):
    """Public teacher registration"""
    # Check if user already exists
    existing_user = UserRepository.get_by_email(db, teacher_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = UserRepository.get_by_username(db, teacher_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if employee_id exists
    from repositories.teacher_repository import TeacherRepository
    existing_teacher = TeacherRepository.get_by_employee_id(db, teacher_data.employee_id)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    # Create user
    user = UserRepository.create(
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
        "phone": teacher_data.phone,
        "department": teacher_data.department,
        "qualification": teacher_data.qualification,
        "specialization": teacher_data.specialization
    }
    
    created_teacher = TeacherRepository.create(db, teacher_profile_data)
    
    return {
        "message": "Teacher account created successfully",
        "user": UserResponse.from_orm(user)
    }

@router.post("/signup/authority")
async def signup_authority(
    authority_data: AuthorityCreate,
    db: Session = Depends(get_db)
):
    """Public authority registration"""
    # Verify secret key
    if authority_data.secret_key != settings.AUTHORITY_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid authority secret key")

    # Check if user already exists
    existing_user = UserRepository.get_by_email(db, authority_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = UserRepository.get_by_username(db, authority_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user
    user = UserRepository.create(
        db=db,
        email=authority_data.email,
        username=authority_data.username,
        password=authority_data.password,
        full_name=authority_data.full_name,
        role=UserRole.AUTHORITY
    )
    
    # Create authority profile
    # We need an AuthorityRepository, but for now we can do it directly or add it.
    # Let's check if AuthorityRepository exists or just use generic DB add.
    # Looking at other endpoints, they use repositories.
    # Let's use direct DB for now to avoid creating a new file if not needed, 
    # but wait, `routes/authority.py` imports `get_current_authority`.
    # Let's just do direct DB insertion for the profile here to be safe and quick.
    from models.models import Authority
    
    authority_profile = Authority(
        user_id=user.id,
        position=authority_data.position,
        department=authority_data.department,
        phone=authority_data.phone
    )
    db.add(authority_profile)
    db.commit()
    db.refresh(authority_profile)
    
    return {
        "message": "Authority account created successfully",
        "user": UserResponse.from_orm(user)
    }