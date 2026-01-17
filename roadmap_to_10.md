# Roadmap to 10/10 Production Readiness

## Current Status: ~8/10

### Goal: Achieve a perfect 10/10 score by addressing architectural, performance, and testing gaps.

---

## Phase 1: Architectural Refactoring
**Problem:** Monolithic `app/web/routes.py` (2000+ lines) is hard to maintain.

- [ ] **Split Routes:** Break `app/web/routes.py` into smaller routers by role:
    - `app/web/routers/authority.py`
    - `app/web/routers/student.py`
    - `app/web/routers/teacher.py`
    - `app/web/routers/parent.py`
- [ ] **Dependency Injection:** Use FastAPI dependencies for database sessions and auth.

## Phase 2: Performance Optimization
**Problem:** Sync database driver (`psycopg2`) blocks the async event loop.

- [ ] **Switch to `asyncpg`:** Update `app/core/database.py` to use `create_async_engine`.
- [ ] **Solve N+1 Issues:** Use `selectinload` or `joinedload` correctly in repositories.
- [ ] **Query Auditing:** Identify and optimize slow queries.

## Phase 3: Automated Testing
**Problem:** Testing is currently manual and integration-focused only.

- [ ] **Implement `pytest`:** Create a test suite under `tests/`.
- [ ] **Mock Database:** Use a separate test database or SQLite in-memory for unit tests.
- [ ] **CI Integration:** Prepare tests to be run in a CI pipeline.

## Phase 4: Security Hardening
- [ ] **Audit Raw SQL:** Ensure no SQL injection risks exist in custom repository methods.
- [ ] **CSRF Implementation:** Re-enable and properly configure CSRF protection.
- [ ] **Rate Limiting:** Implement rate limiting for auth endpoints.
