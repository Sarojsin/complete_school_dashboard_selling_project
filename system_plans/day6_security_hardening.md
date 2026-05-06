# Day 6 Production Implementation Plan
**Date**: 2026-05-11
**Focus**: Security Hardening & Input Validation

## Objectives
- Implement rate limiting on all sensitive endpoints (not just auth)
- Add UUID as public-facing resource identifiers (optional but recommended)
- Implement soft delete mixin for critical models
- Review and tighten CORS configuration
- Add input validation refinements (field-level validators)
- Run security scanner (bandit) on codebase

## Tasks

### 1. Rate Limiting Expansion (Morning - 2 hours)
**Current state**: Only login/signup protected at 5/minute

**Expand rate limits**:
- [ ] Install `slowapi` if not already: `pip install slowapi`
- [ ] Create `modules/shared/rate_limit.py` (already done Day 3):
  - Configure storage: use Redis if available, fallback to in-memory
  ```python
  from slowapi import Limiter
  from slowapi.util import get_remote_address
  from slowapi.middleware import SlowAPIMiddleware
  
  limiter = Limiter(key_func=get_remote_address, default_limits=["200/day", "50/hour"])
  ```
- [ ] In `app/main.py`: `app.add_middleware(SlowAPIMiddleware)`

**Apply limits**:
- [ ] Auth endpoints (already done):
  - `/auth/login`, `/auth/signup`: `@limiter.limit("5/minute")`
- [ ] College write endpoints (POST/PATCH/DELETE):
  - `@limiter.limit("30/minute")` per user for:
    - college_exam_notices create/update/delete
    - college_fee_structure create/update
    - college_enrollments create/update
    - college_faculty create/update (if applicable)
- [ ] General list endpoints (GET):
  - `@limiter.limit("100/minute")` (read-heavy but allow)

**Implementation**:
- [ ] Edit college routers: add decorator on route functions
- [ ] For class-based `APIRouter`, use decorator on endpoint function

**Test rate limiting**:
- [ ] Write `tests/test_rate_limiting.py`:
  - `test_login_rate_limit_exceeded()` – send 6 requests in <1 min, assert 429 on 6th
  - `test_write_endpoint_limited()` – use exam_notice create
  - `test_rate_limit_exempt_for_super_admin()` – if super_admin exempt

### 2. UUID Migration Planning (1.5 hours)
**Decision**: Switch auto-increment integer IDs to UUIDs for public-facing resources to prevent enumeration.

**Current state**: Many models use `id: int = Column(Integer, primary_key=True, autoincrement=True)`

**Plan** (may be multi-day; today do planning & prep):
- [ ] Identify public-facing endpoints that expose IDs in URLs or responses:
  - `/api/v1/college/students/{student_id}` ← exposes integer ID
  - `/api/v1/college/enrollments/{enrollment_id}` ← integer ID
  - All college resources: faculty, courses, programs, semesters, etc.
- [ ] Create `modules/shared/models.py` mixin:
  ```python
  class UUIDMixin:
      id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  ```
- [ ] Decide scope: Apply only to tables accessed by external clients (students, faculty, enrollments, courses). Internal tables (fee_records, exam_notices) can keep integer PK.
- [ ] Draft migration: Alembic batch alter table to:
  1. Add new UUID column `uuid` with default uuid_generate_v4()
  2. Populate from existing `id` (or new random)
  3. Drop old `id` PK, rename `uuid` to `id`
  4. Update all foreign keys referencing this table
- [ ] **NOTE**: This is a complex breaking change; consider if truly needed now or defer to later sprint. For Day 6, we'll:
  - **Assess**: Is ID enumeration a critical blocker for this audit?
  - **If yes**: Implement for at least 1 module as proof of concept (college_students)
  - **If no**: Document as post-MVP improvement; add warning in API docs about ID enumeration risk

**Decision for this plan**: Given the 30-day roadmap, we'll **defer full UUID migration** to Week 3/4 as it's a breaking change requiring data migration and frontend updates. Instead:
- [ ] Document risk in `SECURITY.md` (ID enumeration)
- [ ] Add plan item: "Week 3: Migrate public IDs to UUID"
- [ ] For now, add middleware/guard: Do not expose exact ID count via `/count` endpoints (if any)

### 3. Soft Delete Implementation (2 hours)
**Goal**: Prevent hard deletes; add `is_deleted` flag + `deleted_at` timestamp

**Create mixin**:
- [ ] In `modules/shared/models.py`:
  ```python
  class SoftDeleteMixin:
      is_deleted = Column(Boolean, default=False, nullable=False)
      deleted_at = Column(DateTime(timezone=True), nullable=True)
      
      async def soft_delete(self, db: AsyncSession):
          self.is_deleted = True
          self.deleted_at = datetime.utcnow()
          await db.commit()
  ```
- [ ] Apply to critical models:
  - CollegeFaculty
  - CollegeStudent
  - CollegeCourse
  - CollegeProgram
  - CollegeEnrollment (maybe)
  - CollegeFeeRecord
  - CollegeExamNotice
  - User (already has `is_active`; maybe not needed)
- [ ] Update repository methods:
  - All `get_by_id` should filter `WHERE is_deleted = false`
  - `delete()` endpoint calls `.soft_delete()` not `db.delete()`
  - `get_all()` excludes soft-deleted by default (add `include_deleted` flag if needed)

**Migrations**:
- [ ] Create Alembic migration: `alembic/versions/20260511_add_soft_delete_mixin.py`
- [ ] For each table: add columns `is_deleted BOOLEAN NOT NULL DEFAULT FALSE`, `deleted_at TIMESTAMP`
- [ ] Apply: `alembic upgrade head`

**Tests**:
- [ ] `tests/test_soft_delete.py`:
  - `test_soft_delete_excludes_from_get_all()`
  - ` test_soft_deleted_record_is_inaccessible_by_id()`
  - ` test_undelete_possible()`
  - `test_hard_delete_raises_error()`

### 4. Input Validation Tightening (1 hour)
**Review existing validators** in `schemas.py` files:
- [ ] Check for missing:
  - Email validation: Ensure `EmailStr` from pydantic used everywhere
  - Length constraints: `Field(..., min_length=1, max_length=100)`
  - Number ranges: `Field(..., ge=0, le=100)` for marks
  - Date validation: `Field(..., deprecated=False)`
- [ ] Add custom validators where missing:
  - `college_fee_schema.py`: `amount` must be > 0
  - `college_enrollment_schema`: enrollment date not in future
  - `exam_notice_schema`: `publish_date` ≤ `exam_date`
- [ ] Ensure all `create` and `update` schemas have `validator` methods (using pydantic `@validator`)
- [ ] Test validation errors return 422 with clear messages

**Test**:
- [ ] `tests/test_validation.py`:
  - `test_invalid_email_returns_422()`
  - ` test_negative_amount_rejected()`
  - ` test_overlapping_dates_rejected()`

### 5. CORS & CSRF Review (30 min)
**CORS** (`app/main.py`):
- [ ] Verify `ALLOWED_ORIGINS` from `.env` is list, not wildcard
- [ ] Test: curl with Origin header, check `Access-Control-Allow-Origin` response
- [ ] Ensure credentials allowed only for trusted origins

**CSRF**:
- [ ] Since JWT in Authorization header, CSRF not required (no cookies)
- [ ] Document this in `SECURITY.md`

### 6. Security Scanning (30 min)
**Install & Run bandit**:
- [ ] `pip install bandit`
- [ ] `bandit -r modules/ -f json -o bandit-report.json`
- [ ] Review report: fix any HIGH severity issues (e.g., `subprocess` use, hardcoded secrets)
- [ ] Also run `safety check` for dependency vulnerabilities

**Document**:
- [ ] Add `SECURITY.md` with:
  - Vulnerability reporting process
  - Bandit/Safety scan results (attach to CI later)

### 7. Documentation (30 min)
- [ ] Update `SECURITY.md`:
  - Rate limits documented
  - Soft delete behavior
  - Input validation rules
  - CORS policy
  - Known risks (ID enumeration until UUID migration)
- [ ] Update `README.md` with note on security hardening progress

## Deliverables
- ✅ Rate limiting on auth + all write endpoints
- ✅ Soft delete mixin applied to 6+ critical models + migration
- ✅ Soft delete tests passing
- ✅ Input validation tightened across schemas
- ✅ Bandit scan run with no high-severity findings
- ✅ `SECURITY.md` documented

## Success Criteria
- POST /college/exam_notices limited to 30/min per IP
- GET /college/students does not include soft-deleted students
- All schema validators present; invalid data rejected with 422
- Bandit report shows 0 HIGH, ≤5 MEDIUM (acceptable like `assert` used)
- CORS only allows configured origins

## Notes
- Soft delete requires updating all `get_by_id` repository methods to filter `is_deleted=False`
- Some models already have `is_active` (User). Use consistent naming: `is_deleted` for most, `is_active` for User
- If you encounter conflicts with existing `is_active` fields, keep both as appropriate

## Next: Day 7
Documentation push: Architecture diagram, API documentation enhancements, CONTRIBUTING.md, CHANGELOG.md. Also start Week 2: Feature flags setup and CORS finalization.
