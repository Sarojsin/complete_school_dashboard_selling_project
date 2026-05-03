"""
College Student Model

Student model for college system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase


class CollegeStudent(CollegeBase):
    """
    College Student model (with program enrollment, CGPA)
    """
    __tablename__ = "college_students"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    roll_number = Column(String(50), unique=True, nullable=False, index=True)
    program_id = Column(Integer, ForeignKey("college_programs.id"))
    semester_id = Column(Integer, ForeignKey("college_semesters.id"))
    enrollment_date = Column(Date, default=datetime.utcnow)
    cgpa = Column(Float, default=0.0)
    total_credits_completed = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="college_student_profile")
    program = relationship("Program", back_populates="students")
    semester = relationship("Semester")
    enrollments = relationship("Enrollment", back_populates="student")
    
    @property
    def full_name(self) -> str:
        """Get full name from associated user"""
        return self.user.full_name if self.user else ""
