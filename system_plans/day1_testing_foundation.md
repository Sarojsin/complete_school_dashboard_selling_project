# Day 1 Production Implementation Plan
**Date**: 2026-05-06 (starting tomorrow)
**Focus**: Testing Infrastructure Foundation

## Objectives
- Setup complete testing framework (pytest, pytest-asyncio, pytest-cov)
- Achieve baseline configuration for all test tooling
- Write first batch of unit tests for one complete module
- Verify test coverage reporting works

## Tasks

### 1. Initialize Testing Environment (Morning - 3 hours)
- [ ] Install test dependencies:
  ```bash
  pip install pytest pytest-asyncio pytest-cov httpx
  ```
- [ ] Create `pytest.ini` in project root (already exists, verify config):
  ```ini
  [pytest]
  asyncio_mode = auto
  testpaths = tests
  python_files = test_*.py
  ```
- [ ] Create `conftest.py` in tests/ directory with:
  - Async database fixture using `modules.shared.database.get_db`
  - Test client fixture using `app.main.app`
  - Auth token fixture for authenticated requests
  - Sample data fixtures (test user, test department)
- [ ] Create `tests/__init__.py` if missing

### 2. Create Test Database Strategy (1 hour)
- [ ] Decide on test DB approach:
  - Option A: SQLite in-memory (`sqlite:///:memory:`)
  - Option B: Separate PostgreSQL test DB (`college_sell_test`)
- [ ] Implement fixture that creates/drops tables before test suite
- [ ] Ensure test DB uses same models as production (import from backup.models)
- [ ] Add teardown to clean data between tests

### 3. Write First Test Module: college_exam_section (4 hours)
Create `tests/college/test_exam_section.py` with:

**Unit Tests for Service** (`college_exam_section/service.py`):
- [ ] `test_create_exam_notice_success()` – happy path
- [ ] `test_create_exam_notice_validation_error()` – invalid dates, empty title
- [ ] `test_create_exam_notice_forbidden()` – non-exam-section role
- [ ] `test_get_exam_notices()` – empty list, pagination
- [ ] `test_update_exam_notice()` – found, not found, forbidden
- [ ] `test_delete_exam_notice()` – success, not found, forbidden

**Repository Tests** (if repository has complex logic):
- [ ] `test_get_by_college_with_filters()` – filter by is_published, date range
- [ ] `test_get_by_id()` – found/not found

**Integration Tests (API endpoints)**:
- [ ] `test_exam_notices_endpoint_requires_auth()`
- [ ] `test_exam_notices_list_returns_correct_structure()`
- [ ] `test_create_exam_notice_endpoint_success()` – with valid JWT as exam_section
- [ ] `test_update_exam_notice_endpoint_forbidden_for_other_roles()`

**Expected Coverage for this module**: 70%+ on service layer

### 4. Run Coverage & Verify (1 hour)
- [ ] Run: `pytest tests/college/test_exam_section.py -v`
- [ ] Run: `pytest --cov=modules.college.college_exam_section --cov-report=html`
- [ ] Open `htmlcov/index.html` to verify coverage breakdown
- [ ] Fix any missing imports or DB setup issues

### 5. Add Test for Shared Exceptions (1 hour)
Create `tests/shared/test_exceptions.py`:
- [ ] Test `NotFoundError` raises with correct message
- [ ] Test `ForbiddenError` raises correctly
- [ ] Test `ValidationError` raises correctly

### 6. Commit & Document (1 hour)
- [ ] Git add all new test files
- [ ] Commit: "feat(test): Add pytest foundation + college_exam_section tests"
- [ ] Create `TESTING.md` documenting:
  - How to run tests (`pytest`, `pytest -v`, `pytest --cov`)
  - How to write new tests (fixtures, async patterns)
  - Coverage target (70% minimum per new module)

## Deliverables
- ✅ pytest configured and working
- ✅ conftest.py with DB and auth fixtures
- ✅ `tests/college/test_exam_section.py` with ≥15 tests
- ✅ Coverage report (>70% on college_exam_section service)
- ✅ TESTING.md guide

## Success Criteria
- All tests pass (`pytest -q` shows 15+ passed)
- Coverage for `modules/college/college_exam_section/` ≥70%
- No errors during test collection
- Test database creates tables correctly from models

## Notes
- Use `pytest-asyncio` mark `@pytest.mark.asyncio` on all async tests
- For DB fixture, consider using `session` scope for performance
- Mock external calls if any (email sending, etc.)
- Keep tests isolated – each test cleans up its own data

## Next: Day 2
Expand testing to `college_account_section` module, add integration tests for auth flows, setup test factory (factory-boy) for test data generation.
