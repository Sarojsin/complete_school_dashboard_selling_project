# Day 24 Production Implementation Plan
**Date**: 2026-05-29
**Focus**: Final Security Audit & Performance Load Testing

## Objectives
- Run comprehensive security scans (bandit, safety/pip-audit) and remediate findings
- Perform load testing to validate system under peak traffic (500+ concurrent users)
- Identify and fix performance bottlenecks (slow queries, memory leaks)
- Ensure test coverage ≥70% overall
- Generate final quality gate report before go-live

## Tasks

### 1. Morning: Security Scanning (2 hours)
**Bandit (Python SAST)**:
- [ ] `pip install bandit`
- [ ] Run: `bandit -r modules/ -f json -o bandit-report-final.json`
- [ ] Review report:
  - HIGH severity: must fix (e.g., `subprocess` use, hardcoded secrets)
  - MEDIUM: evaluate, fix if applicable (e.g., `assert` used, pickling)
  - LOW: document
- [ ] Fix any findings:
  - Ensure no hardcoded passwords/keys in code (check backup dir if accidentally included)
  - Replace `assert` statements with proper validation (if flagged)
  - Sanitize any `eval` or `exec` (should be none)
  - Ensure temporary file creation uses `tempfile` module
- [ ] Re-run until 0 HIGH, ≤5 MEDIUM (acceptable)

**Dependency vulnerability scan**:
- [ ] `pip install pip-audit` or `safety`
- [ ] `pip-audit --desc --format json -o pip-audit-report.json` OR
- [ ] `safety check --json --output safety-report.json`
- [ ] Review for known CVEs in dependencies:
  - FastAPI, SQLAlchemy, alembic, passlib, python-jose, etc.
- [ ] Upgrade vulnerable packages:
  - `pip install --upgrade <package>` (test after upgrade)
  - Update `requirements.txt` with new versions
  - Re-run pip-audit to confirm clean

**SQL Injection check**:
- [ ] Ensure no raw SQL with string interpolation: grep `execute("` or `text("`
- [ ] All queries should use SQLAlchemy ORM or parameterized `text()`: `text("SELECT * FROM users WHERE id=:id")`

**Secret leakage**:
- [ ] Verify `.env` not committed (check git history)
- [ ] Ensure `SECRET_KEY`, `ALGORITHM`, DB passwords not in code
- [ ] Run: `git grep -i "password" -- '*.py'` to catch accidental secrets

**Document findings**:
- Create `SECURITY_AUDIT_REPORT.md`:
  - Total issues found (bandit HIGH, MEDIUM, LOW)
  - Remediation steps taken
  - Remaining risks accepted (with justification)
  - Dependency vulnerabilities list + fixed packages

### 2. Load Testing (2 hours)
**Install k6** (or Locust):
- [ ] Download k6: https://k6.io/docs/ or `choco install k6` (Windows)
- [ ] Write test script `load_tests/auth_load_test.js`:

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 50 },   // ramp up to 50 users
    { duration: '1m', target: 200 },  // ramp to 200
    { duration: '2m', target: 500 },  // peak 500 concurrent
    { duration: '30s', target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],   // <1% errors
  },
};

export default function () {
  // Scenario 1: Login
  let loginResponse = http.post('http://localhost:8000/api/v1/auth/login', {
    username: 'testuser@example.com',
    password: 'testpass123',
  });
  check(loginResponse, { 'login 200': (r) => r.status === 200 });
  
  if (loginResponse.status === 200) {
    let token = loginResponse.json('access_token');
    
    // Scenario 2: Access student dashboard
    let dashResponse = http.get('http://localhost:8000/api/v1/college/students/me', {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    check(dashResponse, { 'dashboard 200': (r) => r.status === 200 });
  }
  
  sleep(1);
}
```

**Run test**:
```bash
k6 run load_tests/auth_load_test.js
```

**Monitor server** during load test:
- [ ] CPU/memory usage
- [ ] Database connection pool utilization
- [ ] Response times (p50, p95, p99)
- [ ] Error rate (should be <1%)

**Failing scenarios**:
- If connection pool exhausted: increase `pool_size` (to 50) and `max_overflow` (to 20)
- If DB queries slow: identify with `pg_stat_statements`; add indexes
- If app crashes: check logs for OOM; increase container memory

**Load test other endpoints**:
- College dean analytics (heavy query): `GET /analytics/dean/overview`
- Enrollment list with filters: `GET /enrollments?student_id=...`

**Record results** in `LOAD_TEST_RESULTS.md`:
- Avg response time, p95, p99
- Throughput (req/sec)
- Error rate
- System resource utilization

### 3. Test Coverage Push to 70%+ (1 hour)
**Run full coverage**:
```bash
pytest --cov=modules --cov-report=term-missing --cov-report=html
```

**Identify gaps**:
- Open `htmlcov/index.html`
- Note modules <50%: likely some simple CRUD routers or complex error handlers

**Add targeted tests**:
- [ ] For any module <40%, add tests for missing branches
- [ ] Focus on service layer logic, not just happy paths
- [ ] Use parameterized tests to cover multiple scenarios

**Target**: 
- Overall coverage ≥70%
- No module <50% unless trivial (3 lines)

**Report**:
- Update `COVERAGE.md` with final numbers

### 4. Performance Profiling & Query Optimization (1 hour)
**Enable SQLAlchemy query logging** in dev:
```python
engine = create_async_engine(..., echo=True)  # already configured in debug
```
- [ ] Trigger slow endpoint (dean analytics)
- [ ] Count queries: look for N+1
- [ ] Use `EXPLAIN ANALYZE` in psql for top 5 slowest queries from `pg_stat_statements`

**Add missing indexes** (if any identified):
- [ ] Index on `enrollment_date` (enrollments) for date range queries
- [ ] Index on `created_at` (various tables) for sorting
- [ ] Composite: `(program_id, status)` for fee_records common filter

**Optimize**:
- [ ] Pagination already in place – ensure no `OFFSET` skipping huge numbers without index
- [ ] Use `selectinload` for relationships; verify via query count in tests
- [ ] Consider CTE or materialized view for dean analytics (future)

### 5. Final Documentation (30 min)
**Update**:
- [ ] `PERFORMANCE.md`: Cache strategy, indexes, pool size
- [ ] `SECURITY_AUDIT_REPORT.md`: Findings + remediation
- [ ] `LOAD_TEST_RESULTS.md`: Scenario, metrics, bottlenecks fixed
- [ ] `COVERAGE.md`: final percentages per module
- [ ] `README.md`: add badges for build, coverage

**Create**:
- [ ] `PRODUCTION_READINESS_REPORT.md`: Summary of all features implemented, scorecard (expected: 78%?)

### 6. Commit & Tag (30 min)
- [ ] Git add: security reports, load test script, coverage docs, any fixes
- [ ] Commit: "test(security): Final audit scan 0 HIGH findings; optimize queries; load test 500 users 95th<500ms; coverage 72%"
- [ ] Tag: `v0.8.0-security-performance-final`
- [ ] Push

## Deliverables
- ✅ Bandit scan: 0 HIGH, ≤5 MEDIUM
- ✅ pip-audit: 0 critical/high vulnerabilities (or documented exceptions)
- ✅ Load test: 500 concurrent users, p95 < 500ms, error rate <1%
- ✅ Test coverage ≥70% overall; no module <50% (except trivial)
- ✅ Slow queries identified and optimized
- ✅ `SECURITY_AUDIT_REPORT.md`, `LOAD_TEST_RESULTS.md`, `COVERAGE.md` updated
- ✅ Git tag `v0.8.0-security-performance-final`

## Success Criteria
- Application handles 500 concurrent users without degradation
- No security vulnerabilities at HIGH level
- All critical paths have tests; coverage target met
- Performance SLA: 95% of requests complete <500ms
- Database not saturated (CPU <70%, connections within pool)

## Notes
- Load test should simulate realistic user journeys (login + dashboard + one feature)
- Run on local machine; for more accurate network-included test, deploy to staging VM
- If performance not meeting targets, review indexes, connection pool, and caching effectiveness
- Consider adding Redis cache for heavy analytics queries (already cached)

## Next: Day 25
Pre-launch checklist dry run: staging deployment, smoke tests, rollback drill, final documentation review, team handoff meeting.
