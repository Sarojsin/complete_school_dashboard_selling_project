from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import os
import shutil
import uuid
from datetime import datetime

from backup.core.database import get_async_db
from backup.core.templates import templates
from backup.dependencies.auth import get_current_user
from backup.models.models import User, Student, Teacher, Assignment, AssignmentSubmission, Course, FeeRecord, Notice, Attendance, Grade, Note, Video, Parent
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
from backup.services.parent_service import ParentService
from backup.services.test_service import TestService
from backup.utils.constants import GRADE_LEVELS, DEPARTMENTS, SECTIONS, WEEKDAYS

router = APIRouter()

# ------------------ PARENT PAGES ------------------
@router.get("/parent/dashboard")
async def parent_dashboard(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    data = await ParentService.get_dashboard_data(db, current_user.id)
    if not data:
        return RedirectResponse("/login")
        
    unread_count = await MessageRepository.get_unread_count(db, current_user.id)
    
    return templates.TemplateResponse("parent/dashboard.html", {
        "request": request, 
        "current_user": current_user, 
        "children": data["children"],
        "unread_count": unread_count
    })

@router.get("/parent/child/{id}/attendance")
async def parent_child_attendance(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    data = await ParentService.get_child_attendance(db, id)
    return templates.TemplateResponse("parent/attendance.html", {"request": request, "current_user": current_user, "attendance": data})

@router.get("/parent/child/{id}/grades")
async def parent_child_grades(request: Request, id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    data = await ParentService.get_child_grades(db, id)
    return templates.TemplateResponse("parent/grades.html", {"request": request, "current_user": current_user, "grades": data})

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
