"""
School Student Model

Student model for school system (Classes 1-12).
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backup.models.base import Base

# Import User for relationship resolution
try:
    from modules.shared.models import User
except ImportError:
    User = None  # Handle circular import gracefully


class SchoolStudent(Base):
    """
    School Student model for students in Classes 1-12
    """
    __tablename__ = "school_students"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    date_of_birth = Column(Date)
    phone = Column(String(20))
    address = Column(Text)
    parent_name = Column(String(255))
    parent_phone = Column(String(20))
    parent_id = Column(Integer, ForeignKey("school_parents.id"), nullable=True)
    enrollment_date = Column(Date, default=datetime.utcnow)
    grade_level = Column(String(20))  # Class 1-12
    section = Column(String(10))  # A, B, C
    roll_number = Column(String(20))
    
    # Relationships - COMMENTING OUT to avoid mapper conflicts with User
    # These can be added back once we properly handle the User import
    # user = relationship("User", back_populates="school_student_profile")
    parent = relationship("SchoolParent", back_populates="children")
    school_enrollments = relationship("SchoolCourseEnrollment", back_populates="student", cascade="all, delete-orphan")
    school_attendance = relationship("SchoolAttendance", back_populates="student", cascade="all, delete-orphan")
    school_grades = relationship("SchoolGrade", back_populates="student", cascade="all, delete-orphan")
    school_fees = relationship("SchoolFeeRecord", back_populates="student", cascade="all, delete-orphan")


# For backward compatibility - reference to existing students table
Student = SchoolStudent
