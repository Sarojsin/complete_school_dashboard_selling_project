from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean, Date, Time, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backup.core.database import Base

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


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    profile_picture = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False, cascade="all, delete-orphan")
    authority_profile = relationship("Authority", back_populates="user", uselist=False, cascade="all, delete-orphan")
    parent_profile = relationship("Parent", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Student(Base):
    __tablename__ = "students"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    date_of_birth = Column(Date)
    phone = Column(String(20))
    address = Column(Text)
    parent_name = Column(String(255))
    parent_phone = Column(String(20))
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=True)
    enrollment_date = Column(Date, default=datetime.utcnow)
    grade_level = Column(String(20))
    section = Column(String(10))
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    # Relationships
    department_obj = relationship("Department", back_populates="students", foreign_keys=[department_id])
    
    # Relationships
    user = relationship("User", back_populates="student_profile")
    parent = relationship("Parent", back_populates="children")
    enrollments = relationship("CourseEnrollment", back_populates="student", cascade="all, delete-orphan")
    assignments = relationship("AssignmentSubmission", back_populates="student", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    fees = relationship("FeeRecord", back_populates="student", cascade="all, delete-orphan")
    test_submissions = relationship("TestSubmission", back_populates="student", cascade="all, delete-orphan")
    video_watch_history = relationship("VideoProgress", back_populates="student", cascade="all, delete-orphan")
    exam_results = relationship("ExamResult", back_populates="student", cascade="all, delete-orphan")
    book_loans = relationship("BookLoan", back_populates="student", cascade="all, delete-orphan")


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
    status = Column(String(20), default="active") # active, inactive, on_leave, retired
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    # Relationships
    department_obj = relationship("Department", back_populates="teachers", foreign_keys=[department_id])
    hod_department = relationship("Department", back_populates="hod", uselist=False, foreign_keys="[Department.hod_teacher_id]")
    
    # Relationships
    user = relationship("User", back_populates="teacher_profile")
    courses = relationship("Course", back_populates="teacher")
    assignments = relationship("Assignment", back_populates="teacher")
    tests = relationship("Test", back_populates="teacher")
    notes = relationship("Note", back_populates="teacher", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="teacher", cascade="all, delete-orphan")
    notices = relationship("Notice", back_populates="teacher", cascade="all, delete-orphan")
    payments = relationship("TeacherPayment", back_populates="teacher", cascade="all, delete-orphan")


class Authority(Base):
    __tablename__ = "authorities"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(255))
    position = Column(String(100))
    department = Column(String(100))
    phone = Column(String(20))
    
    # Relationships
    user = relationship("User", back_populates="authority_profile")
    notices = relationship("Notice", back_populates="authority", cascade="all, delete-orphan")

class Parent(Base):
    __tablename__ = "parents"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    occupation = Column(String(100))
    
    # Relationships
    user = relationship("User", back_populates="parent_profile")
    children = relationship("Student", back_populates="parent")


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(50), unique=True, nullable=False, index=True)
    course_name = Column(String(255), nullable=False)
    description = Column(Text)
    credits = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"))
    grade_level = Column(String(20))
    semester = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="course", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="course", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="course", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="course", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="course", cascade="all, delete-orphan")

class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enrollment_date = Column(Date, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Assignment(Base):
    __tablename__ = "assignments"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    due_date = Column(DateTime, nullable=False)
    max_score = Column(Float, default=100.0)
    file_path = Column(String(500))
    target_classes = Column(String(255)) # Comma-separated list of classes (e.g., "9A,9B")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="assignments")
    teacher = relationship("Teacher", back_populates="assignments")
    submissions = relationship("AssignmentSubmission", back_populates="assignment", cascade="all, delete-orphan")

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    submission_text = Column(Text)
    file_path = Column(String(500))
    submitted_at = Column(DateTime, default=datetime.utcnow)
    score = Column(Float)
    feedback = Column(Text)
    graded_at = Column(DateTime)
    
    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="assignments")

class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)  # present, absent, late
    arrival_time = Column(Time, nullable=True)
    remarks = Column(Text)
    
    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    course = relationship("Course", back_populates="attendance_records")

class FeeStructure(Base):
    __tablename__ = "fee_structures"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    grade_level = Column(String(20), nullable=False)
    academic_year = Column(String(20), nullable=False)
    tuition_fee = Column(Float, default=0.0)
    registration_fee = Column(Float, default=0.0)
    library_fee = Column(Float, default=0.0)
    sports_fee = Column(Float, default=0.0)
    lab_fee = Column(Float, default=0.0)
    activity_fee = Column(Float, default=0.0)
    other_charges = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    status = Column(String(20), default="active")
    description = Column(Text)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    grade_type = Column(String(50))  # midterm, final, quiz, assignment
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    grade = Column(String(5))  # A, B+, B, etc.
    remarks = Column(Text)
    date = Column(Date, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")

class FeeRecord(Base):
    __tablename__ = "fee_records"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    fee_type = Column(String(100), nullable=False)  # tuition, library, sports, etc.
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    paid_amount = Column(Float, default=0.0)
    payment_date = Column(Date)
    status = Column(String(20), default="pending")  # pending, paid, overdue, partial
    remarks = Column(Text)
    
    # Relationships
    student = relationship("Student", back_populates="fees")

    @property
    def student_name(self):
        return self.student.user.full_name if self.student and self.student.user else "N/A"

    @property
    def student_avatar(self):
        return "/static/img/avatars/default.png"

    @property
    def grade(self):
        return self.student.grade_level if self.student else "N/A"

    @property
    def section(self):
        return self.student.section if self.student else ""

    @property
    def quarter(self):
        month = self.due_date.month
        if 1 <= month <= 3: return "Q1"
        if 4 <= month <= 6: return "Q2"
        if 7 <= month <= 9: return "Q3"
        return "Q4"

    @property
    def total_amount(self):
        return self.amount

    @property
    def balance(self):
        return self.amount - self.paid_amount

    @property
    def is_overdue(self):
        from datetime import date
        return self.status == 'overdue' or (self.status == 'pending' and self.due_date < date.today())
    
    @property
    def payment_method(self):
        return None

class Notice(Base):
    __tablename__ = "notices"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    authority_id = Column(Integer, ForeignKey("authorities.id", ondelete="CASCADE"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=True)
    target_role = Column(String(20))  # all, student, teacher
    target_grade = Column(String(50))
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    file_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # Relationships
    authority = relationship("Authority", back_populates="notices")
    teacher = relationship("Teacher", back_populates="notices")

class Schedule(Base):
    __tablename__ = "schedules"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room = Column(String(50))
    
    # Relationships
    course = relationship("Course", back_populates="schedules")

class Note(Base):
    __tablename__ = "notes"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50))
    is_approved = Column(Boolean, default=True, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="notes")
    teacher = relationship("Teacher", back_populates="notes")

class Video(Base):
    __tablename__ = "videos"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(500), nullable=False)
    duration = Column(Integer)  # in seconds
    file_size = Column(Integer)
    is_approved = Column(Boolean, default=True, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="videos")
    teacher = relationship("Teacher", back_populates="videos")
    watch_history = relationship("VideoProgress", back_populates="video", cascade="all, delete-orphan")

class VideoProgress(Base):
    __tablename__ = "video_progress"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    is_watched = Column(Boolean, default=True)
    watched_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    video = relationship("Video", back_populates="watch_history")
    student = relationship("Student", back_populates="video_watch_history")

class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
