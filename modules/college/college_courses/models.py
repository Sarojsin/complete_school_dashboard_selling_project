"""
College Course Model

Course model for college system (with credits).
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase as Base


class CollegeCourse(Base):
    """
    Course model for college (with credits)
    """
    __tablename__ = "college_courses"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20))  # e.g., "CS101"
    name = Column(String(255))
    description = Column(Text)
    credits = Column(Integer, default=3)
    department_id = Column(Integer, ForeignKey("college_departments.id", ondelete="SET NULL"), nullable=True)
    semester_id = Column(Integer, ForeignKey("college_semesters.id", ondelete="SET NULL"), nullable=True)
    instructor_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="SET NULL"), nullable=True)
    is_elective = Column(Boolean, default=False)
    max_students = Column(Integer, default=60)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships - using string references to avoid circular imports
    department = relationship("Department", back_populates="courses")
    semester = relationship("Semester", back_populates="courses")
    instructor = relationship("Faculty", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")


# Import other college models from backup to ensure single source of truth
# These imports are just to register the classes, not to redefine them
try:
    from backup.models.college import department, program, semester, student as college_student_mod, faculty as faculty_mod, enrollment
except ImportError:
    # Handle import issues gracefully during development
    pass


__all__ = ["CollegeCourse"]
