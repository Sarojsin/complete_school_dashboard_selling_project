# Authority CRUD Routes - To be appended to app/web/routes.py
# These routes handle create, read, update, delete operations for authority management

from fastapi import APIRouter, Request, HTTPException, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.templates import templates
from app.dependencies.auth import get_current_user
from app.models.models import User
from app.repositories.student_repository import StudentRepository
from app.repositories.teacher_repository import TeacherRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.notice_repository import NoticeRepository
from app.repositories.fee_repository import FeeRepository
from app.utils.constants import GRADE_LEVELS, DEPARTMENTS

router = APIRouter()

# ==================== STUDENT CRUD ====================
@router.get("/authority/students/add")
async def authority_add_student_form(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/add_student.html", {
        "request": request,
        "current_user": current_user,
        "grades": GRADE_LEVELS
    })

@router.post("/authority/students/add")
async def authority_add_student(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    # Create student logic here
    student = StudentRepository.create_student_with_user(db, {
        "full_name": form_data.get("full_name"),
        "email": form_data.get("email"),
        "grade_level": form_data.get("grade_level"),
        "section": form_data.get("section"),
        "phone": form_data.get("phone"),
        "address": form_data.get("address")
    })
    return RedirectResponse(url="/authority/students?success=added", status_code=303)

@router.get("/authority/students/{id}")
async def authority_student_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/student_detail.html", {
        "request": request,
        "current_user": current_user,
        "student": student
    })

@router.get("/authority/students/{id}/edit")
async def authority_edit_student_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/edit_student.html", {
        "request": request,
        "current_user": current_user,
        "student": student,
        "grades": GRADE_LEVELS
    })

@router.post("/authority/students/{id}/edit")
async def authority_edit_student(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    student = StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    
    student.grade_level = form_data.get("grade_level")
    student.section = form_data.get("section")
    student.phone = form_data.get("phone")
    student.address = form_data.get("address")
    if student.user:
        student.user.full_name = form_data.get("full_name")
        student.user.email = form_data.get("email")
    db.commit()
    return RedirectResponse(url=f"/authority/students/{id}?success=updated", status_code=303)

@router.post("/authority/students/{id}/delete", name="authority_delete_student")
async def authority_delete_student(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    StudentRepository.delete(db, student)
    return RedirectResponse(url="/authority/students?success=deleted", status_code=303)

# ==================== TEACHER CRUD ====================
@router.get("/authority/teachers/add")
async def authority_add_teacher_form(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/add_teacher.html", {
        "request": request,
        "current_user": current_user,
        "departments": DEPARTMENTS
    })

@router.post("/authority/teachers/add")
async def authority_add_teacher(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    teacher = TeacherRepository.create_teacher_with_user(db, {
        "full_name": form_data.get("full_name"),
        "email": form_data.get("email"),
        "department": form_data.get("department"),
        "phone": form_data.get("phone"),
        "qualification": form_data.get("qualification"),
        "specialization": form_data.get("specialization")
    })
    db.add(teacher)
    db.commit()
    return RedirectResponse(url="/authority/teachers?success=added", status_code=303)

@router.get("/authority/teachers/{id}")
async def authority_teacher_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_id(db, id)
    if not teacher: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/teacher_detail.html", {
        "request": request,
        "current_user": current_user,
        "teacher": teacher,
        "courses": teacher.courses if hasattr(teacher, 'courses') else []
    })

@router.get("/authority/teachers/{id}/edit")
async def authority_edit_teacher_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_id(db, id)
    if not teacher: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/edit_teacher.html", {
        "request": request,
        "current_user": current_user,
        "teacher": teacher,
        "departments": DEPARTMENTS
    })

@router.post("/authority/teachers/{id}/edit")
async def authority_edit_teacher(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    teacher = TeacherRepository.get_by_id(db, id)
    if not teacher: raise HTTPException(status_code=404)
    
    teacher.department = form_data.get("department")
    teacher.phone = form_data.get("phone")
    if teacher.user:
        teacher.user.full_name = form_data.get("full_name")
        teacher.user.email = form_data.get("email")
    db.commit()
    return RedirectResponse(url=f"/authority/teachers/{id}?success=updated", status_code=303)

@router.post("/authority/teachers/{id}/delete", name="authority_delete_teacher")
async def authority_delete_teacher(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_id(db, id)
    if not teacher: raise HTTPException(status_code=404)
    TeacherRepository.delete(db, teacher)
    return RedirectResponse(url="/authority/teachers?success=deleted", status_code=303)

# ==================== COURSE CRUD ====================
@router.get("/authority/courses/add")
async def authority_add_course_form(request: Request, current_user: User = Depends(get_current_user), db: Session =  Depends(get_db)):
    teachers = TeacherRepository.get_all(db)
    return templates.TemplateResponse("authority/add_course.html", {
        "request": request,
        "current_user": current_user,
        "teachers": teachers,
        "departments": DEPARTMENTS,
        "grades": GRADE_LEVELS
    })

@router.post("/authority/courses/add")
async def authority_add_course(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    course_data = {
        "course_code": form_data.get("course_code"),
        "course_name": form_data.get("course_name"),
        "grade_level": form_data.get("grade_level"),
        "teacher_id": int(form_data.get("teacher_id")) if form_data.get("teacher_id") else None,
        "description": form_data.get("description")
    }
    CourseRepository.create(db, course_data)
    return RedirectResponse(url="/authority/courses?success=added", status_code=303)

@router.get("/authority/courses/{id}")
async def authority_course_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/course_detail.html", {
        "request": request,
        "current_user": current_user,
        "course": course
    })

@router.get("/authority/courses/{id}/edit")
async def authority_edit_course_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404)
    teachers = TeacherRepository.get_all(db)
    return templates.TemplateResponse("authority/edit_course.html", {
        "request": request,
        "current_user": current_user,
        "course": course,
        "teachers": teachers,
        "grades": GRADE_LEVELS
    })

@router.post("/authority/courses/{id}/edit")
async def authority_edit_course(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    course = CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404)
    
    course.course_code = form_data.get("course_code")
    course.course_name = form_data.get("course_name")
    course.grade_level = form_data.get("grade_level")
    course.teacher_id = int(form_data.get("teacher_id")) if form_data.get("teacher_id") else None
    course.description = form_data.get("description")
    db.commit()
    return RedirectResponse(url=f"/authority/courses/{id}?success=updated", status_code=303)

# ==================== NOTICE CRUD ====================
@router.get("/authority/notices/create")
async def authority_create_notice_form(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("authority/create_notice.html", {
        "request": request,
        "current_user": current_user,
        "grades": GRADE_LEVELS
    })

@router.post("/authority/notices/create")
async def authority_create_notice(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    notice_data = {
        "title": form_data.get("title"),
        "content": form_data.get("content"),
        "target_role": form_data.get("target_role"),
        "priority": form_data.get("priority", "normal")
    }
    NoticeRepository.create(db, notice_data)
    return RedirectResponse(url="/authority/notices?success=created", status_code=303)

@router.get("/authority/notices/{id}")
async def authority_view_notice(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notice = NoticeRepository.get_by_id(db, id)
    if not notice: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/view_notice.html", {
        "request": request,
        "current_user": current_user,
        "notice": notice
    })

@router.get("/authority/notices/{id}/edit")
async def authority_edit_notice_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notice = NoticeRepository.get_by_id(db, id)
    if not notice: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/edit_notice.html", {
        "request": request,
        "current_user": current_user,
        "notice": notice,
        "grades": GRADE_LEVELS
    })

@router.post("/authority/notices/{id}/edit")
async def authority_edit_notice(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    notice = NoticeRepository.get_by_id(db, id)
    if not notice: raise HTTPException(status_code=404)
    
    notice.title = form_data.get("title")
    notice.content = form_data.get("content")
    notice.target_role = form_data.get("target_role")
    notice.priority = form_data.get("priority", "normal")
    db.commit()
    return RedirectResponse(url="/authority/notices?success=updated", status_code=303)
