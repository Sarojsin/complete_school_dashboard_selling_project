from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .models import Base

class Book(Base):                                      # NEW MODEL
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    isbn = Column(String(20), unique=True, nullable=True)
    category = Column(String(100))
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    loans = relationship("BookLoan", back_populates="book")

class BookLoan(Base):
    __tablename__ = "book_loans"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    book_id = Column(Integer, ForeignKey("books.id"), nullable=True)  # NEW FK
    book_title = Column(String)
    book_author = Column(String)
    book_isbn = Column(String, nullable=True)
    taken_date = Column(Date, default=datetime.utcnow().date())
    due_date = Column(Date)
    return_date = Column(Date, nullable=True)
    status = Column(String, default="borrowed")  # borrowed, returned, overdue
    fine_amount = Column(Integer, default=0)
    
    # Relationships
    student = relationship("Student", back_populates="book_loans")
    book = relationship("Book", back_populates="loans")              # NEW