"""
Auth Service - Business logic for authentication

Contains authentication, token creation, and user registration.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from jose import jwt, JWTError

from modules.shared.models import User, UserRole, PortalType
from modules.shared.auth_utils import verify_password, create_access_token, get_password_hash
from modules.shared.config import settings
from modules.shared.exceptions import UnauthorizedError, ForbiddenError

from modules.auth.repository import AuthRepository
from modules.auth.schemas import (
    LoginRequest,
    TokenResponse,
    UserResponse,
    StudentCreate,
    TeacherCreate,
    AuthorityCreate,
    AdminCreate,
    ParentCreate,
    SignupResponse,
)


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db: AsyncSession, college_db: Optional[AsyncSession] = None):
        self.db = db
        self.college_db = college_db
        self.repository = AuthRepository(db)

    async def authenticate_user(self, data: LoginRequest) -> TokenResponse:
        """Authenticate user and return access token"""
        user = await self.repository.authenticate(data.username, data.password)
        
        if not user:
            raise UnauthorizedError("Invalid username or password")
        
        if not user.is_active:
            raise ForbiddenError("Account is deactivated")
        
        # Validate portal_type if provided as hint
        if data.portal_type and user.portal_type != data.portal_type:
            raise ForbiddenError(
                f"Account belongs to {user.portal_type} portal. "
                f"Please select the correct portal on the login page."
            )
        
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.value,
            "portal_type": user.portal_type.value
        }
        
        access_token = create_access_token(data=token_data)
        
        return TokenResponse(
            access_token=access_token,
            role=user.role,
            portal_type=user.portal_type
        )

    async def authenticate_user_json(self, data: LoginRequest) -> Dict[str, Any]:
        """Authenticate user and return full response with user info"""
        user = await self.repository.authenticate(data.username, data.password)
        
        if not user:
            raise UnauthorizedError("Invalid username or password")
        
        if not user.is_active:
            raise ForbiddenError("Account is deactivated")
        
        # Validate portal_type if provided as hint
        if data.portal_type and user.portal_type != data.portal_type:
            raise ForbiddenError(
                f"Account belongs to {user.portal_type} portal. "
                f"Please select the correct portal on the login page."
            )
        
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.value,
            "portal_type": user.portal_type.value
        }
        
        access_token = create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        }

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token"""
        try:
            payload = jwt.decode(
                refresh_token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            if not user_id:
                raise UnauthorizedError("Invalid refresh token")
            
            user = await self.repository.get_user_by_id(int(user_id))
            if not user or not user.is_active:
                raise UnauthorizedError("User not found or inactive")
            
            token_data = {
                "sub": str(user.id),
                "username": user.username,
                "role": user.role.value,
                "portal_type": user.portal_type.value
            }
            
            access_token = create_access_token(data=token_data)
            
            return TokenResponse(
                access_token=access_token,
                role=user.role,
                portal_type=user.portal_type
            )
        except JWTError:
            raise UnauthorizedError("Invalid refresh token")

    # ====================
    # Signup Methods
    # ====================

    async def signup_student(self, data: StudentCreate) -> SignupResponse:
        """Register a new student"""
        # Check if user already exists
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Create user
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.STUDENT.value,
            portal_type=data.portal_type.value
        )
        
        # Create student profile in school_student module
        from modules.school.school_student.models import SchoolStudent
        student_profile = SchoolStudent(
            user_id=user.id,
            student_id=data.student_id,
            full_name=data.full_name,
            date_of_birth=data.date_of_birth,
            phone=data.phone,
            address=data.address,
            parent_name=data.parent_name,
            parent_phone=data.parent_phone,
            grade_level=data.grade_level,
            section=data.section,
        )
        self.db.add(student_profile)
        await self.db.commit()
        
        return SignupResponse(
            message="Student account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_teacher(self, data: TeacherCreate) -> SignupResponse:
        """Register a new teacher"""
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Create user
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.TEACHER.value,
            portal_type=data.portal_type.value
        )
        
        # Create teacher profile in school_teacher module
        from modules.school.school_teacher.models import Teacher
        teacher_profile = Teacher(
            user_id=user.id,
            employee_id=data.employee_id,
            full_name=data.full_name,
            phone=data.phone,
            department=data.department,
            qualification=data.qualification,
            specialization=data.specialization,
            status="active"
        )
        self.db.add(teacher_profile)
        await self.db.commit()
        
        return SignupResponse(
            message="Teacher account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_admin(self, data: AdminCreate) -> SignupResponse:
        """Register a new admin (requires secret key)"""
        # Verify secret key
        if not hasattr(settings, 'ADMIN_SECRET_KEY') or not settings.ADMIN_SECRET_KEY:
            raise ValueError("Admin registration is not configured")
        
        if data.secret_key != settings.ADMIN_SECRET_KEY:
            raise ValueError("Invalid admin secret key")
        
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Create user with ADMIN role
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.ADMIN.value,
            portal_type=data.portal_type.value
        )
        
        return SignupResponse(
            message="Admin account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_authority(self, data: AuthorityCreate) -> SignupResponse:
        """Register a new authority"""
        # Verify secret key
        if not hasattr(settings, 'AUTHORITY_SECRET_KEY') or not settings.AUTHORITY_SECRET_KEY:
            raise ValueError("Authority registration is not configured")
        
        if data.secret_key != settings.AUTHORITY_SECRET_KEY:
            raise ValueError("Invalid authority secret key")
        
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Create user
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.AUTHORITY.value,
            portal_type=data.portal_type.value
        )
        
        # Create authority profile in school_authority module
        from modules.school.school_authority.models import SchoolAuthority
        authority_profile = SchoolAuthority(
            user_id=user.id,
            full_name=data.full_name,
            position=data.position or "Authority",
            department=data.department,
            phone=data.phone
        )
        self.db.add(authority_profile)
        await self.db.commit()
        
        return SignupResponse(
            message="Authority account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_parent(self, data: ParentCreate) -> SignupResponse:
        """Register a new parent"""
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # TODO: Verify student exists and doesn't have a parent
        
        # Create user
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.PARENT.value,
            portal_type=data.portal_type.value
        )
        
        # Create parent profile in school_parent module and link to student
        from modules.school.school_parent.models import SchoolParent
        from modules.school.school_student.models import SchoolStudent
        from sqlalchemy import select

        parent_profile = SchoolParent(
            user_id=user.id,
            full_name=data.full_name,
            phone=data.phone,
            address=data.address,
            occupation=data.occupation
        )
        self.db.add(parent_profile)
        await self.db.flush() # Get parent.id

        # Try to link to student if provided
        if data.student_id:
            result = await self.db.execute(
                select(SchoolStudent).filter(SchoolStudent.student_id == data.student_id)
            )
            student = result.scalars().first()
            if student:
                student.parent_id = parent_profile.id
        
        await self.db.commit()
        
        return SignupResponse(
            message="Parent account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_hod(self, data: TeacherCreate) -> SignupResponse:
        """Register a new HOD"""
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Create user
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.HOD.value,
            portal_type=data.portal_type.value
        )
        
        # Create teacher profile for HOD
        from modules.school.school_teacher.models import Teacher
        teacher_profile = Teacher(
            user_id=user.id,
            employee_id=data.employee_id,
            full_name=data.full_name,
            phone=data.phone,
            department=data.department,
            qualification=data.qualification,
            specialization=data.specialization,
            status="active"
        )
        self.db.add(teacher_profile)
        await self.db.commit()
        
        return SignupResponse(
            message="HOD account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_exam_section(self, data: AuthorityCreate) -> SignupResponse:
        """Register a new exam section"""
        if not hasattr(settings, 'AUTHORITY_SECRET_KEY') or not settings.AUTHORITY_SECRET_KEY:
            raise ValueError("Registration is not configured")
        
        if data.secret_key != settings.AUTHORITY_SECRET_KEY:
            raise ValueError("Invalid secret key")
        
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.EXAM_SECTION.value,
            portal_type=data.portal_type.value
        )
        
        # Create authority profile for exam section
        from modules.school.school_authority.models import SchoolAuthority
        profile = SchoolAuthority(
            user_id=user.id,
            full_name=data.full_name,
            position="Exam Section",
            department=data.department,
            phone=data.phone
        )
        self.db.add(profile)
        await self.db.commit()
        
        return SignupResponse(
            message="Exam Section account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_library(self, data: AuthorityCreate) -> SignupResponse:
        """Register a new library manager"""
        if not hasattr(settings, 'AUTHORITY_SECRET_KEY') or not settings.AUTHORITY_SECRET_KEY:
            raise ValueError("Registration is not configured")
        
        if data.secret_key != settings.AUTHORITY_SECRET_KEY:
            raise ValueError("Invalid secret key")
        
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.LIBRARY_MANAGER.value,
            portal_type=data.portal_type.value
        )
        
        # Create authority profile for library
        from modules.school.school_authority.models import SchoolAuthority
        profile = SchoolAuthority(
            user_id=user.id,
            full_name=data.full_name,
            position="Library Manager",
            department=data.department,
            phone=data.phone
        )
        self.db.add(profile)
        await self.db.commit()
        
        return SignupResponse(
            message="Library account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_account(self, data: AuthorityCreate) -> SignupResponse:
        """Register a new account section"""
        if not hasattr(settings, 'AUTHORITY_SECRET_KEY') or not settings.AUTHORITY_SECRET_KEY:
            raise ValueError("Registration is not configured")
        
        if data.secret_key != settings.AUTHORITY_SECRET_KEY:
            raise ValueError("Invalid secret key")
        
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.ACCOUNT_SECTION.value,
            portal_type=data.portal_type.value
        )
        
        # Create authority profile for account section
        from modules.school.school_authority.models import SchoolAuthority
        profile = SchoolAuthority(
            user_id=user.id,
            full_name=data.full_name,
            position="Account Section",
            department=data.department,
            phone=data.phone
        )
        self.db.add(profile)
        await self.db.commit()
        
        return SignupResponse(
            message="Account Section account created successfully",
            user=UserResponse.model_validate(user)
        )


# ====================
# College Signup Methods
# ====================

    async def signup_college_student(self, data: StudentCreate) -> SignupResponse:
        """Register a new college student"""
        # Check if user already exists
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Validate portal_type
        if data.portal_type != PortalType.COLLEGE:
            raise ValueError("College student signup requires portal_type='college'")
        
        # Create user with college portal
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.STUDENT.value,
            portal_type=PortalType.COLLEGE.value
        )
        
        # Ensure at least one program and one semester exist (required by CollegeStudent model)
        from sqlalchemy import select
        from modules.college.college_courses.models import Program, Semester
        
        # Find any existing program
        result = await self.db.execute(select(Program).limit(1))
        program = result.scalars().first()
        if not program:
            program = Program(name="Default Program", code="DEF")
            self.db.add(program)
            await self.db.flush()  # Get ID without committing
        
        # Find any existing semester
        result = await self.db.execute(select(Semester).limit(1))
        semester = result.scalars().first()
        if not semester:
            semester = Semester(name="Semester 1", number=1, program_id=program.id)
            self.db.add(semester)
            await self.db.flush()
        
        # Create college student profile
        from modules.college.college_student.models import CollegeStudent
        college_student = CollegeStudent(
            user_id=user.id,
            roll_number=data.student_id,
            program_id=program.id,
            semester_id=semester.id,
            cgpa=0.0,
            total_credits_completed=0
        )
        
        # Use college database if in separate mode
        target_db = self.college_db if self.college_db else self.db
        target_db.add(college_student)
        await target_db.commit()
        
        return SignupResponse(
            message="College student account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_college_teacher(self, data: TeacherCreate) -> SignupResponse:
        """Register a new college faculty"""
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Validate portal_type
        if data.portal_type != PortalType.COLLEGE:
            raise ValueError("College faculty signup requires portal_type='college'")
        
        # Create user with college portal
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=UserRole.TEACHER.value,
            portal_type=PortalType.COLLEGE.value
        )
        
        # Create college faculty profile
        from modules.college.college_faculty.models import Faculty
        faculty = Faculty(
            user_id=user.id,
            employee_id=data.employee_id,
            # Optional fields - set if provided
            qualification=data.qualification,
            specialization=data.specialization,
            # department_id will be set later (requires department record)
            # designation, experience_years, joining_date will be set later
        )
        
        # Use college database if in separate mode
        target_db = self.college_db if self.college_db else self.db
        target_db.add(faculty)
        await target_db.commit()
        
        return SignupResponse(
            message="College faculty account created successfully",
            user=UserResponse.model_validate(user)
        )

    async def signup_college_authority(self, data: AuthorityCreate) -> SignupResponse:
        """Register a college authority (HOD, Dean, Registrar, Exam Section, Account Section, etc.)"""
        existing_user = await self.repository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = await self.repository.get_user_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Validate portal_type
        if data.portal_type != PortalType.COLLEGE:
            raise ValueError("College authority signup requires portal_type='college'")
        
        # Determine role based on position (or use secret key mapping)
        role = UserRole.HOD  # default for college HOD
        profile_position = data.position or "HOD"
        
        # Map position to role
        position_lower = profile_position.lower()
        if 'hod' in position_lower or 'head' in position_lower:
            role = UserRole.HOD
        elif 'dean' in position_lower:
            # Check if DEAN exists in enum, else use HOD
            role = getattr(UserRole, 'DEAN', UserRole.HOD)
        elif 'registrar' in position_lower:
            role = getattr(UserRole, 'REGISTRAR', UserRole.HOD)
        elif 'exam' in position_lower:
            role = UserRole.EXAM_SECTION
        elif 'account' in position_lower or 'finance' in position_lower:
            role = UserRole.ACCOUNT_SECTION
        elif 'library' in position_lower:
            role = UserRole.LIBRARY_MANAGER
        elif 'placement' in position_lower or 'career' in position_lower:
            role = getattr(UserRole, 'PLACEMENT', UserRole.HOD)
        elif 'research' in position_lower:
            role = getattr(UserRole, 'RESEARCH', UserRole.HOD)
        elif 'hostel' in position_lower or 'warden' in position_lower:
            role = getattr(UserRole, 'HOSTEL', UserRole.HOD)
        elif 'lab' in position_lower:
            role = getattr(UserRole, 'LAB', UserRole.HOD)
        
        # Create user with determined role and college portal
        user = await self.repository.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=role.value,
            portal_type=PortalType.COLLEGE.value
        )
        
        # For college authorities, create SchoolAuthority profile (shared table)
        # The portal_type on user distinguishes school vs college authorities
        from modules.school.school_authority.models import SchoolAuthority
        authority_profile = SchoolAuthority(
            user_id=user.id,
            full_name=data.full_name,
            position=profile_position,
            department=data.department,
            phone=data.phone
        )
        self.db.add(authority_profile)
        await self.db.commit()
        
        return SignupResponse(
            message=f"College {profile_position} account created successfully",
            user=UserResponse.model_validate(user)
        )


__all__ = ["AuthService"]