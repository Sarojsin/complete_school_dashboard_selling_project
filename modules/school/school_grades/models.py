from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.shared.base import Base


class Grade(Base):
    __tablename__ = "school_grades"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("school_courses.id", ondelete="CASCADE"), nullable=False)
    grade_type = Column(String(50), nullable=True)  # midterm, final, quiz, assignment
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    grade = Column(String(5), nullable=True)  # A, B+, B, etc.
    remarks = Column(Text, nullable=True)
    academic_year = Column(String(20), nullable=False)
    term = Column(String(20), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("SchoolStudent")
    course = relationship("SchoolCourse")


class Assessment(Base):
    __tablename__ = "school_assessments"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    course_id = Column(Integer, ForeignKey("school_courses.id", ondelete="CASCADE"), nullable=False)
    academic_year = Column(String(20), nullable=False)
    term = Column(String(20), nullable=True)
    max_marks = Column(Float, default=100.0)
    weight = Column(Float, default=1.0)  # Weight in overall grade
    due_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    course = relationship("SchoolCourse")


class GradeReport(Base):
    __tablename__ = "school_grade_reports"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete="SET NULL"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    term = Column(String(20), nullable=True)
    gpa = Column(Float, nullable=True)
    total_marks = Column(Float, nullable=True)
    rank = Column(Integer, nullable=True)
    report_data = Column(Text, nullable=True)  # JSON string
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("SchoolStudent")