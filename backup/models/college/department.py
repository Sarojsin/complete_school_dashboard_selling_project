"""
Department Model

Department model for college system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from modules.college.base import CollegeBase


class Department(CollegeBase):
    """
    Department model for college system
    """
    __tablename__ = "college_departments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    code = Column(String(20), unique=True)
    hod_teacher_id = Column(Integer, ForeignKey("college_faculty.id"), nullable=True)
    description = Column(Text)
    
    # Relationships
    hod = relationship("Faculty", back_populates="department_hod", foreign_keys=[hod_teacher_id])
    faculty = relationship("Faculty", back_populates="department", foreign_keys="[Faculty.department_id]")
    programs = relationship("Program", back_populates="department")
    labs = relationship("Lab", back_populates="department")
