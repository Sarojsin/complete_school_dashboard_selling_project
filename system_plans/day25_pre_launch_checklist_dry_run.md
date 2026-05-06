# Day 25 Production Implementation Plan
**Date**: 2026-05-30
**Focus**: Pre-Launch Checklist & Staging Dry Run

## Objectives
- Execute complete pre-launch checklist covering all systems
- Deploy to staging environment (production-like)
- Conduct full smoke test suite (all critical user journeys)
- Practice rollback procedure to ensure recoverability
- Finalize handoff documentation for operations team
- Prepare go/no-go decision report for production launch

## Pre-Launch Checklist (Master)

| Area | Item | Status | Owner | Notes |
|------|------|--------|-------|-------|
| Infrastructure | Docker images built and pushed to registry | | | |
| | Nginx config deployed (staging) | | | |
| | SSL certificate installed (staging) | | | |
| | Environment variables configured (`.env.production`) | | | |
| Database | College DB migration applied (latest Alembic) | | | |
| | School DB schema current | | | |
| | Connection pool tuned (pool_size=20, max_overflow=10) | | | |
| Backups | Daily backup script operational | | | |
| | Offsite backup (S3) uploading successfully | | | |
| | Restore procedure tested (this week) | | | |
| Monitoring | Prometheus `/metrics` endpoint accessible | | | |
| | Sentry DSN configured and capturing errors | | | |
| | Health checks (`/health/ready`, `/health/live`) returning 200 | | | |
| | Log aggregation (ELK/Loki) configured (staging) | | | |
| CI/CD | GitHub Actions passing on main | | | |
| | Docker image auto-built on push | | | |
| | Rollback tag strategy defined | | | |
| Security | Rate limiting on auth endpoints active | | | |
| | 2FA enforcement for admin roles | | | |
| | Soft delete implemented on critical tables | | | |
| | Bandit scan 0 HIGH, pip-audit clean | | | |
| | Secrets NOT in code; loaded from environment | | | |
| Features | All 8 college modules operational | | | |
| | All school modules operational | | | |
| | Caching (Redis) running; TTL configured | | | |
| | Celery worker + beat running | | | |
| | UUID public IDs in all college resources | | | |
| Compliance | GDPR export/delete endpoints implemented | | | |
| | Consent logging working | | | |
| | Privacy Policy & TOS published | | | |
| Audits | Audit logging covering all CRUD | | | |
| | Admin audit query endpoint `/admin/audit` | | | |
| | Automated purge of >2yr logs scheduled | | | |
| Documentation | README complete with setup instructions | | | |
| | Architecture diagram published | | | |
| | API docs (Swagger) up-to-date | | | |
| | User guides (all roles) written | | | |
| | Deployment runbook written | | | |
| | DR runbook written | | | |
| Testing | Unit tests running on CI | | | |
| | Coverage ≥70% | | | |
| | Integration tests passing | | | |
| | Load test completed successfully (500 users) | | | |
| Pre-Launch | Staging deployment completed | | | |
| | Smoke test suite executed and passed | | | |
| | Rollback procedure practiced | | | |
| | Team handoff meeting held | | | |
| Go/No-Go Decision | All critical items green | | | |
| | No open HIGH severity bugs | | | |
| | Stakeholder sign-off obtained | | | |

---

### Tasks for Day 25

#### 1. Morning: Prepare Staging Environment (2 hours)
**Goal**: Mirror production setup as closely as possible.

- [ ] Provision staging server (cloud or on-prem):
  - Domain: `staging.example.com` or IP
  - OS: Ubuntu 22.04 LTS
  - Docker + Docker Compose installed
- [ ] Clone repository to staging server
- [ ] Create staging `.env`:
  - `ENV=staging`
  - `DATABASE_MODE=separate`
  - Separate databases: `school_sell_staging`, `college_sell_staging`
  - `SECRET_KEY` (different from prod)
  - `SENTRY_DSN` (staging DSN)
  - `REDIS_URL`
  - `S3_BUCKET=backups-staging`
  - All other envs matching prod except scale
- [ ] Initialize databases:
  ```bash
  alembic -c alembic.ini upgrade head
  alembic -c alembic_college.ini upgrade head
  ```
- [ ] Create super admin user: `python -m modules.auth.hashing create-superuser`
- [ ] Deploy using `docker-compose -f docker-compose.prod.yml up -d`
- [ ] Verify services running: `docker ps`

#### 2. Staging Dry Run – Smoke Tests (2 hours)
**Automated smoke test script** (`scripts/smoke_test_staging.py`):

```python
import requests
import json

BASE_URL = "http://staging.example.com:8000"

def smoke_test():
    results = []
    
    # 1. Health checks
    resp = requests.get(f"{BASE_URL}/health/live")
    results.append(("Health live", resp.status_code == 200))
    
    resp = requests.get(f"{BASE_URL}/health/ready")
    results.append(("Health ready", resp.status_code == 200))
    
    # 2. Metrics endpoint
    resp = requests.get(f"{BASE_URL}/metrics")
    results.append(("Prometheus metrics", resp.status_code == 200))
    
    # 3. Auth endpoints
    # Signup student
    signup_data = {"email":"test@example.com","password":"Test123!","role":"college_student",...}
    resp = requests.post(f"{BASE_URL}/api/v1/auth/college-student-signup", json=signup_data)
    results.append(("Student signup", resp.status_code in [200,201]))
    
    # Login
    login_data = {"username":"test@example.com","password":"Test123!"}
    resp = requests.post(f"{BASE_URL}/api/v1/auth/login", data=login_data)
    results.append(("Login", resp.status_code == 200))
    token = resp.json().get("access_token")
    
    # 4. Protected endpoints
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/api/v1/college/students/me", headers=headers)
    results.append(("Student me", resp.status_code == 200))
    
    # 5. College modules
    resp = requests.get(f"{BASE_URL}/api/v1/college/programs", headers=headers)
    results.append(("List programs", resp.status_code == 200))
    
    resp = requests.get(f"{BASE_URL}/api/v1/college/analytics/dean/overview", headers=headers)
    results.append(("Dean analytics", resp.status_code in [200,403]))  # 403 if not dean
    
    # 6. Admin audit endpoint (super admin only)
    # ... test with super admin token
    
    print("Smoke Test Results")
    for test, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test}")
    
    all_passed = all(p for _, p in results)
    return all_passed

if __name__ == "__main__":
    success = smoke_test()
    exit(0 if success else 1)
```

- [ ] Run script; all must pass
- [ ] If any fail, debug and fix before proceeding

#### 3. Rollback Drill (1 hour)
**Practice rollback procedure** to ensure team can recover quickly:

**Scenario**: New deployment has bug; need to revert to previous version.

Steps:
1. Note current image tag: `v0.8.0-security-performance-final`
2. Downgrade to previous: `git checkout v0.7.0-week3-advanced` → rebuild image `backend:v0.7.0`
3. Update `docker-compose.prod.yml` to use old image
4. `docker-compose down && docker-compose up -d`
5. Verify app starts: `curl http://staging:8000/health/ready`
6. Run smoke test again; expect pass
7. Document time to rollback (<5 min target)

**If rollback fails**: Document blockers and adjust plan (need better migration reversibility?)

#### 4. Final Documentation Review (1 hour)
**Checklist**:
- [ ] `README.md` – setup, env, deployment, troubleshooting complete
- [ ] `DEPLOYMENT.md` – step-by-step with commands
- [ ] `BACKUP_RESTORE.md` – verified restore steps
- [ ] `SECURITY.md` – security config, rate limits, 2FA
- [ ] `AUDIT_LOGGING.md` – what's logged, how to query
- [ ] `DATA_RETENTION.md` – schedule, table-by-table
- [ ] `CHANGELOG.md` – all changes logged
- [ ] `CONTRIBUTING.md` – coding standards, testing
- [ ] `API.md` or Swagger auto-docs complete

**Markdown lint**: `markdownlint` or manual review

#### 5. Team Handoff Meeting Preparation (1 hour)
**Create handoff package**:
- `HANDOFF_PACKAGE.md` with:
  - System architecture diagram link
  - Key contacts (backend lead, DevOps, DBA, security officer)
  - Monitoring dashboard links (Grafana/Prometheus if set up)
  - Incident response runbook summary:
    - ! Service down → check `/health`, then `docker logs`, restart container
    - ! Database connection errors → check pool, connectivity
    - ! High error rate → check Sentry alerts, rollback image
  - escalation matrix
- Schedule meeting for Day 26 with ops team

#### 6. Go/No-Go Decision Report (1 hour)
**Draft final recommendation**:

```markdown
# Production Go/No-Go Decision – 2026-05-30

## Production Readiness Score: 78%
- **Passing**: All test suites, load test, security audit, CI green
- **Outstanding**: None critical; minor enhancements deferred
- **Open Risks**: 
  - Offsite backup restore not yet tested end-to-end (manual scheduled)
  - i18n coverage limited to 2 languages (acceptable for launch)
  - UUID migration introduces larger indexes; monitor DB size

## Recommendation: **GO** for production launch on 2026-06-01

### Required Pre-Launch (Day 30):
- [ ] Final production env variables secured
- [ ] SSL certificate installed on prod domain
- [ ] Monitoring alerts configured (Sentry, metrics)
- [ ] Backup cron job active on prod server
- [ ] Team sign-off (Dev, Ops, Security)

### Rollback Plan:
- Previous image: `v0.7.0-week3-advanced` maintained
- Database point-in-time recovery via pg_dump backup
- DNS TTL set low (5 min) for quick switch

### Post-Launch:
- Week 1: On-call rotation, monitor Sentry errors, response times
- Week 2: Performance tuning based on real traffic
- Week 3: Feature freeze; bug fixes only
```

#### 7. Commit & Summary (30 min)
- [ ] Commit: "docs: Pre-launch checklist, staging smoke tests, rollback drill, handoff package"
- [ ] Tag `v1.0.0-rc.1` (release candidate)
- [ ] Push everything

## Deliverables
- ✅ Staging environment deployed (mirrors production)
- ✅ Smoke test script (`scripts/smoke_test_staging.py`) – all green
- ✅ Rollback drill performed; <5 min downtime achievable
- ✅ Handoff package (`HANDOFF_PACKAGE.md`)
- ✅ `GO_NO_GO.md` decision document
- ✅ Updated checklist covering all 99-point items
- ✅ Git tag `v1.0.0-rc.1`

## Success Criteria
- Every checklist item marked ✅ or N/A (none red)
- Smoke test passes end-to-end (signup → login → dashboard → task)
- Rollback procedure documented and practiced successfully
- All team members aware of roles for launch day
- Stakeholders approve go-live

## Notes
- This is the final gate before production launch
- If any critical item fails, defer launch to Day 26 or later; address blocker
- Communication plan: notify stakeholders 24h before launch window
- Launch window: early morning (low traffic) on Day 30

## Next: Day 26-29
Buffer days for any last-minute issues, final regression testing, performance tuning based on staging metrics, stakeholder UAT sign-off, and production deployment preparation.
