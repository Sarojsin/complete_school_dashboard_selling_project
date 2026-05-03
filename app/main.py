from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os

from modules.shared.config import settings
from modules.shared.exceptions import (
    NotFoundError, ValidationError, ForbiddenError, 
    UnauthorizedError, ConflictError
)
from modules.auth.router import router as auth_router
from modules.school.school_teacher.router import router as teacher_router
from modules.school.school_student.router import router as student_router
from modules.school.school_parent.router import router as parent_router
from modules.school.school_authority.router import router as authority_router
from modules.school.school_account_section.router import router as account_section_router
from modules.school.school_library.router import router as library_router
from modules.school.school_exam_section.router import router as exam_section_router
from modules.school.school_attendance.router import router as attendance_router
from modules.school.school_courses.router import router as courses_router
from modules.school.school_assignments.router import router as assignments_router
from modules.school.school_tests.router import router as tests_router
from modules.school.school_notices.router import router as notices_router
from modules.school.school_grades.router import router as grades_router
from modules.school.school_notes.router import router as notes_router
from modules.school.school_videos.router import router as videos_router
from modules.school.school_hod.router import router as hod_router
from modules.school.school_groups.router import router as groups_router
from modules.school.school_chat.router import router as chat_router
from modules.school.school_timetable.router import router as timetable_router
from modules.school.school_dashboard.router import router as dashboard_router
from modules.super_admin.api import router as super_admin_router

# College Modules
from modules.college.college_faculty.router import router as college_faculty_router
from modules.college.college_student.router import router as college_student_router
from modules.college.college_hod.api import router as college_hod_router
from modules.college.college_dean.api import router as college_dean_router
from modules.college.college_registrar.api import router as college_registrar_router
from modules.college.college_exam_section.api import router as college_exam_section_router
from modules.college.college_account_section.api import router as college_account_section_router
from modules.college.college_placement.router import router as college_placement_router
from modules.college.college_research.router import router as college_research_router
from modules.college.college_hostel.api import router as college_hostel_router
from modules.college.college_lab.router import router as college_lab_router
from modules.college.college_programs.api import router as college_programs_router
from modules.college.college_courses.api import router as college_courses_router
from modules.college.college_enrollments.api import router as college_enrollments_router
from modules.college.college_semesters.api import router as college_semesters_router
from modules.college.college_library.api import router as college_library_router


# Ensure all models are imported so they register with Base.metadata
from modules.shared import models as shared_models
from modules.school.school_teacher import models as teacher_models
from modules.school.school_parent import models as parent_models  # MUST come before student
from modules.school.school_student import models as student_models
from modules.school.school_authority import models as authority_models
from modules.school.school_classes import models as class_models
from modules.school.school_subjects import models as subject_models
from modules.school.school_courses import models as course_models
from modules.school.school_assignments import models as assignment_models
from modules.school.school_notes import models as note_models
from modules.school.school_attendance import models as attendance_models

# College Models
from modules.college.college_courses import models as college_course_models
from modules.college.college_student import models as college_student_models
from modules.college.college_faculty import models as college_faculty_models
from modules.college.college_library import models as college_library_models
from modules.college.college_hostel import models as college_hostel_models
from modules.school.school_exam_section import models as exam_models
from modules.school.school_timetable import models as timetable_models
from modules.school.school_videos import models as video_models
from modules.school.school_account_section import models as account_models
from modules.school.school_library import models as library_models
from modules.school.school_groups import models as group_models
from modules.school.school_chat import models as chat_models
from modules.school.school_notices import models as notice_models
from modules.school.school_grades import models as grade_models
from modules.school.school_tests import models as test_models
from modules.school.school_dashboard import models as dashboard_models

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.is_debug,
    version="1.0.0"
)

# CORS Middleware - Configure appropriately for production
# Get allowed origins from settings, default to common dev origins if not set
_allowed_origins = getattr(settings, 'ALLOWED_ORIGINS', None)
if not _allowed_origins:
    # Default to common localhost origins for development
    _allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    ]
    # In production, this should be explicitly set in environment variables
    if os.getenv("ENVIRONMENT") == "production":
        _allowed_origins = ["https://your-production-domain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

# Custom Exception Handlers
@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": exc.message})

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": exc.message})

@app.exception_handler(ForbiddenError)
async def forbidden_exception_handler(request, exc):
    return JSONResponse(status_code=403, content={"detail": exc.message})

@app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request, exc):
    return JSONResponse(status_code=401, content={"detail": exc.message})

@app.exception_handler(ConflictError)
async def conflict_exception_handler(request, exc):
    return JSONResponse(status_code=409, content={"detail": exc.message})

# Include Routers
app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(teacher_router, prefix="/api/v1/school")
app.include_router(student_router, prefix="/api/v1/school")
app.include_router(parent_router, prefix="/api/v1/school")
app.include_router(authority_router, prefix="/api/v1/school")
app.include_router(account_section_router, prefix="/api/v1/school")
app.include_router(library_router, prefix="/api/v1/school")
app.include_router(exam_section_router, prefix="/api/v1/school")
app.include_router(attendance_router, prefix="/api/v1/school")
app.include_router(courses_router, prefix="/api/v1/school")
app.include_router(assignments_router, prefix="/api/v1/school")
app.include_router(tests_router, prefix="/api/v1/school")
app.include_router(notices_router, prefix="/api/v1/school")
app.include_router(grades_router, prefix="/api/v1/school")
app.include_router(notes_router, prefix="/api/v1/school")
app.include_router(videos_router, prefix="/api/v1/school")
app.include_router(hod_router, prefix="/api/v1/school")
app.include_router(groups_router, prefix="/api/v1/school")
app.include_router(chat_router, prefix="/api/v1/school")
app.include_router(timetable_router, prefix="/api/v1/school")
app.include_router(dashboard_router, prefix="/api/v1/school")
app.include_router(super_admin_router)

# College Routers
app.include_router(college_faculty_router, prefix="/api/v1/college")
app.include_router(college_student_router, prefix="/api/v1/college")
app.include_router(college_hod_router, prefix="/api/v1/college")
app.include_router(college_dean_router, prefix="/api/v1/college")
app.include_router(college_registrar_router, prefix="/api/v1/college")
app.include_router(college_exam_section_router, prefix="/api/v1/college")
app.include_router(college_account_section_router, prefix="/api/v1/college")
app.include_router(college_placement_router, prefix="/api/v1/college")
app.include_router(college_research_router, prefix="/api/v1/college")
app.include_router(college_hostel_router, prefix="/api/v1/college")
app.include_router(college_lab_router, prefix="/api/v1/college")
app.include_router(college_programs_router, prefix="/api/v1/college")
app.include_router(college_courses_router, prefix="/api/v1/college")
app.include_router(college_enrollments_router, prefix="/api/v1/college")
app.include_router(college_semesters_router, prefix="/api/v1/college")
app.include_router(college_library_router, prefix="/api/v1/college")



# WebSocket Endpoint
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket chat endpoint"""
    from modules.web_common.websocket import websocket_chat as ws_handler
    user_id = 0  # In production, get from token
    await ws_handler(websocket, user_id)


@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy", 
        "app": settings.APP_NAME,
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.get("/health/ready")
async def readiness_check():
    """Readiness check - includes database connectivity"""
    from modules.shared.database import engine
    from sqlalchemy import text
    
    try:
        # Test database connectivity using sync approach for simplicity
        # This works with both sync and async engines
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
        return JSONResponse(
            status_code=503,
            content={
                "status": "not ready",
                "database": db_status,
                "app": settings.APP_NAME
            }
        )
    
    return {
        "status": "ready",
        "database": db_status,
        "app": settings.APP_NAME
    }


@app.get("/health/live")
async def liveness_check():
    """Liveness check - simple ping"""
    return {"status": "alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
