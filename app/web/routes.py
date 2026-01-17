from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import os
import shutil
import uuid
from datetime import datetime

from app.core.database import get_db
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

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@router.get("/signup/student", response_class=HTMLResponse)
async def signup_student_page(request: Request):
    return templates.TemplateResponse("auth/signup_student.html", {"request": request, "grades": GRADE_LEVELS})

@router.get("/signup/teacher", response_class=HTMLResponse)
async def signup_teacher_page(request: Request):
    return templates.TemplateResponse("auth/signup_teacher.html", {"request": request, "departments": DEPARTMENTS})

@router.get("/signup/authority", response_class=HTMLResponse)
async def signup_authority_page(request: Request):
    return templates.TemplateResponse("auth/signup_authority.html", {"request": request})

@router.get("/signup/parent", response_class=HTMLResponse)
async def signup_parent_page(request: Request):
    return templates.TemplateResponse("auth/signup_parent.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@router.get("/register/student", response_class=HTMLResponse)
async def register_student_page(request: Request):
    return templates.TemplateResponse("auth/signup_student.html", {"request": request, "grades": GRADE_LEVELS})

@router.get("/register/teacher", response_class=HTMLResponse)
async def register_teacher_page(request: Request):
    return templates.TemplateResponse("auth/signup_teacher.html", {"request": request, "departments": DEPARTMENTS})

@router.get("/register/parent", response_class=HTMLResponse)
async def register_parent_page(request: Request):
    return templates.TemplateResponse("auth/signup_parent.html", {"request": request})

@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response

# ------------------ STUDENT PAGES ------------------
@router.get("/student/dashboard")
async def student_dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    unread_count = MessageRepository.get_unread_count(db, current_user.id)
    return templates.TemplateResponse("student/dashboard.html", {
        "request": request, "current_user": current_user, "student": current_user,
        "unread_count": unread_count, "assignments": [], "recent_grades": []
    })

@router.get("/student/profile")
async def student_profile(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    student_data = {
        "name": current_user.full_name, "id": student.student_id if student else "N/A",
        "grade": student.grade_level if student else "N/A", "section": student.section if student else "N/A",
        "email": current_user.email, "phone": student.phone if student else "N/A",
        "dob": student.date_of_birth.strftime('%Y-%m-%d') if student and student.date_of_birth else "",
        "address": student.address if student else "", "profile_pic": current_user.profile_picture or "/static/images/default-avatar.png",
        "roll_number": student.student_id if student else "N/A", "admission_date": student.enrollment_date.strftime('%Y-%m-%d') if student and student.enrollment_date else "N/A"
    }
    return templates.TemplateResponse("student/profile.html", {"request": request, "current_user": current_user, "student": student_data})

@router.post("/student/profile")
async def student_update_profile(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    if "profile_pic" in form_data and form_data["profile_pic"].filename:
        profile_pic = form_data["profile_pic"]
        ext = os.path.splitext(profile_pic.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join("static/uploads/avatars", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as buffer: shutil.copyfileobj(profile_pic.file, buffer)
        current_user.profile_picture = f"/static/uploads/avatars/{filename}"
    if "email" in form_data: current_user.email = form_data["email"]
    if "full_name" in form_data: current_user.full_name = form_data["full_name"]
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if student:
        if "full_name" in form_data: student.full_name = form_data["full_name"]
        if "phone" in form_data: student.phone = form_data["phone"]
        if "address" in form_data: student.address = form_data["address"]
        if "dob" in form_data and form_data["dob"]:
            try: student.date_of_birth = datetime.strptime(form_data["dob"], '%Y-%m-%d').date()
            except ValueError: pass
        db.add(student)
    db.add(current_user)
    db.commit()
    return RedirectResponse(url="/student/profile?success=1", status_code=303)

@router.get("/student/courses")
async def student_courses(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/courses.html", {"request": request, "current_user": current_user, "student": current_user, "courses": []})

@router.get("/student/assignments")
async def student_assignments(request: Request, status: str = "all", current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    courses = StudentRepository.get_enrolled_courses(db, student.id)
    course_ids = [c.id for c in courses]
    all_assignments = AssignmentRepository.get_student_assignments(db, student.id, course_ids, student_grade=student.grade_level, student_section=student.section)
    stats = {"total": len(all_assignments), "pending": sum(1 for a in all_assignments if a["status"] == "pending"), "submitted": sum(1 for a in all_assignments if a["status"] == "submitted"), "graded": sum(1 for a in all_assignments if a["status"] == "graded"), "overdue": sum(1 for a in all_assignments if a["status"] == "overdue")}
    filtered = [a for a in all_assignments if status == "all" or a["status"] == status]
    return templates.TemplateResponse("student/assignments.html", {"request": request, "current_user": current_user, "student": current_user, "assignments": filtered, "stats": stats, "current_filter": status})

@router.get("/student/fees")
async def student_fees(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    fees = FeeRepository.get_student_fees(db, student.id)
    summary = FeeRepository.get_fee_summary(db, student.id)
    payment_history = FeeRepository.get_payment_history(db, student.id)
    formatted_history = [{"date": p.payment_date, "amount": p.paid_amount, "method": "Online", "transaction_id": f"TXN-{p.id}", "status": "completed", "receipt_url": "#"} for p in payment_history]
    return templates.TemplateResponse("student/fees.html", {"request": request, "current_user": current_user, "student": current_user, "fee_structure": fees, "payment_history": formatted_history, "total_fees": summary['total_amount'], "paid_amount": summary['total_paid'], "pending_amount": summary['total_pending'], "fee_status": "paid" if summary['total_pending'] == 0 else "pending"})

@router.get("/student/assignments/{assignment_id}")
async def student_assignment_detail(request: Request, assignment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    assignment = AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")
    submission = AssignmentRepository.get_submission_by_student(db, assignment_id, student.id)
    status = "pending"
    if submission: status = "graded" if submission.score is not None else "submitted"
    elif assignment.due_date < datetime.utcnow(): status = "overdue"
    assignment_data = {"id": assignment.id, "title": assignment.title, "description": assignment.description, "course": assignment.course.course_name if assignment.course else "Unknown Course", "teacher": assignment.teacher.user.full_name if assignment.teacher else "Unknown Teacher", "due_date": assignment.due_date, "max_score": assignment.max_score, "status": status, "submission": submission, "is_overdue": status == "overdue"}
    return templates.TemplateResponse("student/assignments_detail.html", {"request": request, "current_user": current_user, "assignment": assignment_data})

@router.post("/student/assignments/{assignment_id}/submit")
async def student_assignment_submit(assignment_id: int, request: Request, file: UploadFile = File(None), submission_text: str = Form(None), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student: raise HTTPException(status_code=400, detail="Student profile not found")
    assignment = AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")
    file_path = None
    if file and file.filename:
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = f"/static/uploads/assignments/{filename}"
        save_path = f"{file_path.lstrip('/')}"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    existing_submission = AssignmentRepository.get_submission_by_student(db, assignment_id, student.id)
    if existing_submission:
        update_data = {"submission_text": submission_text if submission_text else existing_submission.submission_text, "submitted_at": datetime.utcnow()}
        if file_path: update_data["file_path"] = file_path
        AssignmentRepository.update_submission(db, existing_submission, **update_data)
    else:
        submission_data = {"assignment_id": assignment_id, "student_id": student.id, "submission_text": submission_text, "file_path": file_path, "submitted_at": datetime.utcnow()}
        AssignmentRepository.create_submission(db, submission_data)
    return RedirectResponse(url=f"/student/assignments", status_code=303)

@router.get("/student/tests")
async def student_test_list(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    tests = TestRepository.get_available_tests_for_student(db, student.id, section=student.section, grade_level=student.grade_level) if student else []
    return templates.TemplateResponse("student/test_list.html", {"request": request, "current_user": current_user, "student": current_user, "tests": tests})

@router.get("/student/tests/{test_id}/start")
async def student_take_test(request: Request, test_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    test = TestRepository.get_by_id(db, test_id)
    if not test: raise HTTPException(status_code=404, detail="Test not found")
    if not TestService.is_test_available(test): raise HTTPException(status_code=400, detail="Test is not currently available")
    if test.target_section and test.target_section != "All" and test.target_section != student.section: raise HTTPException(status_code=403, detail="This test is not assigned to your section")
    if test.grade_level and test.grade_level != student.grade_level: raise HTTPException(status_code=403, detail="This test is not for your grade level")
    if TestService.has_student_submitted(db, test_id, student.id): return RedirectResponse(f"/student/tests/{test_id}/result")
    submission = TestService.get_or_create_submission(db, test_id, student.id)
    return templates.TemplateResponse("student/take_test.html", {"request": request, "test": test, "submission": submission, "user_answers": submission.answers or {}})

@router.post("/student/tests/{test_id}/submit")
async def student_submit_test(request: Request, test_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student: raise HTTPException(status_code=404, detail="Student profile not found")
    test = TestRepository.get_by_id(db, test_id)
    if not test: raise HTTPException(status_code=404, detail="Test not found")
    submission = TestRepository.get_submission(db, test_id, student.id)
    if not submission: raise HTTPException(status_code=400, detail="Test session not found")
    if submission.submitted_at: return RedirectResponse(f"/student/tests/{test_id}/result")
    form_data = await request.form()
    answers = {k.replace("question_", ""): v for k, v in form_data.items() if k.startswith("question_")}
    time_taken = (datetime.utcnow() - submission.started_at).total_seconds()
    submission = TestRepository.update_submission(db, submission, answers=answers, submitted_at=datetime.utcnow(), time_taken=int(time_taken))
    TestService.grade_submission(db, submission, test)
    return RedirectResponse(url=f"/student/tests/{test_id}/result", status_code=303)

@router.get("/student/tests/{test_id}/result")
async def student_test_result(request: Request, test_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    test = TestRepository.get_by_id(db, test_id)
    if not test: raise HTTPException(status_code=404, detail="Test not found")
    submission = TestRepository.get_submission(db, test_id, student.id)
    if not submission or not submission.submitted_at: return RedirectResponse(f"/student/tests/{test_id}/start")
    questions_data = []
    correct_count, wrong_count, skipped_count = 0, 0, 0
    for q in test.questions:
        user_ans = submission.answers.get(str(q.id))
        is_correct = False
        if user_ans:
            if str(user_ans).strip().lower() == str(q.correct_answer).strip().lower(): is_correct = True; correct_count += 1
            else: wrong_count += 1
        else: skipped_count += 1
        questions_data.append({"question_text": q.question_text, "user_answer": user_ans or "Not answered", "correct_answer": q.correct_answer, "is_correct": is_correct, "explanation": getattr(q, 'explanation', None)})
    percentage = submission.percentage or 0
    rating = "Excellent" if percentage >= 80 else "Good" if percentage >= 60 else "Average" if percentage >= 40 else "Needs Improvement"
    return templates.TemplateResponse("student/test_result.html", {"request": request, "test": test, "score": submission.score or 0, "total_questions": len(test.questions), "percentage": round(percentage, 1), "result_status": "Passed" if percentage >= 40 else "Failed", "correct_answers": correct_count, "wrong_answers": wrong_count, "skipped_questions": skipped_count, "time_taken": f"{submission.time_taken // 60}m {submission.time_taken % 60}s" if submission.time_taken else "N/A", "performance_rating": rating, "performance_feedback": "Keep up the great work!" if percentage >= 80 else "Good job!", "questions": questions_data, "improvement_suggestions": ["Review chapters related to incorrect answers."]})

@router.get("/student/notices")
async def student_notices(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notices_data = NoticeRepository.get_active_notices(db, target_role="students")
    notices = [{"id": n.id, "title": n.title, "content": n.content, "excerpt": n.content[:100] + "..." if len(n.content) > 100 else n.content, "priority": n.priority, "date": n.created_at.strftime('%Y-%m-%d'), "time": n.created_at.strftime('%H:%M'), "author": n.authority.full_name if n.authority else "School Authority"} for n in notices_data]
    return templates.TemplateResponse("student/notices.html", {"request": request, "current_user": current_user, "student": current_user, "notices": notices, "important_notices": [n for n in notices if n["priority"] in ["high", "urgent"]], "current_page": 1, "total_pages": 1})

@router.get("/student/timetable")
async def student_timetable(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/timetable.html", {"request": request, "current_user": current_user, "student": current_user, "timetable": [], "dates": []})

@router.get("/student/notes")
async def student_notes(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    notes = []
    if student:
        enrollments = StudentRepository.get_enrolled_courses(db, student.id)
        if not enrollments and student.grade_level: enrollments = CourseRepository.get_all(db, grade_level=student.grade_level)
        for cid in [c.id for c in enrollments]: notes.extend(NotesRepository.get_by_course(db, cid))
    formatted_notes = [{"id": n.id, "title": n.title, "description": n.description or "", "subject": n.course.course_name if n.course else "Unknown", "teacher": n.teacher.full_name if n.teacher else "Unknown", "upload_date": n.uploaded_at.strftime("%Y-%m-%d"), "file_type": n.file_type or "file", "file_url": n.file_path} for n in notes]
    return templates.TemplateResponse("student/notes.html", {"request": request, "current_user": current_user, "student": current_user, "notes": formatted_notes, "stats": {"total_notes": len(formatted_notes), "total_subjects": len(list(set(n["subject"] for n in formatted_notes))), "total_downloads": 0, "recent_uploads": 0}, "subjects": list(set(n["subject"] for n in formatted_notes))})

@router.get("/student/videos")
async def student_videos(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_user_id(db, current_user.id)
    videos = []
    if student:
        enrollments = StudentRepository.get_enrolled_courses(db, student.id)
        if not enrollments and student.grade_level: enrollments = CourseRepository.get_all(db, grade_level=student.grade_level)
        for cid in [c.id for c in enrollments]: videos.extend(VideosRepository.get_by_course(db, cid))
    formatted_videos = [{"id": v.id, "title": v.title, "description": v.description or "", "subject": v.course.course_name if v.course else "Unknown", "teacher": v.teacher.full_name if v.teacher else "Unknown", "upload_date": v.uploaded_at.strftime("%Y-%m-%d"), "video_url": v.file_path, "thumbnail": "https://via.placeholder.com/300x200?text=Video", "duration": f"{v.duration // 60}:{v.duration % 60:02d}" if v.duration else "0:00"} for v in videos]
    return templates.TemplateResponse("student/videos.html", {"request": request, "current_user": current_user, "student": current_user, "videos": formatted_videos, "progress_stats": {"total_watched": 0, "total_videos": len(formatted_videos), "completion_rate": 0, "total_time": "0h 0m", "by_subject": {}}, "subjects": list(set(v["subject"] for v in formatted_videos))})

@router.get("/student/forum")
async def student_forum(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/forum.html", {"request": request, "current_user": current_user, "student": current_user, "posts": []})

@router.get("/student/messages")
async def student_messages(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    messages = MessageRepository.get_inbox(db, current_user.id)
    return templates.TemplateResponse("student/messages.html", {"request": request, "current_user": current_user, "student": current_user, "messages": messages, "unread_count": MessageRepository.get_unread_count(db, current_user.id)})

@router.post("/student/messages/{message_id}/read")
async def mark_message_read(message_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if MessageRepository.mark_as_read(db, message_id): return {"success": True}
    raise HTTPException(status_code=404, detail="Message not found")

@router.get("/student/teachers")
async def student_teachers(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teachers = TeacherRepository.get_all(db)
    return templates.TemplateResponse("student/teachers.html", {"request": request, "current_user": current_user, "student": current_user, "teachers": teachers})

@router.post("/student/teachers/{teacher_id}/contact")
async def student_contact_teacher(teacher_id: int, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    teacher = TeacherRepository.get_by_id(db, teacher_id)
    if not teacher: raise HTTPException(status_code=404, detail="Teacher not found")
    MessageRepository.create(db=db, sender_id=current_user.id, recipient_id=teacher.user_id, subject=form_data.get("subject"), body=form_data.get("message"))
    return {"message": "Message sent successfully"}

@router.get("/student/groups")
async def student_groups(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from repositories.group_repository import GroupRepository
    from services.group_service import GroupService
    groups = GroupService(GroupRepository(db)).get_user_groups(current_user.id, current_user.role)
    return templates.TemplateResponse("student/groups.html", {"request": request, "current_user": current_user, "groups": groups})

@router.get("/student/grades")
async def student_grades(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/grades.html", {"request": request, "current_user": current_user, "student": current_user, "grades": [], "gpa": 0.0})

@router.get("/student/attendance")
async def student_attendance(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/attendance.html", {"request": request, "current_user": current_user, "student": current_user, "attendance": []})

# ------------------ TEACHER PAGES ------------------
@router.get("/teacher/dashboard")
async def teacher_dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: return templates.TemplateResponse("teacher/dashboard.html", {"request": request, "current_user": current_user, "teacher": current_user, "unread_count": 0})
    courses = CourseRepository.get_all(db, teacher_id=teacher.id)
    assignments = db.query(Assignment).filter(Assignment.teacher_id == teacher.id).limit(5).all()
    unread_count = MessageRepository.get_unread_count(db, current_user.id)
    return templates.TemplateResponse("teacher/dashboard.html", {"request": request, "current_user": current_user, "teacher": teacher, "courses": courses, "assignments": assignments, "stats": {"student_count": sum(len(c.enrollments) for c in courses), "course_count": len(courses), "assignment_count": len(assignments), "submission_count": 0}, "unread_count": unread_count, "recent_messages": []})

@router.get("/teacher/profile")
async def teacher_profile(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    teacher_data = {"name": current_user.full_name, "email": current_user.email, "id": teacher.employee_id if teacher else "N/A", "department": teacher.department if teacher else "N/A", "phone": teacher.phone if teacher else "N/A", "qualification": teacher.qualification if teacher else "N/A", "specialization": teacher.specialization if teacher else "N/A", "joining_date": teacher.joining_date.strftime('%Y-%m-%d') if teacher and teacher.joining_date else "N/A", "profile_pic": current_user.profile_picture or "/static/images/default-avatar.png"}
    return templates.TemplateResponse("teacher/profile.html", {"request": request, "current_user": current_user, "teacher_data": teacher_data})

@router.post("/teacher/profile")
async def teacher_update_profile(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if teacher:
        if "full_name" in form_data: teacher.full_name = form_data["full_name"]
        if "phone" in form_data: teacher.phone = form_data["phone"]
        db.add(teacher)
    db.add(current_user)
    db.commit()
    return RedirectResponse(url="/teacher/profile?success=1", status_code=303)

@router.get("/teacher/students")
async def teacher_students(request: Request, grade: str = None, section: str = None, search: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    students = StudentRepository.get_all(db, grade_level=grade, section=section, search=search)
    formatted = []
    for s in students:
        # Simple stats for now, could be made more dynamic
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
async def teacher_student_detail(request: Request, student_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, student_id)
    if not student: raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse("teacher/student_detail.html", {"request": request, "current_user": current_user, "teacher": current_user, "student": student, "student_id": student_id})

@router.get("/teacher/students/{student_id}/grades")
async def teacher_student_grades(request: Request, student_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, student_id)
    if not student: raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse("teacher/student_grades.html", {"request": request, "current_user": current_user, "teacher": current_user, "student": student, "grades": []})

@router.post("/teacher/students/{student_id}/contact")
async def teacher_contact_student(student_id: int, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    student = StudentRepository.get_by_id(db, student_id)
    if not student: raise HTTPException(status_code=404, detail="Student not found")
    MessageRepository.create(db=db, sender_id=current_user.id, recipient_id=student.user_id, subject=form_data.get("subject"), body=form_data.get("message"))
    return {"message": "Message sent successfully"}

@router.get("/teacher/messages")
async def teacher_messages(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    messages = MessageRepository.get_inbox(db, current_user.id)
    return templates.TemplateResponse("teacher/messages.html", {"request": request, "current_user": current_user, "teacher": current_user, "messages": messages, "unread_count": MessageRepository.get_unread_count(db, current_user.id)})

@router.post("/teacher/messages/{message_id}/read")
async def teacher_mark_message_read(message_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if MessageRepository.mark_as_read(db, message_id): return {"success": True}
    raise HTTPException(status_code=404, detail="Message not found")

@router.get("/teacher/assignments")
async def teacher_assignments(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    assignments_data = AssignmentRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    
    formatted = []
    for a in assignments_data:
        submitted_count = db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == a.id).count()
        total_students = len(a.course.enrollments) if a.course else 0
        is_overdue = a.due_date < datetime.utcnow()
        
        formatted.append({
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "subject": a.course.course_name if a.course else "N/A",
            "class": a.course.grade_level if a.course else "N/A",
            "due_date": a.due_date.strftime("%Y-%m-%d %H:%M"),
            "due_in": "Overdue" if is_overdue else "Active",
            "submitted": submitted_count,
            "total_students": total_students,
            "submission_rate": (submitted_count / total_students * 100) if total_students > 0 else 0,
            "status": "completed" if is_overdue else "active",
            "status_color": "secondary" if is_overdue else "success",
            "is_urgent": not is_overdue and (a.due_date - datetime.utcnow()).days < 2,
            "is_overdue": is_overdue
        })
        
    stats = {
        "total_assignments": len(formatted),
        "submitted": sum(a["submitted"] for a in formatted),
        "pending": sum(a["total_students"] - a["submitted"] for a in formatted),
        "overdue": sum(1 for a in formatted if a["is_overdue"])
    }
    
    return templates.TemplateResponse("teacher/assignments.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "assignments": formatted,
        "stats": stats,
        "subjects": DEPARTMENTS,
        "classes": GRADE_LEVELS,
        "upcoming_deadlines": [a for a in formatted if not a["is_overdue"]][:3]
    })

@router.get("/teacher/assignments/{id}/edit")
async def teacher_edit_assignment(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = AssignmentRepository.get_by_id(db, id)
    if not assignment: raise HTTPException(status_code=404)
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/edit_assignment.html", {"request": request, "current_user": current_user, "teacher": current_user, "assignment": assignment, "courses": courses})

@router.post("/teacher/assignments/{id}/edit")
async def teacher_edit_assignment_post(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    assignment = AssignmentRepository.get_by_id(db, id)
    if not assignment: raise HTTPException(status_code=404)
    assignment.title = form_data.get("title")
    assignment.description = form_data.get("description")
    assignment.due_date = datetime.fromisoformat(form_data.get("due_date"))
    assignment.max_score = float(form_data.get("max_score", 100))
    db.commit()
    return RedirectResponse(url="/teacher/assignments?success=updated", status_code=303)

@router.get("/teacher/assignments/create")
async def teacher_create_assignment(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/create_assignment.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses})

@router.post("/teacher/assignments/create")
async def teacher_create_assignment_post(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    assignment_data = {"title": form_data.get("title"), "description": form_data.get("description"), "course_id": int(form_data.get("course_id")), "teacher_id": teacher.id, "due_date": datetime.fromisoformat(form_data.get("due_date")), "max_score": float(form_data.get("max_score", 100))}
    AssignmentRepository.create(db, assignment_data)
    return RedirectResponse(url="/teacher/assignments?success=1", status_code=303)

@router.get("/teacher/assignments/{id}/submissions")
async def teacher_view_submissions(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = AssignmentRepository.get_by_id(db, id)
    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")
    submissions = db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == id).all()
    return templates.TemplateResponse("teacher/view_submissions.html", {"request": request, "current_user": current_user, "teacher": current_user, "assignment": assignment, "submissions": submissions})

@router.post("/teacher/assignments/submissions/{submission_id}/grade")
async def teacher_grade_submission(submission_id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    form_data = await request.form()
    submission = db.query(AssignmentSubmission).get(submission_id)
    if not submission: raise HTTPException(status_code=404, detail="Submission not found")
    submission.score, submission.feedback, submission.graded_at = float(form_data.get("score")), form_data.get("feedback"), datetime.utcnow()
    db.commit()
    return RedirectResponse(url=f"/teacher/assignments/{submission.assignment_id}/submissions?success=1", status_code=303)

@router.delete("/teacher/assignments/delete/{id}")
async def teacher_delete_assignment(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = AssignmentRepository.get_by_id(db, id)
    if assignment: db.delete(assignment); db.commit()
    return JSONResponse(content={"message": "Assignment deleted successfully"})

@router.get("/teacher/notes/upload")
async def teacher_upload_notes(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/upload_notes.html", {"request": request, "current_user": current_user, "teacher": current_user, "courses": courses})

@router.post("/teacher/notes/upload")
async def teacher_upload_notes_post(request: Request, title: str = Form(...), course_id: int = Form(...), description: Optional[str] = Form(None), file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403)
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = f"/static/uploads/notes/{filename}"
    save_path = f"{file_path.lstrip('/')}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    NotesRepository.create(db, {"title": title, "description": description, "course_id": course_id, "teacher_id": teacher.id, "file_path": file_path, "file_type": ext.replace('.', '')})
    return RedirectResponse(url="/teacher/dashboard?success=1", status_code=303)

@router.get("/teacher/courses/{id}")
async def teacher_course_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = CourseRepository.get_by_id(db, id)
    if not course: raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse("teacher/course_detail.html", {"request": request, "current_user": current_user, "teacher": current_user, "course": course})

@router.get("/teacher/courses/{id}/students")
async def teacher_course_students(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = CourseRepository.get_by_id(db, id)
    students = CourseRepository.get_enrolled_students(db, id)
    formatted = []
    for s in students:
        formatted.append({
            "id": s.id,
            "name": s.user.full_name if s.user else "Unknown student",
            "email": s.user.email if s.user else "N/A",
            "grade": s.grade_level,
            "section": s.section,
            "attendance": 100,
            "average_grade": 0,
            "pending_assignments": 0,
            "avatar": f"https://ui-avatars.com/api/?name={s.user.full_name.replace(' ', '+') if s.user else 'User'}&background=random"
        })
    return templates.TemplateResponse("teacher/students.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "students": formatted,
        "filters": {
            "grade": course.grade_level if course else None,
            "section": course.section if course and hasattr(course, 'section') else None
        }
    })

@router.get("/teacher/attendance/take")
async def teacher_take_attendance(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/take_attendance.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": courses,
        "class_info": {
            "id": 0,
            "course_name": "Select a course",
            "grade": "",
            "section": "",
            "period": "",
            "time": "",
            "room": ""
        },
        "students": []
    })

@router.get("/teacher/attendance")
async def teacher_attendance_list(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    
    # Mock data to fulfill template expectations
    stats = {
        "total_students": 150,
        "present_today": 135,
        "absent_today": 10,
        "overall_percentage": 92
    }
    
    monthly_stats = {
        "present_percentage": 90,
        "absent_percentage": 7,
        "late_percentage": 3
    }
    
    return templates.TemplateResponse("teacher/attendance.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "courses": courses,
        "classes": GRADE_LEVELS,
        "subjects": DEPARTMENTS,
        "stats": stats,
        "current_month": datetime.now().strftime("%B %Y"),
        "monthly_overview": [],
        "monthly_stats": monthly_stats,
        "attendance_records": []
    })

@router.get("/teacher/attendance/{id}")
async def teacher_view_attendance(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = CourseRepository.get_by_id(db, id)
    return templates.TemplateResponse("teacher/attendance.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "course": course,
        "classes": GRADE_LEVELS,
        "subjects": DEPARTMENTS,
        "stats": {"total_students": 30, "present_today": 0, "absent_today": 0, "overall_percentage": 0},
        "current_month": datetime.now().strftime("%B %Y"),
        "monthly_overview": [],
        "monthly_stats": {"present_percentage": 0, "absent_percentage": 0, "late_percentage": 0},
        "attendance_records": []
    })

@router.get("/teacher/grades")
async def teacher_grades(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/grades.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": courses,
        "stats": {"average_grade": 85, "top_performers": 12, "failing_students": 2, "pending_grading": 5},
        "grades": []
    })

@router.get("/teacher/grades/add")
async def teacher_grades_add(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/add_grade.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": courses,
        "students": [],
        "assessments": []
    })

@router.post("/teacher/grades/add")
async def teacher_grades_add_post(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    # Logic to save grades
    return RedirectResponse(url="/teacher/grades?success=1", status_code=303)

@router.get("/teacher/attendance/{id}/edit")
async def teacher_edit_attendance(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/take_attendance.html", {"request": request, "current_user": current_user, "teacher": current_user, "students": []})

@router.get("/teacher/tests")
async def teacher_tests(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    tests_data = TestRepository.get_by_teacher(db, teacher.id) if teacher else []
    
    formatted = []
    for t in tests_data:
        total_students = 0 # Placeholder if no course link
        attempted = 0 # Placeholder
        is_overdue = t.end_time < datetime.utcnow()
        
        formatted.append({
            "id": t.id,
            "title": t.title,
            "subject": t.subject_name,
            "grade": t.grade_level,
            "class": t.grade_level,
            "section": t.target_section or "All",
            "start_time": t.start_time.strftime("%Y-%m-%d %H:%M"),
            "time_remaining": "Ended" if is_overdue else "Active",
            "duration": t.duration,
            "total_marks": t.total_points,
            "attempted": attempted,
            "total_students": total_students,
            "participation_rate": 0,
            "status": "completed" if is_overdue else "active",
            "status_color": "secondary" if is_overdue else "success",
            "is_important": False,
            "is_overdue": is_overdue
        })
        
    stats = {
        "total_tests": len(formatted),
        "active_tests": sum(1 for t in formatted if t["status"] == "active"),
        "completed_tests": sum(1 for t in formatted if t["status"] == "completed"),
        "upcoming_tests": 0
    }
    
    return templates.TemplateResponse("teacher/view_tests.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "tests": formatted,
        "stats": stats,
        "subjects": DEPARTMENTS,
        "classes": GRADE_LEVELS,
        "upcoming_tests": []
    })

@router.get("/teacher/tests/create")
async def teacher_create_test(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    return templates.TemplateResponse("teacher/create_test.html", {"request": request, "current_user": current_user, "teacher": current_user, "teacher_courses": teacher.courses if teacher else [], "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "sections": SECTIONS})

@router.get("/teacher/tests/{id}/results")
async def teacher_test_results(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    test = TestRepository.get_by_id(db, id)
    if not test: raise HTTPException(status_code=404)
    return templates.TemplateResponse("teacher/view_tests.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "test": test,
        "results": [],
        "tests": [], # fulfillment
        "stats": {"total_tests": 0, "active_tests": 0, "completed_tests": 0, "upcoming_tests": 0},
        "subjects": DEPARTMENTS,
        "classes": GRADE_LEVELS,
        "upcoming_tests": []
    })

@router.get("/teacher/tests/{id}/edit")
async def teacher_edit_test(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    test = TestRepository.get_by_id(db, id)
    if not test: raise HTTPException(status_code=404)
    return templates.TemplateResponse("teacher/edit_test.html", {"request": request, "current_user": current_user, "teacher": current_user, "test": test, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS, "sections": SECTIONS})

@router.post("/teacher/tests/create")
async def teacher_create_test_post(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    form_data = await request.form()
    # Simple creation for now - in reality this would parse complex question JSON
    test_data = {"title": form_data.get("title"), "subject_name": form_data.get("subject"), "grade_level": form_data.get("grade"), "teacher_id": teacher.id, "duration": int(form_data.get("duration", 60)), "start_time": datetime.fromisoformat(form_data.get("start_time")), "end_time": datetime.fromisoformat(form_data.get("end_time")), "total_points": float(form_data.get("total_marks", 100)), "target_section": form_data.get("section")}
    TestRepository.create(db, test_data, [])
    return RedirectResponse(url="/teacher/tests?success=1", status_code=303)

@router.delete("/teacher/tests/delete/{id}")
async def teacher_delete_test(id: int, db: Session = Depends(get_db)):
    test = TestRepository.get_by_id(db, id)
    if test: db.delete(test); db.commit()
    return JSONResponse(content={"message": "Test deleted successfully"})

@router.get("/teacher/videos/upload")
async def teacher_upload_videos(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    videos = VideosRepository.get_by_teacher(db, teacher.id) if teacher else []
    
    stats = {
        "total_videos": len(videos),
        "total_size": 0,
        "total_views": 0,
        "this_month": 0
    }
    
    return templates.TemplateResponse("teacher/upload_videos.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user, 
        "courses": courses, 
        "videos": videos, 
        "stats": stats,
        "storage": {"used": 0, "total": 10, "percentage": 0}
    })

@router.post("/teacher/videos/upload")
async def teacher_upload_videos_post(request: Request, title: str = Form(...), course_id: int = Form(...), description: Optional[str] = Form(None), video_file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher: raise HTTPException(status_code=403)
    ext = os.path.splitext(video_file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = f"/static/uploads/videos/{filename}"
    save_path = f"{file_path.lstrip('/')}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as buffer: shutil.copyfileobj(video_file.file, buffer)
    VideosRepository.create(db, {"title": title, "description": description, "course_id": course_id, "teacher_id": teacher.id, "file_path": file_path})
    return RedirectResponse(url="/teacher/dashboard?success=1", status_code=303)

@router.get("/teacher/courses")
async def teacher_courses(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses_data = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    
    formatted_courses = []
    for c in courses_data:
        formatted_courses.append({
            "id": c.id,
            "subject": c.course_name,
            "grade": c.grade_level,
            "code": c.course_code,
            "description": c.description,
            "color": "primary",
            "student_count": len(c.enrollments) if hasattr(c, 'enrollments') else 0,
            "schedule": "N/A",
            "progress": 0,
            "assignment_count": len(c.assignments) if hasattr(c, 'assignments') else 0,
            "video_count": 0,
            "note_count": 0
        })
        
    stats = {
        "total_courses": len(formatted_courses),
        "active_classes": len(formatted_courses),
        "total_students": sum(c["student_count"] for c in formatted_courses),
        "upcoming_classes": 0
    }
    
    return templates.TemplateResponse("teacher/courses.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": formatted_courses,
        "stats": stats,
        "subjects": DEPARTMENTS,
        "classes": GRADE_LEVELS,
        "todays_classes": []
    })

@router.get("/teacher/notices/create")
async def teacher_create_notice(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("teacher/create_notice.html", {"request": request, "current_user": current_user, "teacher": current_user, "subjects": DEPARTMENTS, "classes": GRADE_LEVELS})

@router.post("/teacher/notices/create")
async def teacher_create_notice_post(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    # Logic to create notice
    return RedirectResponse(url="/teacher/dashboard?success=notice_created", status_code=303)

@router.get("/teacher/groups")
async def teacher_groups(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("teacher/groups.html", {"request": request, "current_user": current_user, "teacher": current_user, "groups": []})

@router.get("/teacher/chat")
async def teacher_chat(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("teacher/chat.html", {"request": request, "current_user": current_user, "teacher": current_user, "contacts": [], "messages": []})

@router.get("/teacher/messages")
async def teacher_messages(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("teacher/messages.html", {"request": request, "current_user": current_user, "teacher": current_user, "messages": [], "unread_count": 0})

@router.get("/teacher/timetable")
async def teacher_timetable(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    time_slots = ["08:00", "09:00", "10:00", "11:00", "12:00", "01:00", "02:00"]
    
    # Mock data for week view
    week_days = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for d in days:
        week_days.append({
            "name": d,
            "date": "Jan 12", # placeholder
            "is_today": d == datetime.now().strftime("%A"),
            "classes": {slot: [] for slot in time_slots}
        })
    
    return templates.TemplateResponse("teacher/timetable.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "current_week": "Jan 12 - Jan 16, 2026",
        "prev_week": "prev",
        "next_week": "next",
        "week_days": week_days,
        "time_slots": time_slots,
        "todays_schedule": [],
        "upcoming_classes": [],
        "subjects": DEPARTMENTS,
        "classes": GRADE_LEVELS
    })

@router.get("/teacher/chat")
async def teacher_chat(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    parents = ChatRepository.get_teacher_parents(db, teacher.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id)
    
    all_students = []
    for course in courses:
        students = CourseRepository.get_enrolled_students(db, course.id)
        for s in students:
            unread = db.query(ChatMessage).filter(
                ChatMessage.sender_id == s.user_id,
                ChatMessage.receiver_id == current_user.id,
                ChatMessage.is_read == False
            ).count()
            all_students.append({
                "id": s.user_id,
                "name": s.user.full_name,
                "grade": s.grade_level,
                "section": s.section,
                "unread_count": unread
            })
    
    other_teachers = db.query(Teacher).filter(Teacher.id != teacher.id).all()
    formatted_teachers = []
    for t in other_teachers:
        unread = db.query(ChatMessage).filter(
            ChatMessage.sender_id == t.user_id,
            ChatMessage.receiver_id == current_user.id,
            ChatMessage.is_read == False
        ).count()
        formatted_teachers.append({
            "id": t.user_id,
            "name": t.user.full_name,
            "department": t.department,
            "unread_count": unread
        })

    formatted_parents = []
    for p in parents:
        student_names = ", ".join([s.user.full_name for s in p['parent'].children]) if hasattr(p['parent'], 'children') else "N/A"
        formatted_parents.append({
            "id": p['user'].id,
            "name": p['user'].full_name,
            "student_name": student_names,
            "unread_count": p['unread_count']
        })

    return templates.TemplateResponse("teacher/chat.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "students": all_students,
        "parents": formatted_parents,
        "teachers": formatted_teachers,
        "classes": [],
        "announcements": []
    })

@router.get("/teacher/grades")
async def teacher_grades(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    courses = CourseRepository.get_all(db, teacher_id=teacher.id) if teacher else []
    return templates.TemplateResponse("teacher/grades.html", {
        "request": request, 
        "current_user": current_user, 
        "teacher": current_user,
        "grades": [],
        "courses": courses
    })

# ------------------ PARENT PAGES ------------------
@router.get("/parent/dashboard")
async def parent_dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from models.models import Parent
    parent = db.query(Parent).filter(Parent.user_id == current_user.id).first()
    children = parent.children if parent else []
    return templates.TemplateResponse("parent/dashboard.html", {"request": request, "current_user": current_user, "user": current_user, "children": children})

@router.get("/parent/child/{id}/attendance")
async def parent_child_attendance(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("parent/attendance.html", {"request": request, "current_user": current_user})

@router.get("/parent/child/{id}/grades")
async def parent_child_grades(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("parent/grades.html", {"request": request, "current_user": current_user})

@router.get("/parent/child/{id}/homework")
async def parent_child_homework(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("parent/homework.html", {"request": request, "current_user": current_user})

@router.get("/parent/chat")
async def parent_chat(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("parent/chat.html", {"request": request, "current_user": current_user, "user": current_user})

@router.get("/parent/notices")
async def parent_notices(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("parent/notices.html", {"request": request, "current_user": current_user})

@router.get("/parent/profile")
async def parent_profile(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("parent/profile.html", {"request": request, "current_user": current_user})

# ------------------ AUTHORITY PAGES ------------------
@router.get("/authority/dashboard")
async def authority_dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from models.models import Student, Teacher, Course, Notice
    stats = {
        "total_students": db.query(Student).count(),
        "total_teachers": db.query(Teacher).count(),
        "total_courses": db.query(Course).count(),
        "active_notices": db.query(Notice).count()
    }
    return templates.TemplateResponse("authority/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "stats": stats
    })

@router.get("/authority/students")
async def authority_students(request: Request, grade: str = None, section: str = None, status: str = None, search: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    students = StudentRepository.get_all(db, grade_level=grade, section=section, status=status, search=search)
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
async def authority_teachers(request: Request, department: str = None, status: str = None, search: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teachers = TeacherRepository.get_all(db, department=department, status=status, search=search)
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
    
    # Mock department data
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
async def authority_courses(request: Request, search: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    courses = CourseRepository.search(db, search) if search else CourseRepository.get_all(db)
    formatted = []
    for c in courses:
        formatted.append({
            "id": c.id,
            "code": c.course_code,
            "course_code": c.course_code,
            "name": c.course_name,
            "course_name": c.course_name,
            "grade": c.grade_level if hasattr(c, 'grade_level') else "N/A",
            "instructor": c.teacher.user.full_name if c.teacher and c.teacher.user else "Unassigned",
            "instructor_id": c.teacher_id if c.teacher_id else None,
            "instructor_avatar": f"https://ui-avatars.com/api/?name={c.teacher.user.full_name if c.teacher and c.teacher.user else 'Unassigned'}&background=random",
            "student_count":len(c.enrollments) if hasattr(c, 'enrollments') else 0,
            "enrolled": len(c.enrollments) if hasattr(c, 'enrollments') else 0,
            "schedule": "Mon, Wed, Fri",
            "room": "Room 101",
            "status": "active"
        })
    return templates.TemplateResponse("authority/courses.html", {
        "request": request,
        "current_user": current_user,
        "courses": formatted,
        "search_query": search,
        "stats": {"total": len(formatted), "active": len(formatted)}
    })

@router.get("/authority/fees")
async def authority_fees(request: Request, search: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    fees = FeeRepository.search(db, search) if search else db.query(FeeRecord).all()
    summary = FeeRepository.get_all_fees_summary(db)
    
    formatted_fees = []
    for f in fees:
        formatted_fees.append({
            "id": f.id,
            "student_name": f.student.user.full_name if f.student and f.student.user else "N/A",
            "student_id": f.student.student_id if f.student else "N/A",
            "grade": f.student.grade_level if f.student else "N/A",
            "total_amount": f.total_amount if hasattr(f, 'total_amount') else 0,
            "paid_amount": f.paid_amount if hasattr(f, 'paid_amount') else 0,
            "balance": (f.total_amount - f.paid_amount) if hasattr(f, 'total_amount') and hasattr(f, 'paid_amount') else 0,
            "status": "paid" if hasattr(f, 'paid_amount') and f.paid_amount >= (f.total_amount if hasattr(f, 'total_amount') else 0) else "pending",
            "due_date": f.due_date.strftime("%Y-%m-%d") if hasattr(f, 'due_date') and f.due_date else "N/A",
            "payment_method": f.payment_method if hasattr(f, 'payment_method') else "N/A"
        })
    
    return templates.TemplateResponse("authority/fees.html", {
        "request": request,
        "current_user": current_user,
        "fee_records": formatted_fees,
        "total_collected": summary['total_paid'],
        "pending_amount": summary['total_pending'],
        "search_query": search
    })

@router.get("/authority/notices")
async def authority_notices(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notices = NoticeRepository.get_all(db)
    formatted_notices = []
    for n in notices:
        formatted_notices.append({
            "id": n.id,
            "title": n.title,
            "content": n.content if hasattr(n, 'content') else "",
            "date": n.created_at.strftime("%Y-%m-%d") if hasattr(n, 'created_at') and n.created_at else "N/A",
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(n, 'created_at') and n.created_at else "N/A",
            "author": "Admin",
            "target_role": n.target_role if hasattr(n, 'target_role') else "all",
            "priority": n.priority if hasattr(n, 'priority') else "normal",
            "status": "active"
        })
    return templates.TemplateResponse("authority/notices.html", {
        "request": request,
        "current_user": current_user,
        "notices": formatted_notices,
        "stats": {"total_notices": len(formatted_notices)}
    })

@router.get("/authority/analytics")
async def authority_analytics(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Basic data for charts
    return templates.TemplateResponse("authority/analytics_v2.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "grade_dist_data": [10, 20, 30, 40, 5],
        "att_labels": ["Grade 9", "Grade 10", "Grade 11", "Grade 12"],
        "att_data": [95, 92, 88, 90],
        "dept_labels": ["Math", "Science", "English"],
        "dept_data": [85, 82, 88],
        "trend_labels": ["Jan", "Feb", "Mar", "Apr"],
        "trend_data": [70, 75, 80, 85],
        "teacher_performance": [],
        "top_classes": [],
        "demographics_data": [60, 40]
    })

# Authority Student Management
@router.get("/authority/students/add")
async def authority_add_student_form(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("authority/add_student.html", {
        "request": request,
        "current_user": current_user,
        "grades": GRADE_LEVELS,
        "sections": SECTIONS
    })

@router.post("/authority/students/add")
async def authority_add_student(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    from models.models import User, Student
    user = User(
        full_name=form_data.get("full_name"),
        email=form_data.get("email"),
        role="student"
    )
    db.add(user)
    db.flush()
    
    student = Student(
        user_id=user.id,
        student_id=form_data.get("student_id"),
        grade_level=form_data.get("grade_level"),
        section=form_data.get("section"),
        phone=form_data.get("phone"),
        address=form_data.get("address")
    )
    db.add(student)
    db.commit()
    return RedirectResponse(url="/authority/students?success=added", status_code=303)

@router.get("/authority/students/{id}")
async def authority_student_detail(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/student_detail.html", {
        "request": request,
        "current_user": current_user,
        "student": student,
        "courses": student.enrollments if hasattr(student, 'enrollments') else []
    })

@router.get("/authority/students/{id}/edit")
async def authority_edit_student_form(request: Request, id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = StudentRepository.get_by_id(db, id)
    if not student: raise HTTPException(status_code=404)
    return templates.TemplateResponse("authority/edit_student.html", {
        "request": request,
        "current_user": current_user,
        "student": student,
        "grades": GRADE_LEVELS,
        "sections": SECTIONS
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

# Authority Teacher Management
@router.get("/authority/teachers/add")
async def authority_add_teacher_form(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("authority/add_teacher.html", {
        "request": request,
        "current_user": current_user,
        "departments": DEPARTMENTS
    })

@router.post("/authority/teachers/add")
async def authority_add_teacher(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    from models.models import User, Teacher
    user = User(
        full_name=form_data.get("full_name"),
        email=form_data.get("email"),
        role="teacher"
    )
    db.add(user)
    db.flush()
    
    teacher = Teacher(
        user_id=user.id,
        employee_id=form_data.get("employee_id"),
        department=form_data.get("department"),
        phone=form_data.get("phone")
    )
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

# Authority Course Management
@router.get("/authority/courses/add")
async def authority_add_course_form(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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
    students = CourseRepository.get_enrolled_students(db, id)
    return templates.TemplateResponse("authority/course_detail.html", {
        "request": request,
        "current_user": current_user,
        "course": course,
        "students": students
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
        "departments": DEPARTMENTS,
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

# Authority Notice Management
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
    return RedirectResponse(url=f"/authority/notices/{id}?success=updated", status_code=303)

# Authority Fee Management
@router.get("/authority/fees/add")
async def authority_add_fee_form(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    students = StudentRepository.get_all(db)
    return templates.TemplateResponse("authority/add_fee.html", {
        "request": request,
        "current_user": current_user,
        "students": students
    })

@router.post("/authority/fees/add")
async def authority_add_fee(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    form_data = await request.form()
    fee_data = {
        "student_id": int(form_data.get("student_id")),
        "amount": float(form_data.get("amount")),
        "payment_method": form_data.get("payment_method"),
        "transaction_id": form_data.get("transaction_id")
    }
    FeeRepository.create_payment(db, fee_data)
    return RedirectResponse(url="/authority/fees?success=added", status_code=303)

@router.get("/authority/fees/structure")
async def authority_fee_structure(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    structures = FeeStructureRepository.get_all(db)
    return templates.TemplateResponse("authority/fee_structure.html", {
        "request": request,
        "current_user": current_user,
        "fee_structures": structures,
        "grades": GRADE_LEVELS
    })

# Additional Authority Pages
@router.get("/authority/groups")
async def authority_groups(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("authority/groups.html", {
        "request": request,
        "current_user": current_user,
        "groups": []
    })

@router.get("/authority/reports")
async def authority_reports(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return templates.TemplateResponse("authority/reports.html", {
        "request": request,
        "current_user": current_user,
        "reports": []
    })
