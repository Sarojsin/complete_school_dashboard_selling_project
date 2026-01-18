from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload
from typing import Optional, List
import os
import shutil
import uuid
from datetime import datetime

from app.core.database import get_async_db
from app.core.templates import templates
from dependencies import get_current_user
from models.models import User, Student, Teacher, Assignment, AssignmentSubmission, Course, FeeRecord, Notice, Attendance, Grade, Note, Video
from models.group_models import Group
from models.chat_models import ChatMessage
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.message_repository import MessageRepository
from repositories.notice_repository import NoticeRepository
from repositories.course_repository import CourseRepository
from repositories.assignment_repository import AssignmentRepository
from repositories.notes_repository import NotesRepository
from repositories.videos_repository import VideosRepository
from repositories.test_repository import TestRepository
from repositories.fee_repository import FeeRepository
from repositories.fee_structure_repository import FeeStructureRepository
from repositories.chat_repository import ChatRepository
from services.test_service import TestService
from utils.constants import GRADE_LEVELS, DEPARTMENTS, SECTIONS, WEEKDAYS

router = APIRouter()

# ------------------ AUTHORITY PAGES ------------------
@router.get("/authority/dashboard")
async def authority_dashboard(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    from models.models import Student, Teacher, Course, Notice
    
    st_count_res = await db.execute(select(func.count(Student.id)))
    te_count_res = await db.execute(select(func.count(Teacher.id)))
    co_count_res = await db.execute(select(func.count(Course.id)))
    no_count_res = await db.execute(select(func.count(Notice.id)))
    
    stats = {
        "total_students": st_count_res.scalar() or 0,
        "total_teachers": te_count_res.scalar() or 0,
        "total_courses": co_count_res.scalar() or 0,
        "active_notices": no_count_res.scalar() or 0
    }
    return templates.TemplateResponse("authority/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "stats": stats
    })

@router.get("/authority/students")
async def authority_students(request: Request, grade: str = None, section: str = None, status: str = None, search: str = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    students = await StudentRepository.get_all(db, grade_level=grade, section=section, status=status, search=search)
    formatted = []
    for s in students:
        formatted.append({
            "id": s.id,
            "name": s.user.full_name if s.user else "N/A",
            "full_name": s.user.full_name if s.user else "N/A",
            "student_id": s.student_id,
            "grade_level": s.grade_level,
            "grade": s.grade_level,
            "section": s.section or "N/A",
            "phone": s.phone or "N/A",
            "email": s.user.email if s.user else "N/A",
            "address": s.address or "N/A",
            "dob": s.date_of_birth.strftime("%Y-%m-%d") if hasattr(s, 'date_of_birth') and s.date_of_birth else "N/A",
            "gpa": "3.5",  # Placeholder
            "roll_number": s.student_id,
            "fee_status": "paid",  # Placeholder
            "fee_due_date": None,
            "attendance": 92,  # Placeholder
            "status": "active",  # Placeholder
            "avatar": f"https://ui-avatars.com/api/?name={s.user.full_name.replace(' ', '+') if s.user else 'User'}&background=random"
        })
    return templates.TemplateResponse("authority/students.html", {
        "request": request,
        "current_user": current_user,
        "students": formatted,
        "filters": {"grade": grade, "section": section, "status": status},
        "search_query": search
    })

@router.get("/authority/teachers")
async def authority_teachers(request: Request, department: str = None, status: str = None, search: str = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teachers = await TeacherRepository.get_all(db, department=department, status=status, search=search)
    formatted = []
    for t in teachers:
        formatted.append({
            "id": t.id,
            "name": t.user.full_name if t.user else "N/A",
            "full_name": t.user.full_name if t.user else "N/A",
            "employee_id": t.employee_id,
            "department": t.department or "N/A",
            "email": t.user.email if t.user else "N/A",
            "phone": t.phone or "N/A",
            "dob": "1985-01-01",
            "employment_type": "full_time",
            "join_date": "2020-01-01",
            "experience": 5,
            "classes_taught": 3,
            "courses_taught": 2,
            "students_count": 45,
            "performance": 90,
            "rating": 4.5,
            "status": "active",
            "is_class_teacher": False,
            "avatar": f"https://ui-avatars.com/api/?name={t.user.full_name.replace(' ', '+') if t.user else 'User'}&background=random"
        })
    dept_data = [
        {"name": "Mathematics", "teacher_count": 12, "active_count": 10, "class_count": 8, "hod": "Dr. Smith"},
        {"name": "Science", "teacher_count": 10, "active_count": 9, "class_count": 7, "hod": "Dr. Johnson"},
        {"name": "English", "teacher_count": 8, "active_count": 7, "class_count": 6, "hod": "Mr. Brown"},
        {"name": "History", "teacher_count": 6, "active_count": 5, "class_count": 5, "hod": "Ms. Davis"}
    ]
    return templates.TemplateResponse("authority/teachers.html", {
        "request": request,
        "current_user": current_user,
        "teachers": formatted,
        "filters": {"department": department, "status": status},
        "departments": dept_data,
        "search_query": search
    })

@router.get("/authority/courses")
async def authority_courses(request: Request, search: str = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    query = select(Course).options(
        selectinload(Course.enrollments),
        joinedload(Course.teacher).joinedload(Teacher.user)
    )
    if search:
        query = query.filter(Course.course_name.ilike(f"%{search}%") | Course.course_code.ilike(f"%{search}%"))
    res = await db.execute(query)
    courses_data = res.scalars().unique().all()
    
    dept_colors = {"Mathematics": "primary", "Science": "success", "English": "info", "History": "warning", "Arts": "danger", "Physical Education": "secondary", "General": "secondary"}
    formatted_courses = []
    for course in courses_data:
        department = getattr(course, "department", "General")
        dept_color = dept_colors.get(department, "secondary")
        student_count = len(course.enrollments) if hasattr(course, "enrollments") and course.enrollments else 0
        formatted_courses.append({
            "id": course.id, "name": course.course_name, "code": course.course_code, "department": department, "department_color": dept_color, "credits": getattr(course, "credits", 3), "grade_level": getattr(course, "grade_level", "N/A"), "semester": getattr(course, "semester", 1), "instructor": course.teacher.full_name if course.teacher else "Unassigned", "instructor_avatar": f"https://ui-avatars.com/api/?name={course.teacher.full_name}&background=random" if course.teacher else "https://ui-avatars.com/api/?name=Unassigned&background=gray", "status": "active", "student_count": student_count, "class_count": 1, "avg_grade": 85
        })
    departments = [
        {"name": "Mathematics", "color": "primary", "course_count": 12, "student_count": 450, "teacher_count": 8, "avg_grade": 78, "utilization": 85},
        {"name": "Science", "color": "success", "course_count": 10, "student_count": 380, "teacher_count": 6, "avg_grade": 82, "utilization": 90},
        {"name": "English", "color": "info", "course_count": 8, "student_count": 410, "teacher_count": 5, "avg_grade": 80, "utilization": 75}
    ]
    return templates.TemplateResponse("authority/courses.html", {"request": request, "current_user": current_user, "courses": formatted_courses, "departments": departments, "search_query": search})

@router.get("/authority/fees")
async def authority_fees(request: Request, search: str = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    if search:
        fees = await FeeRepository.search(db, search)
    else:
        res = await db.execute(
            select(FeeRecord).options(
                joinedload(FeeRecord.student).joinedload(Student.user)
            )
        )
        fees = res.scalars().unique().all()
        
    summary = await FeeRepository.get_all_fees_summary(db)
    formatted_fees = []
    for f in fees:
        formatted_fees.append({
            "id": f.id, "student_name": f.student.user.full_name if f.student and f.student.user else "N/A", "student_id": f.student.student_id if f.student else "N/A", "grade": f.student.grade_level if f.student else "N/A", "total_amount": f.total_amount if hasattr(f, 'total_amount') else 0, "paid_amount": f.paid_amount if hasattr(f, 'paid_amount') else 0, "balance": (f.total_amount - f.paid_amount) if hasattr(f, 'total_amount') and hasattr(f, 'paid_amount') else 0, "status": "paid" if hasattr(f, 'paid_amount') and f.paid_amount >= (f.total_amount if hasattr(f, 'total_amount') else 0) else "pending", "due_date": f.due_date.strftime("%Y-%m-%d") if hasattr(f, 'due_date') and f.due_date else "N/A", "payment_method": f.payment_method if hasattr(f, 'payment_method') else "N/A"
        })
    return templates.TemplateResponse("authority/fees.html", {"request": request, "current_user": current_user, "fee_records": formatted_fees, "total_collected": summary['total_paid'], "pending_amount": summary['total_pending'], "search_query": search})

@router.get("/authority/notices")
async def authority_notices(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    notices = await NoticeRepository.get_all(db)
    formatted_notices = []
    for n in notices:
        formatted_notices.append({
            "id": n.id, "title": n.title, "content": n.content if hasattr(n, 'content') else "", "date": n.created_at.strftime("%Y-%m-%d") if hasattr(n, 'created_at') and n.created_at else "N/A", "created_at": n.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(n, 'created_at') and n.created_at else "N/A", "author": "Admin", "target_role": n.target_role if hasattr(n, 'target_role') else "all", "priority": n.priority if hasattr(n, 'priority') else "normal", "status": "active"
        })
    return templates.TemplateResponse("authority/notices.html", {"request": request, "current_user": current_user, "notices": formatted_notices, "stats": {"total_notices": len(formatted_notices)}})

@router.get("/authority/analytics")
async def authority_analytics(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    return templates.TemplateResponse("authority/analytics_v2.html", {"request": request, "current_user": current_user, "authority": current_user, "grade_dist_data": [10, 20, 30, 40, 5], "att_labels": ["Grade 9", "Grade 10", "Grade 11", "Grade 12"], "att_data": [95, 92, 88, 90], "dept_labels": ["Math", "Science", "English"], "dept_data": [85, 82, 88], "trend_labels": ["Jan", "Feb", "Mar", "Apr"], "trend_data": [70, 75, 80, 85], "teacher_performance": [], "top_classes": [], "demographics_data": [60, 40]})

# Authority Student Management
@router.get("/authority/students/add")
async def authority_add_student_form(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    return templates.TemplateResponse("authority/add_student.html", {"request": request, "current_user": current_user, "grades": GRADE_LEVELS, "sections": SECTIONS})

@router.post("/authority/students/add")
async def authority_add_student(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    # Using more robust creation if available, else manual
    if hasattr(StudentRepository, 'create_student_with_user'):
        await StudentRepository.create_student_with_user(db, {
            "full_name": form_data.get("full_name"),
            "email": form_data.get("email"),
            "grade_level": form_data.get("grade_level"),
            "section": form_data.get("section"),
            "phone": form_data.get("phone"),
            "address": form_data.get("address")
        })
    else:
        # Check if user already exists
        res = await db.execute(select(User).filter(User.email == form_data.get("email")))
        user = res.scalars().first()
        if not user:
            user = User(full_name=form_data.get("full_name"), email=form_data.get("email"), role="student")
            db.add(user); await db.flush()
        
        student = Student(user_id=user.id, student_id=form_data.get("student_id"), grade_level=form_data.get("grade_level"), section=form_data.get("section"), phone=form_data.get("phone"), address=form_data.get("address"))
        db.add(student)
    await db.commit()
    return RedirectResponse(url="/authority/students?success=added", status_code=303)

@router.get("/authority/students/{id}")
async def authority_student_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/student_detail.html", {"request": request, "current_user": current_user, "student": student, "courses": student.enrollments if hasattr(student, 'enrollments') else []})

@router.get("/authority/students/{id}/edit")
async def authority_edit_student_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/edit_student.html", {"request": request, "current_user": current_user, "student": student, "grades": GRADE_LEVELS, "sections": SECTIONS})

@router.post("/authority/students/{id}/edit")
async def authority_edit_student(id: int, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    student = await StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    student.grade_level = form_data.get("grade_level")
    student.section = form_data.get("section")
    student.phone = form_data.get("phone")
    student.address = form_data.get("address")
    if student.user:
        student.user.full_name = form_data.get("full_name")
        student.user.email = form_data.get("email")
    await db.commit()
    return RedirectResponse(url=f"/authority/students/{id}?success=updated", status_code=303)

@router.post("/authority/students/{id}/delete", name="authority_delete_student")
async def authority_delete_student(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    await StudentRepository.delete(db, student)
    return RedirectResponse(url="/authority/students?success=deleted", status_code=303)

# Authority Teacher Management
@router.get("/authority/teachers/add")
async def authority_add_teacher_form(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teachers = await TeacherRepository.get_all(db)
    return templates.TemplateResponse("authority/add_teacher.html", {"request": request, "current_user": current_user, "departments": DEPARTMENTS})

@router.post("/authority/teachers/add")
async def authority_add_teacher(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    if hasattr(TeacherRepository, 'create_teacher_with_user'):
        await TeacherRepository.create_teacher_with_user(db, {"full_name": form_data.get("full_name"), "email": form_data.get("email"), "department": form_data.get("department"), "phone": form_data.get("phone"), "qualification": form_data.get("qualification"), "specialization": form_data.get("specialization")})
    else:
        # Check if user already exists
        res = await db.execute(select(User).filter(User.email == form_data.get("email")))
        user = res.scalars().first()
        if not user:
            user = User(full_name=form_data.get("full_name"), email=form_data.get("email"), role="teacher")
            db.add(user); await db.flush()
        
        teacher = Teacher(user_id=user.id, employee_id=form_data.get("employee_id"), department=form_data.get("department"), phone=form_data.get("phone"))
        db.add(teacher)
    await db.commit()
    return RedirectResponse(url="/authority/teachers?success=added", status_code=303)

@router.get("/authority/teachers/{id}")
async def authority_teacher_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_id(db, id)
    if not teacher: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/teacher_detail.html", {"request": request, "current_user": current_user, "teacher": teacher, "courses": teacher.courses if hasattr(teacher, 'courses') else []})

@router.get("/authority/teachers/{id}/edit")
async def authority_edit_teacher_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_id(db, id)
    if not teacher: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/edit_teacher.html", {"request": request, "current_user": current_user, "teacher": teacher, "departments": DEPARTMENTS})

@router.post("/authority/teachers/{id}/edit")
async def authority_edit_teacher(id: int, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    teacher = await TeacherRepository.get_by_id(db, id)
    if not teacher: raise HTTPException(status_code=404)
    teacher.department = form_data.get("department")
    teacher.phone = form_data.get("phone")
    if teacher.user:
        teacher.user.full_name = form_data.get("full_name")
        teacher.user.email = form_data.get("email")
    await db.commit()
    return RedirectResponse(url=f"/authority/teachers/{id}?success=updated", status_code=303)

@router.post("/authority/teachers/{id}/delete", name="authority_delete_teacher")
async def authority_delete_teacher(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_id(db, id)
    if not teacher: raise HTTPException(status_code=404)
    await TeacherRepository.delete(db, teacher)
    return RedirectResponse(url="/authority/teachers?success=deleted", status_code=303)

# Authority Course Management
@router.get("/authority/courses/add")
async def authority_add_course_form(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teachers = await TeacherRepository.get_all(db)
    return templates.TemplateResponse("authority/add_course.html", {"request": request, "current_user": current_user, "teachers": teachers, "departments": DEPARTMENTS, "grades": GRADE_LEVELS})

@router.post("/authority/courses/add")
async def authority_add_course(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    course_data = {"course_code": form_data.get("course_code"), "course_name": form_data.get("course_name"), "grade_level": form_data.get("grade_level"), "teacher_id": int(form_data.get("teacher_id")) if form_data.get("teacher_id") else None, "description": form_data.get("description")}
    await CourseRepository.create(db, course_data)
    return RedirectResponse(url="/authority/courses?success=added", status_code=303)

@router.get("/authority/courses/{id}")
async def authority_course_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    course = await CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404)
    students = await CourseRepository.get_enrolled_students(db, id)
    return templates.TemplateResponse("authority/course_detail.html", {"request": request, "current_user": current_user, "course": course, "students": students})

@router.get("/authority/courses/{id}/edit")
async def authority_edit_course_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    course = await CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404)
    teachers = await TeacherRepository.get_all(db)
    return templates.TemplateResponse("authority/edit_course.html", {"request": request, "current_user": current_user, "course": course, "teachers": teachers, "departments": DEPARTMENTS, "grades": GRADE_LEVELS})

@router.post("/authority/courses/{id}/edit")
async def authority_edit_course(id: int, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    course = await CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404)
    course.course_code = form_data.get("course_code")
    course.course_name = form_data.get("course_name")
    course.grade_level = form_data.get("grade_level")
    course.teacher_id = int(form_data.get("teacher_id")) if form_data.get("teacher_id") else None
    course.description = form_data.get("description")
    await db.commit()
    return RedirectResponse(url=f"/authority/courses/{id}?success=updated", status_code=303)

@router.post("/authority/courses/{id}/delete", name="authority_delete_course")
async def authority_delete_course(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    course = await CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404)
    await db.delete(course); await db.commit()
    return RedirectResponse(url="/authority/courses?success=deleted", status_code=303)

# Authority Notice Management
@router.get("/authority/notices/create")
async def authority_create_notice_form(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    return templates.TemplateResponse("authority/create_notice.html", {"request": request, "current_user": current_user, "grades": GRADE_LEVELS})

@router.post("/authority/notices/create")
async def authority_create_notice(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    notice_data = {"title": form_data.get("title"), "content": form_data.get("content"), "target_role": form_data.get("target_role"), "priority": form_data.get("priority", "normal")}
    await NoticeRepository.create(db, notice_data)
    return RedirectResponse(url="/authority/notices?success=created", status_code=303)

@router.get("/authority/notices/{id}")
async def authority_view_notice(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    notice = await NoticeRepository.get_by_id(db, id)
    if not notice: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/view_notice.html", {"request": request, "current_user": current_user, "notice": notice})

@router.get("/authority/notices/{id}/edit")
async def authority_edit_notice_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    notice = await NoticeRepository.get_by_id(db, id)
    if not notice: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/edit_notice.html", {"request": request, "current_user": current_user, "notice": notice, "grades": GRADE_LEVELS})

@router.post("/authority/notices/{id}/edit")
async def authority_edit_notice(id: int, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    notice = await NoticeRepository.get_by_id(db, id)
    if not notice: raise HTTPException(status_code=404)
    notice.title = form_data.get("title")
    notice.content = form_data.get("content")
    notice.target_role = form_data.get("target_role")
    notice.priority = form_data.get("priority", "normal")
    await db.commit()
    return RedirectResponse(url="/authority/notices?success=updated", status_code=303)

# Authority Fee Management
@router.get("/authority/fees/add")
async def authority_add_fee_form(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    students = await StudentRepository.get_all(db)
    return templates.TemplateResponse("authority/add_fee.html", {"request": request, "current_user": current_user, "students": students})

@router.post("/authority/fees/add")
async def authority_add_fee(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    fee_data = {"student_id": int(form_data.get("student_id")), "amount": float(form_data.get("amount")), "payment_method": form_data.get("payment_method"), "transaction_id": form_data.get("transaction_id")}
    await FeeRepository.create_payment(db, fee_data)
    return RedirectResponse(url="/authority/fees?success=added", status_code=303)

@router.get("/authority/fees/structure")
async def authority_fee_structure(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    structures = await FeeStructureRepository.get_all(db)
    return templates.TemplateResponse("authority/fee_structure.html", {"request": request, "current_user": current_user, "fee_structures": structures, "grades": GRADE_LEVELS})

# Authority Group Management
@router.get("/authority/groups")
async def authority_groups(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    res = await db.execute(select(Group))
    groups = res.scalars().all()
    for group in groups: 
        res_m = await db.execute(select(func.count()).select_from(group.members))
        group.member_count = res_m.scalar() or 0
    return templates.TemplateResponse("authority/groups.html", {"request": request, "current_user": current_user, "groups": groups})

@router.get("/authority/groups/create")
async def authority_create_group_form(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/create_group.html", {"request": request})

@router.post("/authority/groups/create")
async def authority_create_group(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    new_group = Group(name=form_data.get("name"), description=form_data.get("description"), created_by=current_user.id)
    db.add(new_group); await db.commit()
    return RedirectResponse(url="/authority/groups", status_code=303)

@router.get("/authority/reports")
async def authority_reports(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    return templates.TemplateResponse("authority/reports.html", {"request": request, "current_user": current_user, "reports": []})
