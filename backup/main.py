from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

from backup.core.config import settings
from backup.core.database import engine, ensure_admin_tables
from backup.middleware.security import SecurityHeadersMiddleware
from backup.middleware.csrf import CSRFMiddleware
from backup.middleware.metrics import MetricsMiddleware
from backup.web.routers.common import router as common_router
from backup.web.routers.student import router as student_router
from backup.web.routers.teacher import router as teacher_router
from backup.web.routers.parent import router as parent_router
from backup.web.routers.authority import router as authority_router
from backup.web.routers.groups import router as groups_router
from backup.web.routers.group_posts import router as group_posts_router
from backup.websocket.router import router as ws_router
from backup.services.chat_cleanup_service import cleanup_expired_messages

# =====================================================
# TEST: New Modular Router (Plan 13 - Router Wiring)
# =====================================================
# This is a test to verify the new modular system works
# We'll test with school.teacher module first
from modules.auth.api import router as auth_router
from modules.super_admin.api import router as super_admin_router
from backup.modules.school.teacher import router as school_teacher_router
from backup.modules.school.authority import router as school_authority_router
from backup.modules.school.student import router as school_student_router
from backup.modules.school.parent import router as school_parent_router
from backup.modules.school.library import router as school_library_router
from backup.modules.school.exam_section import router as school_exam_section_router
from backup.modules.school.account_section import router as school_account_section_router

# College Modules (Elite Plan 4)
from backup.modules.college.faculty import router as college_faculty_router
from backup.modules.college.student import router as college_student_router
from backup.modules.college.hod import router as college_hod_router
from backup.modules.college.dean import router as college_dean_router
from backup.modules.college.registrar import router as college_registrar_router
from backup.modules.college.exam_section import router as college_exam_section_router
from backup.modules.college.account_section import router as college_account_section_router
from backup.modules.college.placement import router as college_placement_router
from backup.modules.college.research import router as college_research_router
from backup.modules.college.hostel import router as college_hostel_router
from backup.modules.college.lab import router as college_lab_router
from backup.modules.college.program import router as college_program_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize scheduler
    ensure_admin_tables()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(cleanup_expired_messages, 'interval', hours=1)
    from backup.services.admin_backup_service import AdminBackupService
    scheduler.add_job(
        AdminBackupService.run_scheduled_backup_job,
        "interval",
        minutes=1,
        id="auto_backup",
        coalesce=True,
        max_instances=1,
    )
    scheduler.start()
    app.state.scheduler = scheduler
    print("Scheduler started for chat message cleanup")
    yield
    # Shutdown: Clean up scheduler
    scheduler.shutdown()
    print("Scheduler shut down")

def create_app() -> FastAPI:
    app = FastAPI(
        title="School Management System",
        description="A modularized, production-ready school management system.",
        version="1.0.0",
        lifespan=lifespan
    )
    
    from backup.core.templates import templates
    app.state.templates = templates

    # 1. Security & CSRF Middleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CSRFMiddleware)
    app.add_middleware(MetricsMiddleware)

    # 2. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 3. Session Middleware (MUST BE OUTERMOST for CSRF to access request.session)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        session_cookie="school_session",
        https_only=not settings.DEBUG,
    )

    # Static files mounting
    # Make sure static directories exist
    os.makedirs("app/static/uploads/avatars", exist_ok=True)
    os.makedirs("app/static/uploads/assignments", exist_ok=True)
    os.makedirs("app/static/uploads/notes", exist_ok=True)
    os.makedirs("app/static/uploads/videos", exist_ok=True)
    
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.mount("/media", StaticFiles(directory="app/media"), name="media")

    # Exception Handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == 401:
            # Redirect to login if it's a web request (not an API request)
            if not request.url.path.startswith("/api/"):
                return RedirectResponse(url="/login")
        
        # Default behavior for other exceptions or API 401s
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    # Domain Exception Handlers (Layered Architecture Support)
    from fastapi.responses import JSONResponse
    from backup.core.exceptions import (
        NotFoundError, ValidationError, ForbiddenError,
        UnauthorizedError, ConflictError
    )

    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(status_code=400, content={"detail": exc.message})

    @app.exception_handler(ForbiddenError)
    async def forbidden_exception_handler(request: Request, exc: ForbiddenError):
        return JSONResponse(status_code=403, content={"detail": exc.message})

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
        # Allow same redirect behavior for domain unauthorized errors
        if not request.url.path.startswith("/api/"):
            return RedirectResponse(url="/login")
        return JSONResponse(status_code=401, content={"detail": exc.message})

    @app.exception_handler(ConflictError)
    async def conflict_exception_handler(request: Request, exc: ConflictError):
        return JSONResponse(status_code=409, content={"detail": exc.message})

    # Include Web Routes
    app.include_router(common_router)
    app.include_router(student_router)
    app.include_router(teacher_router)
    app.include_router(parent_router)
    app.include_router(authority_router)
    app.include_router(groups_router)
    app.include_router(group_posts_router)
    app.include_router(ws_router)

    # Include API Routes (Legacy and New)
    # These are relocated from the root 'routes' folder
    from backup.api.endpoints import auth, students, teachers, authority, tests, parents
    from backup.api.endpoints import courses, assignments, attendance, grades, fees
    from backup.api.endpoints import notices, notes, videos, chat
    from backup.api.endpoints import groups, group_posts

    app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(students.router, prefix="/api/students", tags=["Students"])
    app.include_router(teachers.router, prefix="/api/teachers", tags=["Teachers"])
    app.include_router(authority.router, prefix="/api/authority", tags=["Authority"])
    app.include_router(tests.router, prefix="/api/tests", tags=["Tests"])
    app.include_router(parents.router, prefix="/api/parents", tags=["Parents"])
    app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
    app.include_router(assignments.router, prefix="/api/assignments", tags=["Assignments"])
    app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
    app.include_router(grades.router, prefix="/api/grades", tags=["Grades"])
    app.include_router(fees.router, prefix="/api/fees", tags=["Fees"])
    app.include_router(notices.router, prefix="/api/notices", tags=["Notices"])
    app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
    app.include_router(videos.router, prefix="/api/videos", tags=["Videos"])
    app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
    app.include_router(groups.router, prefix="/api/groups", tags=["Groups"])
    app.include_router(group_posts.router, prefix="/api/group-posts", tags=["Group Posts"])


    # Add these imports
    from backup.api.endpoints import hod, exam_section, library, account
    from backup.api.endpoints import admin_features, admin_dashboard
    from backup.web.routers import hod as web_hod, exam_section as web_exam_section, library as web_library, account as web_account
    from backup.web.routers import admin as web_admin

    # Register API routes
    app.include_router(hod.router)
    app.include_router(exam_section.router)
    app.include_router(library.router)
    app.include_router(account.router)
    
    # Register Admin Feature routes
    app.include_router(admin_features.router, prefix="/api/admin", tags=["Admin Features"])
    app.include_router(admin_dashboard.router, prefix="/api", tags=["Admin Dashboard"])
    
    # Register Admin User Management routes
    from backup.api.endpoints import admin_users
    app.include_router(admin_users.router, prefix="/api", tags=["Admin Users"])
    
    # Register Admin Academic routes
    from backup.api.endpoints import admin_academic
    app.include_router(admin_academic.router, prefix="/api", tags=["Admin Academic"])
    
    # Register Admin Exam routes
    from backup.api.endpoints import admin_exams
    app.include_router(admin_exams.router, prefix="/api", tags=["Admin Exams"])
    
    # Register Admin Finance routes
    from backup.api.endpoints import admin_finance
    app.include_router(admin_finance.router, prefix="/api", tags=["Admin Finance"])
    
    # Register Admin Notices routes
    from backup.api.endpoints import admin_notices
    app.include_router(admin_notices.router, prefix="/api", tags=["Admin Notices"])
    
    # Register Admin Messages routes
    from backup.api.endpoints import admin_messages
    app.include_router(admin_messages.router, prefix="/api", tags=["Admin Messages"])
    
    # Register Admin Media routes
    from backup.api.endpoints import admin_media
    app.include_router(admin_media.router, prefix="/api", tags=["Admin Media"])
    
    # Register Admin System Monitoring routes
    from backup.api.endpoints import admin_system
    app.include_router(admin_system.router, prefix="/api", tags=["Admin System"])
    
    # Register Admin Security routes
    from backup.api.endpoints import admin_security
    app.include_router(admin_security.router, prefix="/api", tags=["Admin Security"])
    
    # Register Admin Backup routes
    from backup.api.endpoints import admin_backup
    app.include_router(admin_backup.router, prefix="/api", tags=["Admin Backup"])
    
    # Register Admin Reports routes
    from backup.api.endpoints import admin_reports
    app.include_router(admin_reports.router, prefix="/api", tags=["Admin Reports"])
    
    # Register Admin Settings routes
    from backup.api.endpoints import admin_settings
    app.include_router(admin_settings.router, prefix="/api", tags=["Admin Settings"])
    
    # Register Admin Advanced routes
    from backup.api.endpoints import admin_advanced
    app.include_router(admin_advanced.router, prefix="/api", tags=["Admin Advanced"])

    # =====================================================
    # NEW: API v1 Routes (School vs College Separation)
    # =====================================================
    from backup.api.v1 import api_router as v1_router
    app.include_router(v1_router, prefix="/api/v1", tags=["API v1"])

    # =====================================================
    # NEW: Modular Routes - Migrated from v2 to v1 (Elite Plan 5 Cutover)
    # =====================================================
    
    # Auth Module (Elite Plan 6)
    app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
    
    # Super Admin Module (Elite Plan 7)
    app.include_router(super_admin_router, prefix="/api/v1", tags=["Super Admin"])
    
    # Feature Modules (Elite Plan 8)
    from modules.chat.api import router as chat_router
    from modules.groups.api import router as groups_router
    from modules.notices.api import router as notices_router
    app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
    app.include_router(groups_router, prefix="/api/v1", tags=["Groups"])
    app.include_router(notices_router, prefix="/api/v1", tags=["Notices"])
    
    # School Modules
    app.include_router(
        school_teacher_router,
        prefix="/api/v1/school",
        tags=["School Teachers"]
    )
    app.include_router(
        school_authority_router,
        prefix="/api/v1/school",
        tags=["School Authority"]
    )
    app.include_router(
        school_student_router,
        prefix="/api/v1/school",
        tags=["School Student"]
    )
    app.include_router(
        school_parent_router,
        prefix="/api/v1/school",
        tags=["School Parent"]
    )
    app.include_router(
        school_library_router,
        prefix="/api/v1/school",
        tags=["School Library"]
    )
    app.include_router(
        school_exam_section_router,
        prefix="/api/v1/school",
        tags=["School Exam"]
    )
    app.include_router(
        school_account_section_router,
        prefix="/api/v1/school",
        tags=["School Account"]
    )

    # College Modules (Elite Plan 4)
    app.include_router(college_faculty_router, prefix="/api/v1/college", tags=["College Faculty"])
    app.include_router(college_student_router, prefix="/api/v1/college", tags=["College Student"])
    app.include_router(college_hod_router, prefix="/api/v1/college", tags=["College HOD"])
    app.include_router(college_dean_router, prefix="/api/v1/college", tags=["College Dean"])
    app.include_router(college_registrar_router, prefix="/api/v1/college", tags=["College Registrar"])
    app.include_router(college_exam_section_router, prefix="/api/v1/college", tags=["College Exam Section"])
    app.include_router(college_account_section_router, prefix="/api/v1/college", tags=["College Account Section"])
    app.include_router(college_placement_router, prefix="/api/v1/college", tags=["College Placement"])
    app.include_router(college_research_router, prefix="/api/v1/college", tags=["College Research"])
    app.include_router(college_hostel_router, prefix="/api/v1/college", tags=["College Hostel"])
    app.include_router(college_lab_router, prefix="/api/v1/college", tags=["College Lab"])
    app.include_router(college_program_router, prefix="/api/v1/college", tags=["College Program"])

    # Register web routes
    app.include_router(web_hod.router, prefix="/hod", tags=["HOD Web"])
    app.include_router(web_exam_section.router, prefix="/exam-section", tags=["Exam Section Web"])
    app.include_router(web_library.router, prefix="/library", tags=["Library Web"])
    app.include_router(web_account.router, prefix="/account", tags=["Account Web"])
    app.include_router(web_admin.router, prefix="/admin", tags=["Admin Web"])
    return app


app = create_app()
 
