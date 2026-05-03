"""
College Student Service
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Dict, Any, List
from .repository import CollegeStudentRepository
from .schemas import CollegeStudentCreate, CollegeStudentUpdate


class CollegeStudentService:
    def __init__(self, db: AsyncSession):
        self.repository = CollegeStudentRepository(db)
    
    async def create_student(self, data: CollegeStudentCreate) -> Dict[str, Any]:
        student = await self.repository.create(
            user_id=data.user_id,
            roll_number=data.roll_number,
            program_id=data.program_id,
            semester_id=data.semester_id
        )
        return {"student": student}
    
    async def get_student(self, student_id: int) -> Optional[Dict[str, Any]]:
        student = await self.repository.get(student_id)
        if student:
            return {"student": student}
        return None

    async def get_my_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get college student profile for current logged-in user"""
        student = await self.repository.get_by_user_id(user_id)
        if student:
            return {"student": student}
        return None
     
    async def list_students(self, program_id: Optional[int] = None,
                           semester_id: Optional[int] = None,
                           skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        students = await self.repository.list(program_id, semester_id, skip, limit)
        total = await self.repository.count(program_id)
        return {"total": total, "students": students}

    async def get_my_courses(self, user_id: int) -> List[Dict[str, Any]]:
        """Get courses enrolled by current student via enrollments"""
        from backup.models.college import Enrollment, CollegeCourse
        
        # Get student profile first
        student = await self.repository.get_by_user_id(user_id)
        if not student or not student.program_id:
            return []
        
        # Get enrollments for this student
        result = await self.db.execute(
            select(Enrollment).where(
                Enrollment.student_id == student.id,
                Enrollment.status == "active"
            )
        )
        enrollments = result.scalars().all()
        
        # Get course details for each enrollment
        courses = []
        for enrollment in enrollments:
            course = await self.db.execute(
                select(CollegeCourse).where(CollegeCourse.id == enrollment.course_id)
            )
            course = course.scalar_one_or_none()
            if course:
                courses.append({
                    "id": course.id,
                    "course_code": course.code,
                    "course_name": course.name,
                    "credits": course.credits,
                    "enrollment_id": enrollment.id
                })
        
        return courses

    async def get_my_grades(self, user_id: int) -> List[Dict[str, Any]]:
        """Get grades/enrollment results for current student"""
        from modules.college.college_enrollments.models import Enrollment
        
        student = await self.repository.get_by_user_id(user_id)
        if not student:
            return []
        
        # Get enrollments with grades
        result = await self.db.execute(
            select(Enrollment).where(
                Enrollment.student_id == student.id,
                Enrollment.grade.isnot(None)
            )
        )
        enrollments = result.scalars().all()
        
        grades = []
        for enrollment in enrollments:
            grades.append({
                "enrollment_id": enrollment.id,
                "course_id": enrollment.course_id,
                "grade": enrollment.grade,
                "status": enrollment.status
            })
        
        return grades

    async def get_my_enrollments(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all enrollments for current student"""
        from modules.college.college_enrollments.models import Enrollment
        
        student = await self.repository.get_by_user_id(user_id)
        if not student:
            return []
        
        result = await self.db.execute(
            select(Enrollment).where(Enrollment.student_id == student.id)
        )
        enrollments = result.scalars().all()
        
        return [
            {
                "id": e.id,
                "course_id": e.course_id,
                "status": e.status,
                "grade": e.grade,
                "enrolled_at": e.enrolled_at
            }
            for e in enrollments
        ]

    async def get_my_hostel_allocation(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get hostel allocation for current student"""
        student = await self.repository.get_by_user_id(user_id)
        if not student:
            return None
        
        from modules.college.college_hostel.models import HostelAllocation
        result = await self.db.execute(
            select(HostelAllocation).where(
                HostelAllocation.student_id == student.id,
                HostelAllocation.status == "active"
            )
        )
        allocation = result.scalar_one_or_none()
        
        if allocation:
            return {
                "id": allocation.id,
                "hostel_id": allocation.hostel_id,
                "room_id": allocation.room_id,
                "allocation_date": allocation.allocation_date,
                "status": allocation.status
            }
        return None


__all__ = ["CollegeStudentService"]
