from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from models.models import Assignment, AssignmentSubmission, Teacher

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

    @staticmethod
    def get_student_assignments(db: Session, student_id: int, course_ids: List[int], student_grade: str = None, student_section: str = None) -> List[dict]:
        """
        Get all assignments for the given courses OR directly targeted to the student's class,
        annotated with the student's submission status.
        """
        from sqlalchemy import or_
        
        query = db.query(Assignment).options(
            joinedload(Assignment.teacher).joinedload(Teacher.user),
            joinedload(Assignment.course)
        )
        
        conditions = []
        if course_ids:
            conditions.append(Assignment.course_id.in_(course_ids))
            
        if student_grade:
            # Check if target_classes matches the student's class (e.g. "9A") or just grade ("9")
            # This is a simple contains check. A more robust way might be needed if "10" matches "110" etc.
            # But for now, assuming standard class names like "9A", "10B", "Grade 9".
            
            # Construct possible target strings
            target_str = student_grade
            if student_section:
                target_str += student_section # e.g. "9A"
                # Also check just grade
                conditions.append(Assignment.target_classes.contains(target_str))
                
            # Also include generic grade match if section specific fails or isn't only thing
            # conditions.append(Assignment.target_classes.contains(student_grade)) 
            # Doing a simple OR
            
            if student_section:
                 conditions.append(Assignment.target_classes.like(f"%{student_grade}{student_section}%"))
            
            conditions.append(Assignment.target_classes.like(f"%{student_grade}%"))

        if conditions:
            # Use distinct to avoid duplicates if matches both course and target
            assignments = query.filter(or_(*conditions)).order_by(Assignment.due_date.desc()).all()
        else:
            assignments = []
    
        result = []
        for assignment in assignments:
            # Check for submission
            submission = db.query(AssignmentSubmission).filter(
                AssignmentSubmission.assignment_id == assignment.id,
                AssignmentSubmission.student_id == student_id
            ).first()
            
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
            result.append(assignment_dict)
            
        return result