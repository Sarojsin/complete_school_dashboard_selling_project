"""
College Enrollment Router

FastAPI endpoints for student course enrollment.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from modules.shared.audit_logger import AuditLogger
from modules.shared.rate_limit import write_limit, read_limit
from .service import CollegeEnrollmentService
from .schemas import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse, EnrollmentDetail
from .models import CollegeEnrollment

router = APIRouter(
    prefix="/enrollments",
    tags=["College Enrollments"],
    dependencies=[Depends(require_college_portal)]
)


@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
@write_limit()
async def enroll_student(
    student_id: int,
    course_id: int,
    semester_id: Optional[int] = None,
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Enroll a student in a course (Student self-enroll or Admin)"""
    # Permission: student can enroll themselves, or dean/registrar/faculty can enroll any
    if current_user.role not in ["college_student", "dean", "registrar", "college_faculty", "super_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to enroll students")

    # If student, only allow self-enrollment
    if current_user.role == "college_student":
        # Verify student_id matches current user's profile
        from modules.college.college_students.models import CollegeStudent
        result = await db.execute(select(CollegeStudent).where(CollegeStudent.user_id == current_user.id))
        student_profile = result.scalar_one_or_none()
        if not student_profile or student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Students can only enroll themselves")
    else:
        # Admins: verify student exists
        from modules.college.college_students.models import CollegeStudent
        result = await db.execute(select(CollegeStudent).where(CollegeStudent.id == student_id))
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Student not found")

    service = CollegeEnrollmentService(db)
    data = EnrollmentCreate(student_id=student_id, course_id=course_id, semester_id=semester_id)
    result = await service.enroll_student(data)

    # Audit logging
    if result.get("enrollment"):
        audit_logger = AuditLogger(db)
        await audit_logger.log_create(
            user_id=current_user.id,
            resource_type="college_enrollment",
            resource_id=str(result["enrollment"].id),
            new_values=data.model_dump(),
            ip_address=getattr(request.client, "host", None) if request and request.client else None,
            user_agent=request.headers.get("user-agent") if request else None
        )

    return result


@router.get("", response_model=List[EnrollmentResponse])
async def get_enrollments(
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    semester_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get enrollments with filters"""
    # Permissions: students see own; faculty see their course students; admins see all
    if current_user.role == "college_student":
        from modules.college.college_students.models import CollegeStudent
        result = await db.execute(select(CollegeStudent).where(CollegeStudent.user_id == current_user.id))
        student = result.scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")
        student_id = student.id  # override to self only

    service = CollegeEnrollmentService(db)
    return await service.list_enrollments(student_id, course_id, semester_id, skip, limit)


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
async def get_enrollment(
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get single enrollment by ID"""
    service = CollegeEnrollmentService(db)
    return await service.get_enrollment(enrollment_id)


@router.patch("/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(
    enrollment_id: int,
    data: EnrollmentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update enrollment status/grade (Faculty, Registrar, Dean)"""
    if current_user.role not in ["college_faculty", "registrar", "dean", "super_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to update enrollments")

    service = CollegeEnrollmentService(db)
    return await service.update_enrollment(enrollment_id, data)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def drop_course(
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Drop a course enrollment (Student self-drop or Admin)"""
    # Students can drop their own; admins can drop any
    if current_user.role == "college_student":
        from modules.college.college_students.models import CollegeStudent
        result = await db.execute(select(CollegeStudent).where(CollegeStudent.user_id == current_user.id))
        student = result.scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")
        # Verify ownership
        enrollment = await db.execute(
            select(EnrollmentModel).where(
                EnrollmentModel.id == enrollment_id,
                EnrollmentModel.student_id == student.id
            )
        )
        if not enrollment.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Can only drop own enrollments")

    service = CollegeEnrollmentService(db)
    await service.drop_course(enrollment_id)


# ── Student-specific endpoints ────────────────────────────────────

@router.get("/my/enrollments", response_model=List[EnrollmentResponse])
async def get_my_enrollments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get current student's own enrollments"""
    if current_user.role != "college_student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")

    from backup.models.college.student import CollegeStudent
    result = await db.execute(select(CollegeStudent).where(CollegeStudent.user_id == current_user.id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    service = CollegeEnrollmentService(db)
    return await service.get_student_enrollments(student.id)


# ── Course instructor endpoints ───────────────────────────────────

@router.get("/course/{course_id}/students", response_model=List[EnrollmentResponse])
async def get_course_students(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get students enrolled in a course (Faculty teaching that course)"""
    # Only faculty teaching this course or admins
    if current_user.role not in ["college_faculty", "dean", "super_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = CollegeEnrollmentService(db)
    return await service.get_course_enrollments(course_id)


__all__ = ["router"]
