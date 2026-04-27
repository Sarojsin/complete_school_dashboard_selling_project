# Migration Phase 6: Create College Features

**Duration:** 3-5 days  
**Goal:** Implement college-specific features not present in school mode

---

## Overview

Phase 6 adds new models, repositories, services, and endpoints for college-specific features that don't exist in the current school management system.

---

## New Features to Implement

| Feature | Description | Priority |
|---------|-------------|----------|
| Programs | Academic programs/degrees | High |
| Semesters | Semester management | High |
| Enrollments | Course enrollment system | High |
| Faculty | College faculty members | High |
| Deans | Dean management | Medium |
| Registrars | Registrar functions | Medium |
| Placements | Campus placement system | Medium |
| Research | Research projects/publications | Medium |
| Hostels | Hostel management | Medium |
| Labs | Laboratory management | Low |

---

## Step-by-Step Tasks

### Step 1: Create College Models

#### 1.1 Program Model
**Create: `app/models/college/program.py`**
```python
from sqlalchemy import Column, Integer, String, Text, Date
from app.core.database import Base

class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True)
    duration_years = Column(Integer, default=4)
    department_id = Column(Integer, ForeignKey("departments.id"))
    description = Column(Text)
    created_at = Column(Date, default=datetime.utcnow)
```

#### 1.2 Semester Model
**Create: `app/models/college/semester.py`**
```python
class Semester(Base):
    __tablename__ = "semesters"
    
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("programs.id"))
    number = Column(Integer)  # 1, 2, 3, 4...
    academic_year = Column(String(20))
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=False)
```

#### 1.3 Enrollment Model
**Create: `app/models/college/enrollment.py`**
```python
class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("college_students.id"))
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    course_id = Column(Integer, ForeignKey("college_courses.id"))
    enrollment_date = Column(Date, default=datetime.utcnow)
    status = Column(String(20))  # enrolled, dropped, completed
    grade = Column(String(5))
    grade_point = Column(Float)
```

#### 1.4 Faculty Model
**Create: `app/models/college/faculty.py`**
```python
class Faculty(Base):
    __tablename__ = "faculty"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    employee_id = Column(String(50), unique=True)
    designation = Column(String(100))
    qualification = Column(String(200))
    specialization = Column(String(200))
    experience_years = Column(Integer)
    joining_date = Column(Date)
```

#### 1.5 Dean Model
**Create: `app/models/college/dean.py`**
```python
class Dean(Base):
    __tablename__ = "deans"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    school_name = Column(String(200))  # School of Engineering, etc.
    appointment_date = Column(Date)
    term_end_date = Column(Date)
```

#### 1.6 Placement Model
**Create: `app/models/college/placement.py`**
```python
class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    industry = Column(String(100))
    website = Column(String(200))
    description = Column(Text)
    logo = Column(String(200))

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String(200))
    description = Column(Text)
    requirements = Column(Text)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    deadline = Column(Date)
    is_active = Column(Boolean, default=True)

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    student_id = Column(Integer, ForeignKey("college_students.id"))
    applied_date = Column(Date, default=datetime.utcnow)
    status = Column(String(20))  # applied, shortlisted, rejected, selected
```

#### 1.7 Research Model
**Create: `app/models/college/research.py`**
```python
class ResearchProject(Base):
    __tablename__ = "research_projects"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    principal_investigator_id = Column(Integer, ForeignKey("faculty.id"))
    co_investigators = Column(JSON)
    funding_amount = Column(Integer)
    funding_agency = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(50))  # ongoing, completed

class Publication(Base):
    __tablename__ = "publications"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    authors = Column(JSON)
    journal = Column(String(200))
    publication_date = Column(Date)
    doi = Column(String(100))
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
```

#### 1.8 Hostel Model
**Create: `app/models/college/hostel.py`**
```python
class Hostel(Base):
    __tablename__ = "hostels"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    capacity = Column(Integer)
    warden_id = Column(Integer, ForeignKey("faculty.id"))
    address = Column(Text)

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"))
    room_number = Column(String(20))
    floor = Column(Integer)
    capacity = Column(Integer)
    occupied = Column(Integer, default=0)
    room_type = Column(String(50))  # single, double, triple

class HostelAllocation(Base):
    __tablename__ = "hostel_allocations"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("college_students.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    allocation_date = Column(Date)
    vacate_date = Column(Date)
```

### Step 2: Create College Repositories

#### 2.1 Program Repository
**Create: `app/repositories/college/program_repository.py`**
```python
from sqlalchemy.orm import Session
from app.models.college.program import Program

class ProgramRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Program).all()
    
    def get_by_id(self, program_id: int):
        return self.db.query(Program).filter(Program.id == program_id).first()
    
    def create(self, program_data: dict):
        program = Program(**program_data)
        self.db.add(program)
        self.db.commit()
        self.db.refresh(program)
        return program
    
    def update(self, program_id: int, program_data: dict):
        program = self.get_by_id(program_id)
        for key, value in program_data.items():
            setattr(program, key, value)
        self.db.commit()
        return program
    
    def delete(self, program_id: int):
        program = self.get_by_id(program_id)
        self.db.delete(program)
        self.db.commit()
```

#### 2.2 Enrollment Repository
**Create: `app/repositories/college/enrollment_repository.py`**
```python
class EnrollmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_student_enrollments(self, student_id: int):
        return self.db.query(Enrollment).filter(
            Enrollment.student_id == student_id
        ).all()
    
    def get_semester_enrollments(self, semester_id: int):
        return self.db.query(Enrollment).filter(
            Enrollment.semester_id == semester_id
        ).all()
    
    def enroll_student(self, enrollment_data: dict):
        enrollment = Enrollment(**enrollment_data)
        self.db.add(enrollment)
        self.db.commit()
        return enrollment
```

#### 2.3 Placement Repository
**Create: `app/repositories/college/placement_repository.py`**
```python
class PlacementRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_active_jobs(self):
        return self.db.query(Job).filter(Job.is_active == True).all()
    
    def apply_for_job(self, job_id: int, student_id: int):
        application = Application(
            job_id=job_id,
            student_id=student_id,
            status="applied"
        )
        self.db.add(application)
        self.db.commit()
        return application
```

### Step 3: Create College Services

**Create: `app/services/college/__init__.py`**

#### 3.1 Program Service
**Create: `app/services/college/program_service.py`**
```python
class ProgramService:
    def __init__(self, program_repo: ProgramRepository):
        self.program_repo = program_repo
    
    def create_program(self, data: dict):
        # Business logic
        return self.program_repo.create(data)
    
    def list_programs(self, department_id: int = None):
        programs = self.program_repo.get_all()
        if department_id:
            programs = [p for p in programs if p.department_id == department_id]
        return programs
```

#### 3.2 Enrollment Service
**Create: `app/services/college/enrollment_service.py`**
```python
class EnrollmentService:
    def __init__(self, enrollment_repo: EnrollmentRepository):
        self.enrollment_repo = enrollment_repo
    
    def enroll_student(self, student_id: int, course_ids: list, semester_id: int):
        enrollments = []
        for course_id in course_ids:
            enrollment = self.enrollment_repo.enroll_student({
                "student_id": student_id,
                "course_id": course_id,
                "semester_id": semester_id,
                "status": "enrolled"
            })
            enrollments.append(enrollment)
        return enrollments
    
    def calculate_gpa(self, student_id: int):
        # Calculate GPA from grades
        pass
```

#### 3.3 Placement Service
**Create: `app/services/college/placement_service.py`**
```python
class PlacementService:
    def __init__(self, placement_repo: PlacementRepository):
        self.placement_repo = placement_repo
    
    def get_eligible_jobs(self, student_id: int):
        # Filter jobs based on student criteria
        return self.placement_repo.get_active_jobs()
    
    def apply_for_job(self, job_id: int, student_id: int):
        return self.placement_repo.apply_for_job(job_id, student_id)
```

### Step 4: Create College API Endpoints

#### 4.1 Programs Endpoint
**Create: `app/api/v1/college/programs.py`**
```python
from fastapi import APIRouter, Depends
from app.repositories.college.program_repository import ProgramRepository
from app.services.college.program_service import ProgramService

router = APIRouter(prefix="/programs")

@router.get("/")
async def list_programs(
    department_id: int = None,
    service: ProgramService = Depends()
):
    programs = service.list_programs(department_id)
    return programs

@router.post("/")
async def create_program(
    program_data: dict,
    service: ProgramService = Depends()
):
    return service.create_program(program_data)

@router.get("/{program_id}")
async def get_program(program_id: int, service: ProgramService = Depends()):
    return service.get_program(program_id)
```

#### 4.2 Enrollments Endpoint
**Create: `app/api/v1/college/enrollments.py`**
```python
from fastapi import APIRouter, Depends
from app.services.college.enrollment_service import EnrollmentService

router = APIRouter(prefix="/enrollments")

@router.get("/student/{student_id}")
async def get_student_enrollments(
    student_id: int,
    service: EnrollmentService = Depends()
):
    return service.get_student_enrollments(student_id)

@router.post("/")
async def enroll_student(
    enrollment_data: dict,
    service: EnrollmentService = Depends()
):
    return service.enroll_student(
        enrollment_data["student_id"],
        enrollment_data["course_ids"],
        enrollment_data["semester_id"]
    )

@router.get("/student/{student_id}/gpa")
async def calculate_gpa(
    student_id: int,
    service: EnrollmentService = Depends()
):
    return {"gpa": service.calculate_gpa(student_id)}
```

#### 4.3 Placements Endpoint
**Create: `app/api/v1/college/placements.py`**
```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/placements")

@router.get("/jobs")
async def list_jobs(service: PlacementService = Depends()):
    return service.get_all_jobs()

@router.post("/apply")
async def apply_for_job(
    job_id: int,
    student_id: int,
    service: PlacementService = Depends()
):
    return service.apply_for_job(job_id, student_id)
```

#### 4.4 Research Endpoint
**Create: `app/api/v1/college/research.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/research")

@router.get("/projects")
async def list_projects():
    pass

@router.get("/publications")
async def list_publications():
    pass
```

#### 4.5 Hostel Endpoint
**Create: `app/api/v1/college/hostels.py`**
```python
from fastapi import APIRouter

router = APIRouter(prefix="/hostels")

@router.get("/")
async def list_hostels():
    pass

@router.post("/allocate")
async def allocate_room():
    pass
```

### Step 5: Register Models in Base

**Modify: `app/models/__init__.py`**
```python
# Add college models
from app.models.college.program import Program
from app.models.college.semester import Semester
from app.models.college.enrollment import Enrollment
from app.models.college.faculty import Faculty
from app.models.college.placement import Company, Job, Application
from app.models.college.research import ResearchProject, Publication
from app.models.college.hostel import Hostel, Room, HostelAllocation
```

---

## Files to Create Summary

| Category | Files |
|----------|-------|
| Models | program.py, semester.py, enrollment.py, faculty.py, dean.py, placement.py, research.py, hostel.py |
| Repositories | program_repository.py, enrollment_repository.py, placement_repository.py |
| Services | program_service.py, enrollment_service.py, placement_service.py |
| Endpoints | programs.py, enrollments.py, placements.py, research.py, hostels.py |

---

## Verification Checklist

- [ ] All college models created
- [ ] Repositories working
- [ ] Services implementing business logic
- [ ] API endpoints responding
- [ ] Database migrations run
- [ ] CRUD operations working

---

## Dependencies

- Phase 2 (Models restructured)
- Phase 3 (Repositories organized)
- Phase 4 (API endpoints structured)

---

## Next Phase

After Phase 6 → Go to [Phase 7: Database Separation](migration_phase7.md)

---

*End of Phase 6*
