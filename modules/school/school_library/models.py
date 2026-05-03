# School Library Models
# ====================

from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func as sql_func

from modules.shared.base import Base


class SchoolBook(Base):
    """School Book model"""
    __tablename__ = "school_books"
    
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), nullable=False, unique=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False)
    publisher = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False, index=True)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    shelf_location = Column(String(50), nullable=True)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=sql_func.now())
    updated_at = Column(DateTime, server_default=sql_func.now(), onupdate=sql_func.now())


class SchoolBookLoan(Base):
    """School Book Loan model"""
    __tablename__ = "school_book_loans"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="issued")
    remarks = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=sql_func.now())
    updated_at = Column(DateTime, server_default=sql_func.now(), onupdate=sql_func.now())


class SchoolBookReservation(Base):
    """School Book Reservation model"""
    __tablename__ = "school_book_reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    reservation_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, server_default=sql_func.now())
    updated_at = Column(DateTime, server_default=sql_func.now(), onupdate=sql_func.now())


__all__ = ["SchoolBook", "SchoolBookLoan", "SchoolBookReservation"]