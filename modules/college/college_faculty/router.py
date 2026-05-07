"""
College Faculty Router

FastAPI endpoints for college faculty operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import time
from modules.college.database import get_college_async_db
from modules.auth.dependencies import get_current_user, require_college_portal
from modules.shared.models import User
from modules.shared.audit_logger import AuditLogger
from modules.shared.logger import logger, log_request_start, log_request_complete
from modules.shared.rate_limit import write_limit, read_limit
from .service import CollegeFacultyService
from .schemas import FacultyResponse, FacultyUpdate, FacultyCreate

router = APIRouter(
    prefix="/faculty",
    tags=["College Faculty"],
    dependencies=[Depends(require_college_portal)],
    responses={
        401: {"description": "Unauthorized - Invalid or missing authentication token"},
        403: {"description": "Forbidden - Insufficient permissions for this operation"},
        404: {"description": "Not Found - Faculty member not found"},
        422: {"description": "Validation Error - Invalid input data"},
        429: {"description": "Too Many Requests - Rate limit exceeded"}
    }
)


@router.post(
    "/",
    response_model=FacultyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new faculty member",
    description="""
    Create a new faculty member in the college system.

    **Required Permissions:** Dean or Super Admin

    **Rate Limit:** 30 requests per minute

    **Audit:** This action is logged for compliance and security monitoring.

    **Business Rules:**
    - Employee ID must be unique and follow the format
    - Department must exist if specified
    - User account must already exist in the system
    """,
    response_description="Successfully created faculty member"
)
@write_limit()
async def create_faculty(
    data: FacultyCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Create a new faculty member (Protected - Dean only)"""
    start_time = time.time()
    correlation_id = getattr(request.state, 'correlation_id', 'unknown')

    log_request_start("POST", "/faculty", correlation_id, user_id=current_user.id)

    try:
        if current_user.role not in ["dean", "super_admin"]:
            logger.warning(
                "unauthorized_faculty_creation_attempt",
                user_id=current_user.id,
                user_role=current_user.role,
                correlation_id=correlation_id
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create faculty"
            )

        service = CollegeFacultyService(db)
        result = await service.create_faculty(data)

        duration = time.time() - start_time
        logger.info(
            "faculty_created_successfully",
            faculty_id=result.get("faculty", {}).id if result.get("faculty") else None,
            user_id=current_user.id,
            duration_seconds=round(duration, 3),
            correlation_id=correlation_id
        )

        # Audit logging
        if result.get("faculty"):
            audit_logger = AuditLogger(db)
            await audit_logger.log_create(
                user_id=current_user.id,
                resource_type="college_faculty",
                resource_id=str(result["faculty"].id),
                new_values=data.model_dump(),
                ip_address=getattr(request.client, "host", None) if request.client else None,
                user_agent=request.headers.get("user-agent")
            )

        log_request_complete("POST", "/faculty", 201, duration, correlation_id)
        return result

    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "faculty_creation_failed",
            error=str(e),
            user_id=current_user.id,
            duration_seconds=round(duration, 3),
            correlation_id=correlation_id
        )
        raise


@router.get("/", response_model=List[FacultyResponse])
async def list_faculty(
    skip: int = 0,
    limit: int = 20,
    department_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """List all faculty members (Protected)"""
    service = CollegeFacultyService(db)
    
    if department_id:
        return await service.list_by_department(department_id, skip, limit)
    return await service.list_faculty(skip, limit)


@router.get("/me", response_model=FacultyResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get current faculty profile (Protected)"""
    service = CollegeFacultyService(db)
    faculty = await service.get_my_profile(current_user.id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty profile not found for current user"
        )
    return faculty


@router.patch("/me", response_model=FacultyResponse)
async def update_my_profile(
    faculty_data: FacultyUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update current faculty profile (Protected)"""
    service = CollegeFacultyService(db)
    faculty = await service.update_profile(current_user.id, faculty_data)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty profile not found"
        )
    return faculty


@router.get("/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(
    faculty_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get faculty by ID (Protected)"""
    service = CollegeFacultyService(db)
    faculty = await service.get_faculty(faculty_id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )
    return faculty


@router.put("/{faculty_id}", response_model=FacultyResponse)
@write_limit()
async def update_faculty(
    faculty_id: int,
    data: FacultyUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Update faculty by ID (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update faculty"
        )

    # Get current faculty data for audit logging
    service = CollegeFacultyService(db)
    current_faculty = await service.get_faculty(faculty_id)
    if not current_faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )

    faculty = await service.update_faculty(faculty_id, data)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )

    # Audit logging
    audit_logger = AuditLogger(db)
    await audit_logger.log_update(
        user_id=current_user.id,
        resource_type="college_faculty",
        resource_id=str(faculty_id),
        old_values=current_faculty.model_dump() if hasattr(current_faculty, 'model_dump') else {},
        new_values=data.model_dump(exclude_unset=True),
        ip_address=getattr(request.client, "host", None) if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    return faculty


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
@write_limit()
async def delete_faculty(
    faculty_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Delete faculty by ID (Protected - Dean only)"""
    if current_user.role not in ["dean", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete faculty"
        )

    # Get faculty data for audit logging before deletion
    service = CollegeFacultyService(db)
    faculty = await service.get_faculty(faculty_id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )

    success = await service.soft_delete_faculty(faculty_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )

    # Audit logging for deletion
    audit_logger = AuditLogger(db)
    await audit_logger.log_delete(
        user_id=current_user.id,
        resource_type="college_faculty",
        resource_id=str(faculty_id),
        deleted_values=faculty.model_dump() if hasattr(faculty, 'model_dump') else {},
        ip_address=getattr(request.client, "host", None) if request.client else None,
        user_agent=request.headers.get("user-agent")
    )


# ── Faculty Dashboard ──────────────────────────────────────────
@router.get("/dashboard")
async def get_faculty_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get faculty dashboard (Protected)"""
    service = CollegeFacultyService(db)
    faculty = await service.get_my_profile(current_user.id)
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty profile not found"
        )
    
    return {
        "faculty_id": faculty.id,
        "employee_id": faculty.employee_id,
        "designation": faculty.designation,
        "department_id": faculty.department_id,
        "message": "College faculty dashboard - extend with courses, students, etc."
    }


# ── Faculty Courses ─────────────────────────────────────────────
@router.get("/my-courses", response_model=List[dict])
async def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get courses taught by current faculty (Protected)"""
    service = CollegeFacultyService(db)
    return await service.get_my_courses(current_user.id)


# ── Faculty Students ────────────────────────────────────────────
@router.get("/my-students", response_model=List[dict])
async def get_my_students(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    """Get students in faculty's courses (Protected)"""
    service = CollegeFacultyService(db)
    return await service.get_my_students(current_user.id)


__all__ = ["router"]