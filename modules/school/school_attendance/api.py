"""
School Attendance API Routes

API endpoints for school attendance tracking and reports.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from datetime import datetime, date

from modules.shared.database import get_db
from modules.shared.models import User
from modules.auth.dependencies import get_current_user, require_school_portal, require_school_teacher
from modules.school.school_attendance.models import AttendanceSession, AttendanceRecord
# Import old Attendance model for compatibility with existing code
from modules.school.school_attendance.models import AttendanceRecord as Attendance

router = APIRouter(prefix="/attendance", tags=["School Attendance"], dependencies=[Depends(require_school_portal)])


@router.get("/dashboard")
async def get_attendance_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance dashboard with overview stats"""
    today = date.today()
    
    # Get today's attendance count
    today_count = await db.execute(
        select(func.count(Attendance.id)).where(
            Attendance.date == today
        )
    )
    
    # Get total students
    total_students = await db.execute(
        select(func.count(Attendance.student_id)).where(
            Attendance.date == today,
            Attendance.status == "present"
        )
    )
    
    return {
        "date": today.isoformat(),
        "attendance_taken": today_count.scalar() or 0,
        "present_today": total_students.scalar() or 0
    }


@router.get("/records")
async def get_attendance_records(
    student_id: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get attendance records with filters"""
    query = select(Attendance)
    
    if student_id:
        query = query.where(Attendance.student_id == student_id)
    if date_from:
        query = query.where(Attendance.date >= datetime.strptime(date_from, "%Y-%m-%d").date())
    if date_to:
        query = query.where(Attendance.date <= datetime.strptime(date_to, "%Y-%m-%d").date())
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    records = result.scalars().all()
    
    return {"records": [
        {
            "id": r.id,
            "student_id": r.student_id,
            "date": str(r.date) if r.date is not None else None,
            "status": r.status,
            "remarks": r.remarks
        }
        for r in records
    ]}


@router.get("/student/{student_id}/summary")
async def get_student_attendance_summary(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get attendance summary for a student"""
    # Get total present
    present = await db.execute(
        select(func.count(Attendance.id)).where(
            Attendance.student_id == student_id,
            Attendance.status == "present"
        )
    )
    
    # Get total absent
    absent = await db.execute(
        select(func.count(Attendance.id)).where(
            Attendance.student_id == student_id,
            Attendance.status == "absent"
        )
    )
    
    # Get total
    total = await db.execute(
        select(func.count(Attendance.id)).where(
            Attendance.student_id == student_id
        )
    )
    
    present_count = present.scalar() or 0
    absent_count = absent.scalar() or 0
    total_count = total.scalar() or 0
    
    return {
        "student_id": student_id,
        "present": present_count,
        "absent": absent_count,
        "total": total_count,
        "percentage": round((present_count / total_count * 100) if total_count > 0 else 0, 2)
    }


@router.post("/mark")
async def mark_attendance(
    student_id: int,
    date: str,
    status: str,
    remarks: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark attendance for a student"""
    attendance_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    # Check if already marked
    existing = await db.execute(
        select(Attendance).where(
            Attendance.student_id == student_id,
            Attendance.date == attendance_date
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")
    
    record = Attendance(
        student_id=student_id,
        date=attendance_date,
        status=status,
        remarks=remarks
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    
    return {"record": record, "message": "Attendance marked successfully"}


# Additional endpoints from backup

@router.post("/bulk")
async def bulk_mark_attendance(
    records: List[dict],
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Mark bulk attendance (Teacher only)"""
    from modules.school.school_teacher.repository import TeacherRepository
    
    teacher = await TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    created_records = []
    errors = []
    
    for record_data in records:
        try:
            student_id = record_data.get("student_id")
            date_str = record_data.get("date")
            status = record_data.get("status", "present")
            remarks = record_data.get("remarks")
            
            if not student_id or not date_str:
                errors.append(f"Missing student_id or date in record")
                continue
            
            attendance_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Check if already marked
            existing = await db.execute(
                select(Attendance).where(
                    Attendance.student_id == student_id,
                    Attendance.date == attendance_date
                )
            )
            if existing.scalar_one_or_none():
                errors.append(f"Attendance already marked for student {student_id} on {date_str}")
                continue
            
            record = Attendance(
                student_id=student_id,
                date=attendance_date,
                status=status,
                remarks=remarks
            )
            db.add(record)
            created_records.append(record)
        except Exception as e:
            errors.append(f"Error processing record: {str(e)}")
    
    await db.commit()
    
    return {
        "created": len(created_records),
        "errors": errors
    }


@router.get("/course/{course_id}")
async def get_course_attendance(
    course_id: int,
    date: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance for a specific course"""
    from modules.school.school_courses.repository import CourseRepository
    
    course = await CourseRepository.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    query = select(Attendance)
    
    # For now, filter by student (would need enrollment table to filter properly)
    if date:
        attendance_date = datetime.strptime(date, "%Y-%m-%d").date()
        query = query.where(Attendance.date == attendance_date)
    
    result = await db.execute(query.limit(100))
    records = result.scalars().all()
    
    return {
        "course_id": course_id,
        "date": date,
        "records": [
            {
                "id": r.id,
                "student_id": r.student_id,
                "date": str(r.date) if r.date else None,
                "status": r.status,
                "remarks": r.remarks
            }
            for r in records
        ]
    }


@router.get("/course/{course_id}/stats")
async def get_course_attendance_stats(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get attendance statistics for a course"""
    # Get total present
    present = await db.execute(
        select(func.count(Attendance.id)).where(
            Attendance.status == "present"
        )
    )
    
    # Get total absent
    absent = await db.execute(
        select(func.count(Attendance.id)).where(
            Attendance.status == "absent"
        )
    )
    
    # Get total records
    total = await db.execute(
        select(func.count(Attendance.id))
    )
    
    present_count = present.scalar() or 0
    absent_count = absent.scalar() or 0
    total_count = total.scalar() or 0
    
    return {
        "course_id": course_id,
        "present": present_count,
        "absent": absent_count,
        "total": total_count,
        "attendance_percentage": round((present_count / total_count * 100) if total_count > 0 else 0, 2)
    }


@router.get("/student/my")
async def get_my_attendance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current student's own attendance"""
    from modules.school.school_student.repository import StudentRepository
    
    if current_user.role.value != "student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")
    
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    result = await db.execute(
        select(Attendance).where(
            Attendance.student_id == student.id
        ).order_by(Attendance.date.desc()).limit(100)
    )
    records = result.scalars().all()
    
    return {
        "student_id": student.id,
        "records": [
            {
                "id": r.id,
                "date": str(r.date) if r.date else None,
                "status": r.status,
                "remarks": r.remarks
            }
            for r in records
        ]
    }


@router.get("/student/my/course/{course_id}")
async def get_my_course_attendance(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current student's attendance for a specific course"""
    from modules.school.school_student.repository import StudentRepository
    
    if current_user.role.value != "student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")
    
    student = await StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    result = await db.execute(
        select(Attendance).where(
            Attendance.student_id == student.id
        ).order_by(Attendance.date.desc())
    )
    records = result.scalars().all()
    
    return {
        "student_id": student.id,
        "course_id": course_id,
        "records": [
            {
                "id": r.id,
                "date": str(r.date) if r.date else None,
                "status": r.status,
                "remarks": r.remarks
            }
            for r in records
        ]
    }


__all__ = ["router"]
