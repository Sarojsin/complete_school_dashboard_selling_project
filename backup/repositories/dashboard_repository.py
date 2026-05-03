from typing import Any, Dict, List, Tuple
from datetime import date, timedelta
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backup.models.models import (
    Authority,
    Course,
    FeeRecord,
    Grade,
    Notice,
    Parent,
    Student,
    Teacher,
    User,
    UserRole,
)
from backup.models.admin_models import SystemFeature
from backup.models.exam_models import ExamNotice
from backup.models.group_models import Group
from backup.repositories.feature_repository import FeatureRepository

class DashboardRepository:
    """Handles all database aggregations and reads for the dashboard."""

    @staticmethod
    async def get_user_role_counts(db: AsyncSession) -> Dict[str, int]:
        role_rows = await db.execute(select(User.role, func.count(User.id)).group_by(User.role))
        return {row[0].value: row[1] for row in role_rows}

    @staticmethod
    async def get_active_users_count(db: AsyncSession) -> int:
        result = await db.execute(select(func.count(User.id)).where(User.is_active.is_(True)))
        return result.scalar() or 0

    @staticmethod
    async def get_features_counts(db: AsyncSession) -> Tuple[int, int]:
        total_r = await db.execute(select(func.count(SystemFeature.id)))
        enabled_r = await db.execute(select(func.count(SystemFeature.id)).where(SystemFeature.is_enabled.is_(True)))
        return total_r.scalar() or 0, enabled_r.scalar() or 0

    @staticmethod
    async def get_feature_category_counts(db: AsyncSession) -> Dict[str, int]:
        categories = await FeatureRepository.get_categories(db)
        counts = {}
        for cat in categories:
            cat_result = await db.execute(
                select(func.count(SystemFeature.id)).where(SystemFeature.feature_category == cat)
            )
            counts[cat] = cat_result.scalar() or 0
        return counts

    @staticmethod
    async def get_user_stats(db: AsyncSession) -> Tuple[int, int, int, int, int]:
        total_r      = await db.execute(select(func.count(User.id)))
        active_r     = await db.execute(select(func.count(User.id)).where(User.is_active.is_(True)))
        students_r   = await db.execute(select(func.count(Student.id)))
        teachers_r   = await db.execute(select(func.count(Teacher.id)))
        authority_r  = await db.execute(select(func.count(Authority.id)))
        return (
            total_r.scalar() or 0,
            active_r.scalar() or 0,
            students_r.scalar() or 0,
            teachers_r.scalar() or 0,
            authority_r.scalar() or 0,
        )

    @staticmethod
    async def get_overview_metrics(db: AsyncSession) -> Dict[str, Any]:
        today = date.today()
        thirty_days_later = today + timedelta(days=30)

        students_r        = await db.execute(select(func.count(Student.id)))
        teachers_r        = await db.execute(select(func.count(Teacher.id)))
        parents_r         = await db.execute(select(func.count(Parent.id)))
        courses_r         = await db.execute(select(func.count(Course.id)))
        total_users_r     = await db.execute(select(func.count(User.id)))
        active_users_r    = await db.execute(select(func.count(User.id)).where(User.is_active.is_(True)))
        total_notices_r   = await db.execute(select(func.count(Notice.id)))
        active_groups_r   = await db.execute(select(func.count(Group.id)).where(Group.is_active.is_(True)))
        upcoming_exams_r  = await db.execute(
            select(func.count(ExamNotice.id)).where(
                ExamNotice.exam_date >= today, ExamNotice.exam_date <= thirty_days_later
            )
        )
        revenue_r = await db.execute(
            select(func.sum(FeeRecord.paid_amount)).where(FeeRecord.status == "paid")
        )
        pending_r = await db.execute(
            select(func.sum(FeeRecord.amount - FeeRecord.paid_amount)).where(
                FeeRecord.status.in_(["pending", "overdue", "partial"])
            )
        )
        pending_cnt_r = await db.execute(
            select(func.count(FeeRecord.id)).where(
                FeeRecord.status.in_(["pending", "overdue", "partial"])
            )
        )

        return {
            "total_students":    students_r.scalar() or 0,
            "total_teachers":    teachers_r.scalar() or 0,
            "total_parents":     parents_r.scalar() or 0,
            "total_courses":     courses_r.scalar() or 0,
            "total_revenue":     round(float(revenue_r.scalar() or 0), 2),
            "pending_fees":      round(float(pending_r.scalar() or 0), 2),
            "pending_fees_count": pending_cnt_r.scalar() or 0,
            "upcoming_exams":    upcoming_exams_r.scalar() or 0,
            "active_groups":     active_groups_r.scalar() or 0,
            "total_users":       total_users_r.scalar() or 0,
            "active_users":      active_users_r.scalar() or 0,
            "total_notices":     total_notices_r.scalar() or 0,
        }

    @staticmethod
    async def get_features_summary(db: AsyncSession) -> Dict[str, Any]:
        global_r  = await db.execute(select(func.count(SystemFeature.id)).where(SystemFeature.is_global.is_(True)))
        global_features = global_r.scalar() or 0

        categories = await FeatureRepository.get_categories(db)
        by_category = {}
        for cat in categories:
            total_cat_r   = await db.execute(
                select(func.count(SystemFeature.id)).where(SystemFeature.feature_category == cat)
            )
            enabled_cat_r = await db.execute(
                select(func.count(SystemFeature.id)).where(
                    SystemFeature.feature_category == cat, SystemFeature.is_enabled.is_(True)
                )
            )
            t = total_cat_r.scalar() or 0
            e = enabled_cat_r.scalar() or 0
            by_category[cat] = {"total": t, "enabled": e, "disabled": t - e}
            
        return {"global_features": global_features, "by_category": by_category}

    @staticmethod
    async def count_enrollments_in_range(db: AsyncSession, start: date, end: date) -> int:
        r = await db.execute(
            select(func.count(Student.id)).where(
                Student.enrollment_date >= start, Student.enrollment_date < end
            )
        )
        return r.scalar() or 0

    @staticmethod
    async def aggregate_fees_in_range(db: AsyncSession, start: date, end: date) -> Tuple[float, float]:
        collected_r = await db.execute(
            select(func.sum(FeeRecord.paid_amount)).where(
                FeeRecord.payment_date >= start, FeeRecord.payment_date < end,
                FeeRecord.status == "paid",
            )
        )
        pending_r = await db.execute(
            select(func.sum(FeeRecord.amount)).where(
                FeeRecord.due_date >= start, FeeRecord.due_date < end
            )
        )
        return float(collected_r.scalar() or 0), float(pending_r.scalar() or 0)

    @staticmethod
    async def get_exam_analytics(db: AsyncSession) -> Tuple[List[Dict], List[Dict]]:
        avg_rows = await db.execute(
            select(Grade.grade_type, func.avg(Grade.score), func.count(Grade.id)).group_by(Grade.grade_type)
        )
        exam_types = [
            {"exam_type": row[0] or "unknown", "average_score": round(float(row[1] or 0), 2), "total_students": row[2]}
            for row in avg_rows
        ]

        dist_rows = await db.execute(
            select(Grade.grade, func.count(Grade.id)).group_by(Grade.grade)
        )
        distribution = [{"grade": row[0] or "N/A", "count": row[1]} for row in dist_rows]
        
        return exam_types, distribution
