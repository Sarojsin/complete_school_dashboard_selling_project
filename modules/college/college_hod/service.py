"""
College HOD Service

Business logic for department head operations.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import HodRepository
from .schemas import HODDashboardResponse, DepartmentDetailResponse, FacultySchema, CourseSchema
from modules.shared.exceptions import NotFoundError, ForbiddenError


class HodService:
    """Service for HOD operations"""

    def __init__(self, db: AsyncSession):
        self.repository = HodRepository(db)

    async def verify_hod_permission(self, user_id: int, department_id: Optional[int] = None) -> bool:
        """Verify that user is HOD of specified department (or any department)"""
        departments = await self.repository.get_departments_by_hod(user_id)
        if not departments:
            raise ForbiddenError("User is not an HOD of any department")

        if department_id:
            if not any(d.id == department_id for d in departments):
                raise ForbiddenError("User is not HOD of specified department")
        return True

    async def get_dashboard(self, user_id: int) -> HODDashboardResponse:
        """Get HOD dashboard summary"""
        departments = await self.repository.get_departments_by_hod(user_id)
        if not departments:
            # Return empty dashboard if not HOD yet
            return HODDashboardResponse(departments_count=0, departments=[])

        dept_count = len(departments)
        return HODDashboardResponse(departments_count=dept_count, departments=departments)

    async def get_department_details(self, dept_id: int, user_id: int) -> DepartmentDetailResponse:
        """Get detailed info for a department (HOD only)"""
        await self.verify_hod_permission(user_id, dept_id)
        dept = await self.repository.get_department_by_id(dept_id)
        if not dept:
            raise NotFoundError("Department not found")

        faculty_count = await self.repository.count_faculty(dept_id)
        # Could count programs, courses etc.
        return DepartmentDetailResponse(
            id=dept.id,
            name=dept.name,
            code=dept.code,
            description=dept.description,
            faculty_count=faculty_count,
            programs_count=0  # TODO: add program count query
        )

    async def get_department_faculty(self, dept_id: int, user_id: int) -> List[FacultySchema]:
        """Get faculty in HOD's department"""
        await self.verify_hod_permission(user_id, dept_id)
        faculty_list = await self.repository.get_faculty_by_department(dept_id)
        return [FacultySchema.model_validate(f) for f in faculty_list]

    async def get_department_courses(self, dept_id: int, user_id: int) -> List[CourseSchema]:
        """Get courses in HOD's department"""
        await self.verify_hod_permission(user_id, dept_id)
        courses = await self.repository.get_courses_by_department(dept_id)
        return [CourseSchema.model_validate(c) for c in courses]


__all__ = ["HodService"]
