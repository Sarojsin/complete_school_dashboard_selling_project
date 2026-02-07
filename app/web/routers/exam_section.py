from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.templates import templates
from app.dependencies import get_async_db, get_current_user_web
from app.models.models import User, UserRole, Student, Course
from app.repositories.exam_repository import ExamRepository
from app.services.exam_service import ExamService

router = APIRouter()

@router.get("/dashboard")
async def exam_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    results = await service.get_all_results()
    
    return templates.TemplateResponse("exam_section/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "results": results[:10]  # Show last 10 results
    })

@router.get("/post-result")
async def post_result_page(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get students and courses for dropdowns
    students = await db.execute("SELECT id, name FROM students")
    courses = await db.execute("SELECT id, name FROM courses")
    
    return templates.TemplateResponse("exam_section/post_result.html", {
        "request": request,
        "current_user": current_user,
        "students": students.fetchall(),
        "courses": courses.fetchall()
    })

@router.post("/post-result")
async def post_result_action(
    request: Request,
    student_id: int = Form(...),
    course_id: int = Form(...),
    marks: float = Form(...),
    semester: str = Form(...),
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    
    from schemas.exam_schemas import ExamResultCreate
    result_data = ExamResultCreate(
        student_id=student_id,
        course_id=course_id,
        marks=marks,
        semester=semester
    )
    
    await service.publish_result(result_data, current_user.id)
    
    return templates.TemplateResponse("exam_section/post_result.html", {
        "request": request,
        "current_user": current_user,
        "success": True,
        "message": "Result published successfully!"
    })