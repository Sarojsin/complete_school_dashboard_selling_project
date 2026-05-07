"""
College Program Models

SQLAlchemy models for college program management.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.college.base import CollegeBase
from modules.shared.models import SoftDeleteMixin

class CollegeProgram(CollegeBase, SoftDeleteMixin):
    __tablename__ = "college_programs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("college_departments.id", ondelete="SET NULL"), nullable=True)
    duration_years = Column(Integer, nullable=True)
    degree_type = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship("CollegeDepartment", back_populates="programs")
    students = relationship("CollegeStudent", back_populates="program")
    semesters = relationship("CollegeSemester", back_populates="program")

    def __repr__(self):
        return f"<CollegeProgram(id={self.id}, code='{self.code}', name='{self.name}')>"


__all__ = ["CollegeProgram"]