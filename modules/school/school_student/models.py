from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.shared.base import Base

class SchoolStudent(Base):
    """
    School Student model for school system
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
    parent_id = Column(Integer, ForeignKey("school_parents.id", ondelete="SET NULL"), nullable=True)
    enrollment_date = Column(Date, default=datetime.utcnow)
    grade_level = Column(String(20))  # Class 1-12
    section = Column(String(10))  # A, B, C
    roll_number = Column(String(20))
    
    # Simple relationship to User
    user = relationship("User", lazy="selectin")
    # Relationship to Parent
    parent = relationship("SchoolParent", overlaps="children")


# For backward compatibility - reference to existing students table
Student = SchoolStudent
