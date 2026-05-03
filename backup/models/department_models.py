from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .models import Base

class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code = Column(String(10), unique=True)
    hod_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    
    # Relationships
    hod = relationship("Teacher", back_populates="hod_department", foreign_keys=[hod_teacher_id])
    teachers = relationship("Teacher", back_populates="department_obj", foreign_keys="[Teacher.department_id]")
    students = relationship("Student", back_populates="department_obj", foreign_keys="[Student.department_id]")
