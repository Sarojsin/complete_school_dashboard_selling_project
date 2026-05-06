# Day 3 Production Implementation Plan
**Date**: 2026-05-08
**Focus**: Complete College Module Testing & Start Performance Fixes

## Objectives
- Achieve ≥50% test coverage for all 8 college modules
- Identify and fix N+1 query issues using selectinload/joinedload
- Add database indexes on frequently queried columns
- Begin rate limiting implementation on auth endpoints

## Tasks

### 1. Morning: Complete College Module Tests (3 hours)
**Target**: college_enrollments, college_programs, college_semesters

**college_enrollments** (`tests/college/test_enrollments.py`):
- [ ] `test_get_enrollments_with_student_and_course_details()` – verify joins, no N+1
- [ ] `test_get_enrollments_by_semester_filtered_by_program()`
- [ ] `test_update_enrollment_status()` – active → dropped
- [ ] `test_delete_enrollment()` – soft delete or hard delete as per model
- [ ] `test_enrollment_unique_constraint()` – student+semester+program unique

**college_programs** (`tests/college/test_programs.py` new):
- [ ] `test_create_program_success()`
- [ ] `test_create_program_duplicate_code()`
- [ ] `test_get_programs_with_department_name()` – verify join eager loading
- [ ] `test_update_program()`
- [ ] `test_delete_program_with_dependencies()` – should fail due to FK

**college_semesters** (`tests/college/test_semesters.py` new):
- [ ] `test_create_semester_success()`
- [ ] `test_create_semester_date_overlap_validation()` – if validation exists
- [ ] `test_get_active_semesters()`
- [ ] `test_get_semesters_by_year()`

**college_hod** (`tests/college/test_hod.py` new):
- [ ] `test_get_hod_profile_success()`
- [ ] `test_get_hod_profile_not_found()`
- [ ] `test_update_hod_profile()`
- [ ] `test_hod_cannot_access_other_dept_hod()`

**college_dean** (`tests/college/test_dean.py` new):
- [ ] `test_get_all_faculty_performance()` – pagination, filters
- [ ] `test_get_program_analytics()` – enrollment counts
- [ ] `test_dean_access_requires_role()`

**college_registrar** (`tests/college/test_registrar.py` new):
- [ ] `test_get_college_stats()`
- [ ] `test_get_enrollment_report()`
- [ ] `test_get_fee_collection_report()`
- [ ] `test_registrar_access_requires_role()`

**Coverage check**:
- [ ] Run `pytest --cov=modules.college --cov-report=term-missing`
- [ ] Target: Each college module ≥50% coverage
- [ ] Document any modules below 40% and reasons (e.g., simple CRUD may have lower coverage but acceptable)

### 2. Afternoon: Performance - N+1 Query Audit (2 hours)
**Step 1: Profile existing queries**
- [ ] Review all `repository.py` files in college modules
- [ ] List all `select()` queries that access relationships:
  - Example: `exam_section/repository.py` get_by_college – may load `department` relationships
  - Example: `enrollments/repository.py` get_by_student – loads `student`, `semester`, `program`
- [ ] Create spreadsheet/table:
  ```
  Module | Method | Relationships accessed | N+1 risk? | Fix needed?
  exam_section | get_all | exam.departments (many-to-many) | YES | selectinload(ExamNotice.departments)
  ```

**Step 2: Implement fixes** (edit repository files):
- [ ] `college_exam_section/repository.py`:
  - `get_by_college`: add `selectinload(CollegeExamNotice.departments)` if querying departments
- [ ] `college_enrollments/repository.py`:
  - `get_by_student`: `selectinload(Enrollment.semester)`, `selectinload(Enrollment.program)`
  - `get_by_semester`: `selectinload(Enrollment.student)`, `selectinload(Enrollment.program)`
- [ ] `college_programs/repository.py`:
  - `get_by_id`: `selectinload(CollegeProgram.department)`
- [ ] `college_student/service.py` (if still using):
  - Profile fetch: `selectinload(CollegeStudent.department)`, `selectinload(CollegeStudent.program)`

**Step 3: Verify with tests**:
- [ ] Write test asserting number of queries (use `pytest` + SQLAlchemy echo/query count)
- [ ] Ensure relationship data present without lazy loading errors

### 3. Late Afternoon: Database Indexes (1.5 hours)
**Analyze Query Patterns** from repository methods:
Common filter columns: `college_id`, `department_id`, `semester_id`, `program_id`, `student_id`, `faculty_id`, `created_at`

**Create migration for indexes**:
- [ ] Create new Alembic migration: `alembic_college/versions/20260508_add_indexes.py`
- [ ] Add indexes:
  ```python
  op.create_index('ix_college_faculty_department_id', 'college_faculty', ['department_id'])
  op.create_index('ix_college_faculty_user_id', 'college_faculty', ['user_id'])
  op.create_index('ix_college_students_department_id', 'college_students', ['department_id'])
  op.create_index('ix_college_students_program_id', 'college_students', ['program_id'])
  op.create_index('ix_college_enrollments_student_id', 'college_enrollments', ['student_id'])
  op.create_index('ix_college_enrollments_program_id', 'college_enrollments', ['program_id'])
  op.create_index('ix_college_enrollments_semester_id', 'college_enrollments', ['semester_id'])
  op.create_index('ix_college_courses_department_id', 'college_courses', ['department_id'])
  op.create_index('ix_college_courses_semester_id', 'college_courses', ['semester_id'])
  op.create_index('ix_college_fee_records_student_id', 'college_fee_records', ['student_id'])
  op.create_index('ix_college_fee_records_program_id', 'college_fee_records', ['program_id'])
  op.create_index('ix_college_exam_notices_department_id', 'college_exam_notices_departments', ['department_id'])  # junction
  ```
- [ ] Apply migration: `alembic -c alembic_college.ini upgrade head`
- [ ] Verify indexes exist in database

### 4. Begin Rate Limiting Implementation (1 hour)
**Install & Setup**:
- [ ] `pip install slowapi` or `fastapi-limiter`
- [ ] Create `modules/shared/rate_limit.py`:
  ```python
  from slowapi import Limiter, _rate_limit_exceeded_handler
  from slowapi.util import get_remote_address
  from slowapi.errors import RateLimitExceeded
  
  limiter = Limiter(key_func=get_remote_address)
  ```
- [ ] Import and attach `limiter` to FastAPI app in `app/main.py`
- [ ] Add exception handler: `app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)`

**Apply to endpoints** (start with auth):
- [ ] In `modules/auth/router.py`:
  ```python
  @router.post("/login")
  @limiter.limit("5/minute")
  async def login(...): ...
  ```
- [ ] Same for `/signup`, `/refresh`
- [ ] Test: Write test that sends 6 rapid requests and asserts 429 on 6th

## Deliverables
- ✅ Test files: `test_programs.py`, `test_semesters.py`, `test_hod.py`, `test_dean.py`, `test_registrar.py`
- ✅ Total test count ≥100
- ✅ Coverage for all college modules ≥50%
- ✅ N+1 query fixes implemented in 4+ repository methods
- ✅ Database indexes added via Alembic migration
- ✅ Rate limiting basic setup + auth endpoints protected

## Success Criteria
- `pytest --cov=modules.college` shows no module <45% coverage
- Queries use eager loading (selectinload) where relationships accessed
- Indexes visible in DB (`\d table_name` in psql)
- Rate limiting returns 429 after threshold exceeded

## Notes
- Keep performance improvements incremental; document each N+1 fix
- Indexes speed up reads but slow down writes; add only on columns used in WHERE/JOIN/ORDER
- Rate limiting can be refined later (per-user vs per-IP); start with IP-based

## Next: Day 4
Focus on backup & recovery: create automated pg_dump scripts, test restore procedure, implement retention policy. Also add audit logging infrastructure.
