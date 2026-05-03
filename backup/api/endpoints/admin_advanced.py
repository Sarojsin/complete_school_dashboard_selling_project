"""
Admin Advanced Features API

API endpoints for analytics, alerts, and automation.
"""

from datetime import date, datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, desc

from backup.core.database import get_async_db
from backup.models.models import User, Student, Grade, Attendance, FeeRecord, Course, Message, Note, Video
from backup.models.admin_models import LoginHistory
from backup.api.deps.admin import get_current_admin
from backup.repositories.admin_settings_repository import AdminSettingsRepository

router = APIRouter(prefix="/admin/advanced", tags=["Admin Advanced"])


async def _get_setting(db: AsyncSession, key: str, default: dict) -> dict:
    return await AdminSettingsRepository.get_setting_value(db, key, default)


async def _update_setting(db: AsyncSession, key: str, updates: dict, updated_by: int) -> dict:
    current = await _get_setting(db, key, {})
    current.update({k: v for k, v in updates.items() if v is not None})
    await AdminSettingsRepository.upsert_setting(db, key, current, updated_by=updated_by)
    return current


async def _student_metrics(db: AsyncSession) -> dict:
    grade_avg = dict(
        (
            await db.execute(
                select(
                    Grade.student_id,
                    func.avg((Grade.score / Grade.max_score) * 100),
                    func.count(Grade.id),
                ).group_by(Grade.student_id)
            )
        ).all()
    )

    present_case = case((Attendance.status == "present", 1), else_=0)
    start = date.today() - timedelta(days=30)
    attendance = dict(
        (
            await db.execute(
                select(
                    Attendance.student_id,
                    func.sum(present_case),
                    func.count(Attendance.id),
                )
                .where(Attendance.date >= start)
                .group_by(Attendance.student_id)
            )
        ).all()
    )

    fee_alerts = dict(
        (
            await db.execute(
                select(FeeRecord.student_id, func.count(FeeRecord.id))
                .where(FeeRecord.status.in_(["pending", "overdue", "partial"]))
                .group_by(FeeRecord.student_id)
            )
        ).all()
    )

    return {"grades": grade_avg, "attendance": attendance, "fees": fee_alerts}


# ============ AI STUDENT PERFORMANCE PREDICTION ============

@router.get("/ai/performance-prediction")
async def get_performance_predictions(
    student_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get heuristic performance predictions"""
    metrics = await _student_metrics(db)
    students_query = select(Student)
    if student_id is not None:
        students_query = students_query.where(Student.id == student_id)
    students = (await db.execute(students_query)).scalars().all()

    predictions = []
    for s in students:
        avg_score, grade_count = metrics["grades"].get(s.id, (0, 0))
        present, total = metrics["attendance"].get(s.id, (0, 0))
        attendance_pct = (present / total * 100) if total else 0
        predicted = round((avg_score * 0.7) + (attendance_pct * 0.3), 2)
        confidence = min(95.0, 50.0 + (grade_count * 2))
        factors = []
        if attendance_pct < 75:
            factors.append("low_attendance")
        if avg_score < 60:
            factors.append("low_scores")
        recommendations = []
        if avg_score < 60:
            recommendations.append("Focus on weak subjects")
        if attendance_pct < 75:
            recommendations.append("Improve attendance")
        if not recommendations:
            recommendations.append("Maintain current performance")

        predictions.append(
            {
                "student_id": s.id,
                "student_name": s.full_name,
                "current_avg": round(avg_score, 2),
                "predicted_next_exam": predicted,
                "confidence": round(confidence, 2),
                "factors": factors or ["attendance", "previous_scores"],
                "recommendations": recommendations,
            }
        )

    return {
        "predictions": predictions,
        "model_accuracy": 0.0,
        "last_trained": None,
    }


@router.get("/ai/at-risk-students")
async def get_at_risk_students(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get students at risk of poor performance"""
    metrics = await _student_metrics(db)
    students = (await db.execute(select(Student))).scalars().all()

    at_risk = []
    for s in students:
        avg_score, _ = metrics["grades"].get(s.id, (0, 0))
        present, total = metrics["attendance"].get(s.id, (0, 0))
        attendance_pct = (present / total * 100) if total else 0
        reasons = []
        if avg_score < 60:
            reasons.append("low_scores")
        if attendance_pct < 75:
            reasons.append("low_attendance")
        if reasons:
            at_risk.append(
                {
                    "student_id": s.id,
                    "name": s.full_name,
                    "class": s.grade_level,
                    "risk_level": "high" if avg_score < 50 else "medium",
                    "current_avg": round(avg_score, 2),
                    "reasons": reasons,
                    "intervention_recommended": "Counseling + Tutoring" if avg_score < 60 else "Extra assignments",
                }
            )

    return {"at_risk_students": at_risk, "total_at_risk": len(at_risk)}


# ============ RISK DETECTION & ALERTS ============

@router.get("/alerts/attendance")
async def get_attendance_alerts(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    metrics = await _student_metrics(db)
    students = (await db.execute(select(Student))).scalars().all()

    alerts = []
    for s in students:
        present, total = metrics["attendance"].get(s.id, (0, 0))
        attendance_pct = (present / total * 100) if total else 0
        if attendance_pct < 75:
            alerts.append(
                {
                    "id": s.id,
                    "student_id": s.id,
                    "student_name": s.full_name,
                    "class": s.grade_level,
                    "attendance_percentage": round(attendance_pct, 2),
                    "threshold": 75.0,
                    "days_below_threshold": 30,
                    "alert_level": "high" if attendance_pct < 60 else "medium",
                    "created_at": datetime.utcnow().isoformat(),
                }
            )

    return {"alerts": alerts, "summary": {"high": len([a for a in alerts if a["alert_level"] == "high"]), "medium": len([a for a in alerts if a["alert_level"] == "medium"]), "low": 0}}


@router.get("/alerts/fees")
async def get_fee_alerts(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    result = await db.execute(
        select(FeeRecord).where(FeeRecord.status.in_(["pending", "overdue", "partial"]))
    )
    records = result.scalars().all()
    alerts = [
        {
            "id": r.id,
            "student_id": r.student_id,
            "student_name": r.student.user.full_name if r.student and r.student.user else None,
            "fee_type": r.fee_type,
            "amount_due": r.amount - r.paid_amount,
            "due_date": r.due_date.isoformat() if r.due_date else None,
            "days_overdue": (date.today() - r.due_date).days if r.due_date and r.due_date < date.today() else 0,
            "alert_level": "high" if r.status == "overdue" else "medium",
        }
        for r in records
    ]
    return {"alerts": alerts}


@router.get("/alerts/performance")
async def get_performance_alerts(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    metrics = await _student_metrics(db)
    students = (await db.execute(select(Student))).scalars().all()
    alerts = []
    for s in students:
        avg_score, _ = metrics["grades"].get(s.id, (0, 0))
        if avg_score < 60:
            alerts.append(
                {
                    "id": s.id,
                    "student_id": s.id,
                    "student_name": s.full_name,
                    "subject": "Overall",
                    "previous_avg": avg_score,
                    "current_avg": avg_score,
                    "decline_percentage": 0,
                    "alert_level": "medium" if avg_score >= 50 else "high",
                }
            )
    return {"alerts": alerts}


# ============ AUTO NOTIFICATION SYSTEM ============

@router.get("/notifications/automations")
async def get_notification_automations(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    default = {
        "automations": [
            {
                "id": 1,
                "name": "Fee Due Reminder",
                "trigger": "3_days_before_due",
                "recipients": ["parent"],
                "channel": ["email", "sms"],
                "enabled": True,
            }
        ]
    }
    return await _get_setting(db, "notification_automations", default)


@router.post("/notifications/automations")
async def create_notification_automation(
    name: str,
    trigger: str,
    recipients: List[str],
    channel: List[str],
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    data = await _get_setting(db, "notification_automations", {"automations": []})
    automations = data.get("automations", [])
    next_id = max([a.get("id", 0) for a in automations], default=0) + 1
    automations.append(
        {
            "id": next_id,
            "name": name,
            "trigger": trigger,
            "recipients": recipients,
            "channel": channel,
            "enabled": True,
        }
    )
    updated = await _update_setting(db, "notification_automations", {"automations": automations}, updated_by=current_user.id)
    return {"success": True, "message": "Automation created", "automation_id": next_id, "automations": updated.get("automations", [])}


@router.patch("/notifications/automations/{automation_id}")
async def update_notification_automation(
    automation_id: int,
    enabled: Optional[bool] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    data = await _get_setting(db, "notification_automations", {"automations": []})
    automations = data.get("automations", [])
    for a in automations:
        if a.get("id") == automation_id and enabled is not None:
            a["enabled"] = enabled
    updated = await _update_setting(db, "notification_automations", {"automations": automations}, updated_by=current_user.id)
    return {"success": True, "message": "Automation updated", "automations": updated.get("automations", [])}


# ============ SMS/EMAIL BROADCAST ============

@router.post("/broadcast/sms")
async def send_sms_broadcast(
    message: str,
    recipients: str,  # all, students, teachers, parents
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    count = (await db.execute(select(func.count(User.id)))).scalar() or 0
    history = await _get_setting(db, "broadcast_history", {"items": []})
    items = history.get("items", [])
    items.append({"id": len(items) + 1, "type": "sms", "subject": message[:20], "recipients": count, "sent_at": datetime.utcnow().isoformat(), "status": "queued"})
    await _update_setting(db, "broadcast_history", {"items": items[-100:]}, updated_by=current_user.id)
    return {"success": True, "message": "SMS broadcast queued", "recipients_count": count, "estimated_cost": count * 1.0}


@router.post("/broadcast/email")
async def send_email_broadcast(
    subject: str,
    body: str,
    recipients: str,  # all, students, teachers, parents
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    count = (await db.execute(select(func.count(User.id)))).scalar() or 0
    history = await _get_setting(db, "broadcast_history", {"items": []})
    items = history.get("items", [])
    items.append({"id": len(items) + 1, "type": "email", "subject": subject, "recipients": count, "sent_at": datetime.utcnow().isoformat(), "status": "queued"})
    await _update_setting(db, "broadcast_history", {"items": items[-100:]}, updated_by=current_user.id)
    return {"success": True, "message": "Email broadcast queued", "recipients_count": count}


@router.get("/broadcast/history")
async def get_broadcast_history(
    channel: Optional[str] = None,  # sms, email
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    history = await _get_setting(db, "broadcast_history", {"items": []})
    items = history.get("items", [])
    if channel:
        items = [i for i in items if i.get("type") == channel]
    items = items[::-1][skip : skip + limit]
    return {"broadcasts": items}


# ============ MULTI-SCHOOL SUPPORT ============

@router.get("/multi-school/schools")
async def get_schools(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    data = await _get_setting(db, "schools", {"schools": []})
    return data


@router.post("/multi-school/schools")
async def create_school(
    name: str,
    code: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    data = await _get_setting(db, "schools", {"schools": []})
    schools = data.get("schools", [])
    next_id = max([s.get("id", 0) for s in schools], default=0) + 1
    schools.append({"id": next_id, "name": name, "code": code, "status": "active"})
    updated = await _update_setting(db, "schools", {"schools": schools}, updated_by=current_user.id)
    return {"success": True, "message": "School created", "school_id": next_id, "schools": updated.get("schools", [])}


# ============ ANALYTICS DASHBOARD ============

@router.get("/analytics/dashboard")
async def get_advanced_analytics(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    # Enrollment trends (last 6 months)
    today = date.today()
    enrollment_trends = []
    for i in range(5, -1, -1):
        month_start = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        count = (await db.execute(
            select(func.count(Student.id)).where(Student.enrollment_date >= month_start, Student.enrollment_date < month_end)
        )).scalar() or 0
        enrollment_trends.append({"month": month_start.strftime("%b"), "students": count})

    # Performance trends by course
    perf_rows = await db.execute(
        select(Course.course_name, func.avg((Grade.score / Grade.max_score) * 100))
        .join(Course, Course.id == Grade.course_id)
        .group_by(Course.course_name)
        .order_by(desc(func.avg((Grade.score / Grade.max_score) * 100)))
        .limit(4)
    )
    perf_trends = [{"name": row[0], "avg_score": round(row[1] or 0, 2)} for row in perf_rows]

    # Engagement metrics
    login_cutoff = datetime.utcnow() - timedelta(days=30)
    active_users = (await db.execute(
        select(func.count(func.distinct(LoginHistory.user_id))).where(LoginHistory.created_at >= login_cutoff)
    )).scalar() or 0
    messages_count = (await db.execute(select(func.count(Message.id)))).scalar() or 0
    content_views = (await db.execute(select(func.count(Note.id)))).scalar() or 0
    content_views += (await db.execute(select(func.count(Video.id)))).scalar() or 0

    metrics = {
        "avg_daily_active_users": round(active_users / 30, 2),
        "avg_time_on_platform_minutes": None,
        "content_views": content_views,
        "chat_messages": messages_count,
    }

    at_risk_count = (await get_at_risk_students(db, current_user))["total_at_risk"]
    pending_revenue = (await db.execute(
        select(func.sum(FeeRecord.amount - FeeRecord.paid_amount)).where(FeeRecord.status.in_(["pending", "overdue", "partial"]))
    )).scalar() or 0

    return {
        "enrollment_trends": {"last_6_months": enrollment_trends},
        "performance_trends": {"subjects": perf_trends},
        "engagement_metrics": metrics,
        "predictions": {
            "next_month_enrollment": enrollment_trends[-1]["students"] if enrollment_trends else 0,
            "expected_revenue": round(float(pending_revenue), 2),
            "at_risk_students": at_risk_count,
        },
    }
