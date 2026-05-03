"""
College Courses Repository

Async CRUD operations for college courses, departments, programs, semesters, enrollments.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
# Import all models from backup to ensure single source of truth
from backup.models.college import Department, Program, Semester, Enrollment
from .models import CollegeCourse


# ── Course Repository ─────────────────────────────────────────
class CollegeCourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, course_id: int) -> Optional[CollegeCourse]:
        result = await self.db.execute(
            select(CollegeCourse).filter(CollegeCourse.id == course_id)
        )
        return result.scalars().first()
    
    async def get_by_code(self, code: str) -> Optional[CollegeCourse]:
        result = await self.db.execute(
            select(CollegeCourse).filter(CollegeCourse.code == code)
        )
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        result = await self.db.execute(
            select(CollegeCourse).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        result = await self.db.execute(
            select(CollegeCourse)
            .filter(CollegeCourse.department_id == department_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_by_semester(self, semester_id: int, skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        result = await self.db.execute(
            select(CollegeCourse)
            .filter(CollegeCourse.semester_id == semester_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_by_instructor(self, instructor_id: int, skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        result = await self.db.execute(
            select(CollegeCourse)
            .filter(CollegeCourse.instructor_id == instructor_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, course: CollegeCourse) -> CollegeCourse:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course
    
    async def update(self, course: CollegeCourse) -> CollegeCourse:
        await self.db.commit()
        await self.db.refresh(course)
        return course
    
    async def delete(self, course_id: int) -> bool:
        course = await self.get_by_id(course_id)
        if course:
            await self.db.delete(course)
            await self.db.commit()
            return True
        return False


# ── Department Repository ─────────────────────────────────────
class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, department_id: int) -> Optional[Department]:
        result = await self.db.execute(
            select(Department).filter(Department.id == department_id)
        )
        return result.scalars().first()
    
    async def get_by_code(self, code: str) -> Optional[Department]:
        result = await self.db.execute(
            select(Department).filter(Department.code == code)
        )
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Department]:
        result = await self.db.execute(
            select(Department).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, department: Department) -> Department:
        self.db.add(department)
        await self.db.commit()
        await self.db.refresh(department)
        return department
    
    async def update(self, department: Department) -> Department:
        await self.db.commit()
        await self.db.refresh(department)
        return department
    
    async def delete(self, department_id: int) -> bool:
        department = await self.get_by_id(department_id)
        if department:
            await self.db.delete(department)
            await self.db.commit()
            return True
        return False


# ── Program Repository ─────────────────────────────────────────
class ProgramRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, program_id: int) -> Optional[Program]:
        result = await self.db.execute(
            select(Program).filter(Program.id == program_id)
        )
        return result.scalars().first()
    
    async def get_by_code(self, code: str) -> Optional[Program]:
        result = await self.db.execute(
            select(Program).filter(Program.code == code)
        )
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Program]:
        result = await self.db.execute(
            select(Program).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[Program]:
        result = await self.db.execute(
            select(Program)
            .filter(Program.department_id == department_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, program: Program) -> Program:
        self.db.add(program)
        await self.db.commit()
        await self.db.refresh(program)
        return program
    
    async def update(self, program: Program) -> Program:
        await self.db.commit()
        await self.db.refresh(program)
        return program
    
    async def delete(self, program_id: int) -> bool:
        program = await self.get_by_id(program_id)
        if program:
            await self.db.delete(program)
            await self.db.commit()
            return True
        return False


# ── Semester Repository ────────────────────────────────────────
class SemesterRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, semester_id: int) -> Optional[Semester]:
        result = await self.db.execute(
            select(Semester).filter(Semester.id == semester_id)
        )
        return result.scalars().first()
    
    async def get_current(self) -> Optional[Semester]:
        result = await self.db.execute(
            select(Semester).filter(Semester.is_current == True)
        )
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Semester]:
        result = await self.db.execute(
            select(Semester).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def list_by_program(self, program_id: int, skip: int = 0, limit: int = 100) -> List[Semester]:
        result = await self.db.execute(
            select(Semester)
            .filter(Semester.program_id == program_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, semester: Semester) -> Semester:
        self.db.add(semester)
        await self.db.commit()
        await self.db.refresh(semester)
        return semester
    
    async def update(self, semester: Semester) -> Semester:
        await self.db.commit()
        await self.db.refresh(semester)
        return semester
    
    async def delete(self, semester_id: int) -> bool:
        semester = await self.get_by_id(semester_id)
        if semester:
            await self.db.delete(semester)
            await self.db.commit()
            return True
        return False


# ── Enrollment Repository ──────────────────────────────────────
class EnrollmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, enrollment_id: int) -> Optional[Enrollment]:
        result = await self.db.execute(
            select(Enrollment).filter(Enrollment.id == enrollment_id)
        )
        return result.scalars().first()
    
    async def get_by_student_id(self, student_id: int) -> List[dict]:
        """Get enrollments for a student with course details"""
        result = await self.db.execute(
            select(Enrollment)
            .filter(Enrollment.student_id == student_id)
        )
        enrollments = result.scalars().all()
        
        return [
            {
                "id": e.id,
                "student_id": e.student_id,
                "course_id": e.course_id,
                "semester_id": e.semester_id,
                "enrollment_date": e.enrollment_date.isoformat() if e.enrollment_date else None,
                "status": e.status,
                "grade": e.grade,
                "grade_points": e.grade_points
            }
            for e in enrollments
        ]
    
    async def get_by_course_id(self, course_id: int) -> List[Enrollment]:
        result = await self.db.execute(
            select(Enrollment).filter(Enrollment.course_id == course_id)
        )
        return list(result.scalars().all())
    
    async def get_by_student_and_course(self, student_id: int, course_id: int) -> Optional[Enrollment]:
        result = await self.db.execute(
            select(Enrollment)
            .filter(Enrollment.student_id == student_id)
            .filter(Enrollment.course_id == course_id)
        )
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[Enrollment]:
        result = await self.db.execute(
            select(Enrollment).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, enrollment: Enrollment) -> Enrollment:
        self.db.add(enrollment)
        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment
    
    async def update(self, enrollment: Enrollment) -> Enrollment:
        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment
    
    async def delete(self, enrollment_id: int) -> bool:
        enrollment = await self.get_by_id(enrollment_id)
        if enrollment:
            await self.db.delete(enrollment)
            await self.db.commit()
            return True
        return False
    
    async def drop_course(self, student_id: int, course_id: int) -> bool:
        enrollment = await self.get_by_student_and_course(student_id, course_id)
        if enrollment:
            enrollment.status = "dropped"
            await self.db.commit()
            return True
        return False