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
from app.dependencies.auth import get_current_user
from app.models.models import User, Student, Teacher, Assignment, AssignmentSubmission, Course, FeeRecord, Notice, Attendance, Grade, Note, Video
from app.models.chat_models import ChatMessage
from app.repositories.student_repository import StudentRepository
from app.repositories.teacher_repository import TeacherRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.notice_repository import NoticeRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.notes_repository import NotesRepository
from app.repositories.videos_repository import VideosRepository
from app.repositories.test_repository import TestRepository
from app.repositories.fee_repository import FeeRepository
from app.repositories.fee_structure_repository import FeeStructureRepository
from app.repositories.chat_repository import ChatRepository
from app.services.test_service import TestService
from app.utils.constants import GRADE_LEVELS, DEPARTMENTS, SECTIONS, WEEKDAYS

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
