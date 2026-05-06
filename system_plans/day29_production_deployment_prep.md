# Day 29: Production Deployment Final Preparation
**Date**: 2026-06-02
**Focus**: Production Environment Validation & Pre-Deployment Checks

## Objectives
- Validate production infrastructure is ready
- Verify all secrets and configurations
- Conduct final backup & restore test on production DB
- Execute final smoke test suite on production-like environment
- Prepare launch checklist and communication plan

## Morning Checklist (3 hours)

### 1. Production Environment Audit
- [ ] Server provisioned with: Ubuntu 22.04 LTS, Docker, Docker Compose, Nginx (if separate)
- [ ] Domain DNS points to server IP (A record)
- [ ] SSL certificate provisioned (Let's Encrypt certbot or purchased cert)
- [ ] Firewall: only 22 (SSH), 80, 443 open; restrict SSH to admin IPs
- [ ] Non-root user created for app (`appuser`)
- [ ] Directory structure: `/app` with repo clone
- [ ] PostgreSQL (college) and SQLite (school) databases created with correct users & passwords
- [ ] Redis server installed/running (`systemctl status redis`)
- [ ] S3 bucket configured for backups with lifecycle rules

### 2. Deploy Application Pre-Release Image
```bash
# On production server
cd /app
git pull origin main
git checkout v0.9.1-perf-optimized  # or latest RC tag
cp .env.example .env
# Edit .env with production values (use editor or fetch from vault)
nano .env

# Build and start services
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker ps
docker logs backend -f  # watch for errors

# Run health checks
curl -f http://localhost:8000/health/live
curl -f http://localhost:8000/health/ready
```

Expected: both return `{"status": "alive"}` or `{"status": "ready"}`

### 3. Database Migration & Initialization
```bash
# School DB (SQLite)
alembic -c alembic.ini upgrade head

# College DB (PostgreSQL)
docker exec backend alembic -c alembic_college.ini upgrade head

# Verify all 23 college tables exist
docker exec backend python -c "from backup.models.college import *; print('All models imported')"

# Create super admin if not exists
docker exec backend python -m modules.auth.hashing create-superadmin
# Provide admin email/password; store securely
```

### 4. Backup Verification (Critical)
```bash
# Run backup script manually
docker exec backend python scripts/backup_databases.py

# Verify local backup files generated in /backups/{school,college}/
docker exec backend ls -lh /backups/

# Verify S3 upload
aws s3 ls s3://school-college-prod-backups/college/ | head

# OPTIONAL: Test restore on staging clone (do on staging, not prod!)
# Document restore procedure works end-to-end
```

If any backup step fails → **BLOCKER**; fix before proceeding

### 5. Monitoring & Alerting Check
- [ ] Prometheus metrics accessible (if running locally, check `curl http://localhost:8000/metrics`)
- [ ] Sentry DSN configured; send test event:
```python
docker exec backend python -c "import sentry_sdk; sentry_sdk.capture_message('Production readiness test')"
```
Check Sentry dashboard for event.
- [ ] Health check `/health/ready` returns 200
- [ ] Alert endpoints (if defined) respond

### 6. Security Final Sweep
- [ ] `docker exec backend bandit -r modules/ -f json -o /tmp/bandit-prod.json` (quick scan)
- [ ] Verify `.env` has no weak defaults:
  - `SECRET_KEY` length ≥32
  - Database passwords strong
  - Debug mode OFF (`DEBUG=false`)
- [ ] Verify `ALLOWED_ORIGINS` in env is not `*` (specific frontend URL)
- [ ] Ensure error detail suppressed in prod (`EXPOSE_ERROR_DETAIL=false`)

### 7. Smoke Test Production (1 hour)
**Use staging script but target production URLs**:

```bash
python scripts/smoke_test_staging.py --url=https://schoolcollege.example.com
```

**Test scenarios** (manual augment):
- [ ] Student signup + login + view dashboard
- [ ] Faculty login + create course + upload marks
- [ ] HOD login + view department analytics
- [ ] Dean login + download report
- [ ] Registrar login + fee summary
- [ ] Super admin login + create user + role assignment
- [ ] All should return 200 OK

If any fails → investigate immediately

---

## Afternoon: Launch Preparation (2 hours)

### 8. Launch Runbook Finalization
**Create `LAUNCH_RUNBOOK.md`**:

| Step | Command / Action | Expected | Rollback |
|------|------------------|----------|----------|
| 1. Pre-launch backup | `python scripts/backup_databases.py` | backup files in /backups & S3 | none |
| 2. Deploy new image | `docker-compose -f prod.yml pull && up -d` | containers running, logs show startup | `docker-compose down && up -d v0.7.0` |
| 3. Run migrations | `docker exec backend alembic upgrade head` | revision applied | `alembic downgrade -1` |
| 4. Health check | `curl /health/ready` → 200 | app ready | restart container |
| 5. Smoke test | `python scripts/smoke_test.py` → all pass | green | rollback if fail |
| 6. Notify users | email/slack announcement | sent | not needed |

**Timeline**:
- T-1 hour: Notify on-call team
- T-30 min: Final backup
- T-10 min: Deploy
- T=0: Launch
- T+5 min: smoke test
- T+15 min: notify users "system live"

### 9. Communication Plan
- [ ] Announcement email to all registered users (24h before):
  ```
  Subject: Scheduled Maintenance & System Upgrade – May 31, 2026
  We will be performing maintenance from 02:00-04:00 AM UTC.
  Expected downtime: <5 minutes.
  ```
- [ ] Slack/Discord #announcements channel post
- [ ] In-app banner (if possible) showing upgrade notice

### 10. On-Call Assignment
- [ ] Primary on-call: [Name] (phone, Slack)
- [ ] Secondary: [Name]
- [ ] Escalation: If not resolved in 15 min → page senior engineer

### 11. Post-Launch Monitoring Plan
**First 24 hours**:
- Hourly check: Sentry error count, Prometheus 5xx rate, response latency
- Daily backup verification (first backup after launch)
- Rotate logs: ensure logs not filling disk

**Week 1**:
- Daily review: error trends, slow queries, DB growth
- Check support tickets; triage bugs

---

## End of Day Deliverables
- ✅ Production environment validated
- ✅ Backup & restore verified (or documented exception)
- ✅ Smoke test all green
- ✅ Launch runbook complete (`LAUNCH_RUNBOOK.md`)
- ✅ Communication sent to users
- ✅ On-call assigned
- ✅ Final commit: `docs: Production launch preparation complete; add runbook`
- ✅ Tag `v1.0.0-rc.3` (final release candidate)

## Success Criteria
- Staging (mirroring prod) passes all smoke tests
- Production environment mirrors staging config (except scale)
- Backup script works; S3 upload verified
- Rollback procedure practiced and documented (<5 min)
- Team aware of launch sequence and responsibilities

## Go/No-Go Decision Gate
**If all items green → GO** for Day 30 launch window 02:00-04:00 AM UTC  
**If any red → STOP**; resolve blocker, reschedule launch

---

## Final Files to Commit
- `LAUNCH_RUNBOOK.md`
- `UAT_SIGN_OFF.md` (if obtained)
- Updated `DEPLOYMENT.md` with production specifics
- `scripts/smoke_test_staging.py` (if newly created)
- Any last-minute config fixes
