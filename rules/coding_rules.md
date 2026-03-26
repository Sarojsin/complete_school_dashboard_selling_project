Production-Ready Development Rules for School/College Management System
🚀 SENIOR DEVELOPER RULES
PART 1: ARCHITECTURE & DESIGN PATTERNS
Rule #1: Layered Architecture Strictly
text
✅ DO: 
API Layer → Service Layer → Repository Layer → Database

❌ DON'T:
API Layer → Database directly
Service Layer → Database directly
Controllers with business logic
Example:

python
# ✅ GOOD
@router.get("/students/{id}")
async def get_student(id: int, service: StudentService = Depends()):
    return await service.get_student_by_id(id)

class StudentService:
    def __init__(self, repo: StudentRepository):
        self.repo = repo
    
    async def get_student_by_id(self, id: int):
        student = await self.repo.get(id)
        if not student:
            raise StudentNotFoundError()
        return student

# ❌ BAD
@router.get("/students/{id}")
async def get_student(id: int, db: Session = Depends()):
    student = db.query(Student).filter(Student.id == id).first()
    return student
Rule #2: Repository Pattern for All Database Operations
Each entity has its own repository

Repositories only handle database operations

No business logic in repositories

Rule #3: Service Layer for Business Logic
All business rules in services

Services call repositories

Services raise custom exceptions

Services handle transactions

Rule #4: Dependency Injection Everywhere
No hard dependencies

Use FastAPI's Depends() properly

Make testing possible

PART 2: DATABASE DESIGN
Rule #5: Use UUIDs for Public IDs
python
# ✅ GOOD
class Student(Base):
    id = Column(Integer, primary_key=True)  # Internal
    uuid = Column(String, unique=True, index=True)  # Public
    enrollment_number = Column(String, unique=True)  # Business

# ❌ BAD
# Exposing auto-increment IDs in URLs: /student/123
Rule #6: Soft Delete Pattern
python
class BaseModel(Base):
    __abstract__ = True
    is_active = Column(Boolean, default=True)
    deleted_at = Column(DateTime, nullable=True)
    
    def soft_delete(self):
        self.is_active = False
        self.deleted_at = datetime.utcnow()
Rule #7: Audit Fields on Every Table
python
class BaseModel(Base):
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
Rule #8: Index Strategy
python
# Index these:
- Foreign keys
- Frequently searched fields (email, enrollment_no)
- Date ranges (for reports)
- Status fields

# Don't index:
- Boolean fields (low cardinality)
- Text/BLOB fields
- Frequently updated fields
Rule #9: Use Enum for Fixed Values
python
from enum import Enum as PyEnum

class UserRole(PyEnum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

# In model:
role = Column(Enum(UserRole), nullable=False)
Rule #10: Never Use String for Money
python
# ✅ GOOD
fee_amount = Column(Numeric(10, 2))  # Decimal

# ❌ BAD
fee_amount = Column(Float)  # Precision issues
fee_amount = Column(String)  # Can't calculate
PART 3: API DESIGN
Rule #11: RESTful URL Conventions
text
✅ GOOD:
GET    /api/v1/students
GET    /api/v1/students/{id}
POST   /api/v1/students
PUT    /api/v1/students/{id}
DELETE /api/v1/students/{id}
GET    /api/v1/students/{id}/grades

❌ BAD:
GET    /api/v1/getAllStudents
POST   /api/v1/saveStudent
GET    /api/v1/studentDetails
Rule #12: Version Your API
python
# main.py
app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")
Rule #13: Consistent Response Format
python
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any]
    errors: Optional[List[str]]
    meta: Optional[Dict]  # pagination info

# Always return this structure
Rule #14: Pagination for All List Endpoints
python
@router.get("/students")
async def get_students(
    page: int = Query(1, ge=1),
    size: int = Query(20, le=100),
    service: StudentService = Depends()
):
    return await service.get_paginated(page, size)
Rule #15: Filtering, Sorting, Searching
python
@router.get("/students")
async def get_students(
    department_id: Optional[int] = None,
    status: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    search: Optional[str] = None
):
    # Implement query building
    pass
PART 4: SECURITY
Rule #16: Never Trust User Input
python
# ✅ GOOD
from pydantic import BaseModel, validator

class StudentCreate(BaseModel):
    name: str
    email: str
    
    @validator('email')
    def validate_email(cls, v):
        if not validators.email(v):
            raise ValueError('Invalid email')
        return v

# ❌ BAD
@router.post("/students")
async def create_student(name: str, email: str):  # Raw input
    pass
Rule #17: Role-Based Access Control (RBAC)
python
def require_roles(roles: List[UserRole]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get('current_user')
            if user.role not in roles:
                raise HTTPException(403)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@router.get("/admin/dashboard")
@require_roles([UserRole.ADMIN])
async def admin_dashboard():
    pass
Rule #18: Rate Limiting
python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request):
    pass
Rule #19: CORS Configuration
python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Rule #20: JWT Best Practices
Short-lived access tokens (15-30 minutes)

Long-lived refresh tokens (7-30 days)

Store refresh tokens in database (allow revocation)

Include minimal claims (user_id, role, exp)

Rotate refresh tokens on use

PART 5: ERROR HANDLING
Rule #21: Custom Exception Classes
python
class AppException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code

class StudentNotFoundError(AppException):
    def __init__(self, student_id: int):
        super().__init__(f"Student {student_id} not found", 404)

class InsufficientPermissionError(AppException):
    def __init__(self):
        super().__init__("Insufficient permissions", 403)
Rule #22: Global Exception Handler
python
@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.code,
        content={
            "success": False,
            "message": exc.message,
            "data": None
        }
    )
PART 6: LOGGING & MONITORING
Rule #23: Structured Logging
python
import structlog

logger = structlog.get_logger()

@router.post("/payment")
async def process_payment():
    logger.info(
        "payment_processed",
        user_id=user.id,
        amount=payment.amount,
        status="success"
    )
Rule #24: Log Levels Properly
ERROR: Something is broken

WARN: Something unexpected but handled

INFO: Important business events

DEBUG: Development only (turn off in production)

Rule #25: Request ID for Tracing
python
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
PART 7: TESTING
Rule #26: Test Pyramid
Unit Tests: 70% (services, utilities)

Integration Tests: 20% (API, database)

E2E Tests: 10% (critical flows)

Rule #27: Fixtures for Test Data
python
@pytest.fixture
async def test_student(db_session):
    student = Student(
        name="Test Student",
        email="test@example.com"
    )
    db_session.add(student)
    await db_session.commit()
    return student
Rule #28: Mock External Services
python
@pytest.mark.asyncio
async def test_send_email(mock_email_service):
    mock_email_service.send.return_value = True
    result = await notification_service.send_email()
    assert result is True
PART 8: PERFORMANCE
Rule #29: N+1 Query Prevention
python
# ✅ GOOD
students = await db.execute(
    select(Student)
    .options(selectinload(Student.enrollments))
    .options(joinedload(Student.department))
)

# ❌ BAD
students = await db.execute(select(Student))
for student in students:
    print(student.enrollments)  # Triggers new query
Rule #30: Use Async Where Possible
python
# ✅ GOOD
async def get_students():
    async with async_session() as session:
        result = await session.execute(select(Student))
        return result.scalars().all()

# ❌ BAD (blocks)
def get_students():
    with sync_session() as session:
        return session.query(Student).all()
Rule #31: Cache Strategy
python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@router.get("/dashboard/stats")
@cache(expire=300)  # 5 minutes
async def get_dashboard_stats():
    # Expensive computation
    pass
Rule #32: Database Connection Pooling
python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True  # Check connection before using
)
PART 9: CODE QUALITY
Rule #33: Type Hints Everywhere
python
def calculate_gpa(grades: List[float]) -> float:
    return sum(grades) / len(grades)
Rule #34: Docstrings for Public Methods
python
def calculate_gpa(grades: List[float]) -> float:
    """
    Calculate GPA from list of grades.
    
    Args:
        grades: List of grade points (0.0 - 4.0)
        
    Returns:
        Average GPA rounded to 2 decimal places
        
    Raises:
        ValueError: If grades list is empty
    """
    if not grades:
        raise ValueError("Grades list cannot be empty")
    return round(sum(grades) / len(grades), 2)
Rule #35: Follow PEP 8
4 spaces indentation

79 character line limit

snake_case for functions/variables

CamelCase for classes

Rule #36: Linter & Formatter
bash
# Use these:
black .           # Auto-format
isort .           # Sort imports
flake8 .          # Style check
mypy .            # Type check
PART 10: DEPLOYMENT & DEVOPS
Rule #37: Environment Variables
python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    ALLOWED_HOSTS: List[str] = ["localhost"]
    
    class Config:
        env_file = ".env"
Rule #38: Health Check Endpoint
python
@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Check database
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "up"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
Rule #39: Graceful Shutdown
python
@app.on_event("shutdown")
async def shutdown():
    await db_engine.dispose()
    await redis_client.close()
Rule #40: Docker Best Practices
dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
PART 11: DOMAIN-SPECIFIC RULES FOR EDUCATION
Rule #41: Academic Year Handling
python
class AcademicYear(Base):
    name = Column(String)  # "2024-2025"
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    
    # Ensure only one current year
    @classmethod
    async def set_current(cls, year_id: int, db: Session):
        await db.execute(
            update(cls).values(is_current=False)
        )
        await db.execute(
            update(cls).where(cls.id == year_id).values(is_current=True)
        )
Rule #42: Fee Structure Rules
One student can have multiple fee heads

Late fee calculation logic in service

Receipt number generation (unique, sequential per year)

Partial payment handling

Scholarship/discount application

Rule #43: Attendance Rules
Mark attendance per subject/period

Percentage calculation (present/total * 100)

Minimum attendance requirement (75% usually)

Leave application workflow

Rule #44: Grading Rules
Different grading scales for different levels

Grade boundaries configurable

Backlog/Failed subject handling

Transcript generation

CGPA calculation (weighted by credits)

Rule #45: Timetable Constraints
No teacher double-booking

No room double-booking

Subject period limits

Teacher workload limits

Break periods

PART 12: DATA INTEGRITY
Rule #46: Unique Constraints
python
class Student(Base):
    __table_args__ = (
        UniqueConstraint('enrollment_number', 'academic_year_id'),
        UniqueConstraint('email'),
    )
Rule #47: Check Constraints
python
class Grade(Base):
    __table_args__ = (
        CheckConstraint('marks >= 0 AND marks <= 100'),
    )
Rule #48: Foreign Key Integrity
Always use foreign keys

Define ondelete behavior

Cascade where appropriate

Restrict where not

PART 13: BUSINESS RULES
Rule #49: No Deletion of Critical Data
Never delete fees records

Never delete attendance records

Never delete grade records

Use soft delete or archive

Rule #50: Data Export/Import
Support bulk operations

CSV/Excel import/export

Validate before import

Transaction rollback on error

Rule #51: Notification Rules
Email for critical events (fee due, result published)

SMS for urgent (exam schedule changed)

In-app notifications

Parent notifications for student events

PART 14: SCALABILITY
Rule #52: Read-Replica for Reports
python
# Separate read/write connections
read_engine = create_async_engine(READ_REPLICA_URL)
write_engine = create_async_engine(WRITE_DATABASE_URL)
Rule #53: Background Tasks
python
from fastapi import BackgroundTasks

@router.post("/generate-report")
async def generate_report(background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_pdf_report)
    return {"message": "Report generation started"}
Rule #54: Queue for Heavy Operations
python
# Use Celery or Redis Queue
- Result processing
- Bulk email sending
- Report generation
- Data export
PART 15: DOCUMENTATION
Rule #55: API Documentation
python
from fastapi import FastAPI

app = FastAPI(
    title="School Management API",
    description="API for managing school operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
Rule #56: OpenAPI/Swagger Annotations
python
@router.post(
    "/students",
    response_model=StudentResponse,
    summary="Create new student",
    description="Create a new student with personal details",
    responses={
        201: {"description": "Student created"},
        400: {"description": "Invalid input"},
        409: {"description": "Email already exists"}
    }
)
async def create_student():
    pass
🚨 CRITICAL MISTAKES TO AVOID
❌ Exposing database IDs in URLs

❌ Storing passwords in plain text

❌ No input validation

❌ SQL injection vulnerabilities

❌ N+1 queries in loops

❌ Business logic in controllers

❌ No error handling

❌ No logging

❌ Ignoring database indexes

❌ Not handling concurrent updates

❌ No transaction management

❌ Hardcoding configuration

❌ No backup strategy

❌ No rate limiting

❌ Not validating user permissions

✅ PRODUCTION CHECKLIST
Before deploying:

All environment variables set

Database indexes created

SSL certificates installed

Rate limiting configured

CORS properly set

Logging configured

Monitoring setup

Backup strategy in place

Error tracking (Sentry)

Health checks implemented

Load testing done

Security audit passed

GDPR/Data privacy compliance

API documentation updated

Deployment rollback plan

Remember: A production-ready app isn't just about working features. It's about security, reliability, maintainability, and scalability. These rules will help you build a system that can handle real users, real data, and real money without crashing! 🚀

