"""
Test Factories for College Module Testing

Provides factory functions for creating consistent test data across tests.
Uses simple async functions instead of factory-boy for better async support.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backup.models.college.department import Department
from backup.models.college.program import Program
from backup.models.college.semester import Semester
from backup.models.college.faculty import Faculty
from backup.models.college.student import CollegeStudent
from backup.models.college.enrollment import Enrollment
from modules.college.college_exam_section.models import CollegeExamNotice


async def create_department(db: AsyncSession, name: str, code: str, description: Optional[str] = None) -> Department:
    """Create a test department"""
    dept = Department(name=name, code=code, description=description or f"{name} Department")
    db.add(dept)
    await db.commit()
    await db.refresh(dept)
    return dept


async def create_program(db: AsyncSession, name: str, dept_id: int, code: Optional[str] = None,
                        level: str = "Bachelor", duration_years: int = 4, total_credits: int = 120) -> Program:
    """Create a test program"""
    if not code:
        code = name.split()[0][:3].upper()
    program = Program(
        name=name,
        code=code,
        department_id=dept_id,
        level=level,
        duration_years=duration_years,
        total_credits=total_credits
    )
    db.add(program)
    await db.commit()
    await db.refresh(program)
    return program


async def create_semester(db: AsyncSession, name: str, program_id: int, number: int,
                         start_date: str, end_date: str, is_current: bool = False) -> Semester:
    """Create a test semester"""
    semester = Semester(
        name=name,
        program_id=program_id,
        number=number,
        start_date=start_date,
        end_date=end_date,
        is_current=is_current
    )
    db.add(semester)
    await db.commit()
    await db.refresh(semester)
    return semester


async def create_faculty(db: AsyncSession, user_id: int, dept_id: int,
                        employee_id: Optional[str] = None, designation: str = "Assistant Professor") -> Faculty:
    """Create a test faculty member"""
    if not employee_id:
        employee_id = f"FAC{user_id}"
    faculty = Faculty(
        user_id=user_id,
        employee_id=employee_id,
        department_id=dept_id,
        designation=designation,
        qualification="Ph.D.",
        specialization="Computer Science",
        experience_years=5
    )
    db.add(faculty)
    await db.commit()
    await db.refresh(faculty)
    return faculty


async def create_student(db: AsyncSession, user_id: int, program_id: int, semester_id: Optional[int] = None,
                        roll_number: Optional[str] = None) -> CollegeStudent:
    """Create a test student"""
    if not roll_number:
        roll_number = f"ROLL{user_id}"
    student = CollegeStudent(
        user_id=user_id,
        roll_number=roll_number,
        program_id=program_id,
        semester_id=semester_id,
        cgpa=0.0,
        total_credits_completed=0
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


async def create_exam_notice(db: AsyncSession, title: str, content: str, notice_type: str = "general",
                           created_by: int = 1, exam_date: Optional[str] = None, semester_id: Optional[int] = None) -> CollegeExamNotice:
    """Create a test exam notice"""
    notice = CollegeExamNotice(
        title=title,
        content=content,
        notice_type=notice_type,
        exam_date=exam_date,
        semester_id=semester_id,
        created_by=created_by
    )
    db.add(notice)
    await db.commit()
    await db.refresh(notice)
    return notice


async def create_enrollment(db: AsyncSession, student_id: int, course_id: int, semester_id: Optional[int] = None,
                           status: str = "enrolled") -> Enrollment:
    """Create a test enrollment"""
    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id,
        semester_id=semester_id,
        status=status
    )
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


__all__ = [
    "create_department",
    "create_program",
    "create_semester",
    "create_faculty",
    "create_student",
    "create_exam_notice",
    "create_enrollment"
]