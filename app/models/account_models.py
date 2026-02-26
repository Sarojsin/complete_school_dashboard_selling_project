from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .models import Base

class TeacherPayment(Base):
    __tablename__ = "teacher_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    amount = Column(Float)
    month = Column(String(7))  # Format: YYYY-MM
    payment_type = Column(String, default="salary")  # salary, bonus, allowance
    paid_by = Column(Integer, ForeignKey("users.id"))
    paid_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    # Relationships
    teacher = relationship("Teacher", back_populates="payments")
    payer = relationship("User")
    
    @property
    def teacher_name(self):
        return self.teacher.full_name if self.teacher else "Unknown"
        
    @property
    def paid_by_name(self):
        return self.payer.full_name if self.payer else (self.payer.username if self.payer else "Authority")