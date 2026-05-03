# Import all repositories for easy access
from backup.repositories.user_repository import UserRepository
from backup.repositories.student_repository import StudentRepository
from backup.repositories.teacher_repository import TeacherRepository
from backup.repositories.parent_repository import ParentRepository
from backup.repositories.course_repository import CourseRepository
from backup.repositories.assignment_repository import AssignmentRepository
from backup.repositories.attendance_repository import AttendanceRepository
from backup.repositories.grade_repository import GradeRepository
from backup.repositories.fee_repository import FeeRepository
from backup.repositories.notice_repository import NoticeRepository
from backup.repositories.notes_repository import NotesRepository
from backup.repositories.videos_repository import VideosRepository
from backup.repositories.chat_repository import ChatRepository
from backup.repositories.test_repository import TestRepository

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