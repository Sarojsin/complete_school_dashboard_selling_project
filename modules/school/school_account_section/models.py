# School Account Section Models
# =============================

from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func as sql_func

from modules.shared.base import Base


class SchoolFee(Base):
    """School Fee model for fee management"""
    __tablename__ = "school_fees"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    fee_type = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False, default=0)
    due_date = Column(Date, nullable=True)
    paid_amount = Column(Float, nullable=False, default=0)
    payment_date = Column(Date, nullable=True)
    payment_status = Column(String(20), nullable=False, default="pending")
    remarks = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=sql_func.now())
    updated_at = Column(DateTime, server_default=sql_func.now(), onupdate=sql_func.now())


class SchoolExpense(Base):
    """School Expense model for expense tracking"""
    __tablename__ = "school_expenses"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False, default=0)
    description = Column(String(500), nullable=True)
    expense_date = Column(Date, nullable=False)
    vendor = Column(String(200), nullable=True)
    receipt_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=sql_func.now())
    updated_at = Column(DateTime, server_default=sql_func.now(), onupdate=sql_func.now())


class SchoolPayment(Base):
    """School Payment model for teacher salary payments"""
    __tablename__ = "school_payments"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_type = Column(String(50), nullable=False)  # salary, bonus, etc.
    description = Column(String(500), nullable=True)
    payment_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=sql_func.now())


__all__ = ["SchoolFee", "SchoolExpense", "SchoolPayment"]