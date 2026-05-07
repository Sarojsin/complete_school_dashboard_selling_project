"""
College Enrollment Models

SQLAlchemy models for college course enrollment management.
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.college.base import CollegeBase

class CollegeEnrollment(CollegeBase):
    __tablename__ = "college_enrollments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("college_courses.id", ondelete="CASCADE"), nullable=False)
    semester_id = Column(Integer, ForeignKey("college_semesters.id", ondelete="SET NULL"), nullable=True)
    enrollment_date = Column(Date, nullable=True)
    grade = Column(String(5), nullable=True)
    status = Column(String(20), default="enrolled")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    student = relationship("CollegeStudent", back_populates="enrollments")
    course = relationship("CollegeCourse", back_populates="enrollments")
    semester = relationship("CollegeSemester", back_populates="enrollments")

    def __repr__(self):
        return f"<CollegeEnrollment(id={self.id}, student_id={self.student_id}, course_id={self.course_id}, status='{self.status}')>"


__all__ = ["CollegeEnrollment"]