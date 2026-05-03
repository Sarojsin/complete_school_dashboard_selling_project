from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backup.models.models import User, Student, Teacher, Parent, Course, FeeRecord
from backup.repositories.student_repository import StudentRepository
from backup.repositories.teacher_repository import TeacherRepository
from backup.repositories.course_repository import CourseRepository

class AuthorityService:
    @staticmethod
    async def get_dashboard_stats(db: AsyncSession):
        # Queries for global stats
        student_count = await db.execute(select(func.count(Student.id)))
        teacher_count = await db.execute(select(func.count(Teacher.id)))
        parent_count = await db.execute(select(func.count(Parent.id)))
        course_count = await db.execute(select(func.count(Course.id)))
        
        # Recent activity (placeholder or real queries)
        return {
            "total_students": student_count.scalar() or 0,
            "total_teachers": teacher_count.scalar() or 0,
            "total_parents": parent_count.scalar() or 0,
            "total_courses": course_count.scalar() or 0,
            "recent_registrations": 12, # Placeholder
            "monthly_revenue": "1.2M", # Placeholder
            "active_sessions": 45      # Placeholder
        }

    @staticmethod
    async def get_fee_report(db: AsyncSession):
        # Replicating logic from authority router
        total_fees = await db.execute(select(func.sum(FeeRecord.amount)))
        total_paid = await db.execute(select(func.sum(FeeRecord.paid_amount)))
        
        tf = total_fees.scalar() or 0
        tp = total_paid.scalar() or 0
        
        return {
            "total_receivable": tf,
            "total_collected": tp,
            "pending_amount": tf - tp,
            "collection_rate": (tp / tf * 100) if tf > 0 else 0
        }
