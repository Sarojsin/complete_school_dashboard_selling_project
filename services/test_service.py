from sqlalchemy.orm import Session
from datetime import datetime
from models.test_models import Test, TestSubmission, TestQuestion, QuestionType
from repositories.test_repository import TestRepository

class TestService:
    @staticmethod
    def is_test_available(test: Test) -> bool:
        now = datetime.utcnow()
        return test.is_active and test.start_time <= now <= test.end_time

    @staticmethod
    def is_test_started(test: Test) -> bool:
        now = datetime.utcnow()
        return now >= test.start_time

    @staticmethod
    def has_student_submitted(db: Session, test_id: int, student_id: int) -> bool:
        submission = TestRepository.get_submission(db, test_id, student_id)
        return submission is not None and submission.submitted_at is not None

    @staticmethod
    def get_or_create_submission(db: Session, test_id: int, student_id: int) -> TestSubmission:
        submission = TestRepository.get_submission(db, test_id, student_id)
        if not submission:
            submission = TestSubmission(
                test_id=test_id,
                student_id=student_id,
                started_at=datetime.utcnow(),
                answers={}
            )
            db.add(submission)
            db.commit()
            db.refresh(submission)
        return submission

    @staticmethod
    def calculate_time_remaining(test: Test) -> int:
        now = datetime.utcnow()
        end_time = test.end_time
        
        # Also check duration from start if applicable?
        # For now, just check end_time
        remaining = (end_time - now).total_seconds()
        return max(0, int(remaining))

    @staticmethod
    def grade_submission(db: Session, submission: TestSubmission, test: Test):
        score = 0.0
        max_score = test.total_points
        
        # Auto-grade objective questions
        for question in test.questions:
            if str(question.id) in submission.answers:
                student_answer = submission.answers[str(question.id)]
                
                if question.question_type in [QuestionType.MCQ, QuestionType.TRUE_FALSE, QuestionType.SHORT_ANSWER]:
                    # Simple string comparison for now
                    if str(student_answer).strip().lower() == str(question.correct_answer).strip().lower():
                        score += question.points
                
                # Essay questions need manual grading
        
        submission.score = score
        submission.max_score = max_score
        submission.percentage = (score / max_score * 100) if max_score > 0 else 0
        
        # If all questions are objective, mark as graded
        has_essay = any(q.question_type == QuestionType.ESSAY for q in test.questions)
        submission.is_graded = not has_essay
        
        db.commit()
        db.refresh(submission)
