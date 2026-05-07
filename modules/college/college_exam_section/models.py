"""
College Exam Section Models

Exam results and notices for college system.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase


class CollegeExamResult(CollegeBase):
    """
    Exam Result model for college.
    Stores individual student results for courses.
    """
    __tablename__ = "college_exam_results"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("college_courses.id", ondelete="CASCADE"), nullable=False)
    marks = Column(Float, nullable=False)
    max_marks = Column(Float, default=100.0)
    grade = Column(String(2), nullable=True)
    exam_type = Column(String(20), default="final")  # midterm, final, quiz, assignment
    is_published = Column(Boolean, default=False)
    published_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    published_at = Column(DateTime, nullable=True)
    semester_id = Column(Integer, ForeignKey("college_semesters.id"), nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("CollegeStudent", back_populates="exam_results")
    course = relationship("CollegeCourse", back_populates="exam_results")
    semester = relationship("CollegeSemester")


class CollegeExamNotice(CollegeBase):
    """
    Exam Notice model for college.
    Used for exam schedules, hall tickets, result notifications.
    """
    __tablename__ = "college_exam_notices"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    notice_type = Column(String(20), nullable=False)  # schedule, hall_ticket, result, general
    exam_date = Column(Date, nullable=True)
    semester_id = Column(Integer, ForeignKey("college_semesters.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    semester = relationship("CollegeSemester")


# Ensure CollegeCourse and CollegeStudent models have backrefs
# This import ensures the models are registered and relationships work
try:
    from backup.models.college import student as college_student_mod, course as college_course_mod  # noqa
except ImportError:
    pass


__all__ = ["CollegeExamResult", "CollegeExamNotice"]
