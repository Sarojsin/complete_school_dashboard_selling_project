"""
College Course Models

SQLAlchemy models for college course management.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.college.base import CollegeBase
from modules.shared.models import SoftDeleteMixin

class CollegeCourse(CollegeBase, SoftDeleteMixin):
    __tablename__ = "college_courses"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, index=True, nullable=False)
    course_name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("college_departments.id", ondelete="SET NULL"), nullable=True)
    instructor_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    semester_id = Column(Integer, ForeignKey("college_semesters.id", ondelete="SET NULL"), nullable=True)
    credits = Column(Integer, nullable=True)
    course_type = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship("CollegeDepartment")
    instructor = relationship("CollegeFaculty")
    semester = relationship("CollegeSemester", back_populates="courses")
    enrollments = relationship("CollegeEnrollment", back_populates="course")
    exam_results = relationship("CollegeExamResult", back_populates="course")

    def __repr__(self):
        return f"<CollegeCourse(id={self.id}, code='{self.course_code}', name='{self.course_name}')>"


__all__ = ["CollegeCourse"]