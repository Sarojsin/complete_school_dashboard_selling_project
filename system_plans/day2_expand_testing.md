# Day 2 Production Implementation Plan
**Date**: 2026-05-07
**Focus**: Expand Testing & Add Integration Tests

## Objectives
- Extend unit test coverage to college_account_section module
- Implement test factory pattern for consistent test data
- Add integration tests for auth endpoints (login, signup, refresh)
- Verify all college module endpoints with integration tests

## Tasks

### 1. Review Day 1 Progress (Morning - 30 min)
- [ ] Check: Did all tests pass? If failures, fix before proceeding
- [ ] Verify coverage report generated correctly
- [ ] Ensure `conftest.py` fixtures are reusable

### 2. Implement Test Factory (1.5 hours)
Create `tests/factories.py` using simple functions or `factory-boy`:

**Factories to implement**:
- [ ] `create_department(name: str, code: str)` – returns Department instance
- [ ] `create_program(name: str, dept_id: int)` – returns CollegeProgram
- [ ] `create_semester(name: str, year: int)` – returns CollegeSemester
- [ ] `create_faculty(user_id: int, dept_id: int)` – returns CollegeFaculty
- [ ] `create_student(user_id: int, dept_id: int, roll: str)` – returns CollegeStudent
- [ ] `create_exam_notice(title: str, dept_ids: list, published: bool)` – returns CollegeExamNotice
- [ ] `create_fee_structure(program_id: int, amount: float)` – returns CollegeFeeStructure
- [ ] `create_enrollment(student_id: int, program_id: int, semester_id: int)` – returns Enrollment

**Usage pattern**:
```python
dept = await create_department("Computer Science", "CS")
program = await create_program("B.Tech CSE", dept.id)
```

### 3. Write Tests: college_account_section (3 hours)
Create `tests/college/test_account_section.py`:

**Service Layer Tests**:
- [ ] `test_create_fee_structure_success()`
- [ ] `test_create_fee_structure_duplicate_constraint()` – same program+semester
- [ ] `test_create_fee_structure_invalid_amount()` – negative amount
- [ ] `test_create_fee_record_success()` – link student, generate receipt_no
- [ ] `test_create_fee_record_duplicate()` – same student+program+semester
- [ ] `test_get_fee_records_by_student()` – filters by student_id
- [ ] `test_get_fee_records_by_program()` – filters by program
- [ ] `test_update_fee_record_status()` – pending → paid, paid → partial
- [ ] `test_create_payment_for_nonexistent_fee_record()` – raises NotFoundError
- [ ] `test_list_payments()` – with and without filters

**Repository Tests**:
- [ ] `test_get_outstanding_fees()` – students with unpaid fees
- [ ] `test_get_collection_summary()` – sums by program/department

**Integration Tests**:
- [ ] `test_fee_structure_endpoints_require_role()` – only account_section/dean
- [ ] `test_post_fee_structure_201_created()`
- [ ] `test_get_fee_structures_200()`
- [ ] `test_fee_record_workflow_flow()` – create → update status → add payment
- [ ] `test_payment_endpoint_requires_fk_constraint()` – invalid fee_record_id

### 4. Write Auth Integration Tests (2 hours)
Create `tests/auth/test_auth.py`:

**Signup Tests**:
- [ ] `test_student_signup_success()` – creates user + student profile
- [ ] `test_faculty_signup_success()` – creates user + faculty profile
- [ ] `test_signup_duplicate_email()` – returns 400
- [ ] `test_signup_weak_password()` – validation rejection

**Login Tests**:
- [ ] `test_login_success()` – returns access_token, refresh_token
- [ ] `test_login_invalid_password()` – 401
- [ ] `test_login_nonexistent_user()` – 401
- [ ] `test_login_rate_limited_after_5_attempts()` – if rate limiting implemented

**Token Tests**:
- [ ] `test_refresh_token_success()` – gets new access token
- [ ] `test_refresh_with_invalid_token()` – 401
- [ ] `test_access_token_expired()` – 401

**Me Tests**:
- [ ] `test_get_current_user_returns_user()`
- [ ] `test_get_current_user_invalid_token()` – 401

**Portal Guard Tests** (already exists, verify):
- [ ] Run existing `tests/test_portal_guard.py` – all must pass
- [ ] Add missing test: college endpoint rejects school tokens

### 5. Run Full Coverage (1 hour)
- [ ] `pytest --cov=modules --cov-report=html`
- [ ] Review `htmlcov/index.html`:
  - Target: college_exam_section ≥70%
  - Target: college_account_section ≥60%
  - Auth module ≥50%
- [ ] Identify untested files; note for tomorrow

### 6. Write Initial Test for college_enrollments (1 hour)
Start `tests/college/test_enrollments.py`:
- [ ] `test_create_enrollment_success()`
- [ ] `test_create_enrollment_duplicate()` – same student+semester+program
- [ ] `test_create_enrollment_invalid_student()` – FK constraint
- [ ] `test_get_enrollments_by_student()`
- [ ] `test_get_enrollments_by_semester()`

### 7. Documentation & Commit (1 hour)
- [ ] Update `TESTING.md` with:
  - Factory functions usage
  - How to run仅特定模块 tests (`pytest tests/college/test_account_section.py`)
  - Coverage reporting instructions
- [ ] Add pre-commit hook suggestion (optional):
  - `pre-commit` config to run `pytest --cov` on staged files
- [ ] Git commit: "feat(test): Add college_account_section tests + auth integration"

## Deliverables
- ✅ `tests/factories.py` with 8+ factory functions
- ✅ `tests/college/test_account_section.py` (≥15 tests)
- ✅ `tests/auth/test_auth.py` (≥12 tests)
- ✅ `tests/college/test_enrollments.py` (≥5 tests started)
- ✅ Coverage report shows increasing trends

## Success Criteria
- Total test count: ≥50 tests
- All tests pass
- Coverage for college modules (exam_section + account_section) ≥60% combined
- Auth endpoints fully covered (login, signup, refresh, me)

## Notes
- Use factory functions to avoid repetitive test data setup
- Keep tests independent; use fixtures for DB rollback or `session` scope with cleanup
- Test both happy paths and error scenarios (validation, auth, not found)
- For integration tests, use `TestClient` or `AsyncClient` with `app`

## Next: Day 3
Test coverage for remaining college modules: enrollments, programs, semesters, HOD/dean/registrar. Add repository-level tests for complex queries.
