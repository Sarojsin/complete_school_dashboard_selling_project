from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database.database import Base

class QuestionType(str, enum.Enum):
    MCQ = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    total_points = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="tests")
    teacher = relationship("Teacher", back_populates="tests")
    questions = relationship("TestQuestion", back_populates="test", cascade="all, delete-orphan")
    submissions = relationship("TestSubmission", back_populates="test", cascade="all, delete-orphan")

class TestQuestion(Base):
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False)
    options = Column(JSON)  # List of options for MCQ
    correct_answer = Column(Text)  # For auto-grading
    points = Column(Float, default=1.0)
    order = Column(Integer, default=0)

    # Relationships
    test = relationship("Test", back_populates="questions")

class TestSubmission(Base):
    __tablename__ = "test_submissions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    answers = Column(JSON)  # Dictionary of question_id: answer
    score = Column(Float)
    max_score = Column(Float)
    percentage = Column(Float)
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime)
    time_taken = Column(Integer)  # in seconds
    is_graded = Column(Boolean, default=False)
    feedback = Column(Text)

    # Relationships
    test = relationship("Test", back_populates="submissions")
    student = relationship("Student", back_populates="test_submissions")
