from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy import select, func, delete, update, desc, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import os
import shutil
import uuid
from datetime import datetime

from backup.core.database import get_async_db
from backup.core.templates import templates
from backup.dependencies.auth import get_current_user
from backup.models.models import User, Student, Teacher, Assignment, AssignmentSubmission, Course, CourseEnrollment, FeeRecord, Notice, Attendance, Grade, Note, Video
from backup.models.chat_models import ChatMessage
from backup.models.group_models import Group, GroupMember, GroupPost
from backup.repositories.student_repository import StudentRepository
from backup.repositories.teacher_repository import TeacherRepository
from backup.repositories.message_repository import MessageRepository
from backup.repositories.notice_repository import NoticeRepository
from backup.repositories.course_repository import CourseRepository
from backup.repositories.assignment_repository import AssignmentRepository
from backup.repositories.notes_repository import NotesRepository
from backup.repositories.videos_repository import VideosRepository
from backup.repositories.test_repository import TestRepository
from backup.repositories.grade_repository import GradeRepository
from backup.repositories.attendance_repository import AttendanceRepository
from backup.repositories.fee_repository import FeeRepository
from backup.repositories.fee_structure_repository import FeeStructureRepository
from backup.repositories.chat_repository import ChatRepository
from backup.repositories.group_repository import GroupRepository
from backup.repositories.group_post_repository import GroupPostRepository
from backup.services.teacher_service import TeacherService
from backup.services.group_service import GroupService
from backup.services.test_service import TestService
from backup.utils.constants import GRADE_LEVELS, DEPARTMENTS, SECTIONS, WEEKDAYS

router = APIRouter()

# ------------------ TEACHER PAGES ------------------
@router.get("/teacher/dashboard")
async def teacher_dashboard(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    data = await TeacherService.get_dashboard_data(db, current_user.id)
    if not data:
        return RedirectResponse("/login")
        
    unread_count = await MessageRepository.get_unread_count(db, current_user.id)
    
    return templates.TemplateResponse("teacher/dashboard.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": data["teacher"], 
        "courses": data["courses"], 
        "assignments": data["recent_assignments"], 
        "stats": data["stats"], 
        "unread_count": unread_count, 
        "recent_messages": []
    })

@router.get("/teacher/profile")
async def teacher_profile(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        return RedirectResponse("/teacher/dashboard")
        
    teacher_data = {
        "name": current_user.full_name, 
        "email": current_user.email, 
        "id": teacher.employee_id, 
        "department": teacher.department, 
        "phone": teacher.phone, 
        "qualification": teacher.qualification, 
        "specialization": teacher.specialization, 
        "joining_date": teacher.joining_date.strftime('%Y-%m-%d') if teacher.joining_date else "N/A", 
        "profile_pic": current_user.profile_picture or "/static/images/default-avatar.png"
    }
    return templates.TemplateResponse("teacher/profile.html", {"request": request, "current_user": current_user, "teacher_data": teacher_data})

@router.post("/teacher/profile")
async def teacher_update_profile(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        return RedirectResponse("/teacher/dashboard")
        
    avatar_file = form_data.get("profile_pic") if "profile_pic" in form_data and form_data["profile_pic"].filename else None
    
    await TeacherService.update_profile(
        db=db,
        teacher_id=teacher.id,
        full_name=form_data.get("full_name"),
        email=form_data.get("email"),
        phone=form_data.get("phone"),
        qualification=form_data.get("qualification"),
        specialization=form_data.get("specialization"),
        avatar_file=avatar_file,
        user=current_user
    )
    return RedirectResponse(url="/teacher/profile", status_code=303)

@router.get("/teacher/students")
async def teacher_students(request: Request, grade: str = None, section: str = None, search: str = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    students = await StudentRepository.get_all(db, grade_level=grade, section=section, search=search)
    formatted = []
    for s in students:
        formatted.append({
            "id": s.id,
            "name": s.user.full_name if s.user else "Unknown student",
            "email": s.user.email if s.user else "N/A",
            "grade": s.grade_level,
            "section": s.section,
            "attendance": 92, # Placeholder
            "average_grade": 85, # Placeholder
            "pending_assignments": 0, # Placeholder
            "avatar": f"https://ui-avatars.com/api/?name={s.user.full_name.replace(' ', '+') if s.user else 'User'}&background=random"
        })
    return templates.TemplateResponse("teacher/students.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "students": formatted,
        "search_query": search,
        "filters": {"grade": grade, "section": section}
    })

@router.get("/teacher/students/{student_id}")
async def teacher_student_detail(request: Request, student_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_id(db, student_id)
    if not student: raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse("teacher/student_detail.html", {"request": request, "current_user": current_user, "teacher": current_user, "student": student, "student_id": student_id})

@router.get("/teacher/students/{student_id}/grades")
async def teacher_student_grades(request: Request, student_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_id(db, student_id)
    if not student: raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse("teacher/student_grades.html", {"request": request, "current_user": current_user, "teacher": current_user, "student": student, "grades": []})

@router.post("/teacher/students/{student_id}/contact")
async def teacher_contact_student(student_id: int, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    student = await StudentRepository.get_by_id(db, student_id)
    if not student: raise HTTPException(status_code=404, detail="Student found")
    await MessageRepository.create(db=db, sender_id=current_user.id, recipient_id=student.user_id, subject=form_data.get("subject"), body=form_data.get("message"))
    return {"message": "Message sent successfully"}

@router.get("/teacher/messages")
async def teacher_messages(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    messages = await MessageRepository.get_inbox(db, current_user.id)
    unread = await MessageRepository.get_unread_count(db, current_user.id)
    return templates.TemplateResponse("teacher/messages.html", {"request": request, "current_user": current_user, "teacher": current_user, "messages": messages, "unread_count": unread})

@router.post("/teacher/messages/{message_id}/read")
async def teacher_mark_message_read(message_id: int, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    if await MessageRepository.mark_as_read(db, message_id): return {"success": True}
    raise HTTPException(status_code=404, detail="Message not found")

@router.get("/teacher/assignments")
async def teacher_assignments(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        return RedirectResponse("/teacher/dashboard")
        
    data = await TeacherService.get_assignments_data(db, teacher.id)
    
    return templates.TemplateResponse("teacher/assignments.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "assignments": data["assignments"], 
        "stats": data["stats"], 
        "subjects": DEPARTMENTS, 
        "classes": GRADE_LEVELS, 
        "upcoming_deadlines": [a for a in data["assignments"] if not a["is_overdue"]][:3]
    })

@router.get("/teacher/assignments/{id}/edit")
async def teacher_edit_assignment(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    assignment = await AssignmentRepository.get_by_id(db, id)
    if not assignment: raise HTTPException(status_code=404)
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/edit_assignment.html", {"request": request, "current_user": current_user, "teacher": current_user, "assignment": assignment, "courses": courses})

@router.post("/teacher/assignments/{id}/edit")
async def teacher_edit_assignment_post(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    assignment = await AssignmentRepository.get_by_id(db, id)
    if not assignment: raise HTTPException(status_code=404)
    assignment.title = form_data.get("title")
    assignment.description = form_data.get("description")
    assignment.due_date = datetime.fromisoformat(form_data.get("due_date"))
    assignment.max_score = float(form_data.get("max_score", 100))
    await db.commit()
    return RedirectResponse(url="/teacher/assignments?success=updated", status_code=303)

@router.get("/teacher/assignments/create")
async def teacher_create_assignment(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/create_assignment.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "sections": SECTIONS})

@router.post("/teacher/assignments/create")
async def teacher_create_assignment_post(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    
    subject = form_data.get("subject")
    grade = form_data.get("grade")
    section = form_data.get("section")
    
    # Find linking course
    result = await db.execute(select(Course).filter(
        Course.teacher_id == teacher.id,
        Course.course_name == subject,
        Course.grade_level == grade
    ))
    course = result.scalars().first()
    
    if not course:
        # Try to find any course with this subject to attach to (fallback)
        result = await db.execute(select(Course).filter(
            Course.teacher_id == teacher.id,
            Course.course_name == subject
        ))
        course = result.scalars().first()
    
    if not course:
        # Auto-create course if it doesn't exist
        # Generate a unique course code
        course_code = f"{subject[:3].upper()}-{grade.replace(' ', '')}-{uuid.uuid4().hex[:6].upper()}"
        
        course_data = {
            "course_name": subject,
            "course_code": course_code,
            "grade_level": grade,
            "teacher_id": teacher.id,
            "description": f"{subject} course for {grade}",
            "credits": 3 # Default credits
        }
        
        course = await CourseRepository.create(db, course_data)

    assignment_data = {
        "title": form_data.get("title"), 
        "description": form_data.get("description"), 
        "course_id": course.id, 
        "teacher_id": teacher.id, 
        "due_date": datetime.fromisoformat(form_data.get("due_date")), 
        "max_score": float(form_data.get("total_marks", 100)),
        "target_classes": section
    }
    await AssignmentRepository.create(db, assignment_data)
    return RedirectResponse(url="/teacher/assignments?success=1", status_code=303)

@router.get("/teacher/assignments/{id}/submissions")
async def teacher_view_submissions(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    assignment = await AssignmentRepository.get_by_id(db, id)
    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")
    res = await db.execute(select(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == id))
    submissions = res.scalars().all()
    return templates.TemplateResponse("teacher/view_submissions.html", {"request": request, "current_user": current_user, "teacher": current_user, "assignment": assignment, "submissions": submissions})

@router.post("/teacher/assignments/submissions/{submission_id}/grade")
async def teacher_grade_submission(submission_id: int, request: Request, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    form_data = await request.form()
    res = await db.execute(select(AssignmentSubmission).filter(AssignmentSubmission.id == submission_id))
    submission = res.scalars().first()
    if not submission: raise HTTPException(status_code=404, detail="Submission not found")
    submission.score, submission.feedback, submission.graded_at = float(form_data.get("score")), form_data.get("feedback"), datetime.utcnow()
    await db.commit()
    return RedirectResponse(url=f"/teacher/assignments/{submission.assignment_id}/submissions?success=1", status_code=303)

@router.delete("/teacher/assignments/delete/{id}")
async def teacher_delete_assignment(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    assignment = await AssignmentRepository.get_by_id(db, id)
    if assignment: await db.delete(assignment); await db.commit()
    return JSONResponse(content={"message": "Assignment deleted successfully"})

@router.get("/teacher/notes/upload")
async def teacher_upload_notes(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/upload_notes.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses})

@router.post("/teacher/notes/upload")
async def teacher_upload_notes_post(request: Request, title: str = Form(...), course_id: int = Form(...), description: Optional[str] = Form(None), file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403)
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = f"/static/uploads/notes/{filename}"
    save_path = f"{file_path.lstrip('/')}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    await NotesRepository.create(db, {"title": title, "description": description, "course_id": course_id, "teacher_id": teacher.id, "file_path": file_path, "file_type": ext.replace('.', '')})
    return RedirectResponse(url="/teacher/dashboard?success=1", status_code=303)

@router.get("/teacher/courses/{id}")
async def teacher_course_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    course = await CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse("teacher/course_detail.html", {"request": request, "current_user": current_user, "teacher": current_user, "course": course})

@router.get("/teacher/courses/{id}/students")
async def teacher_course_students(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    data = await TeacherService.get_course_students(db, id)
    return templates.TemplateResponse("teacher/students.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "students": data["students"], 
        "filters": data["filters"]
    })

@router.get("/teacher/attendance/take")
async def teacher_take_attendance(request: Request, course_id: Optional[int] = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    
    students = []
    class_info = {"id": 0, "course_name": "Select a course", "grade": "", "section": "", "period": "", "time": "", "room": ""}
    
    if course_id:
        course = await CourseRepository.get_by_id(db, course_id)
        if course:
            class_info = {
                "id": course.id,
                "course_name": course.course_name,
                "grade": course.grade_level,
                "section": "", 
                "period": "", "time": "", "room": ""
            }
            # Fetch students via enrollment
            stmt = select(Student).join(CourseEnrollment).join(User).filter(CourseEnrollment.course_id == course_id).options(joinedload(Student.user))
            result = await db.execute(stmt)
            students_list = result.scalars().unique().all()
            
            for s in students_list:
                students.append({
                    "id": s.id,
                    "name": s.user.full_name,
                    "roll_number": s.student_id,
                    "email": s.user.email,
                    "avatar": s.user.profile_picture or "/static/images/default_avatar.png"
                })

    return templates.TemplateResponse("teacher/take_attendance.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "courses": courses, 
        "class_info": class_info, 
        "students": students,
        "today_date": datetime.now().strftime("%Y-%m-%d")
    })

@router.post("/teacher/attendance/save")
async def teacher_save_attendance(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    class_id = int(form_data.get("class_id"))
    attendance_date_str = form_data.get("attendance_date")
    
    try:
        attendance_date = datetime.strptime(attendance_date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        attendance_date = datetime.utcnow().date()
        
    for key in form_data:
        if key.startswith("attendance["):
             try:
                 student_id = int(key.split("[")[1].split("]")[0])
                 status = form_data[key]
                 remarks = form_data.get(f"remarks[{student_id}]")
                 arrival_time_str = form_data.get(f"arrival_time[{student_id}]")
                 
                 arrival_time = None
                 if arrival_time_str:
                     try:
                         arrival_time = datetime.strptime(arrival_time_str, "%H:%M").time()
                     except ValueError:
                         pass

                 existing = await AttendanceRepository.get_by_date(db, student_id, class_id, attendance_date)
                 if existing:
                     existing.status = status
                     existing.remarks = remarks
                     existing.arrival_time = arrival_time
                     db.add(existing)
                 else:
                     new_record = Attendance(
                         student_id=student_id,
                         course_id=class_id,
                         date=attendance_date,
                         status=status,
                         remarks=remarks,
                         arrival_time=arrival_time
                     )
                     db.add(new_record)
             except Exception:
                 continue
                 
    await db.commit()
    return RedirectResponse(url=f"/teacher/attendance/take?course_id={class_id}&success=1", status_code=303)

@router.get("/teacher/attendance")
async def teacher_attendance_list(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403)
    
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id)
    stats = await AttendanceRepository.get_overall_stats(db, teacher.id)
    attendance_records = await AttendanceRepository.get_teacher_attendance_history(db, teacher.id)
    
    return templates.TemplateResponse("teacher/attendance.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "courses": courses, 
        "classes": GRADE_LEVELS, 
        "subjects": DEPARTMENTS, 
        "stats": stats, 
        "current_month": datetime.now().strftime("%B %Y"), 
        "monthly_overview": [], # Could be implemented if needed
        "monthly_stats": stats, 
        "attendance_records": attendance_records
    })

@router.get("/teacher/attendance/view/{id}")
async def teacher_view_attendance(request: Request, id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    try:
        course_id_str, date_str = id.split("_")
        course_id = int(course_id_str)
        session_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
        
    course = await CourseRepository.get_by_id(db, course_id)
    if not course: raise HTTPException(status_code=404)
    
    # Get all attendance records for this course and date
    stmt = select(Attendance).filter(
        Attendance.course_id == course_id,
        Attendance.date == session_date
    ).options(joinedload(Attendance.student).joinedload(Student.user))
    
    result = await db.execute(stmt)
    records = result.scalars().unique().all()
    
    formatted_records = []
    for r in records:
        formatted_records.append({
            "student_name": r.student.user.full_name,
            "roll_number": r.student.student_id,
            "status": r.status,
            "arrival_time": r.arrival_time.strftime("%H:%M") if r.arrival_time else "-",
            "remarks": r.remarks or "-"
        })

    return templates.TemplateResponse("teacher/view_attendance_session.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "course": course, 
        "session_date": session_date,
        "records": formatted_records
    })

@router.get("/teacher/grades")
async def teacher_grades(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/grades.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses, "stats": {"average_grade": 85, "top_performers": 12, "failing_students": 2, "pending_grading": 5}, "grades": []})

@router.get("/teacher/grades/add")
async def teacher_grades_add(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    
    # Fetch all students for the dropdown
    # In a real app, this should probably be filtered via AJAX based on selected course/class
    students = await StudentRepository.get_all(db, limit=1000)
    
    # Format students for template
    student_list = []
    for s in students:
        student_list.append({
            "id": s.id,
            "name": s.user.full_name,
            "student_id": s.student_id
        })
        
    return templates.TemplateResponse("teacher/add_grade.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "courses": courses, 
        "students": student_list, 
        "assessments": []
    })

@router.post("/teacher/grades/add")
async def teacher_grades_add_post(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    
    try:
        student_id = int(form_data.get("student_id"))
        course_id = int(form_data.get("course_id"))
        score = float(form_data.get("score"))
        max_score = float(form_data.get("max_score"))
        
        grading_date_str = form_data.get("grading_date")
        if grading_date_str:
            grading_date = datetime.strptime(grading_date_str, "%Y-%m-%d")
        else:
            grading_date = datetime.utcnow()
            
        grade_data = {
            "student_id": student_id,
            "course_id": course_id,
            "grade_type": form_data.get("grade_type"),
            "score": score,
            "max_score": max_score,
            "grade": form_data.get("letter_grade"),
            "remarks": form_data.get("teacher_comments"),
            "date": grading_date
        }
        
        await GradeRepository.create(db, grade_data)
        
        action = form_data.get("action")
        if action == "save_and_new":
            return RedirectResponse(url="/teacher/grades/add?success=1", status_code=303)
            
        return RedirectResponse(url="/teacher/grades?success=1", status_code=303)
        
    except Exception as e:
        # Log error or handle it
        print(f"Error adding grade: {e}")
        return RedirectResponse(url="/teacher/grades/add?error=Invalid data", status_code=303)

@router.get("/teacher/attendance/{id}/edit")
async def teacher_edit_attendance(request: Request, id: str, current_user: User = Depends(get_current_user)):
    try:
        course_id_str, date_str = id.split("_")
        return RedirectResponse(url=f"/teacher/attendance/take?course_id={course_id_str}", status_code=303)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

@router.get("/teacher/tests")
async def teacher_tests(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    tests_data = await TestRepository.get_by_teacher(db, teacher.id) if teacher else []
    formatted = []
    for t in tests_data:
        total_students = 0; attempted = 0; is_overdue = t.end_time < datetime.utcnow()
        formatted.append({"id": t.id, "title": t.title, "subject": t.subject_name, "grade": t.grade_level, "class": t.grade_level, "section": t.target_section or "All", "start_time": t.start_time.strftime("%Y-%m-%d %H:%M"), "time_remaining": "Ended" if is_overdue else "Active", "duration": t.duration, "total_marks": t.total_points, "attempted": attempted, "total_students": total_students, "participation_rate": 0, "status": "completed" if is_overdue else "active", "status_color": "secondary" if is_overdue else "success", "is_important": False, "is_overdue": is_overdue})
    stats = {"total_tests": len(formatted), "active_tests": sum(1 for t in formatted if t["status"] == "active"), "completed_tests": sum(1 for t in formatted if t["status"] == "completed"), "upcoming_tests": 0}
    return templates.TemplateResponse("teacher/view_tests.html", {"request": request, "current_user": current_user, "teacher": current_user, "tests": formatted, "stats": stats, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "upcoming_tests": []})

@router.get("/teacher/tests/create")
async def teacher_create_test(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    return templates.TemplateResponse("teacher/create_test.html", {"request": request, "current_user": current_user, "teacher": current_user, "teacher_courses": teacher.courses if teacher else [], "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "sections": SECTIONS})

@router.get("/teacher/tests/{id}/results")
async def teacher_test_results(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    test = await TestRepository.get_by_id(db, id)
    if not test: raise HTTPException(status_code=404)
    return templates.TemplateResponse("teacher/view_tests.html", {"request": request, "current_user": current_user, "teacher": current_user, "test": test, "results": [], "tests": [], "stats": {"total_tests": 0, "active_tests": 0, "completed_tests": 0, "upcoming_tests": 0}, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "upcoming_tests": []})

@router.get("/teacher/tests/{id}/edit")
async def teacher_edit_test(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    test = await TestRepository.get_by_id(db, id)
    if not test: raise HTTPException(status_code=404)
    return templates.TemplateResponse("teacher/edit_test.html", {"request": request, "current_user": current_user, "teacher": current_user, "test": test, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "sections": SECTIONS})

@router.post("/teacher/tests/create")
async def teacher_create_test_post(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    form_data = await request.form()
    
    # Parse questions
    questions = []
    q_indices = set()
    for key in form_data.keys():
        if key.startswith("questions["):
            try:
                # format: questions[index][field]
                idx = int(key.split("[")[1].split("]")[0])
                q_indices.add(idx)
            except (IndexError, ValueError):
                continue
    
    sorted_indices = sorted(list(q_indices))
    
    for idx in sorted_indices:
        q_prefix = f"questions[{idx}]"
        q_type = form_data.get(f"{q_prefix}[type]")
        text = form_data.get(f"{q_prefix}[text]")
        if not text: continue
        
        points = float(form_data.get(f"{q_prefix}[marks]", 1.0))
        explanation = form_data.get(f"{q_prefix}[explanation]")
        correct_answer = form_data.get(f"{q_prefix}[correct_answer]")
        
        options = []
        if q_type == "multiple_choice":
            # Extract options
            opt_indices = []
            for key in form_data.keys():
                if key.startswith(f"{q_prefix}[options]["):
                    try:
                        oidx = int(key.split("options][")[1].split("]")[0])
                        opt_indices.append(oidx)
                    except (IndexError, ValueError):
                        continue
            opt_indices.sort()
            for oidx in opt_indices:
                val = form_data.get(f"{q_prefix}[options][{oidx}]")
                if val: options.append(val)
            
            # Map index to value for correct answer
            if correct_answer and correct_answer.isdigit():
                c_idx = int(correct_answer)
                if 0 <= c_idx < len(options):
                    correct_answer = options[c_idx]
        
        questions.append({
            "question_text": text,
            "question_type": q_type,
            "points": points,
            "explanation": explanation,
            "options": options,
            "correct_answer": correct_answer,
            "order": idx
        })

    test_data = {
        "title": form_data.get("title"), 
        "subject_name": form_data.get("subject"), 
        "grade_level": form_data.get("grade"), 
        "teacher_id": teacher.id, 
        "duration": int(form_data.get("duration", 60)), 
        "start_time": datetime.fromisoformat(form_data.get("start_time")), 
        "end_time": datetime.fromisoformat(form_data.get("end_time")), 
        "total_points": float(form_data.get("total_marks", 100)), 
        "target_section": form_data.get("section")
    }
    await TestRepository.create(db, test_data, questions)
    return RedirectResponse(url="/teacher/tests?success=1", status_code=303)

@router.delete("/teacher/tests/delete/{id}")
async def teacher_delete_test(id: int, db: AsyncSession = Depends(get_async_db)):
    test = await TestRepository.get_by_id(db, id)
    if test: await db.delete(test); await db.commit()
    return JSONResponse(content={"message": "Test deleted successfully"})

@router.get("/teacher/videos/upload")
async def teacher_upload_videos(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    videos = await VideosRepository.get_by_teacher(db, teacher.id) if teacher else []
    stats = {"total_videos": len(videos), "total_size": 0, "total_views": 0, "this_month": 0}
    return templates.TemplateResponse("teacher/upload_videos.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses, "videos": videos, "stats": stats, "storage": {"used": 0, "total": 10, "percentage": 0}})

@router.post("/teacher/videos/upload")
async def teacher_upload_videos_post(request: Request, title: str = Form(...), course_id: int = Form(...), description: Optional[str] = Form(None), video_file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403)
    ext = os.path.splitext(video_file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = f"/static/uploads/videos/{filename}"
    save_path = os.path.join("app", "static", "uploads", "videos", filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as buffer: shutil.copyfileobj(video_file.file, buffer)
    await VideosRepository.create(db, {"title": title, "description": description, "course_id": course_id, "teacher_id": teacher.id, "file_path": file_path})
    return RedirectResponse(url="/teacher/dashboard?success=1", status_code=303)

@router.get("/teacher/courses")
async def teacher_courses(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses_data = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    formatted_courses = []
    for c in courses_data:
        formatted_courses.append({"id": c.id, "subject": c.course_name, "grade": c.grade_level, "code": c.course_code, "description": c.description, "color": "primary", "student_count": len(c.enrollments) if hasattr(c, 'enrollments') else 0, "schedule": "N/A", "progress": 0, "assignment_count": len(c.assignments) if hasattr(c, 'assignments') else 0, "video_count": 0, "note_count": 0})
    stats = {"total_courses": len(formatted_courses), "active_classes": len(formatted_courses), "total_students": sum(c["student_count"] for c in formatted_courses), "upcoming_classes": 0}
    return templates.TemplateResponse("teacher/courses.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": formatted_courses, "stats": stats, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "todays_classes": []})

@router.get("/teacher/notices/create")
async def teacher_create_notice(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    return templates.TemplateResponse("teacher/create_notice.html", {"request": request, "current_user": current_user, "teacher": current_user, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS})

@router.post("/teacher/notices/create")
async def teacher_create_notice_post(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403, detail="Only teachers can create notices.")
    
    form_data = await request.form()
    target = form_data.get("target")
    notice_data = {
        "title": form_data.get("title"),
        "content": form_data.get("content"),
        "target_role": "student" if target != "all" else "all",
        "target_grade": target if target != "all" else None,
        "priority": form_data.get("priority", "normal"),
        "teacher_id": teacher.id,
        "created_at": datetime.utcnow()
    }
    
    # If target is specific grade, we might want to store that, but Notice model only has target_role (all, student, teacher).
    # For now, we'll stick to target_role.
    
    await NoticeRepository.create(db, notice_data)
    return RedirectResponse(url="/teacher/dashboard?success=notice_created", status_code=303)

@router.get("/teacher/groups")
async def teacher_groups(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    data = await group_service.get_groups_list(current_user.id)
    return templates.TemplateResponse("teacher/groups.html", {
        "request": request, 
        "current_user": current_user, 
        "groups": data["user_groups"]
    })

@router.get("/teacher/groups/{group_id}")
async def teacher_group_detail(request: Request, group_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    data = await group_service.get_group_detail(group_id, current_user.id)
    if not data:
        raise HTTPException(status_code=404, detail="Group not found")
        
    return templates.TemplateResponse("groups/group_detail.html", {
        "request": request,
        "current_user": current_user,
        "group": data["group"],
        "is_member": data["is_member"],
        "is_creator": data["is_creator"],
        "posts": data["posts"],
        "member_count": data["member_count"],
        "is_teacher": True # For template logic
    })

@router.get("/teacher/groups/{group_id}/posts/create")
async def teacher_create_post_form(
    request: Request,
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(
        select(Group).options(joinedload(Group.members)).filter(Group.id == group_id)
    )
    group = result.scalars().first()
    if not group: raise HTTPException(status_code=404, detail="Group not found")
    
    is_member = any(m.user_id == current_user.id for m in group.members)
    if not is_member: raise HTTPException(status_code=403, detail="Must be a group member to post")
    
    return templates.TemplateResponse("groups/new_post.html", {
        "request": request,
        "current_user": current_user,
        "group": group,
        "role_prefix": "teacher",
        "post_types": ["notice", "note", "link"]
    })

@router.post("/teacher/groups/{group_id}/posts/create")
async def teacher_create_post(
    group_id: int,
    title: str = Form(...),
    content: Optional[str] = Form(None),
    post_type: str = Form("notice"),
    link_url: Optional[str] = Form(None),
    link_description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(
        select(Group).options(joinedload(Group.members)).filter(Group.id == group_id)
    )
    group = result.scalars().first()
    if not group: raise HTTPException(status_code=404, detail="Group not found")
    
    is_member = any(m.user_id == current_user.id for m in group.members)
    if not is_member: raise HTTPException(status_code=403, detail="Must be a group member to post")
    
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
    return RedirectResponse(url=f"/teacher/groups/{group_id}/posts", status_code=303)

@router.get("/teacher/groups/{group_id}/edit")
async def teacher_edit_group_form(request: Request, group_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Group).filter(Group.id == group_id))
    group = result.scalars().first()
    if not group: raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if creator or teacher
    from backup.models.group_models import GroupMember
    res = await db.execute(select(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == current_user.id))
    member = res.scalars().first()
    if not member or member.role not in ['creator', 'teacher']:
        raise HTTPException(status_code=403, detail="Not authorized to edit this group")
        
    return templates.TemplateResponse("groups/edit_group.html", {
        "request": request,
        "current_user": current_user,
        "group": group,
        "role_prefix": "teacher"
    })

@router.post("/teacher/groups/{group_id}/edit")
async def teacher_edit_group(
    group_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(Group).filter(Group.id == group_id))
    group = result.scalars().first()
    if not group: raise HTTPException(status_code=404, detail="Group not found")
    
    from backup.models.group_models import GroupMember
    res = await db.execute(select(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == current_user.id))
    member = res.scalars().first()
    if not member or member.role not in ['creator', 'teacher']:
        raise HTTPException(status_code=403, detail="Not authorized to edit this group")
        
    group.name = name
    group.description = description
    await db.commit()
    return RedirectResponse(url=f"/teacher/groups/{group_id}?success=updated", status_code=303)

@router.get("/teacher/groups/{group_id}/posts")
async def teacher_group_posts(
    request: Request,
    group_id: int,
    post_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    from backup.services.group_post_service import GroupPostService
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
        "is_teacher": True,
        "post_types": ["notice", "note", "link"]
    })

@router.get("/teacher/groups/{group_id}/posts/{post_id}")
async def teacher_view_post(
    request: Request,
    group_id: int,
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    
    is_member = await group_repo.is_group_member(group_id, current_user.id)
    if not is_member: raise HTTPException(status_code=403, detail="Not a member of this group")
    
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

@router.post("/teacher/groups/{group_id}/posts/{post_id}/delete")
async def teacher_delete_post(
    group_id: int,
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    from backup.services.group_post_service import GroupPostService
    post_repo = GroupPostRepository(db)
    group_repo = GroupRepository(db)
    post_service = GroupPostService(post_repo, group_repo)
    
    try:
        await post_service.delete_post(post_id, current_user.id)
        return RedirectResponse(url=f"/teacher/groups/{group_id}/posts?success=deleted", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/teacher/chat")
async def teacher_chat(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=404, detail="Teacher not found")
    parents = await ChatRepository.get_teacher_parents(db, teacher.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id)
    all_students = []
    for course in courses:
        students = await CourseRepository.get_enrolled_students(db, course.id)
        for s in students:
            res = await db.execute(select(func.count(ChatMessage.id)).filter(ChatMessage.sender_id == s.user_id, ChatMessage.receiver_id == current_user.id, ChatMessage.is_read == False))
            unread = res.scalar() or 0
            all_students.append({"id": s.user_id, "name": s.user.full_name, "grade": s.grade_level, "section": s.section, "unread_count": unread})
    
    res = await db.execute(select(Teacher).options(joinedload(Teacher.user)).filter(Teacher.id != teacher.id))
    other_teachers = res.scalars().unique().all()
    formatted_teachers = []
    for t in other_teachers:
        res = await db.execute(select(func.count(ChatMessage.id)).filter(ChatMessage.sender_id == t.user_id, ChatMessage.receiver_id == current_user.id, ChatMessage.is_read == False))
        unread = res.scalar() or 0
        formatted_teachers.append({"id": t.user_id, "name": t.user.full_name, "department": t.department, "unread_count": unread})
    
    formatted_parents = []
    for p in parents:
        student_names = ", ".join([s.user.full_name for s in p['parent'].children]) if hasattr(p['parent'], 'children') else "N/A"
        formatted_parents.append({"id": p['user'].id, "name": p['user'].full_name, "student_name": student_names, "unread_count": p['unread_count']})
    return templates.TemplateResponse("teacher/chat.html", {"request": request, "current_user": current_user, "teacher": current_user, "students": all_students, "parents": formatted_parents, "teachers": formatted_teachers, "classes": [], "announcements": []})

@router.get("/teacher/timetable")
async def teacher_timetable(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    time_slots = ["08:00", "09:00", "10:00", "11:00", "12:00", "01:00", "02:00"]
    week_days = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for d in days:
        week_days.append({"name": d, "date": "Jan 12", "is_today": d == datetime.now().strftime("%A"), "classes": {slot: [] for slot in time_slots}})
    return templates.TemplateResponse("teacher/timetable.html", {"request": request, "current_user": current_user, "teacher": current_user, "current_week": "Jan 12 - Jan 16, 2026", "prev_week": "prev", "next_week": "next", "week_days": week_days, "time_slots": time_slots, "todays_schedule": [], "upcoming_classes": [], "subjects": DEPARTMENTS, "classes": GRADE_LEVELS})

@router.post("/teacher/timetable")
async def teacher_timetable_post(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=403, detail="Only teachers can update timetable")
    
    form_data = await request.form()
    # Handle timetable updates here
    # For now, just redirect back with success
    return RedirectResponse(url="/teacher/timetable?success=1", status_code=303)

