from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database.database import get_db
from dependencies import get_current_student, get_current_teacher, get_current_user
from models.models import User
from repositories.test_repository import TestRepository
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from services.test_service import TestService
from tables.test_tables import (
    TestCreate, TestUpdate, TestResponse, TestForStudent,
    TestSubmissionCreate, TestSubmissionResponse, TestResult
)

router = APIRouter()

# TEACHER ENDPOINTS

@router.post("/", response_model=TestResponse)
async def create_test(
    test_data: TestCreate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Create a new test (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    # Validate dates
    if test_data.start_time >= test_data.end_time:
        raise HTTPException(status_code=400, detail="Start time must be before end time")
    
    if test_data.start_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Start time cannot be in the past")
    
    # Create test with questions
    test = TestRepository.create(
        db,
        test_data={
            "title": test_data.title,
            "description": test_data.description,
            "course_id": test_data.course_id,
            "teacher_id": teacher.id,
            "duration": test_data.duration,
            "start_time": test_data.start_time,
            "end_time": test_data.end_time,
            "instructions": test_data.instructions
        },
        questions_data=[q.dict() for q in test_data.questions]
    )
    
    return test

@router.get("/teacher/my-tests", response_model=List[TestResponse])
async def get_my_tests(
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all tests created by current teacher"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    tests = TestRepository.get_all(db, teacher_id=teacher.id)
    return tests

@router.get("/teacher/{test_id}", response_model=TestResponse)
async def get_test_for_teacher(
    test_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get test details with answers (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    if test.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this test")
    
    return test

@router.put("/{test_id}", response_model=TestResponse)
async def update_test(
    test_id: int,
    test_update: TestUpdate,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Update test details (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    if test.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this test")
    
    # Check if test has started
    if TestService.is_test_started(test):
        raise HTTPException(
            status_code=400,
            detail="Cannot update test after it has started"
        )
    
    updated_test = TestRepository.update(db, test, **test_update.dict(exclude_unset=True))
    return updated_test

@router.delete("/{test_id}")
async def delete_test(
    test_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Delete test (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    if test.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this test")
    
    TestRepository.delete(db, test)
    return {"message": "Test deleted successfully"}

@router.get("/{test_id}/results")
async def get_test_results(
    test_id: int,
    current_user: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """Get all submissions for a test (Teacher only)"""
    teacher = TeacherRepository.get_by_user_id(db, current_user.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    if test.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not authorized to view results")
    
    submissions = TestRepository.get_test_results(db, test_id)
    
    # Calculate statistics
    total_submissions = len(submissions)
    graded_submissions = sum(1 for s in submissions if s.is_graded)
    average_score = sum(s.score for s in submissions if s.score) / total_submissions if total_submissions > 0 else 0
    
    return {
        "test": test,
        "submissions": submissions,
        "statistics": {
            "total_submissions": total_submissions,
            "graded_submissions": graded_submissions,
            "pending_grading": total_submissions - graded_submissions,
            "average_score": round(average_score, 2)
        }
    }

# STUDENT ENDPOINTS

@router.get("/student/available", response_model=List[TestForStudent])
async def get_available_tests(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get available tests for student"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    courses = StudentRepository.get_enrolled_courses(db, student.id)
    course_ids = [c.id for c in courses]
    
    tests = TestRepository.get_available_tests_for_student(db, student.id, course_ids)
    return tests

@router.get("/student/{test_id}", response_model=TestForStudent)
async def get_test_for_student(
    test_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get test details without answers (Student view)"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    # Check if student is enrolled in the course
    courses = StudentRepository.get_enrolled_courses(db, student.id)
    if test.course_id not in [c.id for c in courses]:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    # Check if test is available
    if not TestService.is_test_available(test):
        raise HTTPException(status_code=400, detail="Test is not currently available")
    
    return test

@router.post("/{test_id}/start")
async def start_test(
    test_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Start taking a test"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    # Check if test is available
    if not TestService.is_test_available(test):
        raise HTTPException(status_code=400, detail="Test is not currently available")
    
    # Check if already submitted
    if TestService.has_student_submitted(db, test_id, student.id):
        raise HTTPException(status_code=400, detail="Test already submitted")
    
    # Get or create submission
    submission = TestService.get_or_create_submission(db, test_id, student.id)
    
    # Calculate remaining time
    time_remaining = TestService.calculate_time_remaining(test)
    
    return {
        "test": test,
        "submission": submission,
        "time_remaining": time_remaining
    }

@router.post("/{test_id}/submit", response_model=TestSubmissionResponse)
async def submit_test(
    test_id: int,
    submission_data: TestSubmissionCreate,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Submit test answers"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    # Get existing submission
    submission = TestRepository.get_submission(db, test_id, student.id)
    if not submission:
        raise HTTPException(status_code=404, detail="Test not started")
    
    if submission.submitted_at:
        raise HTTPException(status_code=400, detail="Test already submitted")
    
    # Update submission
    time_taken = (datetime.utcnow() - submission.started_at).total_seconds()
    submission = TestRepository.update_submission(
        db,
        submission,
        answers=submission_data.answers,
        submitted_at=datetime.utcnow(),
        time_taken=int(time_taken)
    )
    
    # Grade the submission
    TestService.grade_submission(db, submission, test)
    
    return submission

@router.get("/student/{test_id}/result", response_model=TestResult)
async def get_test_result(
    test_id: int,
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get test result"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    submission = TestRepository.get_submission(db, test_id, student.id)
    if not submission or not submission.submitted_at:
        raise HTTPException(status_code=404, detail="Test not submitted")
    
    if not submission.is_graded:
        raise HTTPException(status_code=400, detail="Test is being graded")
    
    # Count correct answers
    questions_correct = 0
    for question in test.questions:
        if str(question.id) in submission.answers:
            student_answer = submission.answers[str(question.id)]
            if str(student_answer).strip().lower() == str(question.correct_answer).strip().lower():
                questions_correct += 1
    
    return TestResult(
        test_id=test.id,
        test_title=test.title,
        score=submission.score or 0,
        max_score=submission.max_score or test.total_points,
        percentage=submission.percentage or 0,
        time_taken=submission.time_taken or 0,
        submitted_at=submission.submitted_at,
        feedback=submission.feedback,
        questions_correct=questions_correct,
        total_questions=len(test.questions)
    )

@router.get("/student/my-results")
async def get_my_results(
    current_user: User = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get all test results for student"""
    student = StudentRepository.get_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    results = TestRepository.get_student_results(db, student.id)
    return results