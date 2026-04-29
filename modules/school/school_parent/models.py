"""
School Parent Model

Parent model for school system.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from modules.shared.base import Base


class SchoolParent(Base):
    """
    School Parent model for school system
    """
    __tablename__ = "school_parents"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    occupation = Column(String(100))
    
    # Relationships
    user = relationship("User")
    children = relationship("SchoolStudent", overlaps="parent")


# For backward compatibility - reference to existing parents table
Parent = SchoolParent