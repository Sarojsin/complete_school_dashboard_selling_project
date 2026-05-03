from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from modules.shared.database import get_db
from modules.auth.dependencies import get_current_user, require_school_portal, require_school_teacher
from modules.shared.models import User
from .repository import GradeRepository, AssessmentRepository
from .schemas import (
    GradeCreate, GradeUpdate, GradeResponse, GradeBulkCreate,
    AssessmentCreate, AssessmentResponse
)

router = APIRouter(dependencies=[Depends(require_school_portal)])


@router.post("/", response_model=GradeResponse, status_code=201)
async def create_grade(
    grade: GradeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new grade (Teacher only)"""
    repo = GradeRepository(db)
    grade_data = grade.model_dump()
    created_grade = await repo.create(grade_data)
    return created_grade


@router.get("/{grade_id}", response_model=GradeResponse)
async def get_grade(
    grade_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a grade by ID"""
    repo = GradeRepository(db)
    grade = await repo.get(grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade


@router.get("/", response_model=List[GradeResponse])
async def list_grades(
    student_id: Optional[int] = Query(None),
    course_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List grades with optional filters"""
    repo = GradeRepository(db)
    grades = await repo.get_all(student_id=student_id, course_id=course_id, skip=skip, limit=limit)
    return grades


@router.get("/student/{student_id}", response_model=List[GradeResponse])
async def get_student_grades(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get grades for a specific student"""
    repo = GradeRepository(db)
    grades = await repo.get_by_student(student_id)
    return grades


@router.get("/course/{course_id}", response_model=List[GradeResponse])
async def get_course_grades(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get grades for a specific course"""
    repo = GradeRepository(db)
    grades = await repo.get_by_course(course_id)
    return grades


@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    grade: GradeUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a grade (Teacher only)"""
    repo = GradeRepository(db)
    grade_data = grade.model_dump(exclude_unset=True)
    updated_grade = await repo.update(grade_id, grade_data)
    if not updated_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return updated_grade


@router.delete("/{grade_id}")
async def delete_grade(
    grade_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a grade (Teacher only)"""
    repo = GradeRepository(db)
    success = await repo.delete(grade_id)
    if not success:
        raise HTTPException(status_code=404, detail="Grade not found")
    return {"message": "Grade deleted successfully"}


# Assessment endpoints
@router.post("/assessments", response_model=AssessmentResponse, status_code=201)
async def create_assessment(
    assessment: AssessmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new assessment (Teacher only)"""
    repo = AssessmentRepository(db)
    assessment_data = assessment.model_dump()
    created_assessment = await repo.create(assessment_data)
    return created_assessment


@router.get("/assessments/course/{course_id}", response_model=List[AssessmentResponse])
async def get_course_assessments(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get assessments for a specific course"""
    repo = AssessmentRepository(db)
    assessments = await repo.get_by_course(course_id)
    return assessments


# Bulk operations
@router.post("/bulk", response_model=List[GradeResponse], status_code=201)
async def bulk_create_grades(
    grades: GradeBulkCreate,
    current_user: User = Depends(require_school_teacher),
    db: AsyncSession = Depends(get_db)
):
    """Create multiple grades at once (Teacher only)"""
    repo = GradeRepository(db)
    created_grades = []
    
    for grade_data in grades.grades:
        grade_dict = grade_data.model_dump()
        created_grade = await repo.create(grade_dict)
        created_grades.append(created_grade)
    
    return created_grades


# Top performers
@router.get("/course/{course_id}/top-performers", response_model=List[GradeResponse])
async def get_top_performers(
    course_id: int,
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get top performing students in a course"""
    repo = GradeRepository(db)
    grades = await repo.get_top_performers(course_id, limit)
    return grades


# Student my-grades (role-based)
@router.get("/my-grades")
async def get_my_grades(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get grades for the current user (Student/Parent)"""
    repo = GradeRepository(db)
    
    if current_user.role.value == "student":
        # Get student profile
        from modules.school.school_student.repository import StudentRepository
        student_repo = StudentRepository(db)
        student = await student_repo.get_by_user_id(current_user.id)
        if not student:
            raise HTTPException(status_code=404, detail="Student profile not found")
        grades = await repo.get_by_student(student.id)
        return {"grades": grades, "role": "student"}
    
    elif current_user.role.value == "parent":
        # Get children and their grades
        from modules.school.school_parent.repository import ParentRepository
        parent_repo = ParentRepository(db)
        parent = await parent_repo.get_by_user_id(current_user.id)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent profile not found")
        
        children_grades = []
        for child in parent.children:
            child_grades = await repo.get_by_student(child.id)
            children_grades.append({
                "student_id": child.id,
                "student_name": child.user.full_name,
                "grades": child_grades
            })
        return {"children": children_grades, "role": "parent"}
    
    else:
        raise HTTPException(status_code=403, detail="Not authorized")


__all__ = ["router"]