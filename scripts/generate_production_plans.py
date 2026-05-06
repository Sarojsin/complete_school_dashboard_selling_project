#!/usr/bin/env python3
"""
Generate 30-day production readiness plan documents.
Each document follows the day1production.md template but with day-specific tasks.
"""

import os

# Define all 30 days with their specific content
days_plan = [
    # Week 1: Testing Foundation
    {
        "day": 1,
        "title": "Test Infrastructure Setup",
        "week": 1,
        "tasks": [
            "Add `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-mock` to requirements.txt",
            "Create `pytest.ini` with asyncio settings",
            "Setup `tests/` directory structure (unit/, integration/, conftest.py, factories.py)",
            "Configure coverage reporting in `pyproject.toml` or Makefile",
            "Add `make test`, `make test-cov` commands"
        ],
        "success": "`pytest` runs, collects coverage >0%"
    },
    {
        "day": 2,
        "title": "Factory Pattern & Fixtures",
        "week": 1,
        "tasks": [
            "Implement `tests/factories.py` using `factory_boy` or manual factories for all models",
            "Create `tests/conftest.py` with async DB session fixture, auth token fixture, test client",
            "Setup test database (SQLite in-memory or separate test Postgres DB)",
            "Ensure fixtures generate valid test data for all modules",
            "Make DB session rollback after each test automatically"
        ],
        "success": "Fixtures generate valid data; DB rolls back after each test"
    },
    {
        "day": 3,
        "title": "Unit Tests – Core Services",
        "week": 1,
        "tasks": [
            "Write unit tests for critical services:",
            "  - `AuthService` (login, token refresh, signup validation)",
            "  - `ExamSectionService` (result publishing, grade calculation)",
            "  - `EnrollmentService` (enrollment validation, duplicate checking)",
            "  - `AccountService` (payment validation, stats calculation)",
            "Mock repositories; focus on business logic",
            "Target 80% coverage on service methods"
        ],
        "success": "Service unit tests pass; coverage report shows >70% on tested services"
    },
    {
        "day": 4,
        "title": "Unit Tests – Repositories",
        "week": 1,
        "tasks": [
            "Write repository tests using real (test) database",
            "Test CRUD operations for:",
            "  - UserRepository",
            "  - TeacherRepository",
            "  - StudentRepository",
            "  - FacultyRepository",
            "  - EnrollmentRepository",
            "Test query filters, edge cases, constraint violations"
        ],
        "success": "Repository tests pass; integration with test DB works"
    },
    {
        "day": 5,
        "title": "Integration Tests – API Endpoints",
        "week": 1,
        "tasks": [
            "Write endpoint tests using `TestClient` for key flows:",
            "  - POST `/api/v1/auth/login` → 200, token returned",
            "  - POST `/api/v1/college/enrollments` → 201, enrollment created",
            "  - GET `/api/v1/college/exam_section/results` → 200, list returned",
            "  - POST `/api/v1/college/account/payments` → 201, payment recorded",
            "  - GET `/api/v1/school/hod/dashboard` → 200, dashboard data",
            "Test authentication required (401), authorization (403)"
        ],
        "success": "10+ endpoint tests pass; TestClient works with async DB"
    },
    {
        "day": 6,
        "title": "Coverage & Quality Gate",
        "week": 1,
        "tasks": [
            "Run `pytest --cov=modules --cov-report=html`",
            "Set minimum 70% overall coverage in CI config",
            "Add `bandit` for security scanning (`bandit -r modules/`)",
            "Add `ruff` for linting (`ruff check .`)",
            "Fix all HIGH severity bandit issues",
            "Configure coverage badge for README"
        ],
        "success": "Coverage ≥70%; no HIGH bandit issues; ruff passes"
    },
    {
        "day": 7,
        "title": "CI/CD Integration",
        "week": 1,
        "tasks": [
            "Create `.github/workflows/ci.yml` (or GitLab CI)",
            "Configure pipeline to:",
            "  - Install dependencies",
            "  - Run tests with coverage",
            "  - Run linter (ruff)",
            "  - Run security scan (bandit)",
            "  - Upload coverage to Codecov or similar",
            "Enforce coverage threshold; block merge if <70%",
            "Add status badge to README"
        ],
        "success": "CI pipeline green; coverage badge shows current %"
    },
    # Week 2: Database Reliability & Backup
    {
        "day": 8,
        "title": "Backup Strategy Design",
        "week": 2,
        "tasks": [
            "Confirm production DB: PostgreSQL (school_sell_db, college_sell_db)",
            "Design backup plan:",
            "  • Daily full dump at 2 AM via `pg_dump`",
            "  • Hourly WAL archiving for point-in-time recovery",
            "  • Retention: 30 daily, 12 weekly, 6 monthly",
            "Choose storage: S3 bucket or offsite server",
            "Document backup schedule and retention policy"
        ],
        "success": "Backup plan documented; storage provisioned (S3 bucket created)"
    },
    {
        "day": 9,
        "title": "Backup Script Implementation",
        "week": 2,
        "tasks": [
            "Create `scripts/backup_databases.sh`:",
            "  - Dumps both school and college DBs separately",
            "  - Compresses with gzip",
            "  - Uploads to S3 with timestamp prefix",
            "  - Prunes old backups based on retention policy",
            "Add logging (to file and stdout) and error handling",
            "Test script locally; ensure it runs without errors"
        ],
        "success": "Script runs successfully; backup files stored in S3"
    },
    {
        "day": 10,
        "title": "Restore Procedure & Testing",
        "week": 2,
        "tasks": [
            "Document step-by-step restore guide in `docs/restore.md`",
            "Test restore on staging environment:",
            "  1. Drop test databases",
            "  2. Restore from latest backup using `pg_restore`",
            "  3. Verify data integrity (row counts, sample records)",
            "Measure Recovery Time Objective (RTO) – target <4 hours",
            "Measure Recovery Point Objective (RPO) – target <1 hour"
        ],
        "success": "Restore tested successfully; RTO <4h, RPO <1h"
    },
    {
        "day": 11,
        "title": "Migration Robustness",
        "week": 2,
        "tasks": [
            "Review all Alembic migrations for idempotency",
            "Add CHECK constraints to existing tables:",
            "  - marks between 0-100",
            "  - amount >= 0",
            "  - email format validation",
            "Test migration on fresh DB from scratch: `alembic upgrade head` on empty DB",
            "Fix any migration order issues"
        ],
        "success": "Fresh DB migration succeeds without errors; all constraints applied"
    },
    {
        "day": 12,
        "title": "Data Integrity Checks",
        "week": 2,
        "tasks": [
            "Write script `scripts/check_integrity.py` to verify:",
            "  - No orphaned enrollments (enrollment.student_id exists in college_students)",
            "  - All courses have valid department_id",
            "  - Faculty payments reference existing faculty",
            "  - Exam results reference valid students and courses",
            "Schedule as daily cron job; send alert on failures",
            "Integrate with monitoring (Prometheus alert if checks fail)"
        ],
        "success": "Integrity script runs daily; 0 anomalies on production copy"
    },
    # Week 3: Security Hardening
    {
        "day": 13,
        "title": "Rate Limiting Implementation",
        "week": 3,
        "tasks": [
            "Add `slowapi` or Redis-based rate limiter to FastAPI",
            "Implement limits:",
            "  • `/api/auth/login` – 5 attempts per minute per IP",
            "  • `/api/auth/signup/*` – 3 per hour per IP",
            "  • General API – 1000 requests per minute per user",
            "  • Payment/grade updates – 100 per minute",
            "Return 429 status with Retry-After header"
        ],
        "success": "Rate limiter active; excess requests get 429; legitimate traffic unaffected"
    },
    {
        "day": 14,
        "title": "Audit Logging Implementation",
        "week": 3,
        "tasks": [
            "Create `AuditLog` model (school & college tables as needed)",
            "Fields: user_id, action (CREATE/UPDATE/DELETE), table, record_id, old_values, new_values, timestamp, ip_address",
            "Implement `AuditLogger` middleware/service that logs state-changing operations",
            "Log authentication events: login, logout, failed attempts",
            "Store logs in separate table or external service (e.g., ELK)"
        ],
        "success": "Key operations (user creation, fee payment, result publication) logged and queryable"
    },
    {
        "day": 15,
        "title": "Secrets Management & Rotation",
        "week": 3,
        "tasks": [
            "Remove all secrets from code and .env.example",
            "Ensure production uses environment variables only",
            "Implement secret rotation plan:",
            "  - JWT secret: rotate every 90 days",
            "  - Database passwords: rotate every 30 days",
            "Document rotation procedure and test in staging",
            "Consider AWS Secrets Manager or HashiCorp Vault for production"
        ],
        "success": "No secrets in repo; rotation procedure documented and tested"
    },
    {
        "day": 16,
        "title": "ID Enumeration Protection",
        "week": 3,
        "tasks": [
            "Replace auto-increment IDs in public API responses with UUIDs",
            "Add `uuid` column (String, unique) to sensitive tables: students, faculty, teachers",
            "Update serializers to return UUID instead of numeric ID",
            "Update frontend to use UUIDs for resource identification",
            "Keep numeric IDs internal only"
        ],
        "success": "External APIs no longer expose sequential numeric IDs; UUIDs used consistently"
    },
    {
        "day": 17,
        "title": "Two-Factor Authentication for Privileged Roles",
        "week": 3,
        "tasks": [
            "Add `two_factor_enabled` and `two_factor_secret` columns to User model",
            "Implement TOTP using `pyotp`",
            "Provide QR code generation for setup",
            "Enforce 2FA for super_admin, authority, dean, registrar roles",
            "Provide backup codes (10 one-time use)",
            "Allow users to enable/disable if policy permits"
        ],
        "success": "2FA available; required roles must use it; backup codes generated"
    },
    # Week 4: Observability & Reliability
    {
        "day": 18,
        "title": "Metrics & Monitoring Setup",
        "week": 4,
        "tasks": [
            "Add `prometheus-client` to FastAPI",
            "Expose `/metrics` endpoint with counters:",
            "  - `http_requests_total` (labels: method, path, status)",
            "  - `http_request_duration_seconds` (histogram)",
            "  - `database_errors_total`",
            "  - `business_operations_total` (e.g., enrollments created)",
            "Deploy Prometheus or configure Datadog agent to scrape",
            "Create Grafana dashboard for request rates and errors"
        ],
        "success": "Metrics endpoint returns data; dashboard shows real-time request rates"
    },
    {
        "day": 19,
        "title": "Centralized Logging Integration",
        "week": 4,
        "tasks": [
            "Integrate `structlog` or `json-logging` middleware",
            "Log in JSON format with fields: timestamp, level, user_id, request_id, endpoint, latency",
            "Ship logs to ELK stack (Elasticsearch, Logstash, Kibana) or Loki/Grafana",
            "Ensure logs are indexed and searchable",
            "Configure log rotation on application servers"
        ],
        "success": "Logs searchable by user_id, request_id within seconds"
    },
    {
        "day": 20,
        "title": "Error Tracking & Alerting",
        "week": 4,
        "tasks": [
            "Add Sentry SDK (`sentry-sdk[fastapi]`) to app",
            "Configure environment-specific DSNs",
            "Set up alerts:",
            "  - Error rate > 1% over 5 minutes",
            "  - 5xx responses > 5%",
            "  - Slow requests (>2s) > 10%",
            "Integrate with Slack/PagerDuty notifications",
            "Test by raising test exception in code"
        ],
        "success": "Sentry captures test errors; alerts triggered to team Slack"
    },
    {
        "day": 21,
        "title": "Health Checks & Readiness Enhancement",
        "week": 4,
        "tasks": [
            "Enhance `/health/ready` endpoint:",
            "  - Check database connectivity (run simple query)",
            "  - Check Redis (if used)",
            "  - Check disk space (>1GB free)",
            "  - Check background worker status",
            "Return 503 with JSON details if any check fails",
            "Update `/health/live` to just return 200 if process alive"
        ],
        "success": "`/health/ready` responds 200 under normal conditions; 503 with details on simulated failures"
    },
    {
        "day": 22,
        "title": "Graceful Shutdown & Zero-Downtime",
        "week": 4,
        "tasks": [
            "Test FastAPI signal handling (SIGTERM, SIGINT)",
            "Ensure database connections are closed properly on shutdown",
            "Verify Alembic migrations can run without stopping the app (use online migrations)",
            "Implement rolling updates if using Kubernetes",
            "Document deployment procedure with zero downtime"
        ],
        "success": "App shuts down cleanly; no hanging connections; migrations apply live"
    },
    # Week 5: Performance Optimization
    {
        "day": 23,
        "title": "Connection Pooling Review",
        "week": 5,
        "tasks": [
            "Review SQLAlchemy engine pool configuration",
            "Set appropriate pool size: `pool_size=20`, `max_overflow=10` for PostgreSQL",
            "Monitor pool utilization via metrics (`pool_connections_acquired`)",
            "Tune based on concurrent user load (target <80% pool usage)",
            "Document pool settings for different environments"
        ],
        "success": "Connection pool config optimal; no starvation errors under load"
    },
    {
        "day": 24,
        "title": "N+1 Query Fixes",
        "week": 5,
        "tasks": [
            "Profile endpoints with `silk` or `py-instrument`",
            "Identify N+1 queries (e.g., fetching teacher → user repeatedly)",
            "Add `selectinload` or `joinedload` for lazy relationships",
            "Common fixes:",
            "  - Teacher → user",
            "  - Student → enrollments → course",
            "  - Course → instructor → department",
            "Re-measure query count per request; target <5 for typical page"
        ],
        "success": "N+1 queries eliminated; average queries per request <5"
    },
    {
        "day": 25,
        "title": "Caching Implementation",
        "week": 5,
        "tasks": [
            "Add Redis cache layer (install `redis` or `aioredis`)",
            "Cache read-only, rarely changed data:",
            "  - Fee structures",
            "  - Academic calendar/semesters",
            "  - Program list",
            "  - Department list",
            "Use `aiocache` with TTL (e.g., 1 hour)",
            "Implement cache invalidation on update operations"
        ],
        "success": "Cached endpoints respond 50% faster; DB load reduced by 30%"
    },
    {
        "day": 26,
        "title": "Static Assets & CDN Integration",
        "week": 5,
        "tasks": [
            "Configure S3 bucket + CloudFront CDN for uploaded files",
            "Upload existing avatars, notes, videos to CDN",
            "Generate presigned URLs for protected/private files",
            "Update backend to return CDN URLs instead of local paths",
            "Update frontend to use CDN URLs",
            "Set appropriate cache headers (Cache-Control: max-age=31536000)"
        ],
        "success": "Static assets served from CDN; origin server bandwidth reduced >80%"
    },
    {
        "day": 27,
        "title": "Profiling & Load Testing",
        "week": 5,
        "tasks": [
            "Run load test with `locust` or `k6` simulating 500 concurrent users",
            "Identify bottlenecks (CPU, memory, DB locks, slow queries)",
            "Optimize slowest endpoints (target p95 latency <200ms)",
            "Tune based on findings (increase workers, optimize queries, add indexes)",
            "Document performance baselines"
        ],
        "success": "Load test passes with 500 users; p95 latency <200ms; no errors"
    },
    # Week 6: Final Validation & Go-Live
    {
        "day": 28,
        "title": "Security Audit & Compliance",
        "week": 6,
        "tasks": [
            "Run `bandit` and `safety` to find vulnerabilities",
            "Fix all HIGH severity issues",
            "Review OWASP Top 10 coverage:",
            "  - SQL injection: using SQLAlchemy, verify no raw SQL",
            "  - XSS: ensure proper escaping (React built-in helps)",
            "  - CSRF: if using cookies, verify tokens; JWT less vulnerable",
            "  - Authentication failures: test lockout, token expiry",
            "Document security controls in `docs/security.md`"
        ],
        "success": "No HIGH vulnerabilities; OWASP checklist passed; security doc complete"
    },
    {
        "day": 29,
        "title": "Documentation & Runbooks",
        "week": 6,
        "tasks": [
            "Update `README.md` with production setup steps",
            "Write `docs/architecture.md` with module diagram and DB schema",
            "Create runbooks:",
            "  - Backup restore procedure",
            "  - Scaling steps (horizontal scaling, DB read replica)",
            "  - Incident response (outage, data corruption)",
            "  - Common troubleshooting (high latency, errors)",
            "Generate OpenAPI spec (`/openapi.json`) and share with frontend team",
            "Changelog completed for all releases"
        ],
        "success": "All documentation published; runbooks reviewed by on-call team"
    },
    {
        "day": 30,
        "title": "Staging Deployment & Smoke Test",
        "week": 6,
        "tasks": [
            "Deploy to staging environment (identical to production)",
            "Run full regression test suite (automated + manual)",
            "Verify all 495 endpoints work correctly",
            "Confirm monitoring, logging, backups are active",
            "Performance test staging under load",
            "Conduct security smoke test (try common attacks)",
            "Final sign-off meeting; go-live decision"
        ],
        "success": "Staging validated; all critical flows pass; ready for production deploy"
    }
]

# Template for each day's document
DOC_TEMPLATE = """# Day {day} Production Readiness Plan – {title}

**Week {week} of 6** | **Date:** {date} | **Status:** Planned

## Objectives

- [ ] Complete all tasks listed below
- [ ] Achieve success criteria by end of day

---

## Tasks for Today

{task_list}

---

## Success Criteria

{success_criteria}

---

## Dependencies & Blockers

- List any dependencies on other teams or tasks
- Identify blockers early and escalate

---

## Notes & Deliverables

- What will be delivered by end of day?
- Any documentation updates?
- CI/CD changes?

---

**Completed:** _________________________  
**Reviewed by:** _________________________  
**Date:** _________________________
"""

def generate_all_plans():
    """Generate all 30 daily plan documents"""
    output_dir = "production_plans"
    os.makedirs(output_dir, exist_ok=True)
    
    for day_data in days_plan:
        day = day_data["day"]
        filename = f"{output_dir}/day{day:02d}_production.md"
        
        # Format task list as markdown checklist
        task_list = "\n".join([f"- [ ] {task}" for task in day_data["tasks"]])
        
        # Format date (assuming start date of 2026-05-06)
        start_date = datetime(2026, 5, 6)  # Day 1 start
        current_date = start_date + timedelta(days=day-1)
        date_str = current_date.strftime("%Y-%m-%d")
        
        content = DOC_TEMPLATE.format(
            day=day,
            title=day_data["title"],
            week=day_data["week"],
            date=date_str,
            task_list=task_list,
            success_criteria=day_data["success"]
        )
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✓ Generated {filename}")

    print(f"\n✅ All {len(days_plan)} daily production plans created in '{output_dir}/'")

if __name__ == "__main__":
    from datetime import datetime, timedelta
    generate_all_plans()
