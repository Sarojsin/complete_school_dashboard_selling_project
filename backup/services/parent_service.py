from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backup.models.models import Parent, Student, Attendance, Grade, Assignment
from backup.repositories.student_repository import StudentRepository

class ParentService:
    @staticmethod
    async def get_dashboard_data(db: AsyncSession, user_id: int):
        # Fetch parent and children
        res = await db.execute(select(Parent).filter(Parent.user_id == user_id))
        parent = res.scalars().first()
        if not parent:
            return None
        
        children = parent.children
        children_data = []
        for child in children:
            # Basic summary for each child
            children_data.append({
                "id": child.id,
                "name": child.user.full_name,
                "grade": child.grade_level,
                "section": child.section,
                "attendance_summary": "95%", # Placeholder
                "recent_grade": "A",        # Placeholder
                "pending_assignments": 2    # Placeholder
            })
            
        return {
            "parent": parent,
            "children": children_data
        }

    @staticmethod
    async def get_child_attendance(db: AsyncSession, student_id: int):
        # In a real system, we would check if the child belongs to the parent
        return {
            "percentage": "94%",
            "history": [] # Would be fetched from AttendanceRepository
        }

    @staticmethod
    async def get_child_grades(db: AsyncSession, student_id: int):
        return {
            "gpa": "3.8",
            "report_card": [] # From GradeRepository
        }
