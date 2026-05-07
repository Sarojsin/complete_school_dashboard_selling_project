"""
College Faculty Models

SQLAlchemy models for college faculty management.
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.college.base import CollegeBase
from modules.shared.models import SoftDeleteMixin

class CollegeFaculty(CollegeBase, SoftDeleteMixin):
    __tablename__ = "college_faculty"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    employee_id = Column(String(20), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    department_id = Column(Integer, ForeignKey("college_departments.id", ondelete="SET NULL"), nullable=True)
    designation = Column(String(100), nullable=True)
    qualification = Column(String(200), nullable=True)
    experience_years = Column(Integer, nullable=True)
    joining_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="faculty_profile")
    department = relationship("CollegeDepartment")

    def __repr__(self):
        return f"<CollegeFaculty(id={self.id}, employee_id='{self.employee_id}', name='{self.first_name} {self.last_name}')>"


# Import Teacher from school module for compatibility
from modules.school.school_teacher.models import Teacher

__all__ = ["CollegeFaculty", "Teacher"]