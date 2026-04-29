from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from modules.shared.base import Base

class Teacher(Base):
    __tablename__ = "teachers"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    phone = Column(String(20))
    department = Column(String(100))
    qualification = Column(String(255))
    specialization = Column(String(255))
    joining_date = Column(Date, default=datetime.utcnow)
    status = Column(String(20), default="active")
    
    # Simple relationship to User (User is in modules.shared.models)
    user = relationship("User", lazy="selectin")
