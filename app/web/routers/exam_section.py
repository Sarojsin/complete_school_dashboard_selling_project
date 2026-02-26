from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.templates import templates
from app.dependencies import get_async_db, get_current_user_web
from app.models.models import User, UserRole, Student, Course
from app.models.exam_models import ExamResult, ExamNotice
from app.repositories.exam_repository import ExamRepository
from app.services.exam_service import ExamService
from app.schemas.exam_schemas import ExamResultCreate, ExamNoticeCreate

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
    
    # Get dashboard stats
    stats = await service.get_dashboard_stats()
    results = await service.get_summarized_results(limit=5)
    notices = await service.get_notices()
    
    return templates.TemplateResponse("exam_section/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "stats": stats,
        "results": results[:10],  # Show last 10 results
        "notices": notices[:5]  # Show last 5 notices
    })

@router.get("/post-result")
async def post_result_page(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get students and courses for dropdowns using ORM
    students_result = await db.execute(
        select(Student).order_by(Student.full_name)
    )
    students = students_result.scalars().all()
    
    courses_result = await db.execute(
        select(Course).order_by(Course.course_name)
    )
    courses = courses_result.scalars().all()

    # Get unique grades and sections for filtering
    grades_res = await db.execute(select(Student.grade_level).distinct())
    grades = sorted([r for r in grades_res.scalars().all() if r])
    
    sections_res = await db.execute(select(Student.section).distinct())
    sections = sorted([r for r in sections_res.scalars().all() if r])
    
    return templates.TemplateResponse("exam_section/post_result.html", {
        "request": request,
        "current_user": current_user,
        "students": students,
        "courses": courses,
        "filters": {
            "grades": grades,
            "sections": sections
        }
    })

@router.post("/post-result")
async def post_result_action(
    request: Request,
    student_id: int = Form(...),
    semester: str = Form(...),
    exam_type: str = Form("final"),
    course_ids: list[int] = Form(...),
    marks_list: list[float] = Form(...),
    max_marks_list: list[float] = Form(...),
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    
    # Prepare results data
    results_data = []
    for i in range(len(course_ids)):
        results_data.append({
            "student_id": student_id,
            "course_id": course_ids[i],
            "marks": marks_list[i],
            "max_marks": max_marks_list[i],
            "exam_type": exam_type,
            "semester": semester
        })
    
    await service.publish_results_bulk(results_data, current_user.id)
    
    # Refresh page data
    students_res = await db.execute(select(Student).order_by(Student.full_name))
    students = students_res.scalars().all()
    courses_res = await db.execute(select(Course).order_by(Course.course_name))
    courses = courses_res.scalars().all()

    # Get unique grades and sections for filtering
    grades_res = await db.execute(select(Student.grade_level).distinct())
    grades = sorted([r for r in grades_res.scalars().all() if r])
    sections_res = await db.execute(select(Student.section).distinct())
    sections = sorted([r for r in sections_res.scalars().all() if r])
    
    return templates.TemplateResponse("exam_section/post_result.html", {
        "request": request,
        "current_user": current_user,
        "students": students,
        "courses": courses,
        "filters": {
            "grades": grades,
            "sections": sections
        },
        "success": True,
        "message": f"Successfully published marks for {len(results_data)} subjects!"
    })

@router.get("/results")
async def all_results(
    request: Request,
    grade_level: str = None,
    section: str = None,
    exam_type: str = None,
    semester: str = None,
    search: str = None,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    
    # Get results with student and course details + filtering
    results_with_details = await service.get_results_with_details(
        grade_level=grade_level,
        section=section,
        exam_type=exam_type,
        semester=semester,
        search_query=search
    )
    
    # Get unique filter values for the UI
    grades_res = await db.execute(select(Student.grade_level).distinct())
    grades = [r for r in grades_res.scalars().all() if r]
    
    sections_res = await db.execute(select(Student.section).distinct())
    sections = [r for r in sections_res.scalars().all() if r]
    
    semesters_res = await db.execute(select(ExamResult.semester).distinct())
    semesters = [r for r in semesters_res.scalars().all() if r]
    
    return templates.TemplateResponse("exam_section/results.html", {
        "request": request,
        "current_user": current_user,
        "results": results_with_details,
        "filters": {
            "grades": grades,
            "sections": sections,
            "semesters": semesters,
            "exam_types": ["final", "midterm", "quiz", "assignment"]
        },
        "query": {
            "grade_level": grade_level,
            "section": section,
            "exam_type": exam_type,
            "semester": semester,
            "search": search
        }
    })

@router.get("/grade-sheet/{student_id}")
async def grade_sheet(
    student_id: int,
    request: Request,
    semester: str = None,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get student info
    student_result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = student_result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get grade sheet
    repo = ExamRepository(db)
    service = ExamService(repo)
    
    if semester:
        results = await service.get_grade_sheet(student_id, semester)
    else:
        from app.models.exam_models import ExamResult
        results_result = await db.execute(
            select(ExamResult)
            .where(ExamResult.student_id == student_id)
            .order_by(ExamResult.semester.desc())
        )
        results = results_result.scalars().all()
    
    return templates.TemplateResponse("exam_section/grade_sheet.html", {
        "request": request,
        "current_user": current_user,
        "student": student,
        "results": results,
        "semester": semester
    })

@router.get("/notices")
async def exam_notices(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    
    notices = await service.get_notices()
    
    return templates.TemplateResponse("exam_section/notices.html", {
        "request": request,
        "current_user": current_user,
        "notices": notices
    })

@router.get("/notices/create")
async def create_notice_page(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return templates.TemplateResponse("exam_section/create_notice.html", {
        "request": request,
        "current_user": current_user
    })

@router.post("/notices/create")
async def create_notice_action(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    notice_type: str = Form("schedule"),
    exam_date: str = Form(None),
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    repo = ExamRepository(db)
    service = ExamService(repo)
    
    from datetime import datetime
    notice_data = ExamNoticeCreate(
        title=title,
        content=content,
        notice_type=notice_type,
        exam_date=datetime.strptime(exam_date, "%Y-%m-%d").date() if exam_date else None
    )
    
    await service.create_notice(notice_data, current_user.id)
    
    return RedirectResponse(url="/exam-section/notices", status_code=302)
@router.get("/profile")
async def exam_profile(
    request: Request,
    current_user: User = Depends(get_current_user_web),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role != UserRole.EXAM_SECTION:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return templates.TemplateResponse("exam_section/profile.html", {
        "request": request,
        "current_user": current_user
    })
