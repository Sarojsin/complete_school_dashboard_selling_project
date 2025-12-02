from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from models.models import Assignment, AssignmentSubmission

class AssignmentRepository:
    @staticmethod
    def get_by_id(db: Session, assignment_id: int) -> Optional[Assignment]:
        return db.query(Assignment).options(
            joinedload(Assignment.course),
            joinedload(Assignment.teacher)
        ).filter(Assignment.id == assignment_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100,
                course_id: int = None, teacher_id: int = None) -> List[Assignment]:
        query = db.query(Assignment).options(
            joinedload(Assignment.course),
            joinedload(Assignment.teacher)
        )
        
        if course_id:
            query = query.filter(Assignment.course_id == course_id)
        
        if teacher_id:
            query = query.filter(Assignment.teacher_id == teacher_id)
        
        return query.order_by(Assignment.due_date.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, assignment_data: dict) -> Assignment:
        assignment = Assignment(**assignment_data)
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment
    
    @staticmethod
    def update(db: Session, assignment: Assignment, **kwargs) -> Assignment:
        for key, value in kwargs.items():
            if value is not None and hasattr(assignment, key):
                setattr(assignment, key, value)
        db.commit()
        db.refresh(assignment)
        return assignment
    
    @staticmethod
    def delete(db: Session, assignment: Assignment):
        db.delete(assignment)
        db.commit()
    
    @staticmethod
    def get_submissions(db: Session, assignment_id: int) -> List[AssignmentSubmission]:
        return db.query(AssignmentSubmission).options(
            joinedload(AssignmentSubmission.student)
        ).filter(
            AssignmentSubmission.assignment_id == assignment_id
        ).all()
    
    @staticmethod
    def get_submission_by_student(db: Session, assignment_id: int, 
                                  student_id: int) -> Optional[AssignmentSubmission]:
        return db.query(AssignmentSubmission).filter(
            AssignmentSubmission.assignment_id == assignment_id,
            AssignmentSubmission.student_id == student_id
        ).first()
    
    @staticmethod
    def create_submission(db: Session, submission_data: dict) -> AssignmentSubmission:
        submission = AssignmentSubmission(**submission_data)
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission
    
    @staticmethod
    def update_submission(db: Session, submission: AssignmentSubmission, 
                         **kwargs) -> AssignmentSubmission:
        for key, value in kwargs.items():
            if value is not None and hasattr(submission, key):
                setattr(submission, key, value)
        
        if 'score' in kwargs or 'feedback' in kwargs:
            submission.graded_at = datetime.utcnow()
        
        db.commit()
        db.refresh(submission)
        return submission
    
    @staticmethod
    def get_upcoming_assignments(db: Session, course_ids: List[int], 
                                days: int = 7) -> List[Assignment]:
        from datetime import timedelta
        end_date = datetime.utcnow() + timedelta(days=days)
        
        return db.query(Assignment).filter(
            Assignment.course_id.in_(course_ids),
            Assignment.due_date >= datetime.utcnow(),
            Assignment.due_date <= end_date
        ).order_by(Assignment.due_date).all()
    
    @staticmethod
    def get_overdue_assignments(db: Session, student_id: int) -> List[Assignment]:
        # Get assignments without submissions that are overdue
        submitted_ids = db.query(AssignmentSubmission.assignment_id).filter(
            AssignmentSubmission.student_id == student_id
        ).subquery()
        
        return db.query(Assignment).filter(
            Assignment.due_date < datetime.utcnow(),
            ~Assignment.id.in_(submitted_ids)
        ).all()