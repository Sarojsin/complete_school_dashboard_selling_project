from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import os
import shutil
import uuid
from datetime import datetime

from app.core.database import get_async_db
from app.core.templates import templates
from dependencies import get_current_user
from models.models import User, Student, Teacher, Assignment, AssignmentSubmission, Course, FeeRecord, Notice, Attendance, Grade, Note, Video, Parent
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

# ------------------ PARENT PAGES ------------------
@router.get("/parent/dashboard")
async def parent_dashboard(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    res = await db.execute(select(Parent).filter(Parent.user_id == current_user.id))
    parent = res.scalars().first()
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
async def parent_chat(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    return templates.TemplateResponse("parent/chat.html", {"request": request, "current_user": current_user, "user": current_user})

@router.get("/parent/notices")
async def parent_notices(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    return templates.TemplateResponse("parent/notices.html", {"request": request, "current_user": current_user})

@router.get("/parent/profile")
async def parent_profile(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("parent/profile.html", {"request": request, "current_user": current_user})
