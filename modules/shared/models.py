from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum
import enum
from datetime import datetime
from modules.shared.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    AUTHORITY = "AUTHORITY"
    PARENT = "PARENT"
    HOD = "HOD"
    EXAM_SECTION = "EXAM_SECTION"
    LIBRARY_MANAGER = "LIBRARY_MANAGER"
    ACCOUNT_SECTION = "ACCOUNT_SECTION"
    GROUP_CREATOR = "GROUP_CREATOR"
    # College-specific roles
    DEAN = "DEAN"
    REGISTRAR = "REGISTRAR"

class PortalType(str, enum.Enum):
    SCHOOL = "school"
    COLLEGE = "college"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    portal_type = Column(SQLEnum(PortalType), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
