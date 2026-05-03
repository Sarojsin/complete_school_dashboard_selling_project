from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal, require_hod
from modules.shared.models import User

router = APIRouter(dependencies=[Depends(require_school_portal)])


@router.get("/dashboard")
async def get_hod_dashboard(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_db)
):
    """Get HOD dashboard with overview stats"""
    from modules.school.school_teacher.models import Teacher
    from modules.school.school_student.models import Student
    from modules.shared.models import User
    
    # Get HOD's teacher profile
    result = await db.execute(
        select(Teacher).where(Teacher.user_id == current_user.id)
    )
    hod = result.scalars().first()
    
    if not hod:
        # Return default dashboard instead of 404
        return {
            "department": "Unknown",
            "total_teachers": 0,
            "total_students": 0,
            "total_courses": 0
        }
    
    # Count teachers in department
    teachers_count = await db.execute(
        select(func.count(Teacher.id)).where(Teacher.department == hod.department)
    )
    total_teachers = teachers_count.scalar() or 0
    
    # Count students in department
    students_count = await db.execute(
        select(func.count(Student.id))
    )
    total_students = students_count.scalar() or 0
    
    from modules.school.school_courses.models import SchoolCourse as Course
    # Count courses in department
    courses_count = await db.execute(
        select(func.count(Course.id)).where(Course.grade_level == hod.department)
    )
    total_courses = courses_count.scalar() or 0
    
    return {
        "department": hod.department,
        "total_teachers": total_teachers,
        "total_students": total_students,
        "total_courses": total_courses
    }


@router.get("/departments")
async def get_all_departments(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_db)
):
    """Get list of all departments"""
    from modules.school.school_teacher.models import Teacher
    from sqlalchemy import distinct
    
    result = await db.execute(
        select(distinct(Teacher.department)).where(Teacher.department != None)
    )
    departments = result.scalars().all()
    
    return {"departments": [{"name": d} for d in departments]}


@router.get("/teachers")
async def get_department_teachers(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_db)
):
    """Get teachers in the HOD's department"""
    from modules.school.school_teacher.models import Teacher
    
    result = await db.execute(
        select(Teacher).where(Teacher.user_id == current_user.id)
    )
    hod = result.scalars().first()
    
    if not hod:
        raise HTTPException(status_code=404, detail="HOD profile not found")
    
    teachers_result = await db.execute(
        select(Teacher).where(Teacher.department == hod.department)
    )
    teachers = teachers_result.scalars().all()
    
    return {"teachers": teachers}


@router.get("/courses")
async def get_department_courses(
    current_user: User = Depends(require_hod),
    db: AsyncSession = Depends(get_db)
):
    """Get courses in the HOD's department"""
    from modules.school.school_teacher.models import Teacher
    from modules.shared.models import User
    
    result = await db.execute(
        select(Teacher).where(Teacher.user_id == current_user.id)
    )
    hod = result.scalars().first()
    
    if not hod:
        raise HTTPException(status_code=404, detail="HOD profile not found")
    
    courses_result = await db.execute(
        select(Course).where(Course.grade_level == hod.department)
    )
    courses = courses_result.scalars().all()
    
    return {"courses": courses}


__all__ = ["router"]