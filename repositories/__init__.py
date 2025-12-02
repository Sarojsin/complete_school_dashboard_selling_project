# Import all repositories for easy access
from repositories.user_repository import UserRepository
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.course_repository import CourseRepository
from repositories.assignment_repository import AssignmentRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.grade_repository import GradeRepository
from repositories.fee_repository import FeeRepository
from repositories.notice_repository import NoticeRepository
from repositories.notes_repository import NotesRepository
from repositories.videos_repository import VideosRepository
from repositories.chat_repository import ChatRepository
from repositories.test_repository import TestRepository

__all__ = [
    'UserRepository',
    'StudentRepository',
    'TeacherRepository',
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