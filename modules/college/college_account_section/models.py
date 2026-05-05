"""
College Account Section Models

Payment records for college faculty (salary, bonuses, etc.).
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.college.base import CollegeBase as Base


class CollegeFacultyPayment(Base):
    """
    Faculty Payment model for college account section.
    Records salary/bonus payments to faculty members.
    """
    __tablename__ = "college_faculty_payments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("college_faculty.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    month = Column(String(7))  # Format: YYYY-MM (for salary period)
    payment_type = Column(String(20), default="salary")  # salary, bonus, allowance, reimbursement
    paid_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    paid_at = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(50), default="bank_transfer")  # bank_transfer, cash, check
    transaction_reference = Column(String(100), nullable=True)
    remarks = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    faculty = relationship("Faculty", back_populates="payments")
    paid_by = relationship("User")


# Extend Faculty model to include payments relationship if not already present
# Note: backup.models.college.faculty.Faculty may not have payments defined
# We define it here via extension (but relationship must be on primary model)
# To avoid dual definition issues, we'll just use one-way relationship from payment side.

__all__ = ["CollegeFacultyPayment"]
