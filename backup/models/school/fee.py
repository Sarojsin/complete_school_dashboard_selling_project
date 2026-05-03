"""
School Fee Model

Fee structure and fee records for school system.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backup.models.base import Base


class SchoolFee(Base):
    """
    School Fee Structure model (fee structure by class/grade)
    """
    __tablename__ = "school_fee_structures"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    grade_level = Column(String(20), nullable=False)  # Class 1-12
    academic_year = Column(String(20), nullable=False)
    tuition_fee = Column(Float, default=0.0)
    registration_fee = Column(Float, default=0.0)
    library_fee = Column(Float, default=0.0)
    sports_fee = Column(Float, default=0.0)
    lab_fee = Column(Float, default=0.0)
    activity_fee = Column(Float, default=0.0)
    other_charges = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    status = Column(String(20), default="active")
    description = Column(Text)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)


class SchoolFeeRecord(Base):
    """
    School Fee Record model (individual student fee payments)
    """
    __tablename__ = "school_fee_records"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    fee_type = Column(String(100), nullable=False)  # tuition, library, sports, etc.
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    paid_amount = Column(Float, default=0.0)
    payment_date = Column(Date)
    status = Column(String(20), default="pending")  # pending, paid, overdue, partial
    remarks = Column(Text)
    
    # Relationships
    student = relationship("SchoolStudent", back_populates="school_fees")


# For backward compatibility - reference
FeeStructure = SchoolFee
FeeRecord = SchoolFeeRecord
