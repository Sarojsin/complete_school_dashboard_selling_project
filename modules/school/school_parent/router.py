# School Parent API Routes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal
from modules.shared.models import User, UserRole
from .service import ParentService
from .schemas import ParentResponse, ParentCreate, ParentUpdate

router = APIRouter(prefix="/parents", tags=["School Parents"], dependencies=[Depends(require_school_portal)])


@router.post("/", response_model=ParentResponse, status_code=status.HTTP_201_CREATED)
async def create_parent(
    data: ParentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new parent (Protected - Authority/Admin only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create parents")
    service = ParentService(db)
    return await service.create(data)




@router.get("/", response_model=List[ParentResponse])
async def list_parents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all parents (Protected)"""
    service = ParentService(db)
    return await service.get_all(skip, limit)


@router.get("/me", response_model=ParentResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current parent profile (Protected)"""
    service = ParentService(db)
    parent = await service.get_by_user_id(current_user.id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent profile not found")
    return parent


# ── Parent Dashboard ─────────────────────────────────────────────
@router.get("/dashboard")
async def get_parent_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get parent dashboard (Protected)"""
    service = ParentService(db)
    parent = await service.get_by_user_id(current_user.id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent profile not found")
    
    # Get children
    children = await service.get_children(parent.id)
    
    return {
        "parent_id": parent.id,
        "full_name": parent.full_name,
        "children_count": len(children),
        "children": [{"id": c.id, "name": c.full_name} for c in children],
        "message": "Parent dashboard"
    }


# ── Child Attendance ───────────────────────────────────────────────
@router.get("/child/{student_id}/attendance")
async def get_child_attendance(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance for a specific child (Protected)"""
    from modules.school.school_attendance.repository import AttendanceRepository
    
    # Verify parent has access to this child
    service = ParentService(db)
    parent = await service.get_by_user_id(current_user.id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent profile not found")
    
    # Verify this child belongs to this parent
    children = await service.get_children(parent.id)
    child_ids = [c.id for c in children]
    if student_id not in child_ids:
        raise HTTPException(status_code=403, detail="Not authorized to view this student's records")
    
    # Get attendance
    repo = AttendanceRepository(db)
    records = await repo.get_by_student_id(db, student_id)
    return records


# ── Child Grades ─────────────────────────────────────────────────
@router.get("/child/{student_id}/grades")
async def get_child_grades(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get grades for a specific child (Protected)"""
    from modules.school.school_grades.repository import GradeRepository
    
    # Verify parent has access to this child
    service = ParentService(db)
    parent = await service.get_by_user_id(current_user.id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent profile not found")
    
    # Verify this child belongs to this parent
    children = await service.get_children(parent.id)
    child_ids = [c.id for c in children]
    if student_id not in child_ids:
        raise HTTPException(status_code=403, detail="Not authorized to view this student's records")
    
    # Get grades
    repo = GradeRepository(db)
    grades = await repo.get_by_student_id(db, student_id)
    return grades


# ── Child Homework (Assignments) ──────────────────────────────────
@router.get("/child/{student_id}/homework")
async def get_child_homework(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get homework (assignments) for a specific child (Protected)"""
    from modules.school.school_assignments.repository import AssignmentRepository
    
    # Verify parent has access to this child
    service = ParentService(db)
    parent = await service.get_by_user_id(current_user.id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent profile not found")
    
    # Verify this child belongs to this parent
    children = await service.get_children(parent.id)
    child_ids = [c.id for c in children]
    if student_id not in child_ids:
        raise HTTPException(status_code=403, detail="Not authorized to view this student's records")
    
    # Get assignments
    repo = AssignmentRepository(db)
    assignments = await repo.get_by_student_id(db, student_id)
    return assignments


# ── Notices ───────────────────────────────────────────────────────
@router.get("/notices")
async def get_notices(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get notices for parent (Protected)"""
    from modules.school.school_notices.repository import NoticeRepository
    
    repo = NoticeRepository() # NoticeRepository has static methods
    notices = await NoticeRepository.get_recent_notices(db, days=30)
    return notices


# ── Chat ─────────────────────────────────────────────────────────
@router.get("/chat")
async def get_chat_contacts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get chat contacts for parent (Protected)"""
    # This would typically return teachers and other contacts
    return {
        "message": "Chat functionality - integrate with school_chat module"
    }



@router.get("/{parent_id}", response_model=ParentResponse)
async def get_parent(
    parent_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get parent by ID (Protected)"""
    service = ParentService(db)
    parent = await service.get(parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@router.put("/{parent_id}", response_model=ParentResponse)
async def update_parent(
    parent_id: int,
    data: ParentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update parent by ID (Protected - Authority/Admin only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update parents")
    service = ParentService(db)
    parent = await service.update(parent_id, data)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@router.delete("/{parent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parent(
    parent_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete parent by ID (Protected - Authority/Admin only)"""
    if current_user.role not in [UserRole.AUTHORITY, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete parents")
    service = ParentService(db)
    success = await service.delete(parent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Parent not found")

__all__ = ["router"]