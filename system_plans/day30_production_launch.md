# Day 30: Production Launch Day
**Date**: 2026-06-03
**Focus**: Zero-Downtime Deployment to Production & Post-Launch Validation

## Launch Timeline (02:00-04:00 AM UTC – Low Traffic Window)

### Pre-Launch (T-60 minutes: 01:00 AM)
**Commander**: [Assigned Lead]

1. **Final Pre-flight Checks**:
   - [ ] All on-call team members online (Slack #war-room)
   - [ ] Production monitoring dashboards open (Grafana/Sentry)
   - [ ] Backup just completed (00:30) – verify success in S3
   - [ ] No critical alerts pending (Sentry, uptime)
   - [ ] Rollback image tagged and ready: `v0.9.1-perf-optimized` (current) and `v0.7.0-week3-advanced` (fallback)
   - [ ] Database maintenance window announced (if required)

2. **Create Maintenance Mode Banner** (optional):
   - Enable "maintenance mode" flag in frontend (display banner "Upgrading...")
   - Or configure Nginx to return 503 for non-API routes

3. **Final DB Backup**:
   ```bash
   # Run full backup
   docker exec backend python scripts/backup_databases.py
   # Verify backup exists
   aws s3 ls s3://school-college-prod-backups/college/ | head -1
   ```

---

### Deployment Window (T-10 minutes to T+0)

#### Step 1: Stop Accepting New Traffic (T-5 min)
```bash
# Option A: Nginx maintenance page
sudo nginx -s reload  # reload config with "return 503" for all routes

# Option B: Drain connections (if load balancer)
# Mark instance unhealthy in LB
```

#### Step 2: Pull New Image (T-0)
```bash
cd /app
git fetch --all --tags
git checkout v0.9.1-perf-optimized  # or main if tags used

docker-compose -f docker-compose.prod.yml pull
# Verify image downloaded: docker images school-college-backend
```

#### Step 3: Graceful Shutdown of Old Containers
```bash
# Stop old containers but allow in-flight requests to finish (Docker Compose does this)
docker-compose -f docker-compose.prod.yml down

# Ensure no old containers remain: docker ps -a
```

#### Step 4: Start New Containers
```bash
docker-compose -f docker-compose.prod.yml up -d
# Check logs
docker logs backend -f
# Wait for "Uvicorn running on http://0.0.0.0:8000"
```

Expected startup time: 30-60 seconds

#### Step 5: Run Database Migrations (if any new)
```bash
# If `alembic/versions/` changed since last tag:
docker exec backend alembic -c alembic.ini upgrade head
docker exec backend alembic -c alembic_college.ini upgrade head

# Should output: "Running upgrade ... -> <revision>"
```

#### Step 6: Health Check Verification (T+2 min)
```bash
# Local check
curl -f http://localhost:8000/health/live
curl -f http://localhost:8000/health/ready

# External check (if DNS already points)
curl -f https://schoolcollege.example.com/health/ready
```
Both must return HTTP 200.

#### Step 7: Smoke Test (T+3 min)
```bash
python scripts/smoke_test_staging.py --url=https://schoolcollege.example.com
```
All tests must PASS.

- **If PASS**: proceed to Step 8.
- **If FAIL**: immediately execute rollback (see below), investigate.

#### Step 8: Re-enable Traffic (T+4 min)
```bash
# Remove maintenance mode from Nginx
sudo nginx -s reload
# Or re-enable LB health checks, mark instance healthy
```

#### Step 9: Notify Users (T+5 min)
- Send email: "Maintenance complete – system back online"
- Post to Slack/Discord: ✅ Deployed v0.9.1; all systems operational

---

### Rollback Procedure (if smoke test fails)

**Trigger**: Any smoke test failure OR health check fails OR error rate spiking

1. **Immediate rollback (<2 min)**:
```bash
# Switch to previous known-good tag
git checkout v0.7.0-week3-advanced
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Verify old version health
curl -f http://localhost:8000/health/ready
```

2. **If DB migration caused issue**:
```bash
# Downgrade last migration
docker exec backend alembic -c alembic_college.ini downgrade -1
```

3. **Alert team**: "Rollback executed; investigating" – start post-mortem

Rollback target: restore service within 5 minutes of decision

---

## Post-Launch Monitoring (T+15 min to T+24h)

### 15-Minute Checks
- [ ] Sentry: error count trend (should be near zero)
- [ ] Prometheus: 5xx rate <0.1%, latency p95 <500ms
- [ ] DB connections: pool usage <80%
- [ ] Redis memory: <70% used
- [ ] Backup job: next scheduled at 02:30 (verify runs)

### 1-Hour Checks
- [ ] Application logs: no ERROR or CRITICAL lines
- [ ] Nginx access log: 4xx/5xx proportions normal
- [ ] Disk space: `/var/lib/docker` not full
- [ ] SSL certificate validity: `openssl x509 -in /etc/letsencrypt/live/.../fullchain.pem -noout -dates`

### 4-Hour Checks
- [ ] Active user sessions count (via `/metrics` or DB)
- [ ] Fee collection transactions (if any)
- [ ] Email queue processing (Celery beat tasks running)

### 24-Hour Review
- [ ] Total requests, error count, uptime % (should be 99.9%+)
- [ ] Database growth: check table sizes
- [ ] Backup succeeded (daily at 02:00)
- [ ] User feedback: support tickets volume

---

## Communication & Documentation

### Launch Announcement (Post-Launch, T+10 min)
**Slack/Email**:
```
✅ PRODUCTION LAUNCH COMPLETE

The School/College Management System is now live at:
https://schoolcollege.example.com

Status: All systems operational
Deployed version: v0.9.1-perf-optimized
Deployment time: 02:05 AM UTC (5 min downtime)

Monitoring links:
- Prometheus: http://monitor.example.com:9090
- Sentry: https://sentry.io/.../issues

On-call: @engineer-name (primary), @secondary (backup)
```

### Post-Mortem Preparation (Day 31)
- [ ] Document any incidents during launch (none ideally)
- [ ] Collect metrics: uptime, response times, error rates
- [ ] Team retrospective meeting scheduled

---

## Final Deliverables (End of Day)
- ✅ Production deployed and serving live traffic
- ✅ Smoke test passed in production
- ✅ Monitoring dashboards green
- ✅ On-call team aware and monitoring
- ✅ Launch announcement sent
- ✅ Runbook followed and updated with any discrepancies
- ✅ Git tag `v1.0.0` created (once stable)
- ✅ Celebration! 🎉

---

## If Launch Postponed
- Document reason clearly
- Create action plan for resolution
- Reschedule launch window (next low-traffic period)
- Communicate transparently to stakeholders

---

**Launch is a team effort. Stay calm, follow the runbook, communicate clearly.**
