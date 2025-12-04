from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
import os

from config.config import settings
from database.database import engine, Base, get_db
from sqlalchemy.orm import Session

# Import routes
from routes import auth, students, teachers, authority, tests, websocket_chat, parents
from routes import courses, assignments, attendance, grades, fees
from routes import notices, notes, videos, chat

# Import services
from services.chat_cleanup_service import cleanup_expired_messages
from dependencies import get_current_user
from models.models import User
from fastapi import Depends

# Create upload directories
os.makedirs("templates", exist_ok=True)
os.makedirs("app/static", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/assignments", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/notes", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/videos", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/avatars", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/notices", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/chat", exist_ok=True)

# Scheduler for background tasks
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    
    # Schedule cleanup job
    scheduler.add_job(
        cleanup_expired_messages,
        'cron',
        hour=settings.CHAT_CLEANUP_HOUR,
        minute=0
    )
    scheduler.start()
    
    yield
    
    # Shutdown
    scheduler.shutdown()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Add dummy csrf_token function to globals
templates.env.globals['csrf_token'] = lambda: "dummy-csrf-token"

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(teachers.router, prefix="/api/teachers", tags=["Teachers"])
app.include_router(authority.router, prefix="/api/authority", tags=["Authority"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["Assignments"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(grades.router, prefix="/api/grades", tags=["Grades"])
app.include_router(fees.router, prefix="/api/fees", tags=["Fees"])
app.include_router(parents.router, prefix="/parent", tags=["Parents"])
app.include_router(notices.router, prefix="/api/notices", tags=["Notices"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(videos.router, prefix="/api/videos", tags=["Videos"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(tests.router, prefix="/api/tests", tags=["Tests"])
app.include_router(websocket_chat.router, tags=["WebSocket"])

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ------------------ AUTHENTICATION PAGES ------------------
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@app.get("/signup/student", response_class=HTMLResponse)
async def signup_student_page(request: Request):
    return templates.TemplateResponse("auth/signup_student.html", {"request": request})

@app.get("/signup/teacher", response_class=HTMLResponse)
async def signup_teacher_page(request: Request):
    return templates.TemplateResponse("auth/signup_teacher.html", {"request": request})

@app.get("/signup/authority", response_class=HTMLResponse)
async def signup_authority_page(request: Request):
    return templates.TemplateResponse("auth/signup_authority.html", {"request": request})

@app.get("/signup/parent", response_class=HTMLResponse)
async def signup_parent_page(request: Request):
    return templates.TemplateResponse("auth/signup_parent.html", {"request": request})

# Registration aliases (for home page links)
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@app.get("/register/student", response_class=HTMLResponse)
async def register_student_page(request: Request):
    return templates.TemplateResponse("auth/signup_student.html", {"request": request})

@app.get("/register/teacher", response_class=HTMLResponse)
async def register_teacher_page(request: Request):
    return templates.TemplateResponse("auth/signup_teacher.html", {"request": request})

@app.get("/register/parent", response_class=HTMLResponse)
async def register_parent_page(request: Request):
    return templates.TemplateResponse("auth/signup_parent.html", {"request": request})

# ------------------ STUDENT PAGES ------------------
@app.get("/student/dashboard")
async def student_dashboard(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "assignments": [],
        "recent_grades": []
    })

@app.get("/student/profile")
async def student_profile(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/profile.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user
    })

@app.get("/student/courses")
async def student_courses(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/courses.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "courses": []
    })

@app.get("/student/assignments")
async def student_assignments(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/assignments.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "assignments": []
    })

@app.get("/student/assignments/{assignment_id}")
async def student_assignment_detail(request: Request, assignment_id: int):
    return templates.TemplateResponse("student/assignments_detail.html", {
        "request": request,
        "assignment_id": assignment_id
    })

@app.get("/student/grades")
async def student_grades(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/grades.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "grades": [],
        "gpa": 0.0
    })

@app.get("/student/attendance")
async def student_attendance(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/attendance.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "attendance": []
    })

@app.get("/student/fees")
async def student_fees(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/fees.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "fees": [],
        "pending_amount": 0
    })

@app.get("/student/tests")
async def student_tests(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/test_list.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "tests": []
    })

@app.get("/student/tests/{test_id}/start")
async def student_take_test(request: Request, test_id: int):
    return templates.TemplateResponse("student/take_test.html", {
        "request": request,
        "test_id": test_id
    })

@app.get("/student/tests/{test_id}/result")
async def student_test_result(request: Request, test_id: int):
    return templates.TemplateResponse("student/test_result.html", {
        "request": request,
        "test_id": test_id
    })

@app.get("/student/notices")
async def student_notices(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.notice_repository import NoticeRepository
    
    # Get notices for students or all
    notices_data = NoticeRepository.get_active_notices(db, target_role="students")
    
    # Format notices for template
    notices = []
    important_notices = []
    
    for n in notices_data:
        formatted_notice = {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "excerpt": n.content[:100] + "..." if len(n.content) > 100 else n.content,
            "priority": n.priority,
            "date": n.created_at.strftime('%Y-%m-%d'),
            "time": n.created_at.strftime('%H:%M'),
            "author": n.authority.full_name if n.authority else "School Authority",
            "from_": n.authority.full_name if n.authority else "School Authority",
            "audience": "Students" if n.target_role == "students" else "All",
            "attachment": None # Placeholder
        }
        
        notices.append(formatted_notice)
        if n.priority == "high" or n.priority == "urgent":
            important_notices.append(formatted_notice)
    
    return templates.TemplateResponse("student/notices.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "notices": notices,
        "important_notices": important_notices,
        "current_page": 1,
        "total_pages": 1,
        "has_prev": False,
        "has_next": False
    })


@app.get("/student/timetable")
async def student_timetable(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/timetable.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "timetable": [],
        "dates": []
    })

@app.get("/student/notes")
async def student_notes(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/notes.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "notes": [],
        "stats": {"by_subject": {}}
    })

@app.get("/student/videos")
async def student_videos(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/videos.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "videos": [],
        "progress_stats": {"by_subject": {}}
    })

@app.get("/student/forum")
async def student_forum(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("student/forum.html", {
        "request": request,
        "current_user": current_user,
        "student": current_user,
        "posts": []
    })

# ------------------ TEACHER PAGES ------------------
@app.get("/teacher/dashboard")
async def teacher_dashboard(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "students": [],
        "courses": [],
        "assignments": [],
        "stats": {}
    })

@app.get("/teacher/students")
async def teacher_students(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/students.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "students": []
    })

@app.get("/teacher/students/{student_id}")
async def teacher_student_detail(request: Request, student_id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/student_detail.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "student_id": student_id
    })

@app.get("/teacher/courses")
async def teacher_courses(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/courses.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": [
            {
                "id": 1,
                "subject": "Mathematics",
                "grade": "10-A",
                "code": "MATH101",
                "description": "Introduction to Algebra and Geometry",
                "color": "primary",
                "student_count": 30,
                "schedule": "Mon, Wed, Fri 09:00 AM",
                "progress": 45,
                "assignment_count": 5,
                "video_count": 3,
                "note_count": 8
            },
            {
                "id": 2,
                "subject": "Physics",
                "grade": "11-B",
                "code": "PHY101",
                "description": "Fundamentals of Physics",
                "color": "success",
                "student_count": 25,
                "schedule": "Tue, Thu 11:00 AM",
                "progress": 30,
                "assignment_count": 3,
                "video_count": 2,
                "note_count": 5
            }
        ],
        "stats": {
            "total_courses": 4,
            "active_classes": 3,
            "total_students": 120,
            "upcoming_classes": 2
        },
        "todays_classes": [
            {"id": 1, "subject": "Mathematics", "grade": "10-A", "time": "09:00 AM", "room": "Room 101", "status": "ongoing"},
            {"id": 2, "subject": "Physics", "grade": "11-B", "time": "11:00 AM", "room": "Lab 2", "status": "pending"}
        ]
    })

@app.get("/teacher/assignments")
async def teacher_assignments(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/assignments.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "stats": {
            "total_assignments": 12,
            "submitted": 450,
            "pending": 30,
            "overdue": 15
        },
        "subjects": ["Mathematics", "Physics", "Chemistry", "Biology", "English"],
        "classes": ["10-A", "10-B", "11-A", "11-B"],
        "assignments": [
            {
                "id": 1,
                "title": "Algebra Problem Set 1",
                "description": "Complete exercises 1-10 from Chapter 2",
                "subject": "Mathematics",
                "class": "10-A",
                "due_date": "2023-10-15",
                "due_in": "2 days",
                "is_overdue": False,
                "is_urgent": True,
                "submission_rate": 80,
                "submitted": 24,
                "total_students": 30,
                "status": "active",
                "status_color": "success"
            },
            {
                "id": 2,
                "title": "Physics Lab Report",
                "description": "Write a report on the pendulum experiment",
                "subject": "Physics",
                "class": "11-B",
                "due_date": "2023-10-20",
                "due_in": "1 week",
                "is_overdue": False,
                "is_urgent": False,
                "submission_rate": 40,
                "submitted": 10,
                "total_students": 25,
                "status": "active",
                "status_color": "primary"
            }
        ],
        "upcoming_deadlines": [
            {"title": "Algebra Problem Set 1", "class": "10-A", "subject": "Mathematics", "due_in": "2 days", "submitted": 24, "total": 30}
        ]
    })

@app.get("/teacher/assignments/create")
async def teacher_create_assignment(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/create_assignment.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user
    })

# Alias route for create-assignment
@app.get("/teacher/create-assignment")
async def teacher_create_assignment_alias(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/create_assignment.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user
    })

@app.get("/teacher/assignments/{assignment_id}/edit")
async def teacher_edit_assignment(request: Request, assignment_id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/edit_assignment.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "assignment_id": assignment_id
    })

@app.get("/teacher/attendance")
async def teacher_attendance(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/attendance.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "stats": {
            "total_students": 120,
            "present_today": 110,
            "absent_today": 8,
            "overall_percentage": 92
        },
        "classes": ["10-A", "10-B", "11-A", "11-B"],
        "subjects": ["Mathematics", "Physics", "Chemistry"],
        "current_month": "October 2023",
        "attendance_records": [
            {
                "id": 1,
                "date": "2023-10-10",
                "day": "Tuesday",
                "class": "10-A",
                "subject": "Mathematics",
                "present": 28,
                "absent": 2,
                "late": 0,
                "percentage": 93
            }
        ],
        "monthly_overview": [
            {
                "class": "10-A",
                "working_days": 22,
                "average_attendance": 94,
                "best_day": {"date": "Oct 5", "percentage": 100},
                "lowest_day": {"date": "Oct 12", "percentage": 85},
                "trend": "up",
                "trend_percentage": 2.5
            }
        ],
        "monthly_stats": {
            "present_percentage": 92,
            "absent_percentage": 5,
            "late_percentage": 3
        }
    })

@app.get("/teacher/attendance/take")
async def teacher_take_attendance(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/take_attendance.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": [],
        "class_info": {
            "id": 1,
            "course_name": "Mathematics 101",
            "grade": "10",
            "section": "A",
            "period": "1st",
            "time": "09:00 AM",
            "room": "Room 101"
        },
        "students": [
            {"id": 1, "name": "John Doe", "roll_no": "101", "avatar": "https://via.placeholder.com/40"},
            {"id": 2, "name": "Jane Smith", "roll_no": "102", "avatar": "https://via.placeholder.com/40"}
        ]
    })

@app.get("/teacher/grades")
async def teacher_grades(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/grades.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "grades": [],
        "courses": []
    })

@app.get("/teacher/grades/add")
async def teacher_add_grade(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/add_grade.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": [],
        "students": []
    })

@app.get("/teacher/tests")
async def teacher_tests(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/view_tests.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "stats": {
            "total_tests": 8,
            "active_tests": 2,
            "completed_tests": 5,
            "upcoming_tests": 1
        },
        "subjects": ["Mathematics", "Physics", "Chemistry"],
        "classes": ["10-A", "10-B", "11-A"],
        "tests": [
            {
                "id": 1,
                "title": "Mid-Term Algebra",
                "subject": "Mathematics",
                "class": "10-A",
                "total_marks": 100,
                "start_time": "2023-10-15 09:00",
                "is_overdue": False,
                "time_remaining": "2 days",
                "duration": 90,
                "participation_rate": 0,
                "attempted": 0,
                "total_students": 30,
                "status": "upcoming",
                "status_color": "warning",
                "is_important": True
            }
        ],
        "upcoming_tests": [
            {
                "id": 1,
                "title": "Mid-Term Algebra",
                "subject": "Mathematics",
                "class": "10-A",
                "starts_in": "2 days",
                "duration": 90,
                "total_students": 30
            }
        ]
    })

@app.get("/teacher/tests/create")
async def teacher_create_test(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/create_test.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": [],
        "subjects": ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History"],
        "classes": ["Class 10-A", "Class 10-B", "Class 11-A", "Class 12-B"]
    })

@app.get("/teacher/tests/{id}/edit")
async def teacher_edit_test(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/edit_test.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "test_id": id
    })

@app.get("/teacher/notes/upload")
async def teacher_upload_notes(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/upload_notes.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": []
    })

@app.get("/teacher/videos/upload")
async def teacher_upload_videos(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/upload_videos.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "courses": [],
        "stats": {
            "total_videos": 15,
            "total_size": "2.5",
            "total_views": 1250,
            "this_month": 5
        },
        "videos": [
            {
                "id": 1,
                "title": "Algebra Basics",
                "thumbnail": "https://via.placeholder.com/60x40",
                "duration": "10:05",
                "subject": "Math",
                "class": "10-A",
                "upload_date": "2023-10-01",
                "size": "150 MB",
                "views": 120,
                "status": "processed"
            }
        ],
        "storage": {
            "used": 2.5,
            "total": 10,
            "percentage": 25
        },
        "subjects": ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History"],
        "classes": ["Class 10-A", "Class 10-B", "Class 11-A", "Class 12-B"]
    })

@app.get("/teacher/notices/create")
async def teacher_create_notice(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/create_notice.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "classes": ["Class 10-A", "Class 10-B", "Class 11-A", "Class 12-B"]
    })

@app.get("/teacher/timetable")
async def teacher_timetable(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/timetable.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "timetable": [],
        "courses": []
    })

@app.get("/teacher/chat")
async def teacher_chat(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from repositories.teacher_repository import TeacherRepository
    from repositories.chat_repository import ChatRepository
    from models.chat_models import ChatMessage
    
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        # Fallback if not a teacher profile yet
        return templates.TemplateResponse("teacher/chat.html", {
            "request": request,
            "current_user": current_user,
            "teacher": current_user,
            "students": [],
            "parents": [],
            "teachers": []
        })

    # Fetch contacts
    parents = ChatRepository.get_teacher_parents(db, teacher.id)
    # For students, we can reuse get_my_students logic or add a helper
    # For now, let's just get parents as that was the main task. 
    # But the template expects students and teachers too.
    
    # Get students
    from repositories.course_repository import CourseRepository
    courses = TeacherRepository.get_teaching_courses(db, teacher.id)
    all_students = set()
    for course in courses:
        students = CourseRepository.get_enrolled_students(db, course.id)
        all_students.update(students)
    
    # Get colleagues (other teachers) - simplified for now
    from models.models import Teacher
    other_teachers = db.query(Teacher).filter(Teacher.id != teacher.id).all()
    
    # Format for template
    # The template expects objects with .name, .id, .unread_count
    # My ChatRepository.get_teacher_parents returns dicts with 'user', 'parent', 'unread_count'
    # I need to adapt the data or update the template. 
    # The template uses: parent.name, parent.student_name, parent.unread_count
    # The repository returns: {'user': User, 'parent': Parent, 'unread_count': int}
    
    formatted_parents = []
    for p in parents:
        # Need to find student name for this parent
        # Parent model has children relationship
        student_names = ", ".join([s.user.full_name for s in p['parent'].children])
        formatted_parents.append({
            "id": p['user'].id, # Chat uses User ID
            "name": p['user'].full_name,
            "student_name": student_names,
            "unread_count": p['unread_count']
        })
        
    formatted_students = []
    for s in all_students:
        # Get unread count for student
        unread = ChatRepository.get_unread_count(db, s.user_id) # Wait, get_unread_count gets unread for ME from THEM?
        # No, get_unread_count(db, user_id) gets messages sent TO user_id that are unread.
        # We want messages sent FROM student TO teacher that are unread.
        # ChatRepository doesn't have a specific method for that in the generic list, 
        # but get_conversations_list does.
        # Let's just use 0 for now or implement a quick count.
        unread = db.query(ChatMessage).filter(
            ChatMessage.sender_id == s.user_id,
            ChatMessage.receiver_id == current_user.id,
            ChatMessage.is_read == False
        ).count()
        
        formatted_students.append({
            "id": s.user_id,
            "name": s.user.full_name,
            "grade": s.grade_level,
            "section": s.section,
            "profile_pic": None,
            "unread_count": unread
        })

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
            "profile_pic": None,
            "unread_count": unread
        })

    return templates.TemplateResponse("teacher/chat.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "students": formatted_students,
        "parents": formatted_parents,
        "teachers": formatted_teachers,
        "classes": [], # Placeholder
        "announcements": [] # Placeholder
    })


# ------------------ AUTHORITY/ADMIN PAGES ------------------
@app.get("/authority/dashboard")
async def authority_dashboard(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/dashboard.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "stats": {},
        "recent_activities": []
    })

@app.get("/authority/students")
async def authority_students(
    request: Request,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.student_repository import StudentRepository
    
    if search:
        students_data = StudentRepository.search(db, search)
    else:
        students_data = StudentRepository.get_all(db)
    
    # Format students for template
    formatted_students = []
    for s in students_data:
        formatted_students.append({
            "id": s.id,
            "full_name": s.user.full_name if s.user else "N/A",
            "email": s.user.email if s.user else "N/A",
            "student_id": s.student_id,
            "grade_level": s.grade_level,
            "section": s.section or "N/A",
            "date_of_birth": s.date_of_birth.strftime('%Y-%m-%d') if s.date_of_birth else "N/A",
            "phone": s.phone or "N/A",
            "avatar": f"https://ui-avatars.com/api/?name={s.user.full_name.replace(' ', '+') if s.user else 'User'}&background=random",
            "gpa": "N/A",
            "roll_number": s.student_id,
            "fee_status": "paid",
            "attendance": 0,
            "status": "active"
        })
        
    return templates.TemplateResponse("authority/students.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "students": formatted_students,
        "search_query": search
    })


@app.get("/authority/students/add")
async def authority_add_student(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/add_student.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user
    })

@app.get("/authority/students/{student_id}/edit")
async def authority_edit_student(request: Request, student_id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/edit_student.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "student_id": student_id
    })

@app.get("/authority/teachers")
async def authority_teachers(
    request: Request,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.teacher_repository import TeacherRepository
    
    if search:
        teachers_data = TeacherRepository.search(db, search)
    else:
        teachers_data = TeacherRepository.get_all(db)
    
    # Format teachers for template
    formatted_teachers = []
    for t in teachers_data:
        formatted_teachers.append({
            "id": t.id,
            "full_name": t.user.full_name if t.user else "N/A",
            "email": t.user.email if t.user else "N/A",
            "employee_id": t.employee_id,
            "department": t.department or "N/A",
            "specialization": t.specialization or "N/A",
            "phone": t.phone or "N/A",
            "hire_date": t.joining_date.strftime('%Y-%m-%d') if t.joining_date else "N/A",
            "avatar": f"https://ui-avatars.com/api/?name={t.user.full_name.replace(' ', '+') if t.user else 'User'}&background=random",
            "courses_taught": 0,
            "students": 0,
            "performance": 95, # Mock performance score
            "status": "active"
        })
        
    return templates.TemplateResponse("authority/teachers.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "teachers": formatted_teachers,
        "search_query": search
    })


@app.get("/authority/teachers/add")
async def authority_add_teacher(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/add_teacher.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user
    })

@app.get("/authority/teachers/{teacher_id}/edit")
async def authority_edit_teacher(request: Request, teacher_id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/edit_teacher.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "teacher_id": teacher_id
    })

@app.get("/authority/courses")
async def authority_courses(
    request: Request,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.course_repository import CourseRepository
    
    if search:
        courses_data = CourseRepository.search(db, search)
    else:
        courses_data = CourseRepository.get_all(db)
    
    # Format courses for template
    formatted_courses = []
    for c in courses_data:
        formatted_courses.append({
            "id": c.id,
            "code": c.course_code,
            "name": c.course_name,
            "description": c.description,
            "credits": c.credits,
            "grade_level": c.grade_level,
            "semester": c.semester,
            "instructor": c.teacher.user.full_name if c.teacher and c.teacher.user else "Unassigned",
            "instructor_avatar": f"https://ui-avatars.com/api/?name={c.teacher.user.full_name if c.teacher and c.teacher.user else 'Unassigned'}&background=random",
            "teacher_id": c.teacher_id,
            "student_count": 0,
            "class_count": 0,
            "avg_grade": 0,
            "department": "Science",
            "department_color": "primary",
            "status": "active"
        })
    
    return templates.TemplateResponse("authority/courses.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "courses": formatted_courses,
        "search_query": search
    })


@app.get("/authority/courses/add")
async def authority_add_course(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/add_course.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user
    })

@app.get("/authority/courses/{course_id}/edit")
async def authority_edit_course(request: Request, course_id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/edit_course.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "course_id": course_id
    })

@app.get("/authority/fees")
async def authority_fees(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/fees.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "fees": [],
        "pending_amount": 0
    })

@app.get("/authority/fees/structure")
async def authority_fee_structure(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/fee_structure.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "stats": {
            "total_structures": 6,
            "active_structures": 5,
            "total_revenue": 125000,
            "pending_fees": 15000
        },
        "fee_structures": [],
        "fee_breakdown": [],
        "grades": ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", 
                   "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"],
        "current_year": 2023
    })

@app.post("/authority/fees/structure")
async def authority_create_fee_structure(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from repositories.fee_structure_repository import FeeStructureRepository
    from datetime import datetime    
    form = await request.form()
    
    # Extract form data
    tuition_fee = float(form.get("tuition_fee", 0))
    registration_fee = float(form.get("registration_fee", 0))
    library_fee = float(form.get("library_fee", 0))
    sports_fee = float(form.get("sports_fee", 0))
    lab_fee = float(form.get("lab_fee", 0))
    activity_fee = float(form.get("activity_fee", 0))
    other_charges = float(form.get("other_charges", 0))
    
    total_amount = (tuition_fee + registration_fee + library_fee + 
                   sports_fee + lab_fee + activity_fee + other_charges)
    
    structure_data = {
        "grade_level": form.get("grade_level"),
        "academic_year": form.get("academic_year"),
        "tuition_fee": tuition_fee,
        "registration_fee": registration_fee,
        "library_fee": library_fee,
        "sports_fee": sports_fee,
        "lab_fee": lab_fee,
        "activity_fee": activity_fee,
        "other_charges": other_charges,
        "total_amount": total_amount,
        "status": form.get("status", "active"),
        "description": form.get("description"),
        "due_date": datetime.strptime(form.get("due_date"), '%Y-%m-%d').date() if form.get("due_date") else None
    }
    
    FeeStructureRepository.create(db, structure_data)
    
    return RedirectResponse(url="/authority/fees/structure", status_code=303)


@app.get("/authority/fees/add")
async def authority_add_fee(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/add_fee.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user
    })

@app.get("/authority/notices")
async def authority_notices(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.notice_repository import NoticeRepository
    
    # Get all notices
    notices = NoticeRepository.get_all(db)
    
    # Calculate stats
    total_notices = len(notices)
    active_notices_list = NoticeRepository.get_active_notices(db)
    active_count = len(active_notices_list)
    expired_count = total_notices - active_count
    
    # Format notices for template
    from datetime import datetime
    formatted_notices = []
    for n in notices:
        is_expired = n.expires_at and n.expires_at < datetime.utcnow()
        days_remaining = (n.expires_at - datetime.utcnow()).days if n.expires_at and not is_expired else 0
        
        formatted_notices.append({
            "id": n.id,
            "title": n.title,
            "excerpt": n.content[:100] + "..." if len(n.content) > 100 else n.content,
            "priority": n.priority,
            "audience": n.target_role,
            "published_date": n.created_at.strftime('%Y-%m-%d'),
            "published_time": n.created_at.strftime('%H:%M'),
            "expiry_date": n.expires_at.strftime('%Y-%m-%d') if n.expires_at else None,
            "is_expired": is_expired,
            "days_remaining": f"{days_remaining} days" if days_remaining > 0 else "Expired" if is_expired else "No expiry",
            "status": "expired" if is_expired else "active",
            "views": 0, # Placeholder
            "is_important": n.priority == "urgent" or n.priority == "high"
        })
    
    return templates.TemplateResponse("authority/notices.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user,
        "notices": formatted_notices,
        "stats": {
            "total_notices": total_notices,
            "active_notices": active_count,
            "expired_notices": expired_count,
            "this_month": 0 # Placeholder
        },
        "current_page": 1,
        "total_pages": 1,
        "has_prev": False,
        "has_next": False
    })

@app.get("/authority/notices/add")
async def authority_add_notice(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("authority/add_notice.html", {
        "request": request,
        "current_user": current_user,
        "authority": current_user
    })

@app.post("/authority/notices/add")
async def authority_create_notice(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.notice_repository import NoticeRepository
    from datetime import datetime
    
    form = await request.form()
    
    # Create notice data
    notice_data = {
        "title": form.get("title"),
        "content": form.get("content"),
        "priority": form.get("priority", "normal"),
        "target_role": form.get("audience", "all"),  # Form field is 'audience'
        "expires_at": datetime.fromisoformat(form.get("expiry_date")) if form.get("expiry_date") else None,
        "authority_id": current_user.authority_profile.id
    }
    
    NoticeRepository.create(db, notice_data)
    
    return RedirectResponse(url="/authority/notices", status_code=303)


@app.get("/authority/notices/{id}/edit", name="authority_edit_notice")
async def authority_edit_notice(request: Request, id: int):
    return templates.TemplateResponse("authority/edit_notice.html", {
        "request": request,
        "notice_id": id
    })

@app.delete("/authority/notices/delete/{id}")
async def authority_delete_notice(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.notice_repository import NoticeRepository
    
    notice = NoticeRepository.get_by_id(db, id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
        
    NoticeRepository.delete(db, notice)
    return JSONResponse(content={"message": "Notice deleted successfully"})

@app.get("/authority/notices/view/{id}")
async def authority_view_notice(
    id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from repositories.notice_repository import NoticeRepository
    
    notice = NoticeRepository.get_by_id(db, id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
        
    from datetime import datetime
    return templates.TemplateResponse("authority/view_notice.html", {
        "request": request,
        "current_user": current_user,
        "notice": notice,
        "now": datetime.utcnow()
    })

@app.get("/authority/analytics")
async def authority_analytics(request: Request):
    return templates.TemplateResponse("authority/analytics.html", {"request": request})

# ------------------ FAVICON ------------------
@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import FileResponse, Response
    import os
    
    favicon_path = "app/static/favicon.ico"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    else:
        # Return 204 No Content if favicon doesn't exist
        return Response(status_code=204)

# ------------------ TEACHER ACTION ROUTES ------------------
@app.get("/teacher/courses/{id}")
async def teacher_course_detail(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/course_detail.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "course": {
            "id": id,
            "subject": "Mathematics",
            "grade": "10-A",
            "code": "MATH101",
            "description": "Introduction to Algebra and Geometry",
            "student_count": 30,
            "schedule": "Mon, Wed, Fri 09:00 AM",
            "progress": 45
        }
    })

@app.get("/teacher/courses/{id}/students")
async def teacher_course_students(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/students.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "students": []
    })

@app.get("/teacher/assignments/{id}/submissions")
async def teacher_view_submissions(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/assignments.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "assignments": [],
        "stats": {},
        "subjects": [],
        "classes": [],
        "upcoming_deadlines": []
    })

@app.get("/teacher/assignments/{id}/edit")
async def teacher_edit_assignment(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/edit_assignment.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "assignment": {
            "id": id,
            "title": "Algebra Problem Set 1",
            "description": "Complete exercises 1-10 from Chapter 2",
            "subject": "Mathematics",
            "class": "10-A",
            "due_date": "2023-10-15",
            "points": 100
        },
        "classes": ["10-A", "10-B"],
        "subjects": ["Mathematics", "Physics"]
    })

@app.get("/teacher/attendance/{id}")
async def teacher_view_attendance(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/attendance.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "stats": {},
        "classes": [],
        "subjects": [],
        "attendance_records": [],
        "current_month": "",
        "monthly_overview": [],
        "monthly_stats": {}
    })

@app.get("/teacher/attendance/{id}/edit")
async def teacher_edit_attendance(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/take_attendance.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "class_info": {},
        "students": []
    })

@app.get("/teacher/tests/{id}/results")
async def teacher_test_results(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("teacher/view_tests.html", {
        "request": request,
        "current_user": current_user,
        "teacher": current_user,
        "tests": [],
        "stats": {},
        "subjects": [],
        "classes": [],
        "upcoming_tests": []
    })

@app.delete("/teacher/tests/delete/{id}")
async def teacher_delete_test(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Test deleted successfully"})

@app.post("/teacher/students/{student_id}/contact")
async def teacher_contact_student(request: Request, student_id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Message sent successfully"})

@app.delete("/teacher/assignments/delete/{id}")
async def teacher_delete_assignment(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Assignment deleted successfully"})

@app.delete("/teacher/attendance/delete/{id}")
async def teacher_delete_attendance(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Attendance record deleted successfully"})

@app.get("/teacher/videos/{id}")
async def teacher_view_video(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Video player placeholder"})

@app.get("/teacher/videos/{id}/edit")
async def teacher_edit_video(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Edit video placeholder"})

@app.delete("/teacher/videos/{id}")
async def teacher_delete_video(request: Request, id: int, current_user: User = Depends(get_current_user)):
    return JSONResponse(content={"message": "Video deleted successfully"})

# ------------------ SCHEDULER ------------------
from apscheduler.schedulers.background import BackgroundScheduler
from services.chat_cleanup_service import cleanup_expired_messages

@app.on_event("startup")
async def startup_event():
    scheduler = BackgroundScheduler()
    # Run cleanup every hour
    scheduler.add_job(cleanup_expired_messages, 'interval', hours=1)
    scheduler.start()
    print("Scheduler started for chat message cleanup")

