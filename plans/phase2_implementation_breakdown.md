# Phase 2 Implementation Plan: College Features & Academic System

**Based on: Separate Database Architecture 2 (Comprehensive)**

---

## Phase 2 Focus: College Academic System

This phase adds college-specific features and academic management.

---

## Task 1: College Database Models

### 1.1 Program & Semester Models
**File: `app/models/college_models.py`**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean, Date, Time

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    code = Column(String(20))
    hod_teacher_id = Column(Integer, ForeignKey("teachers.id"))
    description = Column(Text)

class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))   # "Bachelor of Computer Science"
    code = Column(String(20))    # "BCS"
    department_id = Column(Integer, ForeignKey("departments.id"))
    level = Column(String(50))   # "Bachelor", "Master", "PhD"
    duration_years = Column(Float)
    total_credits = Column(Integer)
    is_active = Column(Boolean, default=True)

class Semester(Base):
    __tablename__ = "semesters"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))    # "Fall 2024"
    program_id = Column(Integer, ForeignKey("programs.id"))
    is_current = Column(Boolean, default=False)
    start_date = Column(Date)
    end_date = Column(Date)
```

### 1.2 Course Models (with Credits)
```python
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True)
    course_code = Column(String(20), unique=True)
    course_name = Column(String(255))
    description = Column(Text)
    credits = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    is_elective = Column(Boolean, default=False)

class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    prerequisite_id = Column(Integer, ForeignKey("courses.id"))
```

---

## Task 2: Student Enrollment System

### 2.1 Enrollment Models
```python
class EnrollmentRequest(Base):
    __tablename__ = "enrollment_requests"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    status = Column(String(20))  # pending, approved, rejected
    request_date = Column(DateTime)
    approved_by = Column(Integer, ForeignKey("users.id"))

class ElectiveGroup(Base):
    __tablename__ = "elective_groups"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))  # "Department Elective I"
    program_id = Column(Integer, ForeignKey("programs.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    min_courses = Column(Integer)
    max_courses = Column(Integer)
```

### 2.2 API Endpoints
**File: `app/api/endpoints/college/enrollments.py`**
```python
router = APIRouter(prefix="/college/api/enrollments", tags=["Enrollments"])

@router.get("/available")
async def available_courses(
    student_id: int,
    semester_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Get courses available for enrollment"""
    ...

@router.post("/request")
async def request_enrollment(
    student_id: int,
    course_id: int,
    semester_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Submit course enrollment request"""
    ...

@router.get("/my")
async def my_enrollments(
    student_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Get student's current enrollments"""
    ...

@router.put("/{id}/approve")
async def approve_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Approve enrollment request"""
    ...
```

---

## Task 3: GPA & Grade Management

### 3.1 Grade Models
```python
class Grade(Base):
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    score = Column(Float)
    grade_letter = Column(String(2))  # A, B+, C, etc.
    grade_points = Column(Float)  # 4.0, 3.5, 2.0
    is_active = Column(Boolean, default=True)

class GPACalculation(Base):
    __tablename__ = "gpa_calculations"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    total_credits = Column(Integer)
    weighted_sum = Column(Float)
    gpa = Column(Float)

class CGPA(Base):
    __tablename__ = "cgpa"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    total_credits = Column(Integer)
    total_grade_points = Column(Float)
    cgpa = Column(Float)
    calculated_at = Column(DateTime)
```

### 3.2 GPA API
```python
@router.get("/gpa/{student_id}")
async def get_student_gpa(
    student_id: int,
    semester_id: int = None,
    db: AsyncSession = Depends(get_async_db)
):
    """Calculate GPA for semester or overall CGPA"""
    ...

@router.post("/calculate")
async def calculate_gpa(
    student_id: int,
    semester_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Calculate and store GPA"""
    ...
```

---

## Task 4: Enhanced Library (College)

### 4.1 Library Models
```python
class Journal(Base):
    __tablename__ = "journals"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    issn = Column(String(20))
    publisher = Column(String(255))
    category = Column(String(100))
    subscription_type = Column(String(50))
    cost = Column(Float)
    is_active = Column(Boolean, default=True)

class DigitalResource(Base):
    __tablename__ = "digital_resources"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    resource_type = Column(String(50))  # e-book, journal, database
    url = Column(String(500))
    access_type = Column(String(50))  # free, subscription
    description = Column(Text)

class JournalSubscription(Base):
    __tablename__ = "journal_subscriptions"
    
    id = Column(Integer, primary_key=True)
    journal_id = Column(Integer, ForeignKey("journals.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(Float)
```

---

## Task 5: Faculty & Salary Management

### 5.1 Faculty Models
```python
class FacultySalary(Base):
    __tablename__ = "faculty_salaries"
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    month = Column(String(10))    # "2024-01"
    base_salary = Column(Float)
    allowances = Column(Float)
    deductions = Column(Float)
    research_grant = Column(Float)
    net_pay = Column(Float)
    payment_date = Column(Date)
    status = Column(String(20))  # pending, paid

class ResearchGrant(Base):
    __tablename__ = "research_grants"
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    grant_title = Column(String(255))
    funding_agency = Column(String(255))
    amount = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20))  # active, completed
```

---

## Task 6: College Templates

### 6.1 Student Dashboard
**File: `app/templates/college/student/dashboard.html`**
```html
{% extends "college/base.html" %}

{% block content %}
<div class="dashboard">
    <h2>Welcome, {{ student.full_name }}</h2>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h3>Current GPA</h3>
            <p class="gpa">{{ current_gpa }}</p>
        </div>
        <div class="stat-card">
            <h3>CGPA</h3>
            <p class="cgpa">{{ cgpa }}</p>
        </div>
        <div class="stat-card">
            <h3>Credits Completed</h3>
            <p>{{ total_credits }}</p>
        </div>
        <div class="stat-card">
            <h3>Current Semester</h3>
            <p>{{ current_semester }}</p>
        </div>
    </div>
    
    <div class="sections">
        <section class="courses">
            <h3>My Courses</h3>
            <!-- Course list with grades -->
        </section>
        
        <section class="enrollment">
            <h3>Course Enrollment</h3>
            <a href="/college/student/enrollment">Register Courses</a>
        </section>
    </div>
</div>
{% endblock %}
```

---

## Files Summary

| Category | Files |
|----------|-------|
| Models | `app/models/college_models.py` |
| API | `app/api/endpoints/college/enrollments.py`, `app/api/endpoints/college/grades.py` |
| Templates | `app/templates/college/student/`, `app/templates/college/faculty/` |

---

## Database Changes

| Database | New Tables |
|----------|------------|
| college_db | departments, programs, semesters, courses, course_prerequisites, enrollment_requests, elective_groups, grades, gpa_calculations, cgpa, journals, digital_resources, journal_subscriptions, faculty_salaries, research_grants |
