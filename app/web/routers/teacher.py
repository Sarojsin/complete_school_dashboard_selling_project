from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy import select, func, delete, update, desc, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import os
import shutil
import uuid
from datetime import datetime

from app.core.database import get_async_db
from app.core.templates import templates
from dependencies import get_current_user
from models.models import User, Student, Teacher, Assignment, AssignmentSubmission, Course, FeeRecord, Notice, Attendance, Grade, Note, Video
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

# ------------------ TEACHER PAGES ------------------
@router.get("/teacher/dashboard")
async def teacher_dashboard(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: return templates.TemplateResponse("teacher/dashboard.html", {"request": request, "current_user": current_user, "teacher": current_user, "unread_count": 0})
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id)
    
    # Simple query for assignments
    res = await db.execute(select(Assignment).filter(Assignment.teacher_id == teacher.id).limit(5))
    assignments = res.scalars().all()
    
    unread_count = await MessageRepository.get_unread_count(db, current_user.id)
    return templates.TemplateResponse("teacher/dashboard.html", {"request": request, "current_user": current_user, "teacher": teacher, "courses": courses, "assignments": assignments, "stats": {"student_count": sum(len(c.enrollments) for c in courses), "course_count": len(courses), "assignment_count": len(assignments), "submission_count": 0}, "unread_count": unread_count, "recent_messages": []})

@router.get("/teacher/profile")
async def teacher_profile(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    teacher_data = {"name": current_user.full_name, "email": current_user.email, "id": teacher.employee_id if teacher else "N/A", "department": teacher.department if teacher else "N/A", "phone": teacher.phone if teacher else "N/A", "qualification": teacher.qualification if teacher else "N/A", "specialization": teacher.specialization if teacher else "N/A", "joining_date": teacher.joining_date.strftime('%Y-%m-%d') if teacher and teacher.joining_date else "N/A", "profile_pic": current_user.profile_picture or "/static/images/default-avatar.png"}
    return templates.TemplateResponse("teacher/profile.html", {"request": request, "current_user": current_user, "teacher_data": teacher_data})

@router.post("/teacher/profile")
async def teacher_update_profile(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    if "profile_pic" in form_data and form_data["profile_pic"].filename:
        profile_pic = form_data["profile_pic"]
        ext = os.path.splitext(profile_pic.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join("static/uploads/avatars", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as buffer: shutil.copyfileobj(profile_pic.file, buffer)
        current_user.profile_picture = f"/static/uploads/avatars/{filename}"
    if "full_name" in form_data: current_user.full_name = form_data["full_name"]
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if teacher:
        if "full_name" in form_data: teacher.full_name = form_data["full_name"]
        if "phone" in form_data: teacher.phone = form_data["phone"]
        db.add(teacher)
    db.add(current_user)
    await db.commit()
    return RedirectResponse(url="/teacher/profile?success=1", status_code=303)

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
    assignments_data = await AssignmentRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    
    formatted = []
    for a in assignments_data:
        res = await db.execute(select(func.count(AssignmentSubmission.id)).filter(AssignmentSubmission.assignment_id == a.id))
        submitted_count = res.scalar() or 0
        total_students = len(a.course.enrollments) if a.course else 0
        is_overdue = a.due_date < datetime.utcnow()
        
        formatted.append({
            "id": a.id, "title": a.title, "description": a.description, "subject": a.course.course_name if a.course else "N/A", "class": a.course.grade_level if a.course else "N/A", "due_date": a.due_date.strftime("%Y-%m-%d %H:%M"), "due_in": "Overdue" if is_overdue else "Active", "submitted": submitted_count, "total_students": total_students, "submission_rate": (submitted_count / total_students * 100) if total_students > 0 else 0, "status": "completed" if is_overdue else "active", "status_color": "secondary" if is_overdue else "success", "is_urgent": not is_overdue and (a.due_date - datetime.utcnow()).days < 2, "is_overdue": is_overdue
        })
        
    stats = {"total_assignments": len(formatted), "submitted": sum(a["submitted"] for a in formatted), "pending": sum(a["total_students"] - a["submitted"] for a in formatted), "overdue": sum(1 for a in formatted if a["is_overdue"])}
    return templates.TemplateResponse("teacher/assignments.html", {"request": request, "current_user": current_user, "teacher": current_user, "assignments": formatted, "stats": stats, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "upcoming_deadlines": [a for a in formatted if not a["is_overdue"]][:3]})

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
    return templates.TemplateResponse("teacher/create_assignment.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses})

@router.post("/teacher/assignments/create")
async def teacher_create_assignment_post(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    assignment_data = {"title": form_data.get("title"), "description": form_data.get("description"), "course_id": int(form_data.get("course_id")), "teacher_id": teacher.id, "due_date": datetime.fromisoformat(form_data.get("due_date")), "max_score": float(form_data.get("max_score", 100))}
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
    course = await CourseRepository.get_by_id(db, id)
    students = await CourseRepository.get_enrolled_students(db, id)
    formatted = []
    for s in students:
        formatted.append({
            "id": s.id, "name": s.user.full_name if s.user else "Unknown student", "email": s.user.email if s.user else "N/A", "grade": s.grade_level, "section": s.section, "attendance": 100, "average_grade": 0, "pending_assignments": 0, "avatar": f"https://ui-avatars.com/api/?name={s.user.full_name.replace(' ', '+') if s.user else 'User'}&background=random"
        })
    return templates.TemplateResponse("teacher/students.html", {"request": request, "current_user": current_user, "teacher": current_user, "students": formatted, "filters": {"grade": course.grade_level if course else None, "section": course.section if course and hasattr(course, 'section') else None}})

@router.get("/teacher/attendance/take")
async def teacher_take_attendance(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/take_attendance.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses, "class_info": {"id": 0, "course_name": "Select a course", "grade": "", "section": "", "period": "", "time": "", "room": ""}, "students": []})

@router.get("/teacher/attendance")
async def teacher_attendance_list(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    stats = {"total_students": 150, "present_today": 135, "absent_today": 10, "overall_percentage": 92}
    monthly_stats = {"present_percentage": 90, "absent_percentage": 7, "late_percentage": 3}
    return templates.TemplateResponse("teacher/attendance.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses, "classes": GRADE_LEVELS, "subjects": DEPARTMENTS, "stats": stats, "current_month": datetime.now().strftime("%B %Y"), "monthly_overview": [], "monthly_stats": monthly_stats, "attendance_records": []})

@router.get("/teacher/attendance/{id}")
async def teacher_view_attendance(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    course = await CourseRepository.get_by_id(db, id)
    return templates.TemplateResponse("teacher/attendance.html", {"request": request, "current_user": current_user, "teacher": current_user, "course": course, "classes": GRADE_LEVELS, "subjects": DEPARTMENTS, "stats": {"total_students": 30, "present_today": 0, "absent_today": 0, "overall_percentage": 0}, "current_month": datetime.now().strftime("%B %Y"), "monthly_overview": [], "monthly_stats": {"present_percentage": 0, "absent_percentage": 0, "late_percentage": 0}, "attendance_records": []})

@router.get("/teacher/grades")
async def teacher_grades(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/grades.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses, "stats": {"average_grade": 85, "top_performers": 12, "failing_students": 2, "pending_grading": 5}, "grades": []})

@router.get("/teacher/grades/add")
async def teacher_grades_add(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    courses = await CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/add_grade.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses, "students": [], "assessments": []})

@router.post("/teacher/grades/add")
async def teacher_grades_add_post(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    return RedirectResponse(url="/teacher/grades?success=1", status_code=303)

@router.get("/teacher/attendance/{id}/edit")
async def teacher_edit_attendance(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/take_attendance.html", {"request": request, "current_user": current_user, "teacher": current_user, "students": []})

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
    test_data = {"title": form_data.get("title"), "subject_name": form_data.get("subject"), "grade_level": form_data.get("grade"), "teacher_id": teacher.id, "duration": int(form_data.get("duration", 60)), "start_time": datetime.fromisoformat(form_data.get("start_time")), "end_time": datetime.fromisoformat(form_data.get("end_time")), "total_points": float(form_data.get("total_marks", 100)), "target_section": form_data.get("section")}
    await TestRepository.create(db, test_data, [])
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
    save_path = f"{file_path.lstrip('/')}"
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
    form_data = await request.form()
    return RedirectResponse(url="/teacher/dashboard?success=notice_created", status_code=303)

@router.get("/teacher/groups")
async def teacher_groups(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    from repositories.group_repository import GroupRepository
    from services.group_service import GroupService
    groups = await GroupService(GroupRepository(db)).get_user_groups(current_user.id, current_user.role)
    return templates.TemplateResponse("teacher/groups.html", {"request": request, "current_user": current_user, "teacher": current_user, "groups": groups})

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
