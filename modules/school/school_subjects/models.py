from sqlalchemy import Column, Integer, String, Text
from modules.shared.base import Base

class SchoolSubject(Base):
    """
    School Subject model
    """
    __tablename__ = "school_subjects"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Simple relationship (one-way)
    # Most related fields use subject_id as ForeignKey

# For backward compatibility
Subject = SchoolSubject

__all__ = ["SchoolSubject"]
