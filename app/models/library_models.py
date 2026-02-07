from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .models import Base

class BookLoan(Base):
    __tablename__ = "book_loans"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
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