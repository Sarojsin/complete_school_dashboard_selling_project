from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.dependencies import require_school_authority, require_school_teacher, require_student, require_parent
from modules.shared.models import User
# Modular imports
from modules.shared.models import User as UserModel
from modules.school.school_student.models import Student
from modules.school.school_teacher.models import Teacher
from modules.school.school_authority.models import Authority
from modules.school.school_parent.models import Parent
from modules.school.school_courses.models import SchoolCourse as Course
from modules.school.school_notices.models import Notice
from modules.school.school_account_section.models import SchoolFee as FeeRecord
from modules.school.school_groups.models import Group as GroupModel
from modules.school.school_tests.models import Test
from modules.school.school_exam_section.models import ExamNotice
from modules.school.school_assignments.models import Assignment, AssignmentSubmission
from modules.school.school_courses.models import CourseEnrollment
from modules.school.school_grades.models import Grade
from .schemas import AuthorityDashboard, TeacherDashboard, StudentDashboard, ParentDashboard, DashboardStats

router = APIRouter()


@router.get("/authority", response_model=AuthorityDashboard)
async def get_authority_dashboard(
    current_user: User = Depends(require_school_authority),
    db: AsyncSession = Depends(get_db)
):
    """Get authority dashboard with system statistics"""
    # Get user counts
    total_users_r = await db.execute(select(func.count(UserModel.id)))
    active_users_r = await db.execute(select(func.count(UserModel.id)).where(UserModel.is_active == True))
    students_r = await db.execute(select(func.count(Student.id)))
    teachers_r = await db.execute(select(func.count(Teacher.id)))
    parents_r = await db.execute(select(func.count(Parent.id)))
    courses_r = await db.execute(select(func.count(Course.id)))
    notices_r = await db.execute(select(func.count(Notice.id)))
    groups_r = await db.execute(select(func.count(GroupModel.id)).where(GroupModel.is_active == True))

    # Get fee stats
    revenue_r = await db.execute(select(func.sum(FeeRecord.paid_amount)).where(FeeRecord.status == "paid"))
    pending_r = await db.execute(select(func.sum(FeeRecord.amount - FeeRecord.paid_amount)).where(
        FeeRecord.status.in_(["pending", "overdue", "partial"])
    ))
    pending_cnt_r = await db.execute(select(func.count(FeeRecord.id)).where(
        FeeRecord.status.in_(["pending", "overdue", "partial"])
    ))

    # Get upcoming exams
    from datetime import date, timedelta
    today = date.today()
    thirty_days_later = today + timedelta(days=30)
    exams_r = await db.execute(select(func.count(ExamNotice.id)).where(
        ExamNotice.exam_date >= today, ExamNotice.exam_date <= thirty_days_later
    ))

    stats = DashboardStats(
        total_students=students_r.scalar() or 0,
        total_teachers=teachers_r.scalar() or 0,
        total_parents=parents_r.scalar() or 0,
        total_courses=courses_r.scalar() or 0,
        total_users=total_users_r.scalar() or 0,
        active_users=active_users_r.scalar() or 0,
        total_notices=notices_r.scalar() or 0,
        active_groups=groups_r.scalar() or 0
    )

    return AuthorityDashboard(
        stats=stats,
        total_revenue=round(float(revenue_r.scalar() or 0), 2),
        pending_fees=round(float(pending_r.scalar() or 0), 2),
        pending_fees_count=pending_cnt_r.scalar() or 0,
        upcoming_exams=exams_r.scalar() or 0
    )


@router.get("/teacher", response_model=TeacherDashboard)
async def get_teacher_dashboard(
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Get teacher dashboard data"""
    # Get teacher profile
    teacher_result = await db.execute(select(Teacher).filter(Teacher.user_id == current_user.id))
    teacher = teacher_result.scalars().first()
    
    if not teacher:
        return TeacherDashboard()

    # Get teacher's courses
    courses_r = await db.execute(select(func.count(Course.id)).filter(Course.teacher_id == teacher.id))

    # Get assignments count
    from modules.shared.models import User
    assignments_r = await db.execute(select(func.count(Assignment.id)).filter(Assignment.teacher_id == teacher.id))

    # Get pending grading (assignments without scores)
    from modules.shared.models import User
    pending_r = await db.execute(
        select(func.count(AssignmentSubmission.id)).filter(
            AssignmentSubmission.assignment_id.in_(
                select(Assignment.id).filter(Assignment.teacher_id == teacher.id)
            ),
            AssignmentSubmission.score.is_(None)
        )
    )

    # Get upcoming tests
    tests_r = await db.execute(select(func.count(Test.id)).filter(
        Test.teacher_id == teacher.id,
        Test.end_time >= func.now()
    ))

    # Get recent notices
    notices_result = await db.execute(
        select(Notice).order_by(Notice.created_at.desc()).limit(5)
    )
    recent_notices = [
        {"id": n.id, "title": n.title, "priority": n.priority, "created_at": n.created_at.isoformat()}
        for n in notices_result.scalars().all()
    ]

    return TeacherDashboard(
        my_courses_count=courses_r.scalar() or 0,
        my_assignments_count=assignments_r.scalar() or 0,
        pending_grading_count=pending_r.scalar() or 0,
        upcoming_tests=tests_r.scalar() or 0,
        recent_notices=recent_notices
    )


@router.get("/student", response_model=StudentDashboard)
async def get_student_dashboard(
    current_user: User = Depends(require_student),
    db: AsyncSession = Depends(get_db)
):
    """Get student dashboard data"""
    # Get student profile
    student_result = await db.execute(select(Student).filter(Student.user_id == current_user.id))
    student = student_result.scalars().first()

    if not student:
        return StudentDashboard()

    # Get enrolled courses count
    from modules.shared.models import User
    courses_r = await db.execute(select(func.count(CourseEnrollment.id)).filter(CourseEnrollment.student_id == student.id))

    # Get pending assignments
    from modules.shared.models import User
    from modules.shared.models import User
    
    # Count assignments due that haven't been submitted
    from datetime import datetime
    pending_r = await db.execute(
        select(func.count(Assignment.id)).filter(
            Assignment.due_date >= datetime.utcnow(),
            ~Assignment.id.in_(
                select(AssignmentSubmission.assignment_id).filter(
                    AssignmentSubmission.student_id == student.id
                )
            )
        )
    )

    # Get upcoming tests
    from datetime import date, timedelta
    today = date.today()
    tests_r = await db.execute(select(func.count(Test.id)).filter(
        Test.start_time <= today + timedelta(days=7),
        Test.end_time >= today,
        Test.is_active == True
    ))

    # Get recent grades
    from modules.shared.models import User
    grades_result = await db.execute(
        select(Grade).filter(Grade.student_id == student.id).order_by(Grade.created_at.desc()).limit(5)
    )
    recent_grades = [
        {"id": g.id, "course_id": g.course_id, "score": g.score, "grade": g.grade, "grade_type": g.grade_type}
        for g in grades_result.scalars().all()
    ]

    # Attendance summary (placeholder)
    attendance_summary = {"present": 0, "absent": 0, "leave": 0}

    return StudentDashboard(
        my_courses_count=courses_r.scalar() or 0,
        pending_assignments=pending_r.scalar() or 0,
        upcoming_tests=tests_r.scalar() or 0,
        recent_grades=recent_grades,
        attendance_summary=attendance_summary
    )


@router.get("/parent", response_model=ParentDashboard)
async def get_parent_dashboard(
    current_user: User = Depends(require_parent),
    db: AsyncSession = Depends(get_db)
):
    """Get parent dashboard data"""
    # Get parent profile
    parent_result = await db.execute(select(Parent).filter(Parent.user_id == current_user.id))
    parent = parent_result.scalars().first()

    if not parent:
        return ParentDashboard()

    # Get children count and info
    children_result = await db.execute(select(Student).filter(Student.parent_id == parent.id))
    children = children_result.scalars().all()
    children_count = len(children)
    
    children_info = [
        {
            "id": c.id,
            "name": c.user.full_name if c.user else "Unknown",
            "grade_level": c.grade_level,
            "section": c.section
        }
        for c in children
    ]

    # Get pending fees for children
    child_ids = [c.id for c in children]
    if child_ids:
        pending_r = await db.execute(
            select(func.sum(FeeRecord.amount - FeeRecord.paid_amount)).where(
                FeeRecord.student_id.in_(child_ids),
                FeeRecord.status.in_(["pending", "overdue", "partial"])
            )
        )
        pending_fees = round(float(pending_r.scalar() or 0), 2)
    else:
        pending_fees = 0.0

    return ParentDashboard(
        children_count=children_count,
        children_info=children_info,
        pending_fees=pending_fees
    )


@router.get("/overview")
async def get_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get system overview (available to all authenticated users)"""
    total_users_r = await db.execute(select(func.count(UserModel.id)))
    active_users_r = await db.execute(select(func.count(UserModel.id)).where(UserModel.is_active == True))
    students_r = await db.execute(select(func.count(Student.id)))
    teachers_r = await db.execute(select(func.count(Teacher.id)))

    return {
        "total_users": total_users_r.scalar() or 0,
        "active_users": active_users_r.scalar() or 0,
        "total_students": students_r.scalar() or 0,
        "total_teachers": teachers_r.scalar() or 0
    }