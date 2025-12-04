from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import User, UserRole
from dependencies import get_current_parent
from repositories.parent_repository import ParentRepository
from repositories.student_repository import StudentRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.grade_repository import GradeRepository
from repositories.assignment_repository import AssignmentRepository
from repositories.notice_repository import NoticeRepository

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def parent_dashboard(
    request: Request,
    current_user: User = Depends(get_current_parent),
    db: Session = Depends(get_db)
):
    parent = ParentRepository.get_by_user_id(db, current_user.id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent profile not found")
    
    children = ParentRepository.get_children(db, parent.id)
    
    # For now, if there's only one child, we can show their stats directly on the dashboard
    # If multiple, we might want to show a summary or let them pick.
    # Let's assume we show the first child's quick stats if available.
    
    child_stats = []
    for child in children:
        # Get some basic stats for each child
        attendance_count = len(AttendanceRepository.get_student_attendance(db, child.id))
        assignments_pending = 0 # Placeholder, need repository method for pending assignments
        
        child_stats.append({
            "student": child,
            "attendance_count": attendance_count,
            "assignments_pending": assignments_pending
        })

    return templates.TemplateResponse("parent/dashboard.html", {
        "request": request,
        "user": current_user,
        "parent": parent,
        "children": children,
        "child_stats": child_stats
    })

@router.get("/profile", response_class=HTMLResponse)
async def parent_profile(
    request: Request,
    current_user: User = Depends(get_current_parent),
    db: Session = Depends(get_db)
):
    parent = ParentRepository.get_by_user_id(db, current_user.id)
    return templates.TemplateResponse("parent/profile.html", {
        "request": request,
        "user": current_user,
        "parent": parent
    })

@router.get("/child/{student_id}/attendance", response_class=HTMLResponse)
async def child_attendance(
    student_id: int,
    request: Request,
    current_user: User = Depends(get_current_parent),
    db: Session = Depends(get_db)
):
    parent = ParentRepository.get_by_user_id(db, current_user.id)
    # Verify this student belongs to this parent
    children = ParentRepository.get_children(db, parent.id)
    child = next((c for c in children if c.id == student_id), None)
    
    if not child:
        raise HTTPException(status_code=403, detail="Not authorized to view this student's data")
        
    attendance_records = AttendanceRepository.get_by_student(db, student_id)
    
    return templates.TemplateResponse("parent/attendance.html", {
        "request": request,
        "user": current_user,
        "child": child,
        "attendance_records": attendance_records
    })

@router.get("/child/{student_id}/grades", response_class=HTMLResponse)
async def child_grades(
    student_id: int,
    request: Request,
    current_user: User = Depends(get_current_parent),
    db: Session = Depends(get_db)
):
    parent = ParentRepository.get_by_user_id(db, current_user.id)
    children = ParentRepository.get_children(db, parent.id)
    child = next((c for c in children if c.id == student_id), None)
    
    if not child:
        raise HTTPException(status_code=403, detail="Not authorized to view this student's data")
        
    grades = GradeRepository.get_by_student(db, student_id)
    
    return templates.TemplateResponse("parent/grades.html", {
        "request": request,
        "user": current_user,
        "child": child,
        "grades": grades
    })

@router.get("/child/{student_id}/homework", response_class=HTMLResponse)
async def child_homework(
    student_id: int,
    request: Request,
    current_user: User = Depends(get_current_parent),
    db: Session = Depends(get_db)
):
    parent = ParentRepository.get_by_user_id(db, current_user.id)
    children = ParentRepository.get_children(db, parent.id)
    child = next((c for c in children if c.id == student_id), None)
    
    if not child:
        raise HTTPException(status_code=403, detail="Not authorized to view this student's data")
    
    # We need to get assignments for the courses the student is enrolled in
    # This logic might need to be in AssignmentRepository or Service
    # For now, let's assume we can get all assignments for student's courses
    # This is a bit complex, let's simplify for now or add a method to AssignmentRepository
    
    # Placeholder: Get assignments for student
    # assignments = AssignmentRepository.get_student_assignments(db, student_id)
    assignments = [] # To be implemented
    
    return templates.TemplateResponse("parent/homework.html", {
        "request": request,
        "user": current_user,
        "child": child,
        "assignments": assignments
    })

@router.get("/notices", response_class=HTMLResponse)
async def parent_notices(
    request: Request,
    current_user: User = Depends(get_current_parent),
    db: Session = Depends(get_db)
):
    # Parents see 'all' notices and maybe 'parent' specific notices if we had that role target
    # For now, let's show notices targeting 'all'
    notices = NoticeRepository.get_by_target_role(db, "all")
    
    return templates.TemplateResponse("parent/notices.html", {
        "request": request,
        "user": current_user,
        "notices": notices
    })

@router.get("/chat", response_class=HTMLResponse)
async def parent_chat(
    request: Request,
    current_user: User = Depends(get_current_parent),
    db: Session = Depends(get_db)
):
    # We can pass initial data or let the frontend fetch it via API
    # Let's pass the user info and let the frontend fetch contacts via API
    # to keep it consistent with the dynamic nature of chat
    return templates.TemplateResponse("parent/chat.html", {
        "request": request,
        "user": current_user
    })

