from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, or_, func, desc
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from models.models import Assignment, AssignmentSubmission, Teacher, Course

class AssignmentRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, assignment_id: int) -> Optional[Assignment]:
        result = await db.execute(
            select(Assignment).options(
                joinedload(Assignment.course).selectinload(Course.enrollments),
                joinedload(Assignment.teacher)
            ).filter(Assignment.id == assignment_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100,
                course_id: int = None, teacher_id: int = None) -> List[Assignment]:
        query = select(Assignment).options(
            joinedload(Assignment.course).selectinload(Course.enrollments),
            joinedload(Assignment.teacher)
        )
        
        if course_id:
            query = query.filter(Assignment.course_id == course_id)
        
        if teacher_id:
            query = query.filter(Assignment.teacher_id == teacher_id)
        
        result = await db.execute(query.order_by(desc(Assignment.due_date)).offset(skip).limit(limit))
        return result.scalars().unique().all()
    
    @staticmethod
    async def create(db: AsyncSession, assignment_data: dict) -> Assignment:
        assignment = Assignment(**assignment_data)
        db.add(assignment)
        await db.commit()
        await db.refresh(assignment)
        return assignment
    
    @staticmethod
    async def update(db: AsyncSession, assignment: Assignment, **kwargs) -> Assignment:
        for key, value in kwargs.items():
            if value is not None and hasattr(assignment, key):
                setattr(assignment, key, value)
        await db.commit()
        await db.refresh(assignment)
        return assignment
    
    @staticmethod
    async def delete(db: AsyncSession, assignment: Assignment):
        await db.delete(assignment)
        await db.commit()
    
    @staticmethod
    async def get_submissions(db: AsyncSession, assignment_id: int) -> List[AssignmentSubmission]:
        result = await db.execute(
            select(AssignmentSubmission).options(
                joinedload(AssignmentSubmission.student)
            ).filter(
                AssignmentSubmission.assignment_id == assignment_id
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_submission_by_student(db: AsyncSession, assignment_id: int, 
                                  student_id: int) -> Optional[AssignmentSubmission]:
        result = await db.execute(
            select(AssignmentSubmission).filter(
                AssignmentSubmission.assignment_id == assignment_id,
                AssignmentSubmission.student_id == student_id
            )
        )
        return result.scalars().first()
    
    @staticmethod
    async def create_submission(db: AsyncSession, submission_data: dict) -> AssignmentSubmission:
        submission = AssignmentSubmission(**submission_data)
        db.add(submission)
        await db.commit()
        await db.refresh(submission)
        return submission
    
    @staticmethod
    async def update_submission(db: AsyncSession, submission: AssignmentSubmission, 
                         **kwargs) -> AssignmentSubmission:
        for key, value in kwargs.items():
            if value is not None and hasattr(submission, key):
                setattr(submission, key, value)
        
        if 'score' in kwargs or 'feedback' in kwargs:
            submission.graded_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(submission)
        return submission
    
    @staticmethod
    async def get_upcoming_assignments(db: AsyncSession, course_ids: List[int], 
                                days: int = 7) -> List[Assignment]:
        end_date = datetime.utcnow() + timedelta(days=days)
        
        result = await db.execute(
            select(Assignment).filter(
                Assignment.course_id.in_(course_ids),
                Assignment.due_date >= datetime.utcnow(),
                Assignment.due_date <= end_date
            ).order_by(Assignment.due_date)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_overdue_assignments(db: AsyncSession, student_id: int) -> List[Assignment]:
        # Get assignments without submissions that are overdue
        subquery = select(AssignmentSubmission.assignment_id).filter(
            AssignmentSubmission.student_id == student_id
        )
        
        result = await db.execute(
            select(Assignment).filter(
                Assignment.due_date < datetime.utcnow(),
                ~Assignment.id.in_(subquery)
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_student_assignments(db: AsyncSession, student_id: int, course_ids: List[int], student_grade: str = None, student_section: str = None) -> List[dict]:
        """
        Get all assignments for the given courses OR directly targeted to the student's class,
        annotated with the student's submission status.
        """
        query = select(Assignment).options(
            joinedload(Assignment.teacher).joinedload(Teacher.user),
            joinedload(Assignment.course)
        )
        
        conditions = []
        if course_ids:
            conditions.append(Assignment.course_id.in_(course_ids))
            
        if student_grade:
            if student_section:
                conditions.append(Assignment.target_classes.ilike(f"%{student_grade}{student_section}%"))
            conditions.append(Assignment.target_classes.ilike(f"%{student_grade}%"))

        if conditions:
            result = await db.execute(query.filter(or_(*conditions)).order_by(desc(Assignment.due_date)))
            assignments = result.scalars().unique().all()
        else:
            assignments = []
    
        final_result = []
        for assignment in assignments:
            # Check for submission
            sub_result = await db.execute(
                select(AssignmentSubmission).filter(
                    AssignmentSubmission.assignment_id == assignment.id,
                    AssignmentSubmission.student_id == student_id
                )
            )
            submission = sub_result.scalars().first()
            
            # Determine status
            status = "pending"
            if submission:
                if submission.score is not None:
                    status = "graded"
                else:
                    status = "submitted"
            elif assignment.due_date < datetime.utcnow():
                status = "overdue"
            
            # Add extended info
            assignment_dict = {
                "id": assignment.id,
                "title": assignment.title,
                "description": assignment.description,
                "subject": assignment.course.course_name if assignment.course else "General",
                "teacher_name": assignment.teacher.user.full_name if assignment.teacher and assignment.teacher.user else "Unknown Teacher",
                "due_date": assignment.due_date,
                "status": status,
                "max_score": assignment.max_score,
                "course": assignment.course,
                "submission": submission
            }
            final_result.append(assignment_dict)
            
        return final_result