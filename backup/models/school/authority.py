"""
School Authority Model

Authority model for school system (principals, vice-principals, administrators).
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backup.models.base import Base


class SchoolAuthority(Base):
    """
    School Authority model for school system
    """
    __tablename__ = "school_authorities"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(255))
    position = Column(String(100))  # Principal, Vice Principal, Admin
    department = Column(String(100))
    phone = Column(String(20))
    
    # Relationships
    user = relationship("User", back_populates="school_authority_profile")


# For backward compatibility - reference to existing authorities table
Authority = SchoolAuthority
