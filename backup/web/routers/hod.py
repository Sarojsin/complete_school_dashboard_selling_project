from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backup.core.templates import templates
from backup.dependencies import get_async_db, get_current_user_web
from backup.models.models import User, UserRole
from backup.repositories.department_repository import DepartmentRepository
from backup.services.department_service import DepartmentService

router = APIRouter()

@router.get("/dashboard")
async def hod_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.HOD:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    stats = await service.get_hod_dashboard(current_user.id)
    
    return templates.TemplateResponse("hod/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "stats": stats
    })

@router.get("/teachers")
async def hod_teachers(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.HOD:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    
    # Get department for this HOD
    department = await service.get_hod_department(current_user.id)
    
    if not department:
        raise HTTPException(status_code=404, detail="No department assigned")
    
    teachers = await service.get_department_teachers(department.id)
    
    return templates.TemplateResponse("hod/teachers.html", {
        "request": request,
        "current_user": current_user,
        "department": department,
        "teachers": teachers
    })

@router.get("/students")
async def hod_students(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.HOD:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    
    # Get department for this HOD
    department = await service.get_hod_department(current_user.id)
    
    if not department:
        raise HTTPException(status_code=404, detail="No department assigned")
    
    students = await service.get_department_students(department.id)
    
    return templates.TemplateResponse("hod/students.html", {
        "request": request,
        "current_user": current_user,
        "department": department,
        "students": students
    })

@router.get("/students/{student_id}/performance")
async def student_performance(
    student_id: int,
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.HOD:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get student info
    from sqlalchemy import select
    from backup.models.models import Student, ExamResult
    
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get student's exam results
    exam_result = await db.execute(
        select(ExamResult)
        .where(ExamResult.student_id == student_id)
        .order_by(ExamResult.semester.desc())
    )
    results = exam_result.scalars().all()
    
    return templates.TemplateResponse("hod/student_performance.html", {
        "request": request,
        "current_user": current_user,
        "student": student,
        "results": results
    })

@router.get("/reports")
async def hod_reports(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.HOD:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    
    # Get department for this HOD
    department = await service.get_hod_department(current_user.id)
    
    if not department:
        raise HTTPException(status_code=404, detail="No department assigned")
    
    # Get department statistics
    teachers = await service.get_department_teachers(department.id)
    students = await service.get_department_students(department.id)
    courses = await service.get_department_courses(department.id)
    
    return templates.TemplateResponse("hod/reports.html", {
        "request": request,
        "current_user": current_user,
        "department": department,
        "teachers": teachers,
        "students": students,
        "courses": courses
    })
@router.get("/profile")
async def hod_profile(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.HOD:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    
    # Get department for this HOD
    department = await service.get_hod_department(current_user.id)
    
    return templates.TemplateResponse("hod/profile.html", {
        "request": request,
        "current_user": current_user,
        "department": department
    })
