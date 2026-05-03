"""
College Fee Model

Fee structure for college system (per credit based).
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase


class CollegeFee(CollegeBase):
    """
    College Fee Structure model (per credit based)
    """
    __tablename__ = "college_fee_structures"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("college_programs.id"))
    semester_id = Column(Integer, ForeignKey("college_semesters.id"))
    tuition_per_credit = Column(Integer)
    lab_fee = Column(Integer)
    library_fee = Column(Integer)
    sports_fee = Column(Integer)
    other_fee = Column(Integer)
    total_amount = Column(Integer)
    academic_year = Column(String(20))
    status = Column(String(20), default="active")


class CollegeFeeRecord(CollegeBase):
    """
    College Fee Record model (individual student fee payments)
    """
    __tablename__ = "college_fee_records"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("college_students.id", ondelete="CASCADE"), nullable=False)
    semester_id = Column(Integer, ForeignKey("college_semesters.id"))
    fee_type = Column(String(100), nullable=False)  # tuition, lab, library, etc.
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    paid_amount = Column(Float, default=0.0)
    payment_date = Column(Date)
    status = Column(String(20), default="pending")  # pending, paid, overdue, partial
    remarks = Column(Text)
    
    # Relationships
    student = relationship("CollegeStudent")
    semester = relationship("Semester")
