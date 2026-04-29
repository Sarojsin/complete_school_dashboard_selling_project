from sqlalchemy import Column, Integer, String, Time, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from modules.shared.base import Base
from modules.school.school_classes.models import SchoolClass
from modules.school.school_teacher.models import Teacher
import enum


class DayOfWeek(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class TimetableEntry(Base):
    __tablename__ = "timetable_entries"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("school_courses.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    class_id = Column(Integer, ForeignKey("school_classes.id"), nullable=True)
    day_of_week = Column(SQLEnum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room = Column(String(50), nullable=True)
    academic_year = Column(String(20), nullable=True)
    semester = Column(String(20), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)

    # Relationships
    course = relationship("SchoolCourse")
    teacher = relationship(Teacher)
    school_class = relationship(SchoolClass)


class Period(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True, index=True)
    period_number = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    name = Column(String(50), nullable=True)
    is_break = Column(Integer, default=0, nullable=False)
    academic_year = Column(String(20), nullable=True)

    # Relationships
    class_id = Column(Integer, ForeignKey("school_classes.id"), nullable=True)
    school_class = relationship(SchoolClass)