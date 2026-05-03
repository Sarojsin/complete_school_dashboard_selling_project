"""
Faculty Model

Faculty model for college system (like teachers but with more fields).
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase  # Use CollegeBase for separate college DB


class Faculty(CollegeBase):
    """
    Faculty model for college (like teachers but with more fields)
    """
    __tablename__ = "college_faculty"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("college_departments.id"))
    designation = Column(String(100))  # Professor, Associate Professor, Assistant Professor
    qualification = Column(String(255))
    specialization = Column(String(255))
    experience_years = Column(Integer)
    joining_date = Column(Date, default=datetime.utcnow)
    
    # Relationships - COMMENTED OUT to avoid circular dependency during mapper init
    # These can be re-enabled with string-based relationship() or after all models are loaded
    # user = relationship("User", back_populates="college_faculty_profile")
    # department = relationship("Department", back_populates="faculty", foreign_keys=[department_id])
    # department_hod = relationship("Department", back_populates="hod", foreign_keys="[Department.hod_teacher_id]")
    # courses = relationship("CollegeCourse", back_populates="instructor")
