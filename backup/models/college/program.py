"""
Program Model

Program/Degree model for college system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from modules.college.base import CollegeBase


class Program(CollegeBase):
    """
    Program/Degree model for college (e.g., BSc CS, BSc IT, MBA)
    """
    __tablename__ = "college_programs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))  # "Bachelor of Computer Science"
    code = Column(String(20))  # "BCS"
    department_id = Column(Integer, ForeignKey("college_departments.id"))
    level = Column(String(50))  # "Bachelor", "Master", "PhD"
    duration_years = Column(Integer)
    total_credits = Column(Integer)
    
    # Relationships
    department = relationship("Department", back_populates="programs")
    semesters = relationship("Semester", back_populates="program")
    students = relationship("CollegeStudent", back_populates="program")
