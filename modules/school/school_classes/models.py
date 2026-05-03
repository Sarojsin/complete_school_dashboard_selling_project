from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from modules.school.school_teacher.models import Teacher
from modules.shared.base import Base

class SchoolClass(Base):
    """
    School Class model (Class 1-12 with sections)
    """
    __tablename__ = "school_classes"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))  # "Class 1", "Class 10"
    section = Column(String(10))  # "A", "B"
    class_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    academic_year = Column(String(20))
    
    # Relationships (One-way to avoid circular dependencies in modular structure)
    class_teacher = relationship(Teacher)
    
    
# For backward compatibility
Class = SchoolClass

__all__ = ["SchoolClass"]
