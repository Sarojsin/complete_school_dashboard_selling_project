from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime
from models.test_models import Test, TestQuestion, TestSubmission
from tables.test_tables import TestUpdate

class TestRepository:
    @staticmethod
    def create(db: Session, test_data: Dict[str, Any], questions_data: List[Dict[str, Any]]) -> Test:
        # Calculate total points
        total_points = sum(q.get('points', 1.0) for q in questions_data)
        test_data['total_points'] = total_points
        
        test = Test(**test_data)
        db.add(test)
        db.flush()  # Get ID
        
        for q_data in questions_data:
            question = TestQuestion(**q_data, test_id=test.id)
            db.add(question)
            
        db.commit()
        db.refresh(test)
        return test

    @staticmethod
    def get_all(db: Session, teacher_id: Optional[int] = None) -> List[Test]:
        query = db.query(Test)
        if teacher_id:
            query = query.filter(Test.teacher_id == teacher_id)
        return query.order_by(desc(Test.created_at)).all()

    @staticmethod
    def get_by_id(db: Session, test_id: int) -> Optional[Test]:
        return db.query(Test).filter(Test.id == test_id).first()

    @staticmethod
    def update(db: Session, test: Test, **kwargs) -> Test:
        for key, value in kwargs.items():
            if hasattr(test, key):
                setattr(test, key, value)
        db.commit()
        db.refresh(test)
        return test

    @staticmethod
    def delete(db: Session, test: Test):
        db.delete(test)
        db.commit()

    @staticmethod
    def get_available_tests_for_student(db: Session, student_id: int, course_ids: List[int]) -> List[Test]:
        now = datetime.utcnow()
        # Get tests for enrolled courses that are active and within time window
        # Also exclude tests already submitted? Or maybe include them but mark as submitted?
        # For now, just get available tests
        return db.query(Test).filter(
            Test.course_id.in_(course_ids),
            Test.is_active == True,
            Test.start_time <= now,
            Test.end_time >= now
        ).all()

    @staticmethod
    def get_submission(db: Session, test_id: int, student_id: int) -> Optional[TestSubmission]:
        return db.query(TestSubmission).filter(
            TestSubmission.test_id == test_id,
            TestSubmission.student_id == student_id
        ).first()

    @staticmethod
    def update_submission(db: Session, submission: TestSubmission, **kwargs) -> TestSubmission:
        for key, value in kwargs.items():
            if hasattr(submission, key):
                setattr(submission, key, value)
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def get_student_results(db: Session, student_id: int) -> List[TestSubmission]:
        return db.query(TestSubmission).filter(
            TestSubmission.student_id == student_id,
            TestSubmission.submitted_at.isnot(None)
        ).order_by(desc(TestSubmission.submitted_at)).all()

    @staticmethod
    def get_test_results(db: Session, test_id: int) -> List[TestSubmission]:
        return db.query(TestSubmission).filter(
            TestSubmission.test_id == test_id,
            TestSubmission.submitted_at.isnot(None)
        ).all()
