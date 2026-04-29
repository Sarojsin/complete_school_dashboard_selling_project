"""
Health Check Module

Provides health check endpoints for monitoring:
- /health - Overall system health
- /health/db - Database health
- /health/modules - Module import health
- /metrics - Live system metrics
"""

from fastapi import APIRouter
from sqlalchemy import text
import time
import psutil
import os
from collections import defaultdict

health_router = APIRouter()


@health_router.get("/health", tags=["Health"])
def health_check():
    """Overall system health. Returns 200 if all systems go."""
    checks = {}
    status = "healthy"

    # 1. Database check
    try:
        from modules.shared.database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        checks["database"] = "connected"
    except Exception as e:
        checks["database"] = f"error: {str(e)[:50]}"
        status = "degraded"

    # 2. Memory check
    mem = psutil.virtual_memory()
    mem_used_pct = mem.percent
    checks["memory"] = f"{mem_used_pct:.1f}% used"
    if mem_used_pct > 90:
        status = "degraded"

    # 3. Disk check
    try:
        disk = psutil.disk_usage("/")
        disk_used_pct = disk.percent
        checks["disk"] = f"{disk_used_pct:.1f}% used"
    except:
        checks["disk"] = "unknown"

    # 4. App uptime
    try:
        uptime_seconds = int(time.time() - psutil.Process(os.getpid()).create_time())
        checks["uptime_seconds"] = uptime_seconds
    except:
        checks["uptime_seconds"] = "unknown"

    return {
        "status": status,
        "checks": checks,
        "version": "2.0.0"
    }


@health_router.get("/health/db", tags=["Health"])
def db_health():
    """Detailed database health."""
    try:
        from modules.shared.database import SessionLocal
        db = SessionLocal()
        
        # Count records in key tables
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
        return {"status": "error", "detail": str(e)[:100]}


@health_router.get("/health/modules", tags=["Health"])
def modules_health():
    """Check all modules can be imported."""
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
        "modules.notices.api",
    ]
    
    import importlib
    for mod in modules_to_check:
        try:
            importlib.import_module(mod)
            results[mod] = "ok"
        except Exception as e:
            results[mod] = f"error: {str(e)[:30]}"

    failed = [k for k, v in results.items() if v.startswith("error")]
    return {
        "status": "ok" if not failed else "degraded",
        "total_modules": len(modules_to_check),
        "failed_count": len(failed),
        "failed_modules": failed[:5] if failed else [],
        "modules": results
    }


# Simple in-memory metrics (use Prometheus in production)
class MetricsCollector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.request_counts = defaultdict(int)
            cls._instance.error_counts = defaultdict(int)
            cls._instance.response_times = defaultdict(list)
            cls._instance.start_time = time.time()
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
            if times:
                summary[key] = {
                    "total_requests": self.request_counts[key],
                    "error_count": self.error_counts[key],
                    "avg_ms": round(statistics.mean(times), 2) if times else 0,
                    "p95_ms": round(sorted(times)[int(len(times) * 0.95) - 1], 2) if len(times) >= 2 else 0,
                }
        return summary


metrics = MetricsCollector()


@health_router.get("/metrics", tags=["Health"])
def get_metrics():
    """Live system metrics — request counts, error rates, response times."""
    uptime = int(time.time() - metrics.start_time)
    return {
        "uptime_seconds": uptime,
        "total_requests": sum(metrics.request_counts.values()),
        "total_errors": sum(metrics.error_counts.values()),
        "endpoints": metrics.get_summary()
    }


# Endpoint to manually record metrics (for use with middleware)
@health_router.post("/metrics/record", tags=["Health"])
def record_metric(path: str, method: str, status: int, duration_ms: float):
    """Record a metric (used by middleware)"""
    metrics.record_request(path, method, status, duration_ms)
    return {"recorded": True}
