# Day 22 Production Implementation Plan
**Date**: 2026-05-27
**Focus**: Audit Logging Completion & Admin Interface

## Objectives
- Verify 100% coverage of CRUD operations logged to audit table
- Create admin-only endpoint to query and filter audit logs
- Implement automatic purge of old audit logs (retention: 2 years)
- Integrate audit logs with monitoring dashboard (Sentry + Prometheus metrics)
- Optimize audit logging performance (async writes, batch insertion)

## Tasks

### 1. Audit Logging Coverage Audit (Morning - 1.5 hours)
**Goal**: Every CREATE, UPDATE, DELETE API endpoint must log via AuditLog

**Review all routers**:
- [ ] `modules/college/college_exam_section/router.py` – all POST/PATCH/DELETE call `log_action`
- [ ] `modules/college/college_account_section/router.py` – fee_structure create/update, payment create
- [ ] `modules/college/college_enrollments/router.py` – create/update/delete enrollment
- [ ] `modules/college/college_programs/router.py` – create/update/delete program
- [ ] `modules/college/college_semesters/router.py`
- [ ] `modules/college/college_hod/router.py` – profile update
- [ ] `modules/college/college_dean/router.py` – read-only? maybe no logs
- [ ] `modules/college/college_registrar/router.py` – read-only
- [ ] `modules/auth/router.py` – signup, password change, 2FA enable/disable
- [ ] `modules/school/*/router.py` – all write operations

**Method**:
- [ ] Grep for `@router.post` / `@router.patch` / `@router.delete` across all routers
- [ ] Verify each calls `await log_action(...)` before returning
- [ ] If missing, add at start of service method or in router after service returns

**Example missing logs**:
- College faculty appointments (if endpoint exists)
- Student profile updates
- Course updates by HOD

**Implement helper** (`modules/shared/audit/decorator.py`) to reduce boilerplate:
```python
from functools import wraps
from modules.shared.audit_logger import log_action

def audit_log(action: str, resource_type: str, get_resource_id: callable):
    """Decorator to automatically log action after endpoint completion"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_user), db=AsyncSession=Depends(get_db), **kwargs):
            result = await func(*args, current_user=current_user, db=db, **kwargs)
            resource_id = get_resource_id(result, *args, **kwargs)
            await log_action(db, current_user, action, resource_type, str(resource_id), {})
            return result
        return wrapper
    return decorator
```
- [ ] Apply decorator to new endpoints; retro-fit existing ones

### 2. Admin Audit Query Endpoint (1.5 hours)
**Create `modules/super_admin/router_audit.py`** or extend existing super_admin router:

```python
from modules.super_admin.dependencies import require_super_admin
from modules.shared.audit.models import AuditLog
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/admin/audit", tags=["audit"])

@router.get("/")
async def list_audit_logs(
    current_user=Depends(require_super_admin),
    db: AsyncSession=Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    user_id: int = None,
    action: str = None,
    resource_type: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
):
    """Query audit logs with filters (super admin only)"""
    query = select(AuditLog)
    
    if user_id:
        query = query.where(AuditLog.user_id == user_id)
    if action:
        query = query.where(AuditLog.action == action)
    if resource_type:
        query = query.where(AuditLog.resource_type == resource_type)
    if start_date:
        query = query.where(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.where(AuditLog.timestamp <= end_date)
    
    query = query.order_by(AuditLog.timestamp.desc()).offset((page-1)*limit).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()
    
    total = await db.scalar(select(func.count(AuditLog.id)))  # with filters applied
    
    return {
        "logs": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action.value,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "details": log.details,
                "ip_address": log.ip_address,
                "timestamp": log.timestamp.isoformat(),
            } for log in logs
        ],
        "page": page,
        "limit": limit,
        "total": total,
    }

@router.get("/summary")
async def audit_log_summary(
    current_user=Depends(require_super_admin),
    db: AsyncSession=Depends(get_db)
):
    """Summary stats: actions count, top users, recent activity"""
    last_24h = datetime.utcnow() - timedelta(hours=24)
    actions = await db.execute(
        select(AuditLog.action, func.count(AuditLog.id))
        .where(AuditLog.timestamp >= last_24h)
        .group_by(AuditLog.action)
    )
    return {
        "last_24h": { action: count for action, count in actions },
        "total_logs": await db.scalar(select(func.count(AuditLog.id))),
    }
```

### 3. Audit Log Retention & Auto-Purge (1 hour)
**Celery periodic task** (already partially defined Day 13):
- [ ] Update `cleanup_tasks.py`:
```python
from datetime import datetime, timedelta

@shared_task(name="audit.purge_old_logs")
async def purge_old_logs(retention_days: int = 730):  # 2 years
    """Hard delete audit logs older than retention period"""
    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    async with get_db() as db:
        # Batch delete in chunks to avoid locking
        deleted = 0
        while True:
            result = await db.execute(
                delete(AuditLog)
                .where(AuditLog.timestamp < cutoff)
                .returning(AuditLog.id)
                .limit(10000)  # delete in 10k chunks
            )
            batch_deleted = len(result.all())
            await db.commit()
            deleted += batch_deleted
            if batch_deleted < 10000:
                break
        logger.info("Purged audit logs", cutoff=cutoff.isoformat(), deleted_count=deleted)
        return {"deleted": deleted}
```

**Configure schedule** in `celery_app.py`:
```python
"audit-purge-monthly": {
    "task": "audit.purge_old_logs",
    "schedule": crontab(day_of_month=1, hour=2),  # 1st of month, 2 AM
    "args": (730,),
},
```

**Manual endpoint** (super admin):
```python
@router.post("/purge")
async def trigger_audit_purge(current_user=Depends(require_super_admin)):
    """Manually trigger audit log purge (rare, for compliance)"""
    task = purge_old_logs.delay(730)
    return {"task_id": task.id, "status": "queued"}
```

### 4. Audit Logging Performance Optimization (1 hour)
**Issue**: Synchronous log writes inside endpoint transaction can slow down responses.

**Options**:
1. **AsyncFire (existing)**: `log_action` is async but commits immediately within request; OK for low volume
2. **Better**: Queue audit log as Celery task for truly async (fire-and-forget)

**Refactor**:
```python
# In log_action after DB commit (or before returning response):
from modules.shared.tasks.email_tasks import send_email  # model for audit task
# Create separate task
@shared_task(name="audit.write_log")
async def write_audit_log_async(user_id: int, action: str, resource_type: str, resource_id: str, details: dict):
    async with get_db() as db:
        log = AuditLog(user_id=user_id, action=action, resource_type=resource_type, resource_id=resource_id, details=details, timestamp=datetime.utcnow())
        db.add(log)
        await db.commit()

# In endpoint: instead of await log_action(...), do:
log_action_task.delay(current_user.id, action.value, resource_type, resource_id, details)
```

**Decision**: For simplicity, keep synchronous for now (log within same DB transaction). If performance issue noted, switch to async task. Add metric to track log write latency.

### 5. Metrics & Monitoring Integration (30 min)
**Prometheus metrics**:
```python
from prometheus_client import Counter

AUDIT_LOG_COUNT = Counter('audit_logs_total', 'Total audit logs', ['action', 'resource_type'])
AUDIT_LOG_ERRORS = Counter('audit_log_errors_total', 'Audit logging errors')

# In log_action: increment metric after successful insert
AUDIT_LOG_COUNT.labels(action=action.value, resource_type=resource_type).inc()
```

**Sentry**: Already captures exceptions; ensure audit failures are logged but not raised

### 6. Documentation (30 min)
- [ ] `AUDIT_LOGGING.md`:
  - What is logged (all CRUD + login/logout)
  - How to query logs (admin endpoint + direct SQL)
  - Retention policy (2 years, then purge)
  - Schema of `audit_logs` table
- [ ] Update `SECURITY.md`: audit trail for compliance
- [ ] API docs: describe `/admin/audit/*` endpoints

### 7. Commit (30 min)
- [ ] Commit: "feat(audit): Complete audit coverage on all write endpoints, add admin query API, implement 2-year retention with periodic purge"

## Deliverables
- ✅ All CRUD operations logged (verified via grep + tests)
- ✅ Admin endpoints: `GET /api/v1/admin/audit`, `POST /purge`, `GET /summary`
- ✅ Celery task `audit.purge_old_logs` scheduled monthly
- ✅ Metrics: `audit_logs_total` counter
- ✅ Documentation: `AUDIT_LOGGING.md`

## Success Criteria
- Manual test: Create student → query audit log → shows CREATE action with user_id, timestamp
- Super admin can list/filter audit logs by action, user, date
- Monthly purge task runs; old logs deleted automatically
- No performance degradation from logging overhead (<5ms per request)

## Notes
- Keep audit logs for at least 2 years for security forensics; legal requirements may vary
- Consider indexed `timestamp` for fast range queries; already indexed as PK?
- Audit logs can become huge; partition by month in PostgreSQL (future)
- Ensure PII not logged in details (only IDs, not full payload with emails)

## Next: Day 23
User documentation: Create comprehensive user manuals for students, parents, teachers, and admins. FAQ section, video tutorial outlines, and in-app help system (if applicable).
