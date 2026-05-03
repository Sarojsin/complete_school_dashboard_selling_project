"""
Admin Reports Section API

API endpoints for generating and exporting various reports.
"""

from datetime import date, datetime, timedelta
from typing import Optional
import csv
import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, desc
from sqlalchemy.orm import joinedload

from backup.core.database import get_async_db
from backup.models.models import User, Student, Attendance, FeeRecord, Grade, Course, Teacher
from backup.models.exam_models import ExamResult
from backup.models.library_models import BookLoan, Book
from backup.api.deps.admin import get_current_admin

router = APIRouter(prefix="/admin/reports", tags=["Admin Reports"])


def _parse_date(value: Optional[str], default: date) -> date:
    if not value:
        return default
    try:
        return datetime.fromisoformat(value).date()
    except Exception:
        return default


def _to_iso(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value


def _render_pdf(title: str, lines: list[str]) -> bytes:
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
    except Exception as exc:
        raise HTTPException(status_code=501, detail="PDF generation requires reportlab") from exc

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, title)
    y -= 24
    c.setFont("Helvetica", 10)
    for line in lines:
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(50, y, line)
        y -= 14
    c.save()
    return buffer.getvalue()


# ============ STUDENT ATTENDANCE REPORT ============

@router.get("/attendance/students")
async def get_student_attendance_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    class_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Generate student attendance report"""
    end = _parse_date(end_date, date.today())
    start = _parse_date(start_date, end - timedelta(days=30))

    present_case = case((Attendance.status == "present", 1), else_=0)
    absent_case = case((Attendance.status == "absent", 1), else_=0)
    late_case = case((Attendance.status == "late", 1), else_=0)

    query = (
        select(
            Attendance.student_id,
            Student.full_name,
            Student.grade_level,
            func.sum(present_case).label("present"),
            func.sum(absent_case).label("absent"),
            func.sum(late_case).label("late"),
            func.count(Attendance.id).label("total"),
        )
        .join(Student, Student.id == Attendance.student_id)
        .where(Attendance.date >= start, Attendance.date <= end)
        .group_by(Attendance.student_id, Student.full_name, Student.grade_level)
        .order_by(Student.full_name)
    )

    if class_id is not None:
        query = query.where(Attendance.course_id == class_id)

    result = await db.execute(query)
    students = []
    for row in result.all():
        total = row.total or 0
        pct = round((row.present / total * 100), 2) if total else 0.0
        students.append(
            {
                "student_id": row.student_id,
                "name": row.full_name,
                "class": row.grade_level or "N/A",
                "present": row.present or 0,
                "absent": row.absent or 0,
                "leave": row.late or 0,
                "percentage": pct,
            }
        )

    avg_attendance = round(sum(s["percentage"] for s in students) / len(students), 2) if students else 0.0
    return {
        "report_type": "attendance",
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "students": students,
        "summary": {"total_students": len(students), "avg_attendance": avg_attendance},
    }


# ============ FEE DUE REPORT ============

@router.get("/fees/due")
async def get_fee_due_report(
    class_id: Optional[int] = None,
    fee_type: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Generate fee due report"""
    query = (
        select(FeeRecord, Student)
        .join(Student, Student.id == FeeRecord.student_id)
        .where(FeeRecord.status.in_(["pending", "overdue", "partial"]))
        .order_by(FeeRecord.due_date.asc())
    )
    if fee_type:
        query = query.where(FeeRecord.fee_type == fee_type)
    if class_id is not None:
        query = query.where(Student.grade_level == str(class_id))

    result = await db.execute(query)
    rows = result.all()
    due_fees = []
    for record, student in rows:
        due_fees.append(
            {
                "student_id": record.student_id,
                "name": student.full_name,
                "class": student.grade_level,
                "fee_type": record.fee_type,
                "amount_due": record.amount - record.paid_amount,
                "due_date": record.due_date.isoformat() if record.due_date else None,
                "status": record.status,
            }
        )

    pending = len([d for d in due_fees if d["status"] == "pending"])
    overdue = len([d for d in due_fees if d["status"] == "overdue"])
    total_due = round(sum(d["amount_due"] for d in due_fees), 2)
    return {
        "report_type": "fee_due",
        "due_fees": due_fees,
        "summary": {"total_due": total_due, "pending": pending, "overdue": overdue},
    }


# ============ TEACHER PERFORMANCE REPORT ============

@router.get("/teachers/performance")
async def get_teacher_performance_report(
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Generate teacher performance report"""
    teacher_query = select(Teacher).order_by(Teacher.full_name)
    if department_id is not None:
        teacher_query = teacher_query.where(Teacher.department_id == department_id)
    teachers = (await db.execute(teacher_query)).scalars().all()

    # Course counts per teacher
    course_counts = dict(
        (await db.execute(select(Course.teacher_id, func.count(Course.id)).group_by(Course.teacher_id))).all()
    )

    # Grade averages per teacher
    grade_stats = dict(
        (
            await db.execute(
                select(
                    Course.teacher_id,
                    func.avg((Grade.score / Grade.max_score) * 100).label("avg"),
                )
                .join(Course, Course.id == Grade.course_id)
                .group_by(Course.teacher_id)
            )
        ).all()
    )

    # Attendance stats per teacher
    attendance_stats = dict(
        (
            await db.execute(
                select(
                    Course.teacher_id,
                    func.sum(case((Attendance.status == "present", 1), else_=0)).label("present"),
                    func.count(Attendance.id).label("total"),
                )
                .join(Course, Course.id == Attendance.course_id)
                .group_by(Course.teacher_id)
            )
        ).all()
    )

    # Exam counts per teacher
    exam_counts = dict(
        (
            await db.execute(
                select(Course.teacher_id, func.count(ExamResult.id))
                .join(Course, Course.id == ExamResult.course_id)
                .group_by(Course.teacher_id)
            )
        ).all()
    )

    report = []
    for t in teachers:
        avg_pct = grade_stats.get(t.id, 0) or 0
        rating = round(min(5.0, max(0.0, avg_pct / 20)), 2)
        present, total = attendance_stats.get(t.id, (0, 0))
        attendance_pct = round((present / total * 100), 2) if total else 0.0
        report.append(
            {
                "teacher_id": t.id,
                "name": t.full_name,
                "department": t.department,
                "courses": course_counts.get(t.id, 0),
                "avg_student_rating": rating,
                "classes_conducted": total,
                "exams_conducted": exam_counts.get(t.id, 0),
                "attendance_avg": attendance_pct,
            }
        )

    return {"report_type": "teacher_performance", "teachers": report}


# ============ EXAM PERFORMANCE REPORT ============

@router.get("/exams/performance")
async def get_exam_performance_report(
    exam_id: Optional[int] = None,
    class_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Generate exam performance report"""
    query = select(ExamResult).options(joinedload(ExamResult.course))
    if exam_id is not None:
        query = query.where(ExamResult.course_id == exam_id)
    if class_id is not None:
        query = query.join(Student, Student.id == ExamResult.student_id).where(Student.grade_level == str(class_id))

    rows = (await db.execute(query)).scalars().all()
    if not rows:
        return {"report_type": "exam_performance", "subjects": [], "summary": {"total_students": 0, "avg_score": 0, "overall_pass": 0}}

    subjects = {}
    for r in rows:
        course_name = r.course.course_name if r.course else "Unknown"
        subjects.setdefault(course_name, []).append(r)

    subject_reports = []
    total_scores = 0
    total_students = 0
    total_pass = 0
    for subject, items in subjects.items():
        scores = [i.marks for i in items if i.marks is not None]
        max_marks = [i.max_marks for i in items if i.max_marks is not None]
        if scores:
            avg_score = sum(scores) / len(scores)
            highest = max(scores)
            lowest = min(scores)
        else:
            avg_score = highest = lowest = 0
        pass_count = 0
        for i in items:
            max_mark = i.max_marks or 100
            if max_mark and i.marks is not None and (i.marks / max_mark * 100) >= 40:
                pass_count += 1
        pass_pct = round((pass_count / len(items) * 100), 2) if items else 0
        total_scores += sum(scores)
        total_students += len(items)
        total_pass += pass_count

        subject_reports.append(
            {
                "subject": subject,
                "avg_score": round(avg_score, 2),
                "highest_score": highest,
                "lowest_score": lowest,
                "pass_percentage": pass_pct,
                "grade_distribution": {},
            }
        )

    avg_score = round((total_scores / total_students), 2) if total_students else 0
    overall_pass = round((total_pass / total_students * 100), 2) if total_students else 0

    return {
        "report_type": "exam_performance",
        "exam": "Course Exam",
        "subjects": subject_reports,
        "summary": {
            "total_students": total_students,
            "avg_score": avg_score,
            "overall_pass": overall_pass,
        },
    }


# ============ LIBRARY OVERDUE REPORT ============

@router.get("/library/overdue")
async def get_library_overdue_report(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Generate library overdue books report"""
    today = date.today()
    result = await db.execute(
        select(BookLoan)
        .options(joinedload(BookLoan.book), joinedload(BookLoan.student))
        .where(BookLoan.return_date.is_(None))
    )
    loans = result.scalars().all()

    overdue_books = []
    total_fine = 0
    for loan in loans:
        if loan.due_date and loan.due_date < today:
            days_overdue = (today - loan.due_date).days
            fine_amount = loan.fine_amount or 0
            total_fine += fine_amount
            overdue_books.append(
                {
                    "book_id": loan.book_id,
                    "title": loan.book.title if loan.book else loan.book_title,
                    "student_id": loan.student_id,
                    "student_name": loan.student.full_name if loan.student else None,
                    "class": loan.student.grade_level if loan.student else None,
                    "due_date": loan.due_date.isoformat(),
                    "days_overdue": days_overdue,
                    "fine_amount": fine_amount,
                }
            )

    return {
        "report_type": "library_overdue",
        "overdue_books": overdue_books,
        "summary": {"total_overdue": len(overdue_books), "total_fine": total_fine},
    }


# ============ FINANCIAL REPORT ============

@router.get("/finance/summary")
async def get_financial_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Generate financial summary report"""
    end = _parse_date(end_date, date.today())
    start = _parse_date(start_date, end - timedelta(days=30))

    collected_result = await db.execute(
        select(func.sum(FeeRecord.paid_amount)).where(
            FeeRecord.payment_date >= start, FeeRecord.payment_date <= end
        )
    )
    total_collected = float(collected_result.scalar() or 0)

    pending_result = await db.execute(
        select(func.sum(FeeRecord.amount - FeeRecord.paid_amount)).where(
            FeeRecord.status.in_(["pending", "overdue", "partial"])
        )
    )
    total_pending = float(pending_result.scalar() or 0)

    return {
        "report_type": "finance",
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "income": {
            "total": round(total_collected, 2),
        },
        "expenses": {"total": 0},
        "net_income": round(total_collected, 2),
        "pending_total": round(total_pending, 2),
    }


# ============ EXPORT CSV ============

@router.get("/export/csv")
async def export_report_csv(
    report_type: str,  # attendance, fees, teachers, exams, library, finance
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Export report as CSV"""
    output = io.StringIO()
    writer = csv.writer(output)

    if report_type == "attendance":
        data = await get_student_attendance_report(start_date, end_date, None, db, current_user)
        writer.writerow(["Student ID", "Name", "Class", "Present", "Absent", "Leave", "Percentage"])
        for row in data["students"]:
            writer.writerow([row["student_id"], row["name"], row["class"], row["present"], row["absent"], row["leave"], row["percentage"]])
    elif report_type == "fees":
        data = await get_fee_due_report(None, None, db, current_user)
        writer.writerow(["Student ID", "Name", "Class", "Fee Type", "Amount Due", "Status"])
        for row in data["due_fees"]:
            writer.writerow([row["student_id"], row["name"], row["class"], row["fee_type"], row["amount_due"], row["status"]])
    elif report_type == "teachers":
        data = await get_teacher_performance_report(None, db, current_user)
        writer.writerow(["Teacher ID", "Name", "Department", "Courses", "Avg Rating", "Classes", "Exams", "Attendance Avg"])
        for row in data["teachers"]:
            writer.writerow([row["teacher_id"], row["name"], row["department"], row["courses"], row["avg_student_rating"], row["classes_conducted"], row["exams_conducted"], row["attendance_avg"]])
    elif report_type == "exams":
        data = await get_exam_performance_report(None, None, db, current_user)
        writer.writerow(["Subject", "Avg Score", "Highest", "Lowest", "Pass %"])
        for row in data["subjects"]:
            writer.writerow([row["subject"], row["avg_score"], row["highest_score"], row["lowest_score"], row["pass_percentage"]])
    elif report_type == "library":
        data = await get_library_overdue_report(db, current_user)
        writer.writerow(["Book ID", "Title", "Student ID", "Student Name", "Class", "Due Date", "Days Overdue", "Fine"])
        for row in data["overdue_books"]:
            writer.writerow([row["book_id"], row["title"], row["student_id"], row["student_name"], row["class"], row["due_date"], row["days_overdue"], row["fine_amount"]])
    elif report_type == "finance":
        data = await get_financial_report(start_date, end_date, db, current_user)
        writer.writerow(["Period Start", "Period End", "Total Collected", "Total Pending", "Net Income"])
        writer.writerow([data["period"]["start"], data["period"]["end"], data["income"]["total"], data["pending_total"], data["net_income"]])
    else:
        raise HTTPException(status_code=400, detail="Invalid report_type")

    return {
        "report_type": report_type,
        "format": "csv",
        "content": output.getvalue(),
        "filename": f"{report_type}_report.csv",
    }


# ============ EXPORT PDF ============

@router.get("/export/pdf")
async def export_report_pdf(
    report_type: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Export report as PDF"""
    lines = []
    if report_type == "attendance":
        data = await get_student_attendance_report(start_date, end_date, None, db, current_user)
        lines.append(f"Students: {data['summary']['total_students']}")
        lines.append(f"Average Attendance: {data['summary']['avg_attendance']}")
    elif report_type == "fees":
        data = await get_fee_due_report(None, None, db, current_user)
        lines.append(f"Total Due: {data['summary']['total_due']}")
        lines.append(f"Pending: {data['summary']['pending']}")
        lines.append(f"Overdue: {data['summary']['overdue']}")
    elif report_type == "teachers":
        data = await get_teacher_performance_report(None, db, current_user)
        lines.append(f"Teachers: {len(data['teachers'])}")
    elif report_type == "exams":
        data = await get_exam_performance_report(None, None, db, current_user)
        lines.append(f"Total Students: {data['summary']['total_students']}")
        lines.append(f"Overall Pass: {data['summary']['overall_pass']}")
    elif report_type == "library":
        data = await get_library_overdue_report(db, current_user)
        lines.append(f"Overdue Books: {data['summary']['total_overdue']}")
        lines.append(f"Total Fine: {data['summary']['total_fine']}")
    elif report_type == "finance":
        data = await get_financial_report(start_date, end_date, db, current_user)
        lines.append(f"Total Collected: {data['income']['total']}")
        lines.append(f"Total Pending: {data['pending_total']}")
    else:
        raise HTTPException(status_code=400, detail="Invalid report_type")

    pdf_bytes = _render_pdf(f"{report_type.title()} Report", lines)
    return Response(content=pdf_bytes, media_type="application/pdf")


# ============ COMPREHENSIVE REPORT ============

@router.get("/comprehensive")
async def get_comprehensive_report(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin),
):
    """Get comprehensive school report"""
    students_count = (await db.execute(select(func.count(Student.id)))).scalar() or 0
    teachers_count = (await db.execute(select(func.count(Teacher.id)))).scalar() or 0
    attendance_avg = (await get_student_attendance_report(None, None, None, db, current_user))["summary"]["avg_attendance"]
    exams_summary = await get_exam_performance_report(None, None, db, current_user)
    fee_summary = await get_financial_report(None, None, db, current_user)

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "academic_year": str(date.today().year),
        "total_students": students_count,
        "total_teachers": teachers_count,
        "attendance_avg": attendance_avg,
        "exam_pass_rate": exams_summary["summary"].get("overall_pass", 0),
        "fee_collection_rate": None,
        "library_books_issued": None,
        "revenue": {
            "total": fee_summary["income"]["total"],
            "expenses": fee_summary["expenses"]["total"],
            "profit": fee_summary["net_income"],
        },
    }
