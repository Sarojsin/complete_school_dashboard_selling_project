from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

from app.core.config import settings
from app.core.database import engine, ensure_admin_tables
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.csrf import CSRFMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.web.routers.common import router as common_router
from app.web.routers.student import router as student_router
from app.web.routers.teacher import router as teacher_router
from app.web.routers.parent import router as parent_router
from app.web.routers.authority import router as authority_router
from app.web.routers.groups import router as groups_router
from app.web.routers.group_posts import router as group_posts_router
from app.websocket.router import router as ws_router
from app.services.chat_cleanup_service import cleanup_expired_messages

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize scheduler
    ensure_admin_tables()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(cleanup_expired_messages, 'interval', hours=1)
    from app.services.admin_backup_service import AdminBackupService
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
    
    from app.core.templates import templates
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
    from app.core.exceptions import (
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
    from app.api.endpoints import auth, students, teachers, authority, tests, parents
    from app.api.endpoints import courses, assignments, attendance, grades, fees
    from app.api.endpoints import notices, notes, videos, chat
    from app.api.endpoints import groups, group_posts

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
    from app.api.endpoints import hod, exam_section, library, account
    from app.api.endpoints import admin_features, admin_dashboard
    from app.web.routers import hod as web_hod, exam_section as web_exam_section, library as web_library, account as web_account
    from app.web.routers import admin as web_admin

    # Register API routes
    app.include_router(hod.router)
    app.include_router(exam_section.router)
    app.include_router(library.router)
    app.include_router(account.router)
    
    # Register Admin Feature routes
    app.include_router(admin_features.router, prefix="/api/admin", tags=["Admin Features"])
    app.include_router(admin_dashboard.router, prefix="/api", tags=["Admin Dashboard"])
    
    # Register Admin User Management routes
    from app.api.endpoints import admin_users
    app.include_router(admin_users.router, prefix="/api", tags=["Admin Users"])
    
    # Register Admin Academic routes
    from app.api.endpoints import admin_academic
    app.include_router(admin_academic.router, prefix="/api", tags=["Admin Academic"])
    
    # Register Admin Exam routes
    from app.api.endpoints import admin_exams
    app.include_router(admin_exams.router, prefix="/api", tags=["Admin Exams"])
    
    # Register Admin Finance routes
    from app.api.endpoints import admin_finance
    app.include_router(admin_finance.router, prefix="/api", tags=["Admin Finance"])
    
    # Register Admin Notices routes
    from app.api.endpoints import admin_notices
    app.include_router(admin_notices.router, prefix="/api", tags=["Admin Notices"])
    
    # Register Admin Messages routes
    from app.api.endpoints import admin_messages
    app.include_router(admin_messages.router, prefix="/api", tags=["Admin Messages"])
    
    # Register Admin Media routes
    from app.api.endpoints import admin_media
    app.include_router(admin_media.router, prefix="/api", tags=["Admin Media"])
    
    # Register Admin System Monitoring routes
    from app.api.endpoints import admin_system
    app.include_router(admin_system.router, prefix="/api", tags=["Admin System"])
    
    # Register Admin Security routes
    from app.api.endpoints import admin_security
    app.include_router(admin_security.router, prefix="/api", tags=["Admin Security"])
    
    # Register Admin Backup routes
    from app.api.endpoints import admin_backup
    app.include_router(admin_backup.router, prefix="/api", tags=["Admin Backup"])
    
    # Register Admin Reports routes
    from app.api.endpoints import admin_reports
    app.include_router(admin_reports.router, prefix="/api", tags=["Admin Reports"])
    
    # Register Admin Settings routes
    from app.api.endpoints import admin_settings
    app.include_router(admin_settings.router, prefix="/api", tags=["Admin Settings"])
    
    # Register Admin Advanced routes
    from app.api.endpoints import admin_advanced
    app.include_router(admin_advanced.router, prefix="/api", tags=["Admin Advanced"])

    # Register web routes
    app.include_router(web_hod.router, prefix="/hod", tags=["HOD Web"])
    app.include_router(web_exam_section.router, prefix="/exam-section", tags=["Exam Section Web"])
    app.include_router(web_library.router, prefix="/library", tags=["Library Web"])
    app.include_router(web_account.router, prefix="/account", tags=["Account Web"])
    app.include_router(web_admin.router, prefix="/admin", tags=["Admin Web"])
    return app


app = create_app()
 
