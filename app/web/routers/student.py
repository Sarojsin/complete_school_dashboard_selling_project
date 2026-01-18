from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
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

# ------------------ STUDENT PAGES ------------------
@router.get("/student/dashboard")
async def student_dashboard(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    unread_count = await MessageRepository.get_unread_count(db, current_user.id)
    return templates.TemplateResponse("student/dashboard.html", {
        "request": request, "current_user": current_user, "student": current_user,
        "unread_count": unread_count, "assignments": [], "recent_grades": []
    })

@router.get("/student/profile")
async def student_profile(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
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
async def student_update_profile(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
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
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if student:
        if "full_name" in form_data: student.full_name = form_data["full_name"]
        if "phone" in form_data: student.phone = form_data["phone"]
        if "address" in form_data: student.address = form_data["address"]
        if "dob" in form_data and form_data["dob"]:
            try: student.date_of_birth = datetime.strptime(form_data["dob"], '%Y-%m-%d').date()
            except ValueError: pass
        db.add(student)
    db.add(current_user)
    await db.commit()
    return RedirectResponse(url="/student/profile?success=1", status_code=303)

@router.get("/student/courses")
async def student_courses(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/courses.html", {"request": request, "current_user": current_user, "student": current_user, "courses": []})

@router.get("/student/assignments")
async def student_assignments(request: Request, status: str = "all", current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    courses = await StudentRepository.get_enrolled_courses(db, student.id)
    course_ids = [c.id for c in courses]
    all_assignments = await AssignmentRepository.get_student_assignments(db, student.id, course_ids, student_grade=student.grade_level, student_section=student.section)
    stats = {"total": len(all_assignments), "pending": sum(1 for a in all_assignments if a["status"] == "pending"), "submitted": sum(1 for a in all_assignments if a["status"] == "submitted"), "graded": sum(1 for a in all_assignments if a["status"] == "graded"), "overdue": sum(1 for a in all_assignments if a["status"] == "overdue")}
    filtered = [a for a in all_assignments if status == "all" or a["status"] == status]
    return templates.TemplateResponse("student/assignments.html", {"request": request, "current_user": current_user, "student": current_user, "assignments": filtered, "stats": stats, "current_filter": status})

@router.get("/student/fees")
async def student_fees(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    fees = await FeeRepository.get_student_fees(db, student.id)
    summary = await FeeRepository.get_fee_summary(db, student.id)
    payment_history = await FeeRepository.get_payment_history(db, student.id)
    formatted_history = [{"date": p.payment_date, "amount": p.paid_amount, "method": "Online", "transaction_id": f"TXN-{p.id}", "status": "completed", "receipt_url": "#"} for p in payment_history]
    return templates.TemplateResponse("student/fees.html", {"request": request, "current_user": current_user, "student": current_user, "fee_structure": fees, "payment_history": formatted_history, "total_fees": summary['total_amount'], "paid_amount": summary['total_paid'], "pending_amount": summary['total_pending'], "fee_status": "paid" if summary['total_pending'] == 0 else "pending"})

@router.get("/student/assignments/{assignment_id}")
async def student_assignment_detail(request: Request, assignment_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    assignment = await AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")
    submission = await AssignmentRepository.get_submission_by_student(db, assignment_id, student.id)
    status = "pending"
    if submission: status = "graded" if submission.score is not None else "submitted"
    elif assignment.due_date < datetime.utcnow(): status = "overdue"
    assignment_data = {"id": assignment.id, "title": assignment.title, "description": assignment.description, "course": assignment.course.course_name if assignment.course else "Unknown Course", "teacher": assignment.teacher.user.full_name if assignment.teacher else "Unknown Teacher", "due_date": assignment.due_date, "max_score": assignment.max_score, "status": status, "submission": submission, "is_overdue": status == "overdue"}
    return templates.TemplateResponse("student/assignments_detail.html", {"request": request, "current_user": current_user, "assignment": assignment_data})

@router.post("/student/assignments/{assignment_id}/submit")
async def student_assignment_submit(assignment_id: int, request: Request, file: UploadFile = File(None), submission_text: str = Form(None), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: raise HTTPException(status_code=400, detail="Student profile not found")
    assignment = await AssignmentRepository.get_by_id(db, assignment_id)
    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")
    file_path = None
    if file and file.filename:
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = f"/static/uploads/assignments/{filename}"
        save_path = f"{file_path.lstrip('/')}"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    existing_submission = await AssignmentRepository.get_submission_by_student(db, assignment_id, student.id)
    if existing_submission:
        update_data = {"submission_text": submission_text if submission_text else existing_submission.submission_text, "submitted_at": datetime.utcnow()}
        if file_path: update_data["file_path"] = file_path
        await AssignmentRepository.update_submission(db, existing_submission, **update_data)
    else:
        submission_data = {"assignment_id": assignment_id, "student_id": student.id, "submission_text": submission_text, "file_path": file_path, "submitted_at": datetime.utcnow()}
        await AssignmentRepository.create_submission(db, submission_data)
    return RedirectResponse(url=f"/student/assignments", status_code=303)

@router.get("/student/tests")
async def student_test_list(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    tests = await TestRepository.get_available_tests_for_student(db, student.id, section=student.section, grade_level=student.grade_level) if student else []
    return templates.TemplateResponse("student/test_list.html", {"request": request, "current_user": current_user, "student": current_user, "tests": tests})

@router.get("/student/tests/{test_id}/start")
async def student_take_test(request: Request, test_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    test = await TestRepository.get_by_id(db, test_id)
    if not test: raise HTTPException(status_code=404, detail="Test not found")
    if not TestService.is_test_available(test): raise HTTPException(status_code=400, detail="Test is not currently available")
    if test.target_section and test.target_section != "All" and test.target_section != student.section: raise HTTPException(status_code=403, detail="This test is not assigned to your section")
    if test.grade_level and test.grade_level != student.grade_level: raise HTTPException(status_code=403, detail="This test is not for your grade level")
    if await TestService.has_student_submitted(db, test_id, student.id): return RedirectResponse(f"/student/tests/{test_id}/result")
    submission = await TestService.get_or_create_submission(db, test_id, student.id)
    return templates.TemplateResponse("student/take_test.html", {"request": request, "test": test, "submission": submission, "user_answers": submission.answers or {}})

@router.post("/student/tests/{test_id}/submit")
async def student_submit_test(request: Request, test_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: raise HTTPException(status_code=404, detail="Student profile not found")
    test = await TestRepository.get_by_id(db, test_id)
    if not test: raise HTTPException(status_code=404, detail="Test not found")
    submission = await TestRepository.get_submission(db, test_id, student.id)
    if not submission: raise HTTPException(status_code=400, detail="Test session not found")
    if submission.submitted_at: return RedirectResponse(f"/student/tests/{test_id}/result")
    form_data = await request.form()
    answers = {k.replace("question_", ""): v for k, v in form_data.items() if k.startswith("question_")}
    time_taken = (datetime.utcnow() - submission.started_at).total_seconds()
    submission = await TestRepository.update_submission(db, submission, answers=answers, submitted_at=datetime.utcnow(), time_taken=int(time_taken))
    await TestService.grade_submission(db, submission, test)
    return RedirectResponse(url=f"/student/tests/{test_id}/result", status_code=303)

@router.get("/student/tests/{test_id}/result")
async def student_test_result(request: Request, test_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    test = await TestRepository.get_by_id(db, test_id)
    if not test: raise HTTPException(status_code=404, detail="Test not found")
    submission = await TestRepository.get_submission(db, test_id, student.id)
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
async def student_notices(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    notices_data = await NoticeRepository.get_active_notices(db, target_role="students")
    notices = [{"id": n.id, "title": n.title, "content": n.content, "excerpt": n.content[:100] + "..." if len(n.content) > 100 else n.content, "priority": n.priority, "date": n.created_at.strftime('%Y-%m-%d'), "time": n.created_at.strftime('%H:%M'), "author": n.authority.full_name if n.authority else "School Authority"} for n in notices_data]
    return templates.TemplateResponse("student/notices.html", {"request": request, "current_user": current_user, "student": current_user, "notices": notices, "important_notices": [n for n in notices if n["priority"] in ["high", "urgent"]], "current_page": 1, "total_pages": 1})

@router.get("/student/timetable")
async def student_timetable(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/timetable.html", {"request": request, "current_user": current_user, "student": current_user, "timetable": [], "dates": []})

@router.get("/student/notes")
async def student_notes(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    notes = []
    if student:
        enrollments = await StudentRepository.get_enrolled_courses(db, student.id)
        if not enrollments and student.grade_level: enrollments = await CourseRepository.get_all(db, grade_level=student.grade_level)
        for cid in [c.id for c in enrollments]: notes.extend(await NotesRepository.get_by_course(db, cid))
    formatted_notes = [{"id": n.id, "title": n.title, "description": n.description or "", "subject": n.course.course_name if n.course else "Unknown", "teacher": n.teacher.full_name if n.teacher else "Unknown", "upload_date": n.uploaded_at.strftime("%Y-%m-%d"), "file_type": n.file_type or "file", "file_url": n.file_path} for n in notes]
    return templates.TemplateResponse("student/notes.html", {"request": request, "current_user": current_user, "student": current_user, "notes": formatted_notes, "stats": {"total_notes": len(formatted_notes), "total_subjects": len(list(set(n["subject"] for n in formatted_notes))), "total_downloads": 0, "recent_uploads": 0}, "subjects": list(set(n["subject"] for n in formatted_notes))})

@router.get("/student/videos")
async def student_videos(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    videos = []
    if student:
        enrollments = await StudentRepository.get_enrolled_courses(db, student.id)
        if not enrollments and student.grade_level: enrollments = await CourseRepository.get_all(db, grade_level=student.grade_level)
        for cid in [c.id for c in enrollments]: videos.extend(await VideosRepository.get_by_course(db, cid))
    formatted_videos = [{"id": v.id, "title": v.title, "description": v.description or "", "subject": v.course.course_name if v.course else "Unknown", "teacher": v.teacher.full_name if v.teacher else "Unknown", "upload_date": v.uploaded_at.strftime("%Y-%m-%d"), "video_url": v.file_path, "thumbnail": "https://via.placeholder.com/300x200?text=Video", "duration": f"{v.duration // 60}:{v.duration % 60:02d}" if v.duration else "0:00"} for v in videos]
    return templates.TemplateResponse("student/videos.html", {"request": request, "current_user": current_user, "student": current_user, "videos": formatted_videos, "progress_stats": {"total_watched": 0, "total_videos": len(formatted_videos), "completion_rate": 0, "total_time": "0h 0m", "by_subject": {}}, "subjects": list(set(v["subject"] for v in formatted_videos))})

@router.get("/student/forum")
async def student_forum(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/forum.html", {"request": request, "current_user": current_user, "student": current_user, "posts": []})

@router.get("/student/messages")
async def student_messages(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    messages = await MessageRepository.get_inbox(db, current_user.id)
    unread_count = await MessageRepository.get_unread_count(db, current_user.id)
    return templates.TemplateResponse("student/messages.html", {"request": request, "current_user": current_user, "student": current_user, "messages": messages, "unread_count": unread_count})

@router.post("/student/messages/{message_id}/read")
async def mark_message_read(message_id: int, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    if await MessageRepository.mark_as_read(db, message_id): return {"success": True}
    raise HTTPException(status_code=404, detail="Message not found")

@router.get("/student/teachers")
async def student_teachers(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    teachers = await TeacherRepository.get_all(db)
    return templates.TemplateResponse("student/teachers.html", {"request": request, "current_user": current_user, "student": current_user, "teachers": teachers})

@router.post("/student/teachers/{teacher_id}/contact")
async def student_contact_teacher(teacher_id: int, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    teacher = await TeacherRepository.get_by_id(db, teacher_id)
    if not teacher: raise HTTPException(status_code=404, detail="Teacher not found")
    await MessageRepository.create(db=db, sender_id=current_user.id, recipient_id=teacher.user_id, subject=form_data.get("subject"), body=form_data.get("message"))
    return {"message": "Message sent successfully"}

@router.get("/student/groups")
async def student_groups(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    from repositories.group_repository import GroupRepository
    from services.group_service import GroupService
    groups = await GroupService(GroupRepository(db)).get_user_groups(current_user.id, current_user.role)
    return templates.TemplateResponse("student/groups.html", {"request": request, "current_user": current_user, "groups": groups})

@router.get("/student/grades")
async def student_grades(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/grades.html", {"request": request, "current_user": current_user, "student": current_user, "grades": [], "gpa": 0.0})

@router.get("/student/attendance")
async def student_attendance(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/attendance.html", {"request": request, "current_user": current_user, "student": current_user, "attendance": []})
