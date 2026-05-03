from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from modules.shared.base import Base


class GroupPostType(str, enum.Enum):
    NOTICE = "notice"
    DISCUSSION = "discussion"
    ANNOUNCEMENT = "announcement"


class GroupMemberRole(str, enum.Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    AUTHORITY = "authority"
    PARENT = "parent"


class Group(Base):
    __tablename__ = "groups"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    code = Column(String(20), unique=True, nullable=False)  # Unique code for joining
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships - using string references for now
    # members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    # posts = relationship("GroupPost", back_populates="group", cascade="all, delete-orphan")
    # creator = relationship("User", foreign_keys=[created_by])


class GroupMember(Base):
    __tablename__ = "group_members"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(GroupMemberRole), default=GroupMemberRole.STUDENT)
    is_active = Column(Boolean, default=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships - using string references for now
    # group = relationship("Group", back_populates="members")
    # user = relationship("User", foreign_keys=[user_id])


class GroupPost(Base):
    __tablename__ = "group_posts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    post_type = Column(SQLEnum(GroupPostType), default=GroupPostType.DISCUSSION)
    link_url = Column(String(500))
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships - using string references for now
    # group = relationship("Group", back_populates="posts")
    # author = relationship("User", foreign_keys=[author_id])