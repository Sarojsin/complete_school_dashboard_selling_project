"""
College Student Models

SQLAlchemy models for college student management.
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.college.base import CollegeBase
from modules.shared.models import SoftDeleteMixin

class CollegeStudent(CollegeBase, SoftDeleteMixin):
    __tablename__ = "college_students"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    roll_number = Column(String(20), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    program_id = Column(Integer, ForeignKey("college_programs.id", ondelete="SET NULL"), nullable=True)
    semester_id = Column(Integer, ForeignKey("college_semesters.id", ondelete="SET NULL"), nullable=True)
    enrollment_year = Column(Integer, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="student_profile")
    program = relationship("CollegeProgram", back_populates="students")
    current_semester = relationship("CollegeSemester", back_populates="students")
    enrollments = relationship("CollegeEnrollment", back_populates="student")
    exam_results = relationship("CollegeExamResult", back_populates="student")
    hostel_allocations = relationship("HostelAllocation", back_populates="student")
    hostel_complaints = relationship("HostelComplaint", back_populates="student")
    placement_applications = relationship("PlacementApplication", back_populates="student")

    def __repr__(self):
        return f"<CollegeStudent(id={self.id}, roll_number='{self.roll_number}', name='{self.first_name} {self.last_name}')>"


__all__ = ["CollegeStudent"]