from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from typing import Optional, List
import os
import shutil
import uuid
from datetime import datetime

from backup.core.database import get_async_db
from backup.core.templates import templates
from backup.dependencies.auth import get_current_user
from backup.models.models import User, Student, Teacher, Assignment, AssignmentSubmission, Course, FeeRecord, Notice, Attendance, Grade, Note, Video
from backup.models.chat_models import ChatMessage
from backup.models.group_models import Group, GroupMember
from backup.repositories.student_repository import StudentRepository
from backup.repositories.teacher_repository import TeacherRepository
from backup.repositories.message_repository import MessageRepository
from backup.repositories.notice_repository import NoticeRepository
from backup.repositories.course_repository import CourseRepository
from backup.repositories.assignment_repository import AssignmentRepository
from backup.repositories.notes_repository import NotesRepository
from backup.repositories.videos_repository import VideosRepository
from backup.repositories.test_repository import TestRepository
from backup.repositories.fee_repository import FeeRepository
from backup.repositories.fee_structure_repository import FeeStructureRepository
from backup.repositories.chat_repository import ChatRepository
from backup.repositories.group_repository import GroupRepository
from backup.services.student_service import StudentService
from backup.services.group_service import GroupService
from backup.services.test_service import TestService
from backup.utils.constants import GRADE_LEVELS, DEPARTMENTS, SECTIONS, WEEKDAYS

router = APIRouter()

# ------------------ STUDENT PAGES ------------------
@router.get("/student/dashboard")
async def student_dashboard(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    data = await StudentService.get_dashboard_data(db, current_user.id)
    if not data:
        return RedirectResponse("/login")
        
    unread_count = await MessageRepository.get_unread_count(db, current_user.id)
    
    from datetime import date
    
    return templates.TemplateResponse("student/dashboard.html", {
        "request": request, 
        "current_user": current_user, 
        "student": data["student"], 
        "courses": data["courses"], 
        "assignments": data["assignments"], 
        "recent_grades": data["recent_grades"], 
        "stats": data["stats"], 
        "latest_notice": data["latest_notice"],
        "attendance_overview": data["attendance_overview"],
        "attendance_grid": data["attendance_grid"],
        "days_labels": data["days_labels"],
        "unread_count": unread_count,
        "library_stats": data["library_stats"],
        "today": date.today()
    })

@router.get("/student/profile")
async def student_profile(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        return RedirectResponse("/student/dashboard")
        
    student_data = {
        "name": current_user.full_name, "id": student.student_id,
        "grade": student.grade_level, "section": student.section,
        "email": current_user.email, "phone": student.phone,
        "dob": student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else "",
        "address": student.address, "profile_pic": current_user.profile_picture or "/static/images/default-avatar.png",
        "roll_number": student.student_id, "admission_date": student.enrollment_date.strftime('%Y-%m-%d') if student.enrollment_date else "N/A"
    }
    return templates.TemplateResponse("student/profile.html", {"request": request, "current_user": current_user, "student": student_data})

@router.post("/student/profile")
async def student_update_profile(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        return RedirectResponse("/student/dashboard")
    
    avatar_file = form_data.get("profile_pic") if "profile_pic" in form_data and form_data["profile_pic"].filename else None
    
    await StudentService.update_profile(
        db=db,
        student_id=student.id,
        full_name=form_data.get("full_name"),
        email=form_data.get("email"),
        phone=form_data.get("phone"),
        address=form_data.get("address"),
        dob_str=form_data.get("dob"), # Pass dob as string for service to parse
        avatar_file=avatar_file,
        user=current_user # Pass current_user to update its fields
    )
    return RedirectResponse(url="/student/profile", status_code=303)

@router.get("/student/courses")
async def student_courses(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: return RedirectResponse("/student/dashboard")
    
    courses = await StudentService.get_student_courses_detailed(db, student.id)
    
    return templates.TemplateResponse("student/courses.html", {
        "request": request, 
        "current_user": current_user, 
        "student": current_user, 
        "current_courses": courses,
        "completed_courses": []
    })

@router.get("/student/assignments")
async def student_assignments(request: Request, status: str = "all", current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        return RedirectResponse("/student/dashboard")
        
    assignments_data = await StudentService.get_assignments_data(db, student.id, status)
    
    return templates.TemplateResponse("student/assignments.html", {
        "request": request, 
        "current_user": current_user, 
        "student": current_user, 
        "assignments": assignments_data["filtered_assignments"], 
        "stats": assignments_data["stats"], 
        "current_filter": status
    })

@router.get("/student/fees")
async def student_fees(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: 
        return RedirectResponse("/student/dashboard")
        
    data = await StudentService.get_fee_summary(db, student.id)
    
    return templates.TemplateResponse("student/fees.html", {
        "request": request, 
        "current_user": current_user, 
        "student": current_user, 
        "fee_structure": data["fee_structure"], 
        "payment_history": data["payment_history"], 
        "total_fees": data["total_fees"], 
        "paid_amount": data["paid_amount"], 
        "pending_amount": data["pending_amount"], 
        "fee_status": data["fee_status"]
    })

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
async def student_notices(
    request: Request, 
    category: Optional[str] = Query("all"),
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_async_db)
):
    from sqlalchemy.orm import joinedload
    from backup.models.models import Notice, Authority, Teacher
    from backup.models.exam_models import ExamNotice
    
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    grade = student.grade_level if student else None
    
    # 1. Fetch General Notices
    query_general = select(Notice).options(
        joinedload(Notice.authority).joinedload(Authority.user),
        joinedload(Notice.teacher).joinedload(Teacher.user)
    ).filter(
        or_(Notice.expires_at.is_(None), Notice.expires_at >= datetime.utcnow())
    )
    
    if grade:
        query_general = query_general.filter(
            or_(
                Notice.target_role == 'all',
                and_(Notice.target_role == 'student', or_(Notice.target_grade == grade, Notice.target_grade.is_(None)))
            )
        )
    else:
        query_general = query_general.filter(or_(Notice.target_role == 'student', Notice.target_role == 'all'))
        
    res_general = await db.execute(query_general)
    general_notices = res_general.scalars().unique().all()
    
    # 2. Fetch Exam Notices
    query_exam = select(ExamNotice).options(
        joinedload(ExamNotice.creator)
    )
    res_exam = await db.execute(query_exam)
    exam_notices = res_exam.scalars().all()
    
    # 3. Unify and Categorize
    all_notices = []
    
    # Process General Notices
    for n in general_notices:
        cat = "Authority"
        author_name = "School Office"
        
        if n.teacher:
            cat = "Teacher"
            author_name = n.teacher.user.full_name
        elif n.authority:
            author_name = n.authority.user.full_name
            dept = (n.authority.department or "").lower()
            if "library" in dept: cat = "Library"
            elif "account" in dept: cat = "Account"
            elif "hod" in dept: cat = "HOD"
            elif "exam" in dept: cat = "Exam"
            
        all_notices.append({
            "id": f"gen_{n.id}",
            "title": n.title,
            "content": n.content,
            "category": cat,
            "priority": n.priority,
            "author": author_name,
            "date": n.created_at.strftime('%Y-%m-%d'),
            "time": n.created_at.strftime('%H:%M'),
            "raw_date": n.created_at
        })
        
    # Process Exam Notices
    for n in exam_notices:
        all_notices.append({
            "id": f"exam_{n.id}",
            "title": n.title,
            "content": n.content,
            "category": "Exam",
            "priority": "normal",
            "author": n.creator.full_name if n.creator else "Exam Section",
            "date": n.created_at.strftime('%Y-%m-%d'),
            "time": n.created_at.strftime('%H:%M'),
            "raw_date": n.created_at
        })
        
    # 4. Sort by Date
    all_notices.sort(key=lambda x: x["raw_date"], reverse=True)
    
    # 5. Apply Category Filter
    if category and category != "all":
        all_notices = [n for n in all_notices if n["category"].lower() == category.lower()]
        
    # 6. Pagination (simple slice for combined list)
    per_page = 10
    total_items = len(all_notices)
    total_pages = (total_items + per_page - 1) // per_page if total_items > 0 else 1
    start = (page - 1) * per_page
    end = start + per_page
    paginated_notices = all_notices[start:end]
    
    important_notices = [n for n in all_notices if n["priority"] in ["high", "urgent"]][:3]
    
    return templates.TemplateResponse("student/notices.html", {
        "request": request, 
        "current_user": current_user, 
        "student": current_user, 
        "notices": paginated_notices, 
        "important_notices": important_notices,
        "current_page": page,
        "total_pages": total_pages,
        "current_category": category,
        "categories": ["All", "Exam", "Library", "Account", "HOD", "Teacher", "Authority"]
    })

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
    watched_ids = []
    if student:
        watched_ids = await VideosRepository.get_student_watched_ids(db, student.id)
        enrollments = await StudentRepository.get_enrolled_courses(db, student.id)
        if not enrollments and student.grade_level: enrollments = await CourseRepository.get_all(db, grade_level=student.grade_level)
        for cid in [c.id for c in enrollments]: videos.extend(await VideosRepository.get_by_course(db, cid))
    
    formatted_videos = [{
        "id": v.id, 
        "title": v.title, 
        "description": v.description or "", 
        "subject": v.course.course_name if v.course else "Unknown", 
        "teacher": v.teacher.user.full_name if v.teacher and v.teacher.user else "Unknown", 
        "upload_date": v.uploaded_at.strftime("%Y-%m-%d"), 
        "video_url": v.file_path, 
        "thumbnail": "https://via.placeholder.com/300x200?text=Video", 
        "duration": f"{v.duration // 60}:{v.duration % 60:02d}" if v.duration else "0:00",
        "watched": v.id in watched_ids
    } for v in videos]
    
    total_watched = len(watched_ids)
    total_videos = len(formatted_videos)
    completion_rate = round((total_watched / total_videos * 100)) if total_videos > 0 else 0
    
    return templates.TemplateResponse("student/videos.html", {
        "request": request, 
        "current_user": current_user, 
        "student": current_user, 
        "videos": formatted_videos, 
        "progress_stats": {
            "total_watched": total_watched, 
            "total_videos": total_videos, 
            "completion_rate": completion_rate, 
            "total_time": "0h 0m", 
            "by_subject": {}
        }, 
        "subjects": list(set(v["subject"] for v in formatted_videos))
    })

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
    from backup.repositories.group_repository import GroupRepository
    from backup.services.group_service import GroupService
    groups = await GroupService(GroupRepository(db)).get_user_groups(current_user.id, current_user.role)
    return templates.TemplateResponse("student/groups.html", {"request": request, "current_user": current_user, "groups": groups})

@router.get("/student/grades")
async def student_grades(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        return RedirectResponse("/student/dashboard")
        
    grades_data = await StudentService.get_grades_data(db, student.id)
    return templates.TemplateResponse("student/grades.html", {
        "request": request, 
        "current_user": current_user, 
        "student": current_user, 
        "grades": grades_data["grades"], 
        "gpa": grades_data["gpa"],
        "stats": grades_data["stats"]
    })

@router.get("/student/attendance")
async def student_attendance(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        return RedirectResponse("/student/dashboard")
        
    data = await StudentService.get_attendance_data(db, student.id)
    return templates.TemplateResponse("student/attendance.html", {
        "request": request, 
        "current_user": current_user, 
        "student": current_user, 
        "stats": data
    })

@router.post("/student/mark-video-watched/{video_id}")
async def mark_video_watched(video_id: int, db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)):
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student: raise HTTPException(status_code=404, detail="Student not found")
    await VideosRepository.mark_as_watched(db, video_id, student.id)
    return {"success": True}

@router.get("/student/groups")
async def student_groups(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    data = await group_service.get_groups_list(current_user.id)
    return templates.TemplateResponse("student/groups.html", {
        "request": request, 
        "current_user": current_user, 
        "groups": data["user_groups"]
    })

@router.get("/student/groups/{group_id}")
async def student_group_detail(request: Request, group_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
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
        "is_teacher": False
    })

@router.post("/student/groups/join")
async def student_join_group(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    form_data = await request.form()
    code = form_data.get("code")
    group_repo = GroupRepository(db)
    group_service = GroupService(group_repo)
    
    # Needs a method to join by code
    res = await db.execute(select(Group).filter(Group.code == code, Group.is_active == True))
    group = res.scalars().first()
    if not group:
        return RedirectResponse(url="/student/groups?error=invalid_code", status_code=303)
        
    # Check if already member
    res_m = await db.execute(select(GroupMember).filter(GroupMember.group_id == group.id, GroupMember.user_id == current_user.id))
    if res_m.scalars().first():
        return RedirectResponse(url=f"/student/groups/{group.id}", status_code=303)
        
    member = GroupMember(group_id=group.id, user_id=current_user.id, role="student")
    db.add(member); await db.commit()
    return RedirectResponse(url=f"/student/groups/{group.id}?success=joined", status_code=303)

@router.get("/student/groups/{group_id}/posts")
async def student_group_posts(
    request: Request,
    group_id: int,
    post_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    from backup.repositories.group_post_repository import GroupPostRepository
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
        "is_teacher": False,
        "post_types": ["notice", "note", "link"]
    })

@router.get("/student/groups/{group_id}/posts/{post_id}")
async def student_view_post(
    request: Request,
    group_id: int,
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    from backup.repositories.group_post_repository import GroupPostRepository
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
        "is_teacher": False,
        "is_author": post.author_id == current_user.id
    })

# ------------------ EXAM RESULTS & LIBRARY VIEWS ------------------

@router.get("/student/exam-results")
async def student_exam_results(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    """Student view of their own exam results"""
    from sqlalchemy.orm import joinedload
    from backup.models.exam_models import ExamResult
    
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        return RedirectResponse("/student/dashboard")
    
    # Get student's exam results with course eager loaded
    result = await db.execute(
        select(ExamResult)
        .options(joinedload(ExamResult.course))
        .where(ExamResult.student_id == student.id)
        .order_by(ExamResult.semester.desc(), ExamResult.published_at.desc())
    )
    exam_results = result.scalars().all()
    
    return templates.TemplateResponse("student/exam_results.html", {
        "request": request,
        "current_user": current_user,
        "student": student,
        "exam_results": exam_results
    })

@router.get("/student/library")
async def student_library(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    """Student view of their borrowed books and library status"""
    from datetime import date
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        return RedirectResponse("/student/dashboard")
    
    # Get student's book loans
    from backup.models.library_models import BookLoan
    result = await db.execute(
        select(BookLoan)
        .where(BookLoan.student_id == student.id)
        .order_by(BookLoan.taken_date.desc())
    )
    book_loans = result.scalars().all()
    
    # Calculate total fines
    total_fines = sum(loan.fine_amount for loan in book_loans if loan.fine_amount > 0)
    
    # Separate active and returned loans
    active_loans = [loan for loan in book_loans if loan.status == 'borrowed']
    returned_loans = [loan for loan in book_loans if loan.status == 'returned']
    
    # Calculate currently borrowed count
    currently_borrowed = len(active_loans)
    
    # Calculate overdue count
    today = date.today()
    overdue_count = sum(1 for loan in active_loans if loan.due_date and loan.due_date < today)
    
    return templates.TemplateResponse("student/library.html", {
        "request": request,
        "current_user": current_user,
        "student": student,
        "book_loans": book_loans,
        "active_loans": active_loans,
        "returned_loans": returned_loans,
        "total_fines": total_fines,
        "currently_borrowed": currently_borrowed,
        "overdue_count": overdue_count,
        "today": today
    })
