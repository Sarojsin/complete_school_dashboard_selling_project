"""
School HOD Service

Business logic for HOD operations with permission checks.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import HODRepository
from .models import Teacher
from .schemas import (
    HODDashboardSchema,
    DepartmentListResponse,
    TeacherListResponse,
    CourseListResponse,
    TeacherShortSchema,
    CourseSchema,
    DepartmentSchema
)
from modules.shared.exceptions import NotFoundError, ForbiddenError


class HODService:
    """Service for HOD operations"""

    def __init__(self, db: AsyncSession):
        self.repository = HODRepository(db)

    async def verify_hod_permission(self, user_id: int) -> Teacher:
        """
        Verify that the user is an HOD (has teacher profile + department).
        Returns the Teacher profile if valid.
        """
        teacher = await self.repository.get_teacher_by_user_id(user_id)
        if not teacher:
            raise ForbiddenError("User is not registered as a teacher")
        if not teacher.department:
            raise ForbiddenError("Teacher is not assigned as HOD of any department")
        return teacher

    async def get_dashboard(self, user_id: int) -> HODDashboardSchema:
        """Get HOD dashboard statistics"""
        teacher = await self.verify_hod_permission(user_id)
        department = await self.repository.get_department_name(teacher)

        total_teachers = await self.repository.count_teachers_in_department(department)
        total_students = await self.repository.count_students_in_department()
        total_courses = await self.repository.count_courses_in_department(department)

        return HODDashboardSchema(
            department=department,
            total_teachers=total_teachers,
            total_students=total_students,
            total_courses=total_courses
        )

    async def get_departments(self) -> DepartmentListResponse:
        """Get all distinct departments in the school"""
        departments = await self.repository.get_all_departments()
        dept_schemas = [DepartmentSchema(name=d) for d in departments]
        return DepartmentListResponse(departments=dept_schemas)

    async def get_department_teachers(self, user_id: int) -> TeacherListResponse:
        """Get all teachers in the HOD's department"""
        teacher = await self.verify_hod_permission(user_id)
        department = await self.repository.get_department_name(teacher)
        teachers = await self.repository.get_teachers_in_department(department)
        teacher_schemas = [TeacherShortSchema.model_validate(t) for t in teachers]
        return TeacherListResponse(teachers=teacher_schemas)

    async def get_department_courses(self, user_id: int) -> CourseListResponse:
        """Get all courses in the HOD's department"""
        teacher = await self.verify_hod_permission(user_id)
        department = await self.repository.get_department_name(teacher)
        courses = await self.repository.get_courses_in_department(department)
        course_schemas = [CourseSchema.model_validate(c) for c in courses]
        return CourseListResponse(courses=course_schemas)


__all__ = ["HODService"]
