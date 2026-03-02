from datetime import date, datetime, timedelta
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
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
    async def get_attendance_analytics() -> Dict[str, Any]:
        return {
            "overall_percentage": 87.5,
            "by_grade": [
                {"grade": "Grade 10", "percentage": 89.2},
                {"grade": "Grade 11", "percentage": 85.7},
                {"grade": "Grade 12", "percentage": 88.1},
            ],
            "weekly_trend": [
                {"day": "Mon", "percentage": 92.0},
                {"day": "Tue", "percentage": 88.5},
                {"day": "Wed", "percentage": 85.0},
                {"day": "Thu", "percentage": 87.2},
                {"day": "Fri", "percentage": 84.8},
            ],
        }

    @staticmethod
    async def get_exam_analytics(db: AsyncSession) -> Dict[str, Any]:
        exam_types, distribution = await DashboardRepository.get_exam_analytics(db)
        return {"by_exam_type": exam_types, "distribution": distribution}

    @staticmethod
    async def get_analytics_summary(db: AsyncSession) -> Dict[str, Any]:
        enrollment = await DashboardService.get_enrollment_analytics(db, "yearly")
        fees       = await DashboardService.get_fee_analytics(db, "yearly")
        attendance = await DashboardService.get_attendance_analytics()
        exams      = await DashboardService.get_exam_analytics(db)
        return {"enrollment": enrollment, "fees": fees, "attendance": attendance, "exams": exams}
