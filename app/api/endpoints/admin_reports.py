"""
Admin Reports Section API

API endpoints for generating and exporting various reports.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, timedelta
import csv
import io
import json

from app.core.database import get_async_db
from app.models.models import User, Student, Attendance, FeeRecord, Grade
from app.api.deps.admin import get_current_admin


# Create router
router = APIRouter(prefix="/admin/reports", tags=["Admin Reports"])


# ============ STUDENT ATTENDANCE REPORT ============

@router.get("/attendance/students")
async def get_student_attendance_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    class_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate student attendance report"""
    
    # Placeholder data
    students = [
        {"student_id": 1, "name": "John Doe", "class": "Class 10-A", "present": 45, "absent": 3, "leave": 2, "percentage": 93.75},
        {"student_id": 2, "name": "Jane Smith", "class": "Class 10-A", "present": 48, "absent": 1, "leave": 1, "percentage": 96.00},
        {"student_id": 3, "name": "Mike Johnson", "class": "Class 10-B", "present": 42, "absent": 6, "leave": 2, "percentage": 84.00}
    ]
    
    return {
        "report_type": "attendance",
        "period": {"start": start_date, "end": end_date},
        "students": students,
        "summary": {
            "total_students": len(students),
            "avg_attendance": 91.25
        }
    }


# ============ FEE DUE REPORT ============

@router.get("/fees/due")
async def get_fee_due_report(
    class_id: Optional[int] = None,
    fee_type: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate fee due report"""
    
    return {
        "report_type": "fee_due",
        "due_fees": [
            {"student_id": 1, "name": "John Doe", "class": "Class 10-A", "fee_type": "Tuition", "amount_due": 5000, "due_date": "2024-01-31", "status": "pending"},
            {"student_id": 2, "name": "Jane Smith", "class": "Class 10-A", "fee_type": "Transport", "amount_due": 2000, "due_date": "2024-01-31", "status": "pending"},
            {"student_id": 3, "name": "Mike Johnson", "class": "Class 10-B", "fee_type": "Tuition", "amount_due": 5000, "due_date": "2024-01-31", "status": "overdue"}
        ],
        "summary": {
            "total_due": 12000,
            "pending": 2,
            "overdue": 1
        }
    }


# ============ TEACHER PERFORMANCE REPORT ============

@router.get("/teachers/performance")
async def get_teacher_performance_report(
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate teacher performance report"""
    
    return {
        "report_type": "teacher_performance",
        "teachers": [
            {
                "teacher_id": 1,
                "name": "Mr. Sharma",
                "department": "Mathematics",
                "courses": 3,
                "avg_student_rating": 4.5,
                "classes_conducted": 45,
                "exams_conducted": 5,
                "attendance_avg": 95.0
            },
            {
                "teacher_id": 2,
                "name": "Mrs. Gupta",
                "department": "Science",
                "courses": 2,
                "avg_student_rating": 4.8,
                "classes_conducted": 40,
                "exams_conducted": 4,
                "attendance_avg": 92.5
            }
        ]
    }


# ============ EXAM PERFORMANCE REPORT ============

@router.get("/exams/performance")
async def get_exam_performance_report(
    exam_id: Optional[int] = None,
    class_id: Optional[int] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate exam performance report"""
    
    return {
        "report_type": "exam_performance",
        "exam": "Mid-Term 2024",
        "subjects": [
            {
                "subject": "Mathematics",
                "avg_score": 72.5,
                "highest_score": 98,
                "lowest_score": 35,
                "pass_percentage": 85.0,
                "grade_distribution": {"A": 15, "B": 25, "C": 30, "D": 20, "F": 10}
            },
            {
                "subject": "English",
                "avg_score": 68.0,
                "highest_score": 92,
                "lowest_score": 28,
                "pass_percentage": 78.0,
                "grade_distribution": {"A": 10, "B": 20, "C": 35, "D": 25, "F": 10}
            }
        ],
        "summary": {
            "total_students": 100,
            "avg_score": 70.25,
            "overall_pass": 81.5
        }
    }


# ============ LIBRARY OVERDUE REPORT ============

@router.get("/library/overdue")
async def get_library_overdue_report(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate library overdue books report"""
    
    return {
        "report_type": "library_overdue",
        "overdue_books": [
            {
                "book_id": 101,
                "title": "Introduction to Python",
                "student_id": 1,
                "student_name": "John Doe",
                "class": "Class 10-A",
                "due_date": "2024-01-10",
                "days_overdue": 5,
                "fine_amount": 50
            },
            {
                "book_id": 205,
                "title": "Physics Fundamentals",
                "student_id": 3,
                "student_name": "Mike Johnson",
                "class": "Class 10-B",
                "due_date": "2024-01-08",
                "days_overdue": 7,
                "fine_amount": 70
            }
        ],
        "summary": {
            "total_overdue": 2,
            "total_fine": 120
        }
    }


# ============ FINANCIAL REPORT ============

@router.get("/finance/summary")
async def get_financial_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Generate financial summary report"""
    
    return {
        "report_type": "finance",
        "period": {"start": start_date or "2024-01-01", "end": end_date or "2024-01-31"},
        "income": {
            "tuition_fees": 500000,
            "transport_fees": 100000,
            "exam_fees": 50000,
            "library_fines": 5000,
            "total": 655000
        },
        "expenses": {
            "salaries": 300000,
            "maintenance": 50000,
            "utilities": 30000,
            "supplies": 20000,
            "total": 400000
        },
        "net_income": 255000
    }


# ============ EXPORT CSV ============

@router.get("/export/csv")
async def export_report_csv(
    report_type: str,  # attendance, fees, teachers, exams, library, finance
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Export report as CSV"""
    
    # Generate CSV content based on report type
    output = io.StringIO()
    writer = csv.writer(output)
    
    if report_type == "attendance":
        writer.writerow(["Student ID", "Name", "Class", "Present", "Absent", "Leave", "Percentage"])
        writer.writerow([1, "John Doe", "Class 10-A", 45, 3, 2, 93.75])
        writer.writerow([2, "Jane Smith", "Class 10-A", 48, 1, 1, 96.00])
    elif report_type == "fees":
        writer.writerow(["Student ID", "Name", "Class", "Fee Type", "Amount Due", "Status"])
        writer.writerow([1, "John Doe", "Class 10-A", "Tuition", 5000, "pending"])
    
    csv_content = output.getvalue()
    
    return {
        "report_type": report_type,
        "format": "csv",
        "content": csv_content,
        "filename": f"{report_type}_report.csv"
    }


# ============ EXPORT PDF (placeholder) ============

@router.get("/export/pdf")
async def export_report_pdf(
    report_type: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Export report as PDF (placeholder)"""
    
    return {
        "report_type": report_type,
        "format": "pdf",
        "message": "PDF generation requires additional libraries (e.g., ReportLab, WeasyPrint)",
        "download_url": f"/api/admin/reports/download/pdf/{report_type}"
    }


# ============ COMPREHENSIVE REPORT ============

@router.get("/comprehensive")
async def get_comprehensive_report(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_admin)
):
    """Get comprehensive school report"""
    
    return {
        "generated_at": datetime.utcnow().isoformat(),
        "academic_year": "2023-2024",
        "total_students": 500,
        "total_teachers": 50,
        "attendance_avg": 91.5,
        "exam_pass_rate": 85.0,
        "fee_collection_rate": 92.0,
        "library_books_issued": 350,
        "top_performing_class": "Class 10-A",
        "revenue": {
            "total": 655000,
            "expenses": 400000,
            "profit": 255000
        }
    }
