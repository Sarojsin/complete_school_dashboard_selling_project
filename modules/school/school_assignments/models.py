from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.shared.base import Base
from modules.school.school_student.models import SchoolStudent


class Assignment(Base):
    __tablename__ = "school_assignments"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey("school_courses.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    due_date = Column(DateTime, nullable=False)
    max_score = Column(Float, default=100.0)
    file_path = Column(String(500), nullable=True)
    target_classes = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    course = relationship("SchoolCourse", overlaps="assignments")
    teacher = relationship("Teacher")
    submissions = relationship("AssignmentSubmission", back_populates="assignment", cascade="all, delete-orphan")


class AssignmentSubmission(Base):
    __tablename__ = "school_assignment_submissions"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("school_assignments.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    submission_text = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    graded_at = Column(DateTime, nullable=True)
    is_late = Column(Boolean, default=False)
    
    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("SchoolStudent")