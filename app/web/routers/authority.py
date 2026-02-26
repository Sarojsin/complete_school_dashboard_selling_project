from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form, Query
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
from app.dependencies.auth import get_current_user
from app.models.models import User, Student, Teacher, Assignment, AssignmentSubmission, Course, FeeRecord, Notice, Attendance, Grade, Note, Video
from app.models.department_models import Department
from app.models.group_models import Group, GroupMember
from app.models.chat_models import ChatMessage
from app.repositories.student_repository import StudentRepository
from app.repositories.teacher_repository import TeacherRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.notice_repository import NoticeRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.notes_repository import NotesRepository
from app.repositories.videos_repository import VideosRepository
from app.repositories.test_repository import TestRepository
from app.repositories.fee_repository import FeeRepository
from app.repositories.fee_structure_repository import FeeStructureRepository
from app.repositories.chat_repository import ChatRepository
from app.repositories.group_repository import GroupRepository
from app.services.authority_service import AuthorityService
from app.services.test_service import TestService
from app.utils.constants import GRADE_LEVELS, DEPARTMENTS, SECTIONS, WEEKDAYS

router = APIRouter()

# ------------------ AUTHORITY PAGES ------------------
@router.get("/authority/dashboard")
async def authority_dashboard(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    data = await AuthorityService.get_dashboard_stats(db)
    unread_count = await MessageRepository.get_unread_count(db, current_user.id)
    
    return templates.TemplateResponse("authority/dashboard.html", {
        "request": request, 
        "current_user": current_user, 
        "stats": data,
        "unread_count": unread_count
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
    
    # Calculate stats
    all_teachers_res = await db.execute(select(Teacher).options(joinedload(Teacher.user), joinedload(Teacher.courses).selectinload(Course.enrollments)))
    all_teachers = all_teachers_res.scalars().unique().all()
    
    total_count = len(all_teachers)
    active_count = len([t for t in all_teachers if t.status == 'active'])
    on_leave_count = len([t for t in all_teachers if t.status == 'on_leave'])
    
    formatted = []
    for t in teachers:
        formatted.append({
            "id": t.id,
            "name": t.user.full_name if t.user else (t.full_name or "N/A"),
            "full_name": t.user.full_name if t.user else (t.full_name or "N/A"),
            "employee_id": t.employee_id,
            "department": t.department or "N/A",
            "email": t.user.email if t.user else "N/A",
            "phone": t.phone or "N/A",
            "dob": "N/A", # Model doesn't have DOB
            "employment_type": "full_time",
            "join_date": t.joining_date.strftime("%Y-%m-%d") if t.joining_date else "N/A",
            "experience": 5, # Placeholder or could be calculated
            "classes_taught": len(t.courses) if t.courses else 0,
            "courses_taught": len(t.courses) if t.courses else 0,
            "students_count": sum(len(c.enrollments) for c in t.courses) if t.courses else 0,
            "performance": 90,
            "rating": 4.5,
            "status": t.status or "active",
            "is_class_teacher": False,
            "avatar": f"https://ui-avatars.com/api/?name={t.user.full_name.replace(' ', '+') if t.user else 'User'}&background=random"
        })
    
    # Get dynamic department stats
    dept_stats = {}
    for t in all_teachers:
        dept = t.department or "Unassigned"
        if dept not in dept_stats:
            dept_stats[dept] = {"name": dept, "teacher_count": 0, "active_count": 0, "class_count": 0, "hod": "N/A"}
        dept_stats[dept]["teacher_count"] += 1
        if t.status == 'active':
            dept_stats[dept]["active_count"] += 1
        dept_stats[dept]["class_count"] += len(t.courses) if t.courses else 0
        
    return templates.TemplateResponse("authority/teachers.html", {
        "request": request,
        "current_user": current_user,
        "teachers": formatted,
        "filters": {"department": department, "status": status},
        "departments": list(dept_stats.values()),
        "search_query": search,
        "stats": {
            "total": total_count,
            "active": active_count,
            "on_leave": on_leave_count,
            "departments": len(dept_stats)
        }
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
    
    # Get all students for the assignment modal
    all_students = await StudentRepository.get_all(db)
    
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
    return templates.TemplateResponse("authority/courses.html", {
        "request": request, 
        "current_user": current_user, 
        "courses": formatted_courses, 
        "departments": departments, 
        "students": all_students,
        "search_query": search
    })

@router.get("/authority/fees")
async def authority_fees(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    report = await AuthorityService.get_fee_report(db)
    # Fetch recent fee records for the list
    fee_records = await FeeRepository.get_all(db, limit=10)
    
    return templates.TemplateResponse("authority/fees.html", {
        "request": request, 
        "current_user": current_user, 
        "fee_records": fee_records,
        "report": report
    })

@router.get("/authority/notices")
async def authority_notices(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    notices = await NoticeRepository.get_all(db)
    formatted_notices = []
    for n in notices:
        formatted_notices.append({
            "id": n.id, 
            "title": n.title, 
            "content": n.content if hasattr(n, 'content') else "", 
            "excerpt": (n.content[:100] + "...") if hasattr(n, 'content') and n.content and len(n.content) > 100 else (n.content if hasattr(n, 'content') else ""),
            "date": n.created_at.strftime("%Y-%m-%d") if hasattr(n, 'created_at') and n.created_at else "N/A", 
            "published_date": n.created_at.strftime("%Y-%m-%d") if hasattr(n, 'created_at') and n.created_at else "N/A",
            "published_time": n.created_at.strftime("%H:%M") if hasattr(n, 'created_at') and n.created_at else "N/A",
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(n, 'created_at') and n.created_at else "N/A", 
            "author": "Admin", 
            "audience": n.target_role if hasattr(n, 'target_role') else "all",
            "target_role": n.target_role if hasattr(n, 'target_role') else "all", 
            "priority": n.priority if hasattr(n, 'priority') else "normal",
            "status": "active",
            "is_important": getattr(n, 'priority', 'normal') == 'high',
            "expiry_date": None,
            "is_expired": False,
            "days_remaining": "Active",
            "views": 0
        })
    
    stats = {
        "total_notices": len(formatted_notices),
        "active_notices": sum(1 for n in formatted_notices if n["status"] == "active"),
        "expired_notices": 0,
        "this_month": len(formatted_notices)
    }
    
    return templates.TemplateResponse("authority/notices.html", {
        "request": request, 
        "current_user": current_user, 
        "notices": formatted_notices, 
        "stats": stats,
        "current_page": 1,
        "total_pages": 1,
        "has_prev": False,
        "has_next": False
    })

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
    # Check if user already exists
    res = await db.execute(select(User).filter(User.email == form_data.get("email")))
    user = res.scalars().first()
    if not user:
        user = User(full_name=form_data.get("name"), email=form_data.get("email"), role="teacher")
        user.set_password(form_data.get("password") or "password123")
        db.add(user); await db.flush()
    
    joining_date = datetime.strptime(form_data.get("joining_date"), "%Y-%m-%d") if form_data.get("joining_date") else datetime.utcnow()
    
    teacher = Teacher(
        user_id=user.id, 
        employee_id=form_data.get("employee_id"), 
        department=form_data.get("department"), 
        phone=form_data.get("phone"),
        full_name=form_data.get("name"),
        qualification=form_data.get("qualifications"),
        specialization=form_data.get("specialization"),
        joining_date=joining_date,
        status="active"
    )
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
    teacher.full_name = form_data.get("name")
    teacher.qualification = form_data.get("qualifications")
    teacher.specialization = form_data.get("specialization")
    teacher.status = form_data.get("status", "active")
    
    if form_data.get("joining_date"):
        teacher.joining_date = datetime.strptime(form_data.get("joining_date"), "%Y-%m-%d")
        
    if teacher.user:
        teacher.user.full_name = form_data.get("name")
        teacher.user.email = form_data.get("email")
        
    await db.commit()
    return RedirectResponse(url=f"/authority/teachers/{id}?success=updated", status_code=303)

@router.post("/authority/teachers/{id}/delete", name="authority_delete_teacher")
async def authority_delete_teacher(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    print(f"DEBUG: Attempting to delete teacher with ID: {id}")
    teacher = await TeacherRepository.get_by_id(db, id)
    if not teacher:
        print(f"DEBUG: Teacher with ID {id} not found in database!")
        raise HTTPException(status_code=404, detail=f"Teacher with ID {id} not found")
    
    print(f"DEBUG: Found teacher: {teacher.user.full_name if teacher.user else 'No User'}")
    
    # Capture user object before deleting teacher if relationship might be cleared
    user = teacher.user
    
    await TeacherRepository.delete(db, teacher)
    
    # Also delete the user record to prevent orphans
    if user:
        await db.delete(user)
        await db.commit()
    
    print(f"DEBUG: Teacher and associated User deleted successfully")
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
    
    # Get available students (not enrolled)
    all_students = await StudentRepository.get_all(db)
    enrolled_ids = {s.id for s in students}
    available_students = [s for s in all_students if s.id not in enrolled_ids]
    
    return templates.TemplateResponse("authority/course_detail.html", {
        "request": request, 
        "current_user": current_user, 
        "course": course, 
        "students": students,
        "available_students": available_students
    })

@router.post("/authority/courses/{id}/enroll")
async def authority_enroll_student(id: int, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    student_id = int(form_data.get("student_id"))
    redirect_url = form_data.get("redirect_url") or f"/authority/courses/{id}"
    await CourseRepository.enroll_student(db, id, student_id)
    return RedirectResponse(url=f"{redirect_url}?success=enrolled", status_code=303)

@router.post("/authority/courses/{id}/unenroll")
async def authority_unenroll_student(id: int, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    student_id = int(form_data.get("student_id"))
    await CourseRepository.remove_student(db, id, student_id)
    return RedirectResponse(url=f"/authority/courses/{id}?success=unenrolled", status_code=303)

@router.get("/authority/courses/{id}/edit")
async def authority_edit_course_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    course = await CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404)
    teachers = await TeacherRepository.get_all(db)
    
    # Prepare stats for the template
    enrollment_count = len(course.enrollments) if course.enrollments else 0
    stats = {
        "enrolled_students": enrollment_count,
        "completion_rate": 88, # Placeholder
        "avg_grade": 78, # Placeholder
        "assignments": len(course.assignments) if hasattr(course, "assignments") and course.assignments else 0,
        "avg_attendance": 85 # Placeholder
    }
    
    return templates.TemplateResponse("authority/edit_course.html", {"request": request, "current_user": current_user, "course": course, "teachers": teachers, "departments": DEPARTMENTS, "grades": GRADE_LEVELS, "stats": stats})

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
    
    # Calculate stats
    stats = {
        "total_structures": len(structures),
        "active_structures": sum(1 for s in structures if hasattr(s, 'status') and s.status == 'active'),
        "total_revenue": 0,
        "pending_fees": 0
    }
    
    # Create fee breakdown by grade (avoid duplicates)
    fee_breakdown = []
    seen_grades = set()
    for s in structures:
        if s.grade_level not in seen_grades:
            seen_grades.add(s.grade_level)
            other_fees = (getattr(s, 'registration_fee', 0) or 0) + \
                        (getattr(s, 'library_fee', 0) or 0) + \
                        (getattr(s, 'sports_fee', 0) or 0) + \
                        (getattr(s, 'lab_fee', 0) or 0) + \
                        (getattr(s, 'activity_fee', 0) or 0) + \
                        (getattr(s, 'other_charges', 0) or 0)
            
            fee_breakdown.append({
                "grade_level": s.grade_level,
                "tuition_fee": s.tuition_fee or 0,
                "other_fees": other_fees,
                "total_amount": (s.tuition_fee or 0) + other_fees,
                "student_count": 0  # Could be calculated from enrollments
            })
    
    from datetime import datetime
    current_year = datetime.now().year
    
    return templates.TemplateResponse("authority/fee_structure.html", {
        "request": request, 
        "current_user": current_user, 
        "fee_structures": structures, 
        "grades": GRADE_LEVELS,
        "stats": stats,
        "fee_breakdown": fee_breakdown,
        "current_year": current_year
    })

# Authority Group Management
@router.get("/authority/groups")
async def authority_groups(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    res = await db.execute(select(Group).order_by(Group.created_at.desc()))
    groups = res.scalars().all()
    
    # Enrich groups with member counts
    enriched_groups = []
    for group in groups:
        res_count = await db.execute(select(func.count(GroupMember.id)).filter(GroupMember.group_id == group.id))
        count = res_count.scalar() or 0
        enriched_groups.append({
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "code": group.code,
            "member_count": count,
            "created_at": group.created_at
        })
        
    return templates.TemplateResponse("authority/groups.html", {
        "request": request, 
        "current_user": current_user, 
        "groups": enriched_groups
    })

@router.get("/authority/groups/create")
async def authority_create_group_form(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/create_group.html", {"request": request, "current_user": current_user})

@router.post("/authority/groups/create")
async def authority_create_group(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    import uuid
    import string
    import random
    
    # Generate unique 6-character code
    group_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    new_group = Group(
        name=form_data.get("name"), 
        description=form_data.get("description"), 
        code=group_code,
        created_by=current_user.id
    )
    db.add(new_group)
    await db.flush() # Get id
    
    # Add creator as member
    member = GroupMember(
        group_id=new_group.id,
        user_id=current_user.id,
        role="creator"
    )
    db.add(member)
    await db.commit()
    
    return RedirectResponse(url="/authority/groups?success=created", status_code=303)

@router.get("/authority/groups/{group_id}/manage")
async def authority_manage_group(request: Request, group_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    group_repo = GroupRepository(db)
    group = await group_repo.get_group_with_members(group_id)
    if not group: raise HTTPException(status_code=404)
    
    return templates.TemplateResponse("authority/manage_group.html", {
        "request": request,
        "current_user": current_user,
        "group": group
    })

@router.post("/authority/groups/{group_id}/delete")
async def authority_delete_group(group_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    res = await db.execute(select(Group).filter(Group.id == group_id))
    group = res.scalars().first()
    if not group: raise HTTPException(status_code=404)
    
    await db.delete(group)
    await db.commit()
    return RedirectResponse(url="/authority/groups?success=deleted", status_code=303)

@router.post("/authority/groups/{group_id}/add-member")
async def authority_add_group_member(
    group_id: int, 
    user_id: int = Form(...), 
    role: str = Form("student"),
    db: AsyncSession = Depends(get_async_db)
):
    from app.models.group_models import GroupMember
    # Check if already member
    res = await db.execute(select(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id))
    if res.scalars().first():
        return RedirectResponse(url=f"/authority/groups/{group_id}/manage?error=already_member", status_code=303)
        
    member = GroupMember(group_id=group_id, user_id=user_id, role=role)
    db.add(member); await db.commit()
    return RedirectResponse(url=f"/authority/groups/{group_id}/manage?success=added", status_code=303)

@router.post("/authority/groups/{group_id}/remove-member")
async def authority_remove_group_member(
    group_id: int, 
    user_id: int = Form(...),
    db: AsyncSession = Depends(get_async_db)
):
    from app.models.group_models import GroupMember
    res = await db.execute(select(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id))
    member = res.scalars().first()
    if member:
        if member.role == "creator":
            return RedirectResponse(url=f"/authority/groups/{group_id}/manage?error=cannot_remove_creator", status_code=303)
        await db.delete(member); await db.commit()
    return RedirectResponse(url=f"/authority/groups/{group_id}/manage?success=removed", status_code=303)

@router.get("/authority/groups/{group_id}/posts")
async def authority_group_posts(
    request: Request,
    group_id: int,
    post_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    from app.repositories.group_post_repository import GroupPostRepository
    from app.services.group_post_service import GroupPostService
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    post_service = GroupPostService(post_repo, group_repo)
    
    limit = 20
    offset = (page - 1) * limit
    
    posts_data = await post_service.get_group_posts(group_id, current_user.id, post_type, limit, offset)
    
    return templates.TemplateResponse("groups/group_posts.html", {
        "request": request,
        "current_user": current_user,
        "group": {"id": group_id, "name": posts_data["group_name"]},
        "posts": posts_data["posts"],
        "post_type": post_type,
        "page": page,
        "has_more": posts_data["has_more"],
        "is_teacher": True, # For template permissions
        "post_types": ["notice", "note", "link"]
    })

@router.get("/authority/groups/{group_id}/posts/create")
async def authority_create_post_form(
    request: Request,
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(Group).filter(Group.id == group_id))
    group = result.scalars().first()
    if not group: raise HTTPException(status_code=404, detail="Group not found")
    
    return templates.TemplateResponse("groups/new_post.html", {
        "request": request,
        "current_user": current_user,
        "group": group,
        "role_prefix": "authority",
        "post_types": ["notice", "note", "link"]
    })

@router.post("/authority/groups/{group_id}/posts/create")
async def authority_create_post(
    group_id: int,
    title: str = Form(...),
    content: Optional[str] = Form(None),
    post_type: str = Form("notice"),
    link_url: Optional[str] = Form(None),
    link_description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    from app.models.group_models import GroupPost
    post = GroupPost(
        group_id=group_id, 
        author_id=current_user.id, 
        title=title, 
        content=content, 
        post_type=post_type,
        link_url=link_url,
        link_description=link_description
    )
    db.add(post); await db.commit()
    return RedirectResponse(url=f"/authority/groups/{group_id}/posts", status_code=303)

@router.get("/authority/groups/{group_id}/posts/{post_id}")
async def authority_view_post(
    request: Request,
    group_id: int,
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    from app.repositories.group_post_repository import GroupPostRepository
    post_repo = GroupPostRepository(db)
    
    post = await post_repo.get_post_by_id(post_id)
    if not post or post.group_id != group_id: raise HTTPException(status_code=404, detail="Post not found")
    
    return templates.TemplateResponse("groups/view_post.html", {
        "request": request,
        "current_user": current_user,
        "post": post,
        "group_id": group_id,
        "is_teacher": True,
        "is_author": post.author_id == current_user.id
    })

@router.post("/authority/groups/{group_id}/posts/{post_id}/delete")
async def authority_delete_post(
    group_id: int,
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    from app.repositories.group_post_repository import GroupPostRepository
    from app.services.group_post_service import GroupPostService
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    post_service = GroupPostService(post_repo, group_repo)
    
    await post_service.delete_post(post_id, current_user.id)
    return RedirectResponse(url=f"/authority/groups/{group_id}/posts?success=deleted", status_code=303)

@router.get("/authority/reports")
async def authority_reports(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    return templates.TemplateResponse("authority/reports.html", {"request": request, "current_user": current_user, "reports": []})
# Authority Department Management
@router.get("/authority/departments")
async def authority_departments(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Department).options(joinedload(Department.hod).joinedload(Teacher.user)))
    departments = result.scalars().all()
    
    # Get teachers for the HOD dropdown
    teachers_res = await db.execute(select(Teacher).options(joinedload(Teacher.user)))
    teachers = teachers_res.scalars().all()
    
    return templates.TemplateResponse("authority/departments.html", {
        "request": request,
        "current_user": current_user,
        "departments": departments,
        "teachers": teachers
    })

@router.post("/authority/departments/add")
async def authority_add_department(
    request: Request,
    name: str = Form(...),
    code: str = Form(...),
    hod_teacher_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    new_dept = Department(name=name, code=code, hod_teacher_id=hod_teacher_id)
    db.add(new_dept)
    await db.commit()
    return RedirectResponse(url="/authority/departments?success=added", status_code=303)

@router.post("/authority/departments/{id}/edit")
async def authority_edit_department(
    id: int,
    request: Request,
    name: str = Form(...),
    code: str = Form(...),
    hod_teacher_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(Department).where(Department.id == id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    dept.name = name
    dept.code = code
    dept.hod_teacher_id = hod_teacher_id
    
    await db.commit()
    return RedirectResponse(url="/authority/departments?success=updated", status_code=303)

@router.post("/authority/departments/{id}/delete")
async def authority_delete_department(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(Department).where(Department.id == id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    await db.delete(dept)
    await db.commit()
    return RedirectResponse(url="/authority/departments?success=deleted", status_code=303)
