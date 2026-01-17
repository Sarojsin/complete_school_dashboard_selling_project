from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.csrf import CSRFMiddleware
from app.web.routes import router as web_router
from services.chat_cleanup_service import cleanup_expired_messages

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_expired_messages, 'interval', hours=1)
    scheduler.start()
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

    # Security Middleware first
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CSRFMiddleware)

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Session Middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        session_cookie="school_session"
    )

    # Static files mounting
    # Make sure static directories exist
    os.makedirs("static/uploads/avatars", exist_ok=True)
    os.makedirs("static/uploads/assignments", exist_ok=True)
    os.makedirs("static/uploads/notes", exist_ok=True)
    os.makedirs("static/uploads/videos", exist_ok=True)
    
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/media", StaticFiles(directory="media"), name="media")

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

    # Include Web Routes
    app.include_router(web_router)

    # Include API Routes (Legacy and New)
    # We will eventually move these into app/api/v1/endpoints
    from routes import auth, students, teachers, authority, tests, websocket_chat, parents
    from routes import courses, assignments, attendance, grades, fees
    from routes import notices, notes, videos, chat
    from routes import groups, group_posts

    app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
    app.include_router(students.router, prefix="/api/students", tags=["Students"])
    app.include_router(teachers.router, prefix="/api/teachers", tags=["Teachers"])
    app.include_router(authority.router, prefix="/api/authority", tags=["Authority"])
    app.include_router(tests.router, prefix="/api/tests", tags=["Tests"])
    app.include_router(websocket_chat.router, prefix="/api/ws", tags=["WebSocket Chat"])
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

    return app

app = create_app()
