from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import os
import shutil

from modules.shared.database import get_db
from modules.auth.dependencies import require_school_portal, require_school_teacher, require_student
from modules.shared.models import User
from .models import Assignment, AssignmentSubmission
from .service import AssignmentService
from .schemas import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
    AssignmentSubmissionCreate,
    AssignmentSubmissionUpdate,
    AssignmentSubmissionResponse,
)
from modules.school.school_teacher.repository import TeacherRepository
from modules.school.school_student.repository import StudentRepository
from modules.shared.config import settings


def get_assignment_service(db: AsyncSession = Depends(get_db)) -> AssignmentService:
    return AssignmentService(db)


router = APIRouter(prefix="/assignments", tags=["School Assignments"], dependencies=[Depends(require_school_portal)])


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment: AssignmentCreate,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Create a new assignment (Teacher only)"""
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_user_id(current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    assignment_data = assignment.model_dump()
    assignment_data["teacher_id"] = teacher.id

    created_assignment = await service.create_assignment(assignment_data)
    return created_assignment


@router.post("/{assignment_id}/upload")
async def upload_assignment_file(
    assignment_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Upload file for assignment (Teacher only)"""
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_user_id(current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    assignment = await service.get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Validate file
    file_ext = os.path.splitext(file.filename)[1].lower().replace(".", "")
    if file_ext not in settings.allowed_extensions_list:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # Save file
    upload_dir = f"{settings.UPLOAD_DIR}/assignments"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{assignment_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update assignment
    updated_assignment = await service.update_assignment(assignment, file_path=file_path)

    return {"message": "File uploaded successfully", "file_path": file_path}


@router.get("/teacher/my-assignments", response_model=List[AssignmentResponse])
async def get_my_assignments(
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Get all assignments created by current teacher"""
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_user_id(current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    assignments = await service.get_teacher_assignments(teacher.id)
    return assignments


@router.get("/{assignment_id}/submissions")
async def get_assignment_submissions(
    assignment_id: int,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Get all submissions for an assignment (Teacher only)"""
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_user_id(current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    assignment = await service.get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    submissions = await service.get_submissions(assignment_id)

    return {
        "assignment": assignment,
        "submissions": submissions,
        "total_submissions": len(submissions),
        "graded": sum(1 for s in submissions if s.score is not None),
        "pending": sum(1 for s in submissions if s.score is None),
    }


@router.put("/submissions/{submission_id}/grade")
async def grade_submission(
    submission_id: int,
    grade_data: AssignmentSubmissionUpdate,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Grade an assignment submission (Teacher only)"""
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_user_id(current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    submission = await service.get_submission(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    assignment = await service.get_assignment(submission.assignment_id)
    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated_submission = await service.update_submission(
        submission, **grade_data.model_dump(exclude_unset=True)
    )

    return updated_submission


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment_update: AssignmentUpdate,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Update assignment (Teacher only)"""
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_user_id(current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    assignment = await service.get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated_assignment = await service.update_assignment(
        assignment, **assignment_update.model_dump(exclude_unset=True)
    )
    return updated_assignment


@router.delete("/{assignment_id}")
async def delete_assignment(
    assignment_id: int,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Delete assignment (Teacher only)"""
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_user_id(current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    assignment = await service.get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await service.delete_assignment(assignment)
    return {"message": "Assignment deleted successfully"}


# STUDENT ENDPOINTS


@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: int,
    current_user: User = Depends(require_student),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Get assignment details (Student)"""
    assignment = await service.get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return assignment


@router.post("/{assignment_id}/submit")
async def submit_assignment(
    assignment_id: int,
    file: Optional[UploadFile] = File(None),
    submission_text: Optional[str] = Form(None),
    current_user: User = Depends(require_student),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Submit an assignment (Student)"""
    student_repo = StudentRepository(db)
    student = await student_repo.get_by_user_id(current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    assignment = await service.get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Check if already submitted
    existing = await service.get_submission_by_student(assignment_id, student.id)
    if existing:
        raise HTTPException(status_code=400, detail="Assignment already submitted")

    file_path = None
    if file:
        # Validate and save file
        file_ext = os.path.splitext(file.filename)[1].lower().replace(".", "")
        if file_ext not in settings.allowed_extensions_list:
            raise HTTPException(status_code=400, detail="File type not allowed")

        upload_dir = f"{settings.UPLOAD_DIR}/assignments/submissions"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = f"{upload_dir}/{student.id}_{assignment_id}_{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Create submission
    submission_data = {
        "assignment_id": assignment_id,
        "student_id": student.id,
        "submission_text": submission_text,
        "file_path": file_path,
        "submitted_at": datetime.utcnow(),
    }

    submission = await service.create_submission(submission_data)

    return {"message": "Assignment submitted successfully", "submission": submission}


@router.get("/{assignment_id}/my-submission")
async def get_my_submission(
    assignment_id: int,
    current_user: User = Depends(require_student),
    db: AsyncSession = Depends(get_db),
    service: AssignmentService = Depends(get_assignment_service),
):
    """Get student's submission for an assignment"""
    student_repo = StudentRepository(db)
    student = await student_repo.get_by_user_id(current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    submission = await service.get_submission_by_student(assignment_id, student.id)

    if not submission:
        return {"submitted": False, "submission": None}

    return {"submitted": True, "submission": submission}
