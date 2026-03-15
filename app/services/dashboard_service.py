from datetime import date, datetime, timedelta
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case

from app.models.models import User, Attendance, Student
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.feature_repository import FeatureRepository

class DashboardService:
    """Handles business logic for the admin dashboard, decoupling routes from DB queries."""

    @staticmethod
    def _month_range(months_ago: int) -> tuple[date, date]:
        """Return (month_start, month_end) for a month that is ``months_ago`` months back."""
        today = date.today()
        # We step back by ~30-day intervals from the 1st of this month
        approx = today.replace(day=1) - timedelta(days=months_ago * 30)
        start = approx.replace(day=1)
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)
        return start, end

    @staticmethod
    async def get_dashboard_summary(db: AsyncSession, current_user: User) -> Dict[str, Any]:
        user_counts = await DashboardRepository.get_user_role_counts(db)
        total_users = sum(user_counts.values())
        active_users = await DashboardRepository.get_active_users_count(db)
        
        total_features, enabled_features = await DashboardRepository.get_features_counts(db)
        category_counts = await DashboardRepository.get_feature_category_counts(db)

        return {
            "users": {"total": total_users, "active": active_users, "by_role": user_counts},
            "features": {
                "total": total_features,
                "enabled": enabled_features,
                "disabled": total_features - enabled_features,
                "by_category": category_counts,
            },
            "welcome": f"Welcome, {current_user.full_name}!",
        }

    @staticmethod
    async def get_system_stats(db: AsyncSession) -> Dict[str, Any]:
        total, active, students, teachers, authorities = await DashboardRepository.get_user_stats(db)
        return {
            "users": {
                "total": total,
                "active": active,
                "inactive": total - active,
                "students": students,
                "teachers": teachers,
                "authorities": authorities,
            }
        }

    @staticmethod
    async def get_users_by_role(db: AsyncSession) -> Dict[str, Any]:
        user_counts = await DashboardRepository.get_user_role_counts(db)
        return {"users_by_role": user_counts}

    @staticmethod
    async def get_dashboard_overview(db: AsyncSession) -> Dict[str, Any]:
        overview = await DashboardRepository.get_overview_metrics(db)
        return {
            "overview": overview,
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    async def get_features_summary(db: AsyncSession) -> Dict[str, Any]:
        total, enabled = await DashboardRepository.get_features_counts(db)
        summary = await DashboardRepository.get_features_summary(db)
        
        return {
            "total":                   total,
            "enabled":                 enabled,
            "disabled":                total - enabled,
            "global_features":         summary["global_features"],
            "role_specific_features":  total - summary["global_features"],
            "by_category":             summary["by_category"],
        }

    @staticmethod
    async def get_enabled_features(db: AsyncSession, category: Optional[str] = None) -> Dict[str, Any]:
        features = await FeatureRepository.get_all(db, category=category, enabled_only=True)
        return {
            "features": [
                {"id": f.id, "feature_code": f.feature_code, "feature_name": f.feature_name,
                 "feature_category": f.feature_category, "is_global": f.is_global}
                for f in features
            ],
            "total": len(features),
        }

    @staticmethod
    async def get_disabled_features(db: AsyncSession, category: Optional[str] = None) -> Dict[str, Any]:
        all_features = await FeatureRepository.get_all(db, category=category)
        disabled = [f for f in all_features if not f.is_enabled]
        return {
            "features": [
                {"id": f.id, "feature_code": f.feature_code, "feature_name": f.feature_name,
                 "feature_category": f.feature_category, "is_global": f.is_global}
                for f in disabled
            ],
            "total": len(disabled),
        }

    @staticmethod
    async def get_enrollment_analytics(db: AsyncSession, period: str) -> Dict[str, Any]:
        if period == "yearly":
            data = []
            for i in range(11, -1, -1):
                start, end = DashboardService._month_range(i)
                count = await DashboardRepository.count_enrollments_in_range(db, start, end)
                data.append({"month": start.strftime("%b %Y"), "count": count})
            return {"period": "yearly", "data": data}

        # monthly — last 30 days
        data = []
        for i in range(29, -1, -1):
            day = date.today() - timedelta(days=i)
            end = day + timedelta(days=1)
            count = await DashboardRepository.count_enrollments_in_range(db, day, end)
            data.append({"date": day.strftime("%d %b"), "count": count})
        return {"period": "monthly", "data": data}

    @staticmethod
    async def get_fee_analytics(db: AsyncSession, period: str) -> Dict[str, Any]:
        if period == "yearly":
            data = []
            for i in range(11, -1, -1):
                start, end = DashboardService._month_range(i)
                collected, pending = await DashboardRepository.aggregate_fees_in_range(db, start, end)
                data.append({
                    "month":     start.strftime("%b %Y"),
                    "collected": collected,
                    "pending":   pending,
                })
            return {"period": "yearly", "data": data}

        data = []
        for i in range(29, -1, -1):
            day = date.today() - timedelta(days=i)
            end = day + timedelta(days=1)
            collected, _ = await DashboardRepository.aggregate_fees_in_range(db, day, end)
            data.append({"date": day.strftime("%d %b"), "collected": collected})
        return {"period": "monthly", "data": data}

    @staticmethod
    async def get_attendance_analytics(db: AsyncSession) -> Dict[str, Any]:
        today = date.today()
        start = today - timedelta(days=30)

        present_case = case((Attendance.status == "present", 1), else_=0)

        # Overall attendance percentage for last 30 days
        overall_rows = await db.execute(
            select(
                func.sum(present_case).label("present"),
                func.count(Attendance.id).label("total"),
            ).where(Attendance.date >= start, Attendance.date <= today)
        )
        overall_present, overall_total = overall_rows.first() or (0, 0)
        overall_pct = round((overall_present / overall_total * 100), 2) if overall_total else 0.0

        # By grade
        grade_rows = await db.execute(
            select(
                Student.grade_level,
                func.sum(present_case).label("present"),
                func.count(Attendance.id).label("total"),
            )
            .join(Student, Student.id == Attendance.student_id)
            .where(Attendance.date >= start, Attendance.date <= today)
            .group_by(Student.grade_level)
        )
        by_grade = []
        for grade_level, present, total in grade_rows:
            pct = round((present / total * 100), 2) if total else 0.0
            label = grade_level or "N/A"
            by_grade.append({"grade": label, "percentage": pct})

        # Weekly trend (last 7 days)
        trend_start = today - timedelta(days=6)
        trend_rows = await db.execute(
            select(
                Attendance.date,
                func.sum(present_case).label("present"),
                func.count(Attendance.id).label("total"),
            )
            .where(Attendance.date >= trend_start, Attendance.date <= today)
            .group_by(Attendance.date)
        )
        trend_map = {row[0]: row for row in trend_rows}
        weekly_trend = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            present, total = 0, 0
            if day in trend_map:
                _, present, total = trend_map[day]
            pct = round((present / total * 100), 2) if total else 0.0
            weekly_trend.append({"day": day.strftime("%a"), "percentage": pct})

        return {
            "overall_percentage": overall_pct,
            "by_grade": by_grade,
            "weekly_trend": weekly_trend,
        }

    @staticmethod
    async def get_exam_analytics(db: AsyncSession) -> Dict[str, Any]:
        exam_types, distribution = await DashboardRepository.get_exam_analytics(db)
        return {"by_exam_type": exam_types, "distribution": distribution}

    @staticmethod
    async def get_analytics_summary(db: AsyncSession) -> Dict[str, Any]:
        enrollment = await DashboardService.get_enrollment_analytics(db, "yearly")
        fees       = await DashboardService.get_fee_analytics(db, "yearly")
        attendance = await DashboardService.get_attendance_analytics(db)
        exams      = await DashboardService.get_exam_analytics(db)
        return {"enrollment": enrollment, "fees": fees, "attendance": attendance, "exams": exams}
