"""
College Courses Service

Business logic for college courses, departments, programs, semesters, enrollments.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .repository import (
    CollegeCourseRepository, DepartmentRepository, ProgramRepository,
    SemesterRepository, EnrollmentRepository
)
from .models import CollegeCourse
from backup.models.college import Department, Program, Semester, Enrollment
from .schemas import (
    CollegeCourseCreate, CollegeCourseUpdate,
    DepartmentCreate, DepartmentUpdate,
    ProgramCreate, ProgramUpdate,
    SemesterCreate, SemesterUpdate,
    EnrollmentCreate, EnrollmentUpdate
)


class CollegeCoursesService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.course_repo = CollegeCourseRepository(db)
        self.dept_repo = DepartmentRepository(db)
        self.program_repo = ProgramRepository(db)
        self.semester_repo = SemesterRepository(db)
        self.enroll_repo = EnrollmentRepository(db)
    
    # ── Course Methods ──────────────────────────────────────────
    async def create_course(self, data: CollegeCourseCreate) -> CollegeCourse:
        course = CollegeCourse(**data.model_dump())
        return await self.course_repo.create(course)
    
    async def get_course(self, course_id: int) -> Optional[CollegeCourse]:
        return await self.course_repo.get_by_id(course_id)
    
    async def list_courses(self, skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        return await self.course_repo.list(skip, limit)
    
    async def list_courses_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        return await self.course_repo.list_by_department(department_id, skip, limit)
    
    async def list_courses_by_semester(self, semester_id: int, skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        return await self.course_repo.list_by_semester(semester_id, skip, limit)
    
    async def list_courses_by_instructor(self, instructor_id: int, skip: int = 0, limit: int = 100) -> List[CollegeCourse]:
        return await self.course_repo.list_by_instructor(instructor_id, skip, limit)
    
    async def update_course(self, course_id: int, data: CollegeCourseUpdate) -> Optional[CollegeCourse]:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(course, key, value)
        return await self.course_repo.update(course)
    
    async def delete_course(self, course_id: int) -> bool:
        return await self.course_repo.delete(course_id)
    
    # ── Department Methods ─────────────────────────────────────
    async def create_department(self, data: DepartmentCreate) -> Department:
        department = Department(**data.model_dump())
        return await self.dept_repo.create(department)
    
    async def get_department(self, department_id: int) -> Optional[Department]:
        return await self.dept_repo.get_by_id(department_id)
    
    async def list_departments(self, skip: int = 0, limit: int = 100) -> List[Department]:
        return await self.dept_repo.list(skip, limit)
    
    async def update_department(self, department_id: int, data: DepartmentUpdate) -> Optional[Department]:
        department = await self.dept_repo.get_by_id(department_id)
        if not department:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(department, key, value)
        return await self.dept_repo.update(department)
    
    async def delete_department(self, department_id: int) -> bool:
        return await self.dept_repo.delete(department_id)
    
    # ── Program Methods ─────────────────────────────────────────
    async def create_program(self, data: ProgramCreate) -> Program:
        program = Program(**data.model_dump())
        return await self.program_repo.create(program)
    
    async def get_program(self, program_id: int) -> Optional[Program]:
        return await self.program_repo.get_by_id(program_id)
    
    async def list_programs(self, skip: int = 0, limit: int = 100) -> List[Program]:
        return await self.program_repo.list(skip, limit)
    
    async def list_programs_by_department(self, department_id: int, skip: int = 0, limit: int = 100) -> List[Program]:
        return await self.program_repo.list_by_department(department_id, skip, limit)
    
    async def update_program(self, program_id: int, data: ProgramUpdate) -> Optional[Program]:
        program = await self.program_repo.get_by_id(program_id)
        if not program:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(program, key, value)
        return await self.program_repo.update(program)
    
    async def delete_program(self, program_id: int) -> bool:
        return await self.program_repo.delete(program_id)
    
    # ── Semester Methods ───────────────────────────────────────
    async def create_semester(self, data: SemesterCreate) -> Semester:
        semester = Semester(**data.model_dump())
        return await self.semester_repo.create(semester)
    
    async def get_semester(self, semester_id: int) -> Optional[Semester]:
        return await self.semester_repo.get_by_id(semester_id)
    
    async def get_current_semester(self) -> Optional[Semester]:
        return await self.semester_repo.get_current()
    
    async def list_semesters(self, skip: int = 0, limit: int = 100) -> List[Semester]:
        return await self.semester_repo.list(skip, limit)
    
    async def list_semesters_by_program(self, program_id: int, skip: int = 0, limit: int = 100) -> List[Semester]:
        return await self.semester_repo.list_by_program(program_id, skip, limit)
    
    async def update_semester(self, semester_id: int, data: SemesterUpdate) -> Optional[Semester]:
        semester = await self.semester_repo.get_by_id(semester_id)
        if not semester:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(semester, key, value)
        return await self.semester_repo.update(semester)
    
    async def delete_semester(self, semester_id: int) -> bool:
        return await self.semester_repo.delete(semester_id)
    
    # ── Enrollment Methods ──────────────────────────────────────
    async def enroll_student(self, data: EnrollmentCreate) -> Enrollment:
        # Check if already enrolled
        existing = await self.enroll_repo.get_by_student_and_course(data.student_id, data.course_id)
        if existing:
            raise ValueError("Student already enrolled in this course")
        
        enrollment = Enrollment(**data.model_dump())
        return await self.enroll_repo.create(enrollment)
    
    async def get_enrollment(self, enrollment_id: int) -> Optional[Enrollment]:
        return await self.enroll_repo.get_by_id(enrollment_id)
    
    async def get_student_enrollments(self, student_id: int) -> List[dict]:
        return await self.enroll_repo.get_by_student_id(student_id)
    
    async def get_course_enrollments(self, course_id: int) -> List[Enrollment]:
        return await self.enroll_repo.get_by_course_id(course_id)
    
    async def list_enrollments(self, skip: int = 0, limit: int = 100) -> List[Enrollment]:
        return await self.enroll_repo.list(skip, limit)
    
    async def update_enrollment(self, enrollment_id: int, data: EnrollmentUpdate) -> Optional[Enrollment]:
        enrollment = await self.enroll_repo.get_by_id(enrollment_id)
        if not enrollment:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(enrollment, key, value)
        return await self.enroll_repo.update(enrollment)
    
    async def drop_course(self, student_id: int, course_id: int) -> bool:
        return await self.enroll_repo.drop_course(student_id, course_id)
    
    async def delete_enrollment(self, enrollment_id: int) -> bool:
        return await self.enroll_repo.delete(enrollment_id)