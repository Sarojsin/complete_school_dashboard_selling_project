"""
Student Service

Business logic layer for student.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from backup.modules.college.student.repository import StudentRepository
from backup.modules.college.student.schemas import StudentCreate, StudentUpdate


class StudentService:
    """Service for student business logic"""
    
    def __init__(self):
        self.repo = StudentRepository()
    
    async def get_student(self, db: AsyncSession, student_id: int):
        """Get student by ID"""
        return await self.repo.get_by_id(db, student_id)
    
    async def get_student_by_user(self, db: AsyncSession, user_id: int):
        """Get student by user ID"""
        return await self.repo.get_by_user_id(db, user_id)
    
    async def get_student_by_enrollment(self, db: AsyncSession, student_id: str):
        """Get student by enrollment number"""
        return await self.repo.get_by_student_id(db, student_id)
    
    async def list_students(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """List all students"""
        students = await self.repo.get_all(db, skip, limit)
        total = await self.repo.get_count(db)
        return {
            "students": students,
            "total": total
        }
    
    async def list_students_by_program(self, db: AsyncSession, program_id: int, skip: int = 0, limit: int = 100):
        """List students by program"""
        return await self.repo.get_by_program(db, program_id, skip, limit)
    
    async def list_students_by_semester(self, db: AsyncSession, semester_id: int, skip: int = 0, limit: int = 100):
        """List students by semester"""
        return await self.repo.get_by_semester(db, semester_id, skip, limit)
    
    async def create_student(self, db: AsyncSession, student_data: StudentCreate):
        """Create new student"""
        # Check if user already has student profile
        existing = await self.repo.get_by_user_id(db, student_data.user_id)
        if existing:
            raise ValueError("User already has student profile")
        
        # Check if student ID is unique
        existing_enroll = await self.repo.get_by_student_id(db, student_data.student_id)
        if existing_enroll:
            raise ValueError("Student ID already exists")
        
        return await self.repo.create(db, student_data.model_dump())
    
    async def update_student(self, db: AsyncSession, student_id: int, student_data: StudentUpdate):
        """Update student"""
        update_data = student_data.model_dump(exclude_unset=True)
        return await self.repo.update(db, student_id, update_data)
    
    async def delete_student(self, db: AsyncSession, student_id: int):
        """Delete student"""
        return await self.repo.delete(db, student_id)
