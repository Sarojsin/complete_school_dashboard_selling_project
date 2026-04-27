# Migration Phase 2: Restructure Models

**Duration:** 2-3 days  
**Goal:** Organize database models into school/college folders

---

## Overview

Phase 2 reorganizes the models directory into a structured format with separate folders for school-specific and college-specific models, plus a base model.

---

## Current State

```
app/models/
├── __init__.py           # Exports all models
├── account_models.py     # Account related
├── admin_models.py       # Admin/feature related
├── chat_models.py       # Chat
├── department_models.py  # Department (college)
├── exam_models.py       # Exam
├── group_models.py       # Groups
├── library_models.py    # Library
├── models.py            # Main models (User, Student, Teacher)
└── test_models.py       # Tests/assignments
```

---

## Target State After Phase 2

```
app/models/
├── __init__.py
├── base.py               # Base model class
├── user.py              # User model (shared)
├── school/              # ← NEW: School-specific models
│   ├── __init__.py
│   ├── student.py       # Student model
│   ├── teacher.py      # Teacher model
│   ├── parent.py       # Parent model
│   ├── authority.py    # Authority model
│   ├── class.py        # Class/Grade model
│   ├── section.py      # Section model
│   └── fee.py          # Fee structure
│
└── college/            # ← NEW: College-specific models
    ├── __init__.py
    ├── student.py      # Student model (different fields)
    ├── faculty.py     # Faculty model (like teacher)
    ├── department.py  # Department model
    ├── program.py     # Program model
    ├── semester.py    # Semester model
    ├── course.py      # Course model (with credits)
    ├── enrollment.py  # Enrollment model
    └── fee.py         # Fee structure (per credit)
```

---

## Step-by-Step Tasks

### Step 1: Create Base Model

**Create: `app/models/base.py`**
```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base model for all tables"""
    pass
```

### Step 2: Create School Models Directory

Create folder: `app/models/school/`

### Step 3: Move/Create School Models

#### 3.1 Student Model
**Create: `app/models/school/student.py`**
```python
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.models.base import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(String(50), unique=True)
    grade_level = Column(String(20))  # Class 1-12
    section = Column(String(10))      # A, B, C
    roll_number = Column(String(20))
    # ... other school-specific fields
```

#### 3.2 Teacher Model
**Create: `app/models/school/teacher.py`**
```python
# Teacher model for school
class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(String(50))
    qualification = Column(String(255))
    # ... school-specific fields
```

#### 3.3 Parent Model
**Create: `app/models/school/parent.py`**
```python
class Parent(Base):
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    occupation = Column(String(100))
    # ... parent-specific fields
```

#### 3.4 Authority Model
**Create: `app/models/school/authority.py`**
```python
class Authority(Base):
    __tablename__ = "authorities"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    position = Column(String(100))
    # ... authority-specific fields
```

#### 3.5 Class Model (NEW)
**Create: `app/models/school/class.py`**
```python
class SchoolClass(Base):
    __tablename__ = "school_classes"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))    # "Class 1", "Class 10"
    section = Column(String(10)) # "A", "B"
    class_teacher_id = Column(Integer, ForeignKey("teachers.id"))
    academic_year = Column(String(20))
```

#### 3.6 Fee Model
**Create: `app/models/school/fee.py`**
```python
class SchoolFee(Base):
    __tablename__ = "school_fees"
    
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("school_classes.id"))
    fee_type = Column(String(50))
    amount = Column(Integer)
    academic_year = Column(String(20))
```

#### 3.7 Create __init__.py
**Create: `app/models/school/__init__.py`**
```python
from .student import Student
from .teacher import Teacher
from .parent import Parent
from .authority import Authority
from .class import SchoolClass
from .fee import SchoolFee

__all__ = ["Student", "Teacher", "Parent", "Authority", "SchoolClass", "SchoolFee"]
```

### Step 4: Create College Models Directory

Create folder: `app/models/college/`

### Step 5: Move/Create College Models

#### 5.1 Department Model (Move existing)
**Current: `app/models/department_models.py`**  
→ Move to → `app/models/college/department.py`

```python
# Update with new structure
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    code = Column(String(20))
    hod_id = Column(Integer, ForeignKey("faculty.id"))
    description = Column(Text)
```

#### 5.2 Program Model (NEW)
**Create: `app/models/college/program.py`**
```python
class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))      # "Bachelor of Computer Science"
    code = Column(String(20))       # "BCS"
    department_id = Column(Integer, ForeignKey("departments.id"))
    level = Column(String(50))      # "Bachelor", "Master", "PhD"
    duration_years = Column(Integer)
    total_credits = Column(Integer)
```

#### 5.3 Semester Model (NEW)
**Create: `app/models/college/semester.py`**
```python
class Semester(Base):
    __tablename__ = "semesters"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))      # "Fall 2024"
    program_id = Column(Integer, ForeignKey("programs.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
```

#### 5.4 Course Model (NEW)
**Create: `app/models/college/course.py`**
```python
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20))
    name = Column(String(255))
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    instructor_id = Column(Integer, ForeignKey("faculty.id"))
    is_elective = Column(Boolean, default=False)
```

#### 5.5 Faculty Model (NEW)
**Create: `app/models/college/faculty.py`**
```python
class Faculty(Base):
    __tablename__ = "faculty"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(String(50))
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation = Column(String(100))
    qualification = Column(String(255))
    specialization = Column(String(255))
```

#### 5.6 Student Model (College)
**Create: `app/models/college/student.py`**
```python
class CollegeStudent(Base):
    __tablename__ = "college_students"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    roll_number = Column(String(50))
    program_id = Column(Integer, ForeignKey("programs.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    enrollment_date = Column(Date)
    cgpa = Column(Float)
```

#### 5.7 Enrollment Model (NEW)
**Create: `app/models/college/enrollment.py`**
```python
class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("college_students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    enrollment_date = Column(Date)
    status = Column(String(20))  # enrolled, completed, dropped
```

#### 5.8 Fee Model (College)
**Create: `app/models/college/fee.py`**
```python
class CollegeFee(Base):
    __tablename__ = "college_fees"
    
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    tuition_per_credit = Column(Integer)
    lab_fee = Column(Integer)
    total_amount = Column(Integer)
```

#### 5.9 Create __init__.py
**Create: `app/models/college/__init__.py`**
```python
from .department import Department
from .program import Program
from .semester import Semester
from .course import Course
from .faculty import Faculty
from .student import CollegeStudent
from .enrollment import Enrollment
from .fee import CollegeFee

__all__ = [
    "Department", "Program", "Semester", "Course", 
    "Faculty", "CollegeStudent", "Enrollment", "CollegeFee"
]
```

### Step 6: Update Main __init__.py

**Modify: `app/models/__init__.py`**
```python
from app.models.base import Base
from app.models.user import User

# School models
from app.models.school import Student, Teacher, Parent, Authority, SchoolClass, SchoolFee

# College models
from app.models.college import (
    Department, Program, Semester, Course, Faculty, 
    CollegeStudent, Enrollment, CollegeFee
)

__all__ = [
    "Base", "User",
    # School
    "Student", "Teacher", "Parent", "Authority", "SchoolClass", "SchoolFee",
    # College
    "Department", "Program", "Semester", "Course", "Faculty",
    "CollegeStudent", "Enrollment", "CollegeFee"
]
```

---

## Files to Create

| File | Purpose |
|------|---------|
| `app/models/base.py` | Base model class |
| `app/models/school/__init__.py` | School package |
| `app/models/school/student.py` | School student |
| `app/models/school/teacher.py` | School teacher |
| `app/models/school/parent.py` | Parent model |
| `app/models/school/authority.py` | Authority model |
| `app/models/school/class.py` | Class/grade model |
| `app/models/school/fee.py` | School fee model |
| `app/models/college/__init__.py` | College package |
| `app/models/college/department.py` | Department |
| `app/models/college/program.py` | Program |
| `app/models/college/semester.py` | Semester |
| `app/models/college/course.py` | Course with credits |
| `app/models/college/faculty.py` | Faculty |
| `app/models/college/student.py` | College student |
| `app/models/college/enrollment.py` | Course enrollment |
| `app/models/college/fee.py` | College fee |

---

## Files to Modify

| File | Change |
|------|--------|
| `app/models/__init__.py` | Update exports |
| `app/models/department_models.py` | Move to college/ or remove |
| All repository files | Update model imports |
| All service files | Update model imports |
| `app/core/database.py` | Check base import |

---

## Verification Checklist

- [ ] `app/models/base.py` created
- [ ] `app/models/school/` folder with all files
- [ ] `app/models/college/` folder with all files
- [ ] `app/models/__init__.py` updated
- [ ] All imports working
- [ ] Database tables created correctly
- [ ] Application runs without errors

---

## Testing Commands

```bash
# Test imports
python -c "from app.models.school import Student"
python -c "from app.models.college import Program"

# Test database
python -c "from app.core.database import engine; print(engine.table_names())"
```

---

## Next Phase

After Phase 2 → Go to [Phase 3: Create Module Structure](migration_phase3.md)

---

*End of Phase 2*
