# Day 9 Production Implementation Plan
**Date**: 2026-05-14
**Focus**: Complete Testing Suite & Integration Validation

## Objectives
- Write tests for remaining college modules (HOD, Dean, Registrar)
- Ensure all school modules have at least minimal test coverage
- Run full integration test suite (end-to-end workflows)
- Fix any broken tests from previous days
- Achieve overall code coverage ≥50% target

## Tasks

### 1. Morning: Complete College Module Tests (3 hours)
**Remaining modules to test**:

**college_hod** – `tests/college/test_hod.py`:
- [ ] `test_get_hod_profile_returns_department_and_faculty_info()`
- [ ] `test_get_hod_profile_404_if_not_hod()`
- [ ] `test_get_department_faculty_list()` – HOD sees only own dept faculty
- [ ] `test_update_hod_profile_limited_fields()` – only certain fields editable
- [ ] `test_hod_cannot_access_other_hod_data()`

**college_dean** – `tests/college/test_dean.py`:
- [ ] `test_get_all_faculty_list_with_performance_metrics()`
- [ ] `test_get_program_analytics_returns_enrollment_counts()`
- [ ] `test_get_department_wise_analysis()`
- [ ] `test_dean_can_view_any_department()`
- [ ] `test_dean_cannot_edit_faculty()`

**college_registrar** – `tests/college/test_registrar.py`:
- [ ] `test_get_college_stats_returns_aggregates()`
- [ ] `test_get_enrollment_report_filters_by_semester()`
- [ ] `test_get_fee_collection_report_returns_totals()`
- [ ] `test_registrar_can_export_csv()` – if CSV endpoint exists
- [ ] `test_registrar_access_denied_for_non_roles()`

**college_library** – if module exists:
- [ ] Check `modules/college/college_library/` exists with router
- [ ] Create `tests/college/test_library.py`:
  - `test_add_book()`, `test_issue_book()`, `test_return_book()`
  - `test_search_books()`
  - `test_librarian_role_required()`

**college_hostel** – if exists:
- [ ] `tests/college/test_hostel.py`: allocation, complaint, room listing

**college_research** – if exists:
- [ ] `tests/college/test_research.py`: project creation, publication upload

**coverage check after each**:
- [ ] `pytest --cov=modules.college.college_hod --cov-report=term`
- [ ] Target ≥50% per module

### 2. School Module Testing (2 hours)
**Assess current coverage**: school modules likely have lower test coverage

**Create minimal test sets** (aim 40%+ per module):
- [ ] `tests/school/test_student.py`:
  - Create student, get by roll, update, soft delete (if implemented)
- [ ] `tests/school/test_teacher.py`:
  - CRUD, assign classes
- [ ] `tests/school/test_parent.py`:
  - Parent linked to multiple students; fetch children
- [ ] `tests/school/test_attendance.py`:
  - Mark attendance, get by date/student
- [ ] `tests/school/test_classes.py`:
  - Create class, assign teacher, list students
- [ ] `tests/school/test_subjects.py`: CRUD
- [ ] `tests/school/test_timetable.py`: create entry, conflicts
- [ ] `tests/school/test_exam.py`: create exam, enter marks, publish results
- [ ] `tests/school/test_homework/assignments`: create, submit, grade

**Note**: If modules are large, test service layer thoroughly; router layer minimal (already tested via auth guards)

### 3. Integration Tests: Full Workflows (1.5 hours)
Create `tests/integration/` directory for end-to-end scenarios:

**Scenario 1: College Student Registration Flow** (`test_college_student_journey.py`):
- [ ] Test full signup → login → create enrollment → view results
  1. POST `/auth/college-student-signup` with valid data
  2. Extract `access_token`, set `Authorization: Bearer`
  3. GET `/api/v1/college/students/me` → assert 200, correct data
  4. POST `/api/v1/college/enrollments` with program/semester
  5. GET `/api/v1/college/enrollments?student_id=me` → assert enrollment exists

**Scenario 2: College Faculty Upload Results** (`test_exam_workflow.py`):
- [ ] Login as faculty with exam_section role
- [ ] POST `/api/v1/college/exam_section/notices` (create exam notice)
- [ ] POST `/api/v1/college/exam_section/results` (upload marks CSV or JSON)
- [ ] GET `/api/v1/college/exam_section/results?exam_id=` → verify marks stored
- [ ] As student, GET `/api/v1/college/student/results` → see own results only

**Scenario 3: Account Section Fee Collection** (`test_fee_workflow.py`):
- [ ] As account_section: create fee structure for program
- [ ] As registrar: enroll student (creates fee_record automatically?)
- [ ] As account_section: post payment for fee_record
- [ ] Verify fee_record.status changed to PAID
- [ ] GET fee report → includes payment

**Scenario 4: Dean Analytics Dashboard** (`test_dean_analytics.py`):
- [ ] As dean: GET `/api/v1/college/dean/faculty-performance` → returns list
- [ ] GET `/api/v1/college/dean/program-analytics` → enrollment counts per program

**Scenario 5: HOD Department Management** (`test_hod_workflow.py`):
- [ ] As HOD: list faculty in department
- [ ] Update own profile
- [ ] Attempt to edit other dept faculty → should fail (403)

**Run all integration tests**:
- [ ] `pytest tests/integration/ -v`
- [ ] Fix any auth or DB fixture issues

### 4. Fix Broken Tests & Flakyness (1 hour)
- [ ] Run full suite: `pytest -x` (stop on first failure)
- [ ] Identify failing tests:
  - DB constraint violations (unique, FK)
  - Missing relationships (soft delete filter not applied correctly)
  - Timezone/date issues
- [ ] Fix repository methods or test data setup
- [ ] Ensure tests independent: use fixtures for DB rollback or atomic transactions

### 5. Coverage Audit & Gap Analysis (1 hour)
- [ ] Run `pytest --cov=modules --cov-report=html`
- [ ] Open `htmlcov/index.html`; note:
  - Modules <40% coverage: list them
  - Reasons: generated code, simple CRUD with few branches, unreachable error handlers
- [ ] For any critical module <30%, add tests to reach 40%
- [ ] For simple third-party integrations (e.g., external API), annotation OK if not core

**Document coverage**:
- [ ] Update `COVERAGE.md` with per-module percentages:
  ```
  Module                     Coverage
  college_exam_section       85%
  college_account_section    72%
  college_enrollments        65%
  college_programs           58%
  college_semesters          55%
  college_hod                52%
  college_dean               50%
  college_registrar          48%
  school_student             45% (target 60% next week)
  ...
  Overall: 52% (target: 60% by Day 15)
  ```

### 6. Commit & Tag (30 min)
- [ ] Git add all new test files
- [ ] Commit: "test: Complete college module tests + integration workflows; achieve 50%+ coverage"
- [ ] Tag as `v0.4.0-tests`

## Deliverables
- ✅ Test files for HOD, Dean, Registrar (≥45 new tests)
- ✅ School module tests (≥30 tests)
- ✅ Integration tests in `tests/integration/` (≥5 scenarios, 20+ tests)
- ✅ Full test suite passing (`pytest -q` shows all green)
- ✅ Coverage report: modules ≥50%, overall ≥45% (pushing to 50%)
- ✅ `COVERAGE.md` tracking per-module coverage

## Success Criteria
- `pytest` exits code 0 (no failures)
- `coverage report --show-missing` highlights no critical uncovered lines
- Integration tests exercise realistic user journeys (student signup → enrollment → fee payment → view results)
- All test files follow naming: `tests/<portal>/test_<module>.py`

## Notes
- Keep tests deterministic: use fixed timestamps, avoid relying on `datetime.now()`
- For async tests, always use `@pytest.mark.asyncio` and `await` fixtures
- Use factory functions to create test data quickly; parameterize tests with `@pytest.mark.parametrize` where possible
- If any module is just thin wrappers around CRUD (low complexity), document and accept lower coverage

## Next: Day 10
Weekly review: audit progress against 99-point checklist, verify Week 1 completed items, plan Week 2 (caching, background tasks, CI/CD pipeline, database tuning, CI pipeline setup).
