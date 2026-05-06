# Days 26-28: Buffer & Final Polish
**Dates**: 2026-05-31 – 2026-06-02
**Focus**: Issue Resolution, UAT, & Final Pre-Launch Tuning

## Overview
These are buffer days to address any issues discovered during staging dry run, accommodate scope adjustments, and ensure absolute readiness. No new features – only stabilization.

---

## Day 26 – Final Regression Testing & Bug Fixes

**Objectives**:
- Execute full regression test suite against staging
- Fix any remaining bugs discovered
- Verify rollback mechanism (tagged images)

**Tasks**:
- [ ] Run **complete test suite**: `pytest -v` (target: 100% pass)
- [ ] Run **integration tests**: `pytest tests/integration/ -v`
- [ ] Manual regression checklist:
  - [ ] Student signup → login → view dashboard
  - [ ] Faculty login → upload marks → publish results
  - [ ] HOD login → view department analytics
  - [ ] Dean login → college overview → export report
  - [ ] Registrar login → fee collection report
  - [ ] Super admin → create user → assign role → test login
- [ ] Fix any failing tests or broken flows
- [ ] Verify all 495 routes respond (use `scripts/verify_app.py`)
- [ ] Confirm rollback tags exist: `git tag -l | grep v0.7.0` and `v0.8.0`
- [ ] Commit fixes, tag `v0.9.0-regression-fixes`

**Deliverable**: All tests passing, staging smoke test clean, regression suite green

---

## Day 27 – Performance Optimization Pass

**Objectives**:
- Final query optimization based on staging metrics
- Connection pool fine-tuning
- Cache hit rate optimization

**Tasks**:
- [ ] Review staging metrics: Prometheus query response times, DB CPU
- [ ] Identify top 5 slowest queries (via `pg_stat_statements` or `pgBadger`)
- [ ] Optimize:
  - Add/adjust indexes
  - Refactor complex queries (subqueries → CTE or joins)
  - Increase cache TTL for stable data
  - Reduce N+1 if any missed
- [ ] Tune DB connection pool: `pool_size=30`, `max_overflow=15` if needed
- [ ] Monitor Redis memory: ensure fit in instance; configure eviction policy `volatile-lru`
- [ ] Run load test again (if changes significant)
- [ ] Document final performance settings in `PERFORMANCE.md`
- [ ] Commit performance tweaks, tag `v0.9.1-perf-optimized`

**Deliverable**: 95th percentile response time ≤400ms for all core endpoints

---

## Day 28 – User Acceptance Testing (UAT) & Stakeholder Review

**Objectives**:
- Invite key stakeholders to test staging
- Collect feedback; triage critical issues
- Obtain sign-off for production launch

**Tasks**:
- [ ] Deploy latest to staging (if not already)
- [ ] Create UAT sign-off document (`UAT_SIGN_OFF.md`)
- [ ] Email stakeholders (admin, dean, registrar) with staging URL + test accounts
- [ ] Provide test scenarios (like Day 26 manual regression)
- [ ] Collect feedback in shared doc (Google Sheet or GitHub Issues)
- [ ] Triage:
  - **Critical** (blocks launch): fix immediately
  - **High** (should fix post-launch): document in known issues
  - **Medium/Low**: log for future sprint
- [ ] Address any critical blockers
- [ ] Final demo call with stakeholders (30 min)
- [ ] Obtain written sign-off (email or `UAT_SIGN_OFF.md` signed)
- [ ] Commit any critical fixes, tag `v1.0.0-rc.2`

**Deliverable**: ✅ UAT sign-off document; no showstoppers

---

## Day 29 – Final Production Deployment Prep

**Objectives**:
- Final production environment provisioning
- Pre-deployment verification
- Launch runthrough checklist
- Team standup & go-live readiness

**Tasks**:
- [ ] Provision production server(s) (if not already):
  - Domain configured (e.g., `schoolcollege.example.com`)
  - SSL cert obtained (Let's Encrypt) or provisioned
  - Firewall rules (only 80/443 open)
  - SSH key access restricted to ops team
- [ ] Create production `.env` (secure vault entry):
  ```
  ENV=production
  DATABASE_MODE=separate
  SCHOOL_DATABASE_URL=postgresql://.../school_sell_prod
  COLLEGE_DATABASE_URL=postgresql://.../college_sell_prod
  SECRET_KEY=<32+ random>
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=15
  BACKUP_S3_BUCKET=school-college-prod-backups
  SENTRY_DSN=<production DSN>
  REDIS_URL=redis://prod-redis:6379/0
  ```
  (Use AWS Secrets Manager or similar for injection at deploy time)
- [ ] Initialize production databases:
  ```bash
  # Connect to prod DB servers
  alembic -c alembic.ini upgrade head
  alembic -c alembic_college.ini upgrade head
  ```
- [ ] Create initial super admin: `python -m modules.auth.hashing create-superadmin`
- [ ] Test DB connectivity: `python -c "from modules.shared.database import test_connection; test_connection()"`
- [ ] Run final backup: `python scripts/backup_databases.py` → verify offsite upload
- [ ] Prepare deployment command:
  ```bash
  docker-compose -f docker-compose.prod.yml down
  docker-compose -f docker-compose.prod.yml pull
  docker-compose -f docker-compose.prod.yml up -d
  ```
- [ ] Health check post-deploy:
  ```bash
  curl -f https://schoolcollege.example.com/health/ready
  ```
- [ ] Smoke test production:
  ```bash
  python scripts/smoke_test_staging.py --url=https://schoolcollege.example.com
  ```
- [ ] If smoke fails: rollback immediately; else continue
- [ ] Set up monitoring alerts:
  - Sentry alert on >5 errors/min
  - Prometheus alert if 5xx rate >1%
  - Health check fails → PagerDuty
- [ ] Final team call: confirm readiness, assign on-call

**Deliverable**: Production deployed, smoke test passes, monitoring active, on-call assigned

---

## Overall Week 4 (Days 21-29) Deliverables

| Day | Completed | 
|-----|-----------|
| 21 | GDPR export/delete, consent, privacy policy |
| 22 | Audit logging full coverage, admin endpoint, retention purge |
| 23 | User manuals (all roles), FAQ, video scripts, help API |
| 24 | Security audit (bandit 0 HIGH), load test (500 users, p95 <500ms), coverage ≥70% |
| 25 | Staging dry-run, smoke test, rollback drill, handoff package |
| 26 | Regression testing bug fixes |
| 27 | Performance optimization pass |
| 28 | UAT sign-off from stakeholders |
| 29 | Production deployment preparation complete |

Estimated Production Readiness Score after Week 4: **~90%**

---

## Remaining Items for Post-Launch (Day 30+)
- Offsite backup restore test (monthly)
- Production load monitoring (weekly review)
- Security patches (monthly `pip-audit`)
- Feature requests roadmap (v1.1+)

---

## Day 30: Production Launch (if everything green)

**Scripted deployment**:
```bash
# 1. Final backup of staging (snapshot)
# 2. Deploy to production with zero-downtime strategy:
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --no-deps backend
# Rolling: if multiple instances, update one at a time
# 3. Run production migrations: docker exec backend alembic upgrade head
# 4. Smoke test production (same script)
# 5. Notify stakeholders of successful launch
# 6. Monitor metrics + Sentry for 24h
```

If issues: execute rollback plan, investigate, redeploy.

**Post-Launch Review** (Day 31 or +1 week):
- Metrics review: traffic, errors, latency
- User feedback collection
- Lessons learned document

---

*These buffer days ensure we have time to address any unexpected blockers before launch. Adjust as needed if earlier weeks finish early.*
