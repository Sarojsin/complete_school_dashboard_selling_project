# Phase 3 Implementation Plan: Advanced College Features

**Based on: Separate Database Architecture 2 (Comprehensive)**

---

## Phase 3 Focus: Research, Placements, Hostel & Lab Management

---

## Task 1: Research Management

### 1.1 Research Models
**File: `app/models/college_models.py`** - Add:
```python
class ResearchProject(Base):
    __tablename__ = "research_projects"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    project_type = Column(String(50))  # individual, group, funded
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20))  # ongoing, completed
    funding_amount = Column(Float)
    funding_agency = Column(String(255))

class ResearchStudent(Base):
    __tablename__ = "research_students"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    role = Column(String(50))  # leader, member
    join_date = Column(Date)

class Publication(Base):
    __tablename__ = "publications"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    authors = Column(String(500))  # JSON array
    journal_name = Column(String(255))
    publication_date = Column(Date)
    doi = Column(String(100))
    impact_factor = Column(Float)
    status = Column(String(20))  # published, accepted, under_review
```

### 1.2 Research API
```python
@router.get("/projects")
async def list_projects(
    department_id: int = None,
    db: AsyncSession = Depends(get_async_db)
):
    """List all research projects"""
    ...

@router.post("/projects")
async def create_project(
    title: str,
    teacher_id: int,
    department_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Create new research project"""
    ...

@router.get("/publications")
async def list_publications(
    teacher_id: int = None,
    db: AsyncSession = Depends(get_async_db)
):
    """List publications"""
    ...
```

---

## Task 2: Placement Cell

### 2.1 Placement Models
```python
class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    industry = Column(String(100))
    website = Column(String(255))
    description = Column(Text)
    hr_name = Column(String(255))
    hr_email = Column(String(255))
    hr_phone = Column(String(20))
    is_active = Column(Boolean, default=True)

class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String(255))
    description = Column(Text)
    job_type = Column(String(50))  # internship, full_time
    location = Column(String(100))
    salary_min = Column(Float)
    salary_max = Column(Float)
    eligibility_criteria = Column(Text)
    application_deadline = Column(Date)
    status = Column(String(20))  # active, closed

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    job_id = Column(Integer, ForeignKey("job_postings.id"))
    apply_date = Column(DateTime)
    status = Column(String(20))  # applied, shortlisted, selected, rejected
    resume_path = Column(String(500))
```

### 2.2 Placement API
```python
@router.get("/companies")
async def list_companies(db: AsyncSession = Depends(get_async_db)):
    ...

@router.post("/companies")
async def add_company(db: AsyncSession = Depends(get_async_db)):
    ...

@router.get("/jobs")
async def list_jobs(status: str = "active", db: AsyncSession = Depends(get_async_db)):
    ...

@router.post("/jobs")
async def post_job(db: AsyncSession = Depends(get_async_db)):
    ...

@router.post("/apply/{job_id}")
async def apply_for_job(job_id: int, student_id: int, db: AsyncSession = Depends(get_async_db)):
    ...
```

---

## Task 3: Hostel Management

### 3.1 Hostel Models
```python
class Hostel(Base):
    __tablename__ = "hostels"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(500))
    total_rooms = Column(Integer)
    warden_name = Column(String(255))
    warden_contact = Column(String(20))

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"))
    room_number = Column(String(20))
    floor = Column(Integer)
    capacity = Column(Integer)
    occupied = Column(Integer, default=0)
    room_type = Column(String(20))  # single, double, triple
    rent_per_bed = Column(Float)

class HostelAllocation(Base):
    __tablename__ = "hostel_allocations"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    allocation_date = Column(Date)
    vacate_date = Column(Date)
    status = Column(String(20))  # active, vacated

class HostelComplaint(Base):
    __tablename__ = "hostel_complaints"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    category = Column(String(50))
    description = Column(Text)
    status = Column(String(20))  # pending, resolved
```

---

## Task 4: Lab Management

### 4.1 Lab Models
```python
class Lab(Base):
    __tablename__ = "labs"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    department_id = Column(Integer, ForeignKey("departments.id"))
    location = Column(String(100))
    capacity = Column(Integer)
    equipment_count = Column(Integer)

class LabEquipment(Base):
    __tablename__ = "lab_equipment"
    
    id = Column(Integer, primary_key=True)
    lab_id = Column(Integer, ForeignKey("labs.id"))
    name = Column(String(255))
    serial_number = Column(String(100))
    purchase_date = Column(Date)
    status = Column(String(20))  # working, maintenance, broken

class LabBooking(Base):
    __tablename__ = "lab_bookings"
    
    id = Column(Integer, primary_key=True)
    lab_id = Column(Integer, ForeignKey("labs.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    purpose = Column(String(255))
    status = Column(String(20))  # pending, approved, rejected
```

---

## Files Summary

| Category | Files |
|----------|-------|
| Models | `app/models/college_models.py` (extend) |
| API | `app/api/endpoints/college/research.py`, `app/api/endpoints/college/placements.py`, `app/api/endpoints/college/hostel.py`, `app/api/endpoints/college/lab.py` |
| Templates | `app/templates/college/research/`, `app/templates/college/placement/`, `app/templates/college/hostel/`, `app/templates/college/lab/` |

---

## Database Changes

| Database | New Tables |
|----------|------------|
| college_db | research_projects, research_students, publications, companies, job_postings, job_applications, hostels, rooms, hostel_allocations, hostel_complaints, labs, lab_equipment, lab_bookings |
