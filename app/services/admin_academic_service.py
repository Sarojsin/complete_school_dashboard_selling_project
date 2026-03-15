from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Course, Teacher
from app.models.department_models import Department
from app.api.schemas.admin.academic import (
    CourseCreateRequest, CourseUpdateRequest,
    DepartmentCreateRequest, DepartmentUpdateRequest
)
from app.repositories.admin_academic_repository import AdminAcademicRepository
from app.core.exceptions import NotFoundError, ValidationError


class AdminAcademicService:
    """Business logic for Admin Academic management."""

    # -----------------------------------------------------------------------
    # Shared / Internal
    # -----------------------------------------------------------------------
    @staticmethod
    async def get_teacher_or_raise(db: AsyncSession, teacher_id: int) -> Teacher:
        from app.repositories.user_repository import UserRepository # Teacher is tied to user conceptually, but we have no Teacher repository wrapper locally 
        # For strict check, querying directly using existing repositories or standard pattern is best. 
        # Here we just implement the simple fetch inline to the service if a generic repo isn't there, 
        # but the request was "Repositories handle DB interaction". Let's put it in AdminAcademicRepository.
        from sqlalchemy import select
        result = await db.execute(select(Teacher).where(Teacher.id == teacher_id))
        teacher = result.scalar_one_or_none()
        if not teacher:
            raise ValidationError("Teacher not found")
        return teacher

    # -----------------------------------------------------------------------
    # Courses
    # -----------------------------------------------------------------------
    @staticmethod
    async def get_all_courses(
        db: AsyncSession, grade_level: Optional[str], teacher_id: Optional[int],
        search: Optional[str], skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        courses = await AdminAcademicRepository.get_courses_list(db, grade_level, teacher_id, search, skip, limit)
        return [
            {
                "id": c.id,
                "name": c.name,
                "code": c.code,
                "description": c.description,
                "grade_level": c.grade_level,
                "capacity": c.capacity,
                "teacher_id": c.teacher_id,
                "teacher_name": c.teacher.full_name if getattr(c, 'teacher', None) else None,
                "enrollment_count": len(c.enrollments) if getattr(c, 'enrollments', None) else 0,
                "is_active": c.is_active,
            }
            for c in courses
        ]

    @staticmethod
    async def create_course(db: AsyncSession, course_data: CourseCreateRequest) -> Dict[str, Any]:
        existing = await AdminAcademicRepository.get_course_by_code(db, course_data.code)
        if existing:
            raise ValidationError("Course code already exists")

        if course_data.teacher_id:
            await AdminAcademicService.get_teacher_or_raise(db, course_data.teacher_id)

        course = Course(**course_data.model_dump())
        db.add(course)
        await db.commit()
        await db.refresh(course)
        return {"success": True, "course": {"id": course.id, "name": course.name, "code": course.code}}

    @staticmethod
    async def update_course(db: AsyncSession, course_id: int, course_data: CourseUpdateRequest) -> Dict[str, Any]:
        course = await AdminAcademicRepository.get_course_by_id(db, course_id)
        if not course:
            raise NotFoundError("Course not found")

        updates = course_data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(course, field, value)
        await db.commit()
        return {"success": True, "message": "Course updated"}

    @staticmethod
    async def delete_course(db: AsyncSession, course_id: int) -> Dict[str, Any]:
        course = await AdminAcademicRepository.get_course_by_id(db, course_id)
        if not course:
            raise NotFoundError("Course not found")

        await db.delete(course)
        await db.commit()
        return {"success": True, "message": "Course deleted"}

    # -----------------------------------------------------------------------
    # Departments
    # -----------------------------------------------------------------------
    @staticmethod
    async def get_all_departments(
        db: AsyncSession, search: Optional[str], skip: int, limit: int
    ) -> List[Dict[str, Any]]:
        departments = await AdminAcademicRepository.get_departments_list(db, search, skip, limit)
        return [
            {
                "id": d.id,
                "name": d.name,
                "code": d.code,
                "description": d.description,
                "hod_id": d.hod_teacher_id,
                "hod_name": d.hod.full_name if getattr(d, 'hod', None) else None,
                "teacher_count": len(d.teachers) if getattr(d, 'teachers', None) else 0,
                "student_count": len(d.students) if getattr(d, 'students', None) else 0,
                "is_active": d.is_active,
            }
            for d in departments
        ]

    @staticmethod
    async def create_department(db: AsyncSession, dept_data: DepartmentCreateRequest) -> Dict[str, Any]:
        existing = await AdminAcademicRepository.get_department_by_code(db, dept_data.code)
        if existing:
            raise ValidationError("Department code already exists")

        if dept_data.hod_teacher_id:
            await AdminAcademicService.get_teacher_or_raise(db, dept_data.hod_teacher_id)

        department = Department(**dept_data.model_dump())
        db.add(department)
        await db.commit()
        await db.refresh(department)
        return {
            "success": True,
            "department": {"id": department.id, "name": department.name, "code": department.code},
        }

    @staticmethod
    async def update_department(db: AsyncSession, dept_id: int, dept_data: DepartmentUpdateRequest) -> Dict[str, Any]:
        dept = await AdminAcademicRepository.get_department_by_id(db, dept_id)
        if not dept:
            raise NotFoundError("Department not found")

        for field, value in dept_data.model_dump(exclude_unset=True).items():
            setattr(dept, field, value)
        await db.commit()
        return {"success": True, "message": "Department updated"}

    @staticmethod
    async def delete_department(db: AsyncSession, dept_id: int) -> Dict[str, Any]:
        dept = await AdminAcademicRepository.get_department_by_id(db, dept_id)
        if not dept:
            raise NotFoundError("Department not found")

        await db.delete(dept)
        await db.commit()
        return {"success": True, "message": "Department deleted"}

    # -----------------------------------------------------------------------
    # Statistics
    # -----------------------------------------------------------------------
    @staticmethod
    async def get_academic_stats(db: AsyncSession) -> Dict[str, Any]:
        stats = await AdminAcademicRepository.get_academic_stats(db)
        return {
            "courses": {
                "total": stats["total_courses"], 
                "active": stats["active_courses"], 
                "inactive": stats["total_courses"] - stats["active_courses"]
            },
            "departments": {
                "total": stats["total_departments"], 
                "with_hod": stats["hod_departments"], 
                "without_hod": stats["total_departments"] - stats["hod_departments"]
            },
            "teachers": stats["total_teachers"],
            "students": stats["total_students"],
        }

    # -----------------------------------------------------------------------
    # Timetable
    # -----------------------------------------------------------------------
    @staticmethod
    async def get_timetable(
        db: AsyncSession,
        course_id: Optional[int],
        day: Optional[str],
    ) -> List[Dict[str, Any]]:
        entries = await AdminAcademicRepository.get_timetable_entries(db, course_id, day)
        return [
            {
                "id": e.id,
                "course_id": e.course_id,
                "day_of_week": e.day_of_week,
                "start_time": e.start_time.isoformat() if e.start_time else None,
                "end_time": e.end_time.isoformat() if e.end_time else None,
                "room": e.room,
            }
            for e in entries
        ]

    @staticmethod
    async def check_timetable_conflicts(
        db: AsyncSession,
        course_id: int,
        day_of_week: str,
        start_time: str,
        end_time: str,
    ) -> Dict[str, Any]:
        try:
            start = datetime.strptime(start_time, "%H:%M").time()
            end = datetime.strptime(end_time, "%H:%M").time()
        except ValueError:
            raise ValidationError("Time must be in HH:MM format")

        conflicts = await AdminAcademicRepository.find_timetable_conflicts(
            db, course_id, day_of_week, start, end
        )
        return {
            "has_conflicts": len(conflicts) > 0,
            "conflicting_courses": [
                {
                    "course_id": c.course_id,
                    "day_of_week": c.day_of_week,
                    "start_time": c.start_time.isoformat() if c.start_time else None,
                    "end_time": c.end_time.isoformat() if c.end_time else None,
                    "room": c.room,
                }
                for c in conflicts
            ],
        }
