"""
College Semester Models

SQLAlchemy models for college semester management.
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.college.base import CollegeBase

class CollegeSemester(CollegeBase):
    __tablename__ = "college_semesters"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("college_programs.id", ondelete="SET NULL"), nullable=True)
    semester_number = Column(Integer, nullable=False)
    academic_year = Column(String(20), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    program = relationship("CollegeProgram", back_populates="semesters")
    students = relationship("CollegeStudent", back_populates="current_semester")
    courses = relationship("CollegeCourse", back_populates="semester")
    enrollments = relationship("CollegeEnrollment", back_populates="semester")

    def __repr__(self):
        return f"<CollegeSemester(id={self.id}, program_id={self.program_id}, semester={self.semester_number}, year='{self.academic_year}')>"


__all__ = ["CollegeSemester"]