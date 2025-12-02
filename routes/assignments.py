from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import shutil
from database.database import get_db
from dependencies import get_current_user, get_current_teacher, get_current_student
from models.models import User, UserRole
from repositories.assignment_repository import AssignmentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.student_repository import StudentRepository
from tables.tables import (
    AssignmentCreate, AssignmentUpdate, AssignmentResponse,
    AssignmentSubmissionCreate, AssignmentSubmissionUpdate, AssignmentSubmissionResponse
)
from config.config import settings

router = APIRouter()

# TEACHER ENDPOINTS

@router.post("/", response_model=AssignmentResponse)
async def create_assignment(
    assignment: AssignmentCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Create a new assignment (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    assignment_data = assignment.dict()
    assignment_data['teacher_id'] = teacher.id
    
    created_assignment = AssignmentRepository.create(db, assignment_data)
    return created_assignment

@router.post("/{assignment_id}/upload")
async def upload_assignment_file(
    assignment_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Upload file for assignment (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    assignment = AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate file
    file_ext = os.path.splitext(file.filename)[1].lower().replace('.', '')
    if file_ext not in settings.allowed_extensions_list:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Save file
    upload_dir = f"{settings.UPLOAD_DIR}/assignments"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{assignment_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update assignment
    updated_assignment = AssignmentRepository.update(db, assignment, file_path=file_path)
    
    return {"message": "File uploaded successfully", "file_path": file_path}

@router.get("/teacher/my-assignments", response_model=List[AssignmentResponse])
async def get_my_assignments(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all assignments created by current teacher"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    assignments = AssignmentRepository.get_all(db, teacher_id=teacher.id)
    return assignments

@router.get("/{assignment_id}/submissions")
async def get_assignment_submissions(
    assignment_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all submissions for an assignment (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    assignment = AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    submissions = AssignmentRepository.get_submissions(db, assignment_id)
    
    return {
        "assignment": assignment,
        "submissions": submissions,
        "total_submissions": len(submissions),
        "graded": sum(1 for s in submissions if s.score is not None),
        "pending": sum(1 for s in submissions if s.score is None)
    }

@router.put("/submissions/{submission_id}/grade")
async def grade_submission(
    submission_id: int,
    grade_data: AssignmentSubmissionUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Grade an assignment submission (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    submission = db.query(AssignmentRepository.get_by_id.__self__).get(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    assignment = AssignmentRepository.get_by_id(db, submission.assignment_id)
    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_submission = AssignmentRepository.update_submission(
        db, submission, **grade_data.dict(exclude_unset=True)
    )
    
    return updated_submission

@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: int,
    assignment_update: AssignmentUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update assignment (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    assignment = AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_assignment = AssignmentRepository.update(
        db, assignment, **assignment_update.dict(exclude_unset=True)
    )
    return updated_assignment

@router.delete("/{assignment_id}")
async def delete_assignment(
    assignment_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Delete assignment (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    assignment = AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    AssignmentRepository.delete(db, assignment)
    return {"message": "Assignment deleted successfully"}

# STUDENT ENDPOINTS

@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get assignment details (Student)"""
    assignment = AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return assignment

@router.post("/{assignment_id}/submit")
async def submit_assignment(
    assignment_id: int,
    file: Optional[UploadFile] = File(None),
    submission_text: Optional[str] = Form(None),
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Submit an assignment (Student)"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    assignment = AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check if already submitted
    existing = AssignmentRepository.get_submission_by_student(db, assignment_id, student.id)
    if existing:
        raise HTTPException(status_code=400, detail="Assignment already submitted")
    
    file_path = None
    if file:
        # Validate and save file
        file_ext = os.path.splitext(file.filename)[1].lower().replace('.', '')
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
        "submitted_at": datetime.utcnow()
    }
    
    submission = AssignmentRepository.create_submission(db, submission_data)
    
    return {"message": "Assignment submitted successfully", "submission": submission}

@router.get("/{assignment_id}/my-submission")
async def get_my_submission(
    assignment_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get student's submission for an assignment"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    submission = AssignmentRepository.get_submission_by_student(db, assignment_id, student.id)
    
    if not submission:
        return {"submitted": False, "submission": None}
    
    return {"submitted": True, "submission": submission}