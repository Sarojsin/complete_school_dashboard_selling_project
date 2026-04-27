# 🔭 ELITE PLAN 12 — Monitoring & Observability
## Phase: PRODUCTION HEALTH — Health checks, Error tracking, Metrics, Alerts
### Goal: Know instantly when something breaks, where, and why

---

## 📌 Pre-Conditions
- [ ] ✅ All plans complete and app running in production
- [ ] ✅ `app/main.py` using full modular router setup
- [ ] ✅ Alembic migrations applied and DB stable

---

## 🎯 The 4 Pillars of Observability

```
1. Health Checks    → "Is the system alive?"
2. Logging          → "What happened?"
3. Metrics          → "How is it performing?"
4. Alerting         → "Tell me when something breaks"
```

---

## ✅ STEP 1 — Health Check Endpoints

Add a `/health` route that checks all critical subsystems:

**File: `modules/shared/health.py`**
```python
# modules/shared/health.py
from fastapi import APIRouter
from sqlalchemy import text
from modules.shared.database import SessionLocal
import time, psutil, os

health_router = APIRouter()

@health_router.get("/health", tags=["🔭 Health"])
def health_check():
    """Overall system health. Returns 200 if all systems go."""
    checks = {}
    status = "healthy"

    # 1. Database check
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        checks["database"] = "✅ connected"
    except Exception as e:
        checks["database"] = f"❌ error: {str(e)}"
        status = "degraded"

    # 2. Memory check
    mem = psutil.virtual_memory()
    mem_used_pct = mem.percent
    checks["memory"] = f"{'✅' if mem_used_pct < 80 else '⚠️'} {mem_used_pct:.1f}% used"
    if mem_used_pct > 90:
        status = "degraded"

    # 3. Disk check
    disk = psutil.disk_usage("/")
    disk_used_pct = disk.percent
    checks["disk"] = f"{'✅' if disk_used_pct < 85 else '⚠️'} {disk_used_pct:.1f}% used"

    # 4. App uptime
    checks["uptime_seconds"] = int(time.time() - psutil.Process(os.getpid()).create_time())

    return {
        "status": status,
        "checks": checks,
        "version": "2.0.0"
    }

@health_router.get("/health/db", tags=["🔭 Health"])
def db_health():
    """Detailed database health."""
    try:
        db = SessionLocal()
        # Count records in key tables
        from sqlalchemy import text
        tables = ["users", "teachers", "students", "exams"]
        counts = {}
        for t in tables:
            try:
                count = db.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
                counts[t] = count
            except:
                counts[t] = "error"
        db.close()
        return {"status": "connected", "table_counts": counts}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@health_router.get("/health/modules", tags=["🔭 Health"])
def modules_health():
    """Check all 32 modules can be imported."""
    results = {}
    modules_to_check = [
        "modules.auth.api",
        "modules.super_admin.api",
        "modules.school_authority.api",
        "modules.school_teacher.api",
        "modules.school_student.api",
        "modules.school_parent.api",
        "modules.school_exam_section.api",
        "modules.school_account_section.api",
        "modules.school_library.api",
        "modules.school_attendance.api",
        "modules.college_faculty.api",
        "modules.college_student.api",
        "modules.college_hod.api",
        "modules.chat.api",
        "modules.groups.api",
        "modules.assignments.api",
        "modules.grades.api",
        "modules.notices.api",
    ]
    import importlib
    for mod in modules_to_check:
        try:
            importlib.import_module(mod)
            results[mod] = "✅"
        except Exception as e:
            results[mod] = f"❌ {str(e)}"

    failed = [k for k, v in results.items() if v.startswith("❌")]
    return {
        "status": "ok" if not failed else "degraded",
        "failed_count": len(failed),
        "modules": results
    }
```

**Wire into `app/main.py`:**
```python
from modules.shared.health import health_router
app.include_router(health_router)
```

**Test:**
```powershell
curl http://localhost:8000/health
curl http://localhost:8000/health/db
curl http://localhost:8000/health/modules
```

---

## ✅ STEP 2 — Structured Logging

Replace scattered `print()` calls with structured JSON logs:

**File: `modules/shared/logger.py`**
```python
# modules/shared/logger.py
import logging
import json
import sys
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
```

**Usage in any module:**
```python
# modules/school_teacher/service.py
from modules.shared.logger import get_logger
logger = get_logger("school_teacher")

class TeacherService:
    def create_teacher(self, data, admin_id):
        logger.info(f"Creating teacher: {data.name} by admin {admin_id}")
        try:
            result = self.repo.create(data)
            logger.info(f"Teacher created: id={result.id}")
            return result
        except Exception as e:
            logger.error(f"Failed to create teacher: {e}")
            raise
```

---

## ✅ STEP 3 — Request Logging Middleware

Log every incoming request automatically:

**File: `app/middleware/request_logger.py`**
```python
# app/middleware/request_logger.py
import time
from fastapi import Request
from modules.shared.logger import get_logger

logger = get_logger("http")

async def request_logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    logger.info(json.dumps({
        "method": request.method,
        "path": str(request.url.path),
        "status": response.status_code,
        "duration_ms": round(duration_ms, 2),
        "client_ip": request.client.host if request.client else "unknown"
    }))

    # Add response time header
    response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
    return response
```

**Wire into `app/main.py`:**
```python
from app.middleware.request_logger import request_logging_middleware
app.middleware("http")(request_logging_middleware)
```

---

## ✅ STEP 4 — Error Tracking (Sentry Integration)

```powershell
pip install sentry-sdk[fastapi]
```

**In `app/main.py`:**
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from modules.shared.config import settings

if settings.SENTRY_DSN:  # Only if DSN is configured
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,  # 10% of requests
        environment=settings.ENVIRONMENT,  # "production" or "development"
        release="2.0.0",
    )
```

**In `.env`:**
```env
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
ENVIRONMENT=production
```

Sentry will automatically capture:
- All unhandled exceptions
- Slow requests (> 1 second)
- DB query performance

---

## ✅ STEP 5 — Metrics Collection

**File: `modules/shared/metrics.py`**
```python
# modules/shared/metrics.py
# Simple in-memory metrics (use Prometheus in production)
from collections import defaultdict
import time

class MetricsCollector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.request_counts   = defaultdict(int)
            cls._instance.error_counts     = defaultdict(int)
            cls._instance.response_times   = defaultdict(list)
            cls._instance.start_time       = time.time()
        return cls._instance

    def record_request(self, path: str, method: str, status: int, duration_ms: float):
        key = f"{method}:{path}"
        self.request_counts[key] += 1
        self.response_times[key].append(duration_ms)
        if status >= 500:
            self.error_counts[key] += 1

    def get_summary(self):
        import statistics
        summary = {}
        for key, times in self.response_times.items():
            summary[key] = {
                "total_requests": self.request_counts[key],
                "error_count": self.error_counts[key],
                "avg_ms": round(statistics.mean(times), 2) if times else 0,
                "p95_ms": round(sorted(times)[int(len(times)*0.95)-1], 2) if len(times) >= 2 else 0,
            }
        return summary

metrics = MetricsCollector()
```

**Metrics endpoint:**
```python
# In modules/shared/health.py — add:
from modules.shared.metrics import metrics

@health_router.get("/metrics", tags=["🔭 Health"])
def get_metrics():
    """Live system metrics — request counts, error rates, response times."""
    uptime = int(time.time() - metrics.start_time)
    return {
        "uptime_seconds": uptime,
        "endpoints": metrics.get_summary()
    }
```

---

## ✅ STEP 6 — Alerting Rules

Define when to raise alerts. Document these in `.env` or a config file:

```env
# Alerting thresholds (configure in modules/shared/config.py)
ALERT_P95_THRESHOLD_MS=500       # Alert if p95 > 500ms
ALERT_ERROR_RATE_THRESHOLD=0.05  # Alert if error rate > 5%
ALERT_MEMORY_THRESHOLD=85        # Alert if memory > 85%
ALERT_DISK_THRESHOLD=90          # Alert if disk > 90%
```

**Simple alert check script:**
```python
# scripts/check_alerts.py
"""Run periodically (e.g., cron every 5 minutes) to check thresholds."""
import httpx

r = httpx.get("http://localhost:8000/health")
data = r.json()

if data["status"] != "healthy":
    print(f"🚨 ALERT: System health = {data['status']}")
    print(f"   Details: {data['checks']}")
    # In production: send email, Slack message, or SMS here
else:
    print("✅ System healthy")
```

---

## ✅ STEP 7 — Module-Level Error Handling

Each module should have structured exception handling:

**Example for `modules/school_teacher/api.py`:**
```python
from fastapi import HTTPException
from modules.shared.logger import get_logger
from sqlalchemy.exc import IntegrityError

logger = get_logger("school_teacher.api")

@router.post("/teachers/")
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    try:
        return TeacherService(db).create_teacher(data)
    except IntegrityError:
        logger.warning(f"Duplicate teacher email: {data.email}")
        raise HTTPException(status_code=409, detail="Teacher with this email already exists")
    except Exception as e:
        logger.error(f"Unexpected error creating teacher: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 📊 Phase 12 Completion Checklist

### Health Checks
- [ ] `GET /health` returns 200 with all checks passing
- [ ] `GET /health/db` shows correct table counts
- [ ] `GET /health/modules` shows all 32 modules as ✅
- [ ] Health endpoints excluded from auth requirement

### Logging
- [ ] `modules/shared/logger.py` created
- [ ] At least 3 modules use `get_logger()` instead of `print()`
- [ ] Request logging middleware active — every request logged to stdout
- [ ] `X-Response-Time` header appears in all responses

### Error Tracking
- [ ] Sentry DSN configured in `.env` (or alternative chosen)
- [ ] Test error triggered and visible in Sentry dashboard

### Metrics
- [ ] `GET /metrics` shows live request counts and response times
- [ ] N+1 queries resolved (from Plan 10 benchmarks)

### Alerting
- [ ] `scripts/check_alerts.py` runs clean against live app
- [ ] Memory and disk usage within acceptable thresholds

---

## 🏆 COMPLETE — All 12 Plans Done

```
Plan 1  → Foundation & Safety            ✅ Zero risk foundation
Plan 2  → Simple School Modules          ✅ 6 core school modules
Plan 3  → Complex School Modules         ✅ exam + account (merged)
Plan 4  → College Modules                ✅ 12 college modules
Plan 5  → Cutover & Cleanup              ✅ Switch v2→v1, test, archive
Plan 6  → Auth Module                    ✅ JWT, roles, dependencies
Plan 7  → Super Admin Module             ✅ Full system control
Plan 8  → Shared Features                ✅ chat, groups, grades, etc.
Plan 9  → DB Migration + Rollback        ✅ Alembic, data safety, rollback
Plan 10 → Performance Benchmarking       ✅ Before/after, load test, N+1
Plan 11 → Documentation                  ✅ README, API docs, changelog
Plan 12 → Monitoring & Observability     ✅ Health, logging, metrics, alerts
```
