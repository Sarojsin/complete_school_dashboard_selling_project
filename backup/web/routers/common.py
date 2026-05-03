from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
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
from backup.services.test_service import TestService
from backup.utils.constants import GRADE_LEVELS, DEPARTMENTS, SECTIONS, WEEKDAYS

router = APIRouter()

# ==================== HOME & AUTH ROUTES ====================
@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/logout")
async def logout(request: Request):
    """Logout route"""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response

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

@router.get("/signup/hod", response_class=HTMLResponse)
async def signup_hod_page(request: Request):
    return templates.TemplateResponse("auth/signup_hod.html", {"request": request, "departments": DEPARTMENTS})

@router.get("/signup/exam-section", response_class=HTMLResponse)
async def signup_exam_section_page(request: Request):
    return templates.TemplateResponse("auth/signup_exam_section.html", {"request": request})

@router.get("/signup/library", response_class=HTMLResponse)
async def signup_library_page(request: Request):
    return templates.TemplateResponse("auth/signup_library.html", {"request": request})

@router.get("/signup/account", response_class=HTMLResponse)
async def signup_account_page(request: Request):
    return templates.TemplateResponse("auth/signup_account.html", {"request": request})

@router.get("/signup/admin", response_class=HTMLResponse)
async def signup_admin_page(request: Request):
    return templates.TemplateResponse("auth/signup_admin.html", {"request": request})

@router.post("/signup/admin")
async def signup_admin_handler(request: Request):
    """Handle admin signup form submission"""
    form = await request.form()
    import httpx
    import os
    
    api_base = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    data = {
        "email": form.get("email"),
        "username": form.get("username"),
        "full_name": form.get("full_name"),
        "password": form.get("password"),
        "secret_key": form.get("secret_key")
    }
    
    # Get CSRF token from request state (set by middleware)
    csrf_token = getattr(request.state, "csrf_token", None)
    
    async with httpx.AsyncClient() as client:
        try:
            # Include CSRF token in headers
            headers = {}
            if csrf_token:
                headers["X-CSRF-Token"] = csrf_token
                headers["Cookie"] = f"csrf_token={csrf_token}"
            
            response = await client.post(
                f"{api_base}/api/auth/signup/admin",
                json=data,
                headers=headers,
                timeout=10.0
            )
            if response.status_code == 201:
                return templates.TemplateResponse(
                    "auth/signup_admin.html",
                    {"request": request, "success": True}
                )
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", "Registration failed")
                except:
                    error_msg = f"Registration failed (status: {response.status_code})"
                return templates.TemplateResponse(
                    "auth/signup_admin.html",
                    {"request": request, "error": error_msg}
                )
        except Exception as e:
            return templates.TemplateResponse(
                "auth/signup_admin.html",
                {"request": request, "error": str(e)}
            )


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
