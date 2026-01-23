# Import all repositories for easy access
from app.repositories.user_repository import UserRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.teacher_repository import TeacherRepository
from app.repositories.parent_repository import ParentRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.grade_repository import GradeRepository
from app.repositories.fee_repository import FeeRepository
from app.repositories.notice_repository import NoticeRepository
from app.repositories.notes_repository import NotesRepository
from app.repositories.videos_repository import VideosRepository
from app.repositories.chat_repository import ChatRepository
from app.repositories.test_repository import TestRepository

__all__ = [
    'UserRepository',
    'StudentRepository',
    'TeacherRepository',
    'ParentRepository',
    'CourseRepository',
    'AssignmentRepository',
    'AttendanceRepository',
    'GradeRepository',
    'FeeRepository',
    'NoticeRepository',
    'NotesRepository',
    'VideosRepository',
    'ChatRepository',
    'TestRepository'
]