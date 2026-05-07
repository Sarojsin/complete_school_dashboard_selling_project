# Audit Logging System

## Overview

The audit logging system provides comprehensive tracking of all state-changing operations in the college management system. Every CREATE, UPDATE, and DELETE operation is automatically logged with full context for compliance, security, and debugging purposes.

## Architecture

### Components

1. **AuditLog Model**: Database table storing audit events
2. **AuditLogger Service**: Business logic for logging operations
3. **AuditLoggingMiddleware**: Automatic logging of API requests
4. **Manual Logging**: Explicit logging in service methods

### Database Schema

```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,  -- NULL for system operations
    action VARCHAR(50) NOT NULL,  -- CREATE, UPDATE, DELETE, etc.
    resource_type VARCHAR(100) NOT NULL,  -- e.g., "college_faculty"
    resource_id VARCHAR(100) NOT NULL,  -- String ID of the resource
    details JSON,  -- Old/new values, metadata
    ip_address VARCHAR(45),  -- IPv6 support
    user_agent TEXT,
    session_id VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Automatic Logging

### Middleware Configuration

The audit logging middleware is automatically applied to all API requests:

```python
# app/main.py
from modules.shared.middleware.audit_middleware import AuditLoggingMiddleware

app.add_middleware(AuditLoggingMiddleware)
```

### What Gets Logged

**State-Changing Operations:**
- `POST` requests (resource creation)
- `PUT/PATCH` requests (resource updates)
- `DELETE` requests (resource deletion)

**Excluded Paths:**
- `/docs`, `/redoc`, `/openapi.json`
- `/health`, `/metrics`, `/status`
- Static file endpoints

### Log Entry Structure

Each audit log entry contains:

```json
{
  "user_id": 123,
  "action": "UPDATE",
  "resource_type": "college_faculty",
  "resource_id": "456",
  "details": {
    "method": "PUT",
    "path": "/college/faculty/456",
    "query_params": {},
    "response_status": 200,
    "duration_seconds": 0.123,
    "old_values": {"name": "John Doe", "department": "CS"},
    "new_values": {"name": "Jane Doe", "department": "CS"},
    "changed_fields": ["name"]
  },
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "timestamp": "2026-05-06T17:30:00Z"
}
```

## Manual Logging

### Using AuditLogger Service

```python
from modules.shared.audit_logger import AuditLogger

async def create_faculty(self, data, current_user):
    # Create the faculty
    faculty = await self.repository.create(data)

    # Log the creation
    audit_logger = AuditLogger(self.db)
    await audit_logger.log_create(
        user_id=current_user.id,
        resource_type="college_faculty",
        resource_id=str(faculty.id),
        new_values=data.model_dump(),
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    return faculty
```

### Available Logging Methods

#### log_create()
```python
await audit_logger.log_create(
    user_id=user_id,
    resource_type="resource_type",
    resource_id="resource_id",
    new_values={"field": "value"},
    ip_address="192.168.1.1",
    user_agent="Browser/1.0"
)
```

#### log_update()
```python
await audit_logger.log_update(
    user_id=user_id,
    resource_type="resource_type",
    resource_id="resource_id",
    old_values={"field": "old_value"},
    new_values={"field": "new_value"},
    ip_address="192.168.1.1",
    user_agent="Browser/1.0"
)
```

#### log_delete()
```python
await audit_logger.log_delete(
    user_id=user_id,
    resource_type="resource_type",
    resource_id="resource_id",
    deleted_values={"field": "value"},
    ip_address="192.168.1.1",
    user_agent="Browser/1.0"
)
```

#### Special Events

```python
# User authentication
await audit_logger.log_login(user_id=user.id, ip_address=ip, user_agent=ua)
await audit_logger.log_logout(user_id=user.id)

# Failed authentication
await audit_logger.log_failed_login(
    username=username,
    ip_address=ip,
    reason="invalid_credentials"
)

# System events
await audit_logger.log_system_event(
    event_type="backup_completed",
    details={"size": "1.2GB", "duration": "45s"}
)
```

## Querying Audit Logs

### Basic Queries

```sql
-- All actions by a user
SELECT * FROM audit_logs
WHERE user_id = 123
ORDER BY timestamp DESC;

-- Actions on a specific resource
SELECT * FROM audit_logs
WHERE resource_type = 'college_faculty' AND resource_id = '456'
ORDER BY timestamp DESC;

-- Recent changes to student records
SELECT * FROM audit_logs
WHERE resource_type = 'college_students'
AND timestamp > '2026-05-01'
ORDER BY timestamp DESC;

-- Failed login attempts
SELECT * FROM audit_logs
WHERE action = 'FAILED_LOGIN'
AND timestamp > '2026-05-01'
ORDER BY timestamp DESC;
```

### Advanced Queries

```sql
-- Most active users this week
SELECT user_id, COUNT(*) as action_count
FROM audit_logs
WHERE timestamp >= date('now', '-7 days')
GROUP BY user_id
ORDER BY action_count DESC;

-- Resource changes by type
SELECT resource_type, COUNT(*) as change_count
FROM audit_logs
WHERE action IN ('CREATE', 'UPDATE', 'DELETE')
AND timestamp >= date('now', '-30 days')
GROUP BY resource_type
ORDER BY change_count DESC;

-- Suspicious activity (multiple failed logins)
SELECT resource_id as username, COUNT(*) as failed_attempts,
       MAX(timestamp) as last_attempt
FROM audit_logs
WHERE action = 'FAILED_LOGIN'
AND timestamp >= date('now', '-1 day')
GROUP BY resource_id
HAVING failed_attempts > 5;
```

### Using Python

```python
from sqlalchemy import select
from modules.shared.audit import AuditLog

# Get recent faculty changes
async def get_recent_faculty_changes(db, days=7):
    cutoff_date = datetime.now() - timedelta(days=days)

    query = select(AuditLog).where(
        AuditLog.resource_type == "college_faculty",
        AuditLog.timestamp >= cutoff_date
    ).order_by(AuditLog.timestamp.desc())

    result = await db.execute(query)
    return result.scalars().all()
```

## Retention Policy

### Default Retention
- **Audit logs retained for**: 2 years
- **Automated cleanup**: Monthly job
- **Archival**: Move to cold storage after 1 year

### Cleanup Script

```python
# scripts/cleanup_audit_logs.py
async def cleanup_old_audit_logs():
    cutoff_date = datetime.now() - timedelta(days=730)  # 2 years

    # Archive old logs to JSON files
    old_logs = await db.execute(
        select(AuditLog).where(AuditLog.timestamp < cutoff_date)
    )

    # Export to JSON for archival
    # Then delete from database

    await db.execute(
        delete(AuditLog).where(AuditLog.timestamp < cutoff_date)
    )
    await db.commit()
```

### Compliance Considerations
- **Legal requirements**: Retain logs as required by regulations
- **Business needs**: Keep logs for auditing and debugging
- **Storage costs**: Balance retention with storage efficiency

## Security & Privacy

### Data Protection
- Audit logs contain sensitive information
- Access restricted to administrators only
- Encryption at rest recommended
- Mask sensitive data in logs (passwords, tokens)

### Access Control
```python
# Only admins can view audit logs
@router.get("/audit/logs")
async def get_audit_logs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    if current_user.role not in ["admin", "auditor"]:
        raise HTTPException(403, "Access denied")

    # Return filtered audit logs
```

### Privacy Considerations
- **IP Address Logging**: May be subject to privacy regulations
- **User Agent**: Contains device/browser information
- **PII in Details**: Ensure sensitive data is not logged

## Monitoring & Alerts

### Log Analysis

```python
# scripts/audit_monitor.py
async def check_audit_anomalies():
    """Check for suspicious audit patterns"""

    # Unusual number of deletions
    delete_count = await db.execute(
        select(func.count(AuditLog.id)).where(
            AuditLog.action == "DELETE",
            AuditLog.timestamp >= datetime.now() - timedelta(hours=1)
        )
    )

    if delete_count.scalar() > 100:  # Threshold
        alert_admin("High deletion activity detected")

    # Failed login spikes
    failed_logins = await db.execute(
        select(func.count(AuditLog.id)).where(
            AuditLog.action == "FAILED_LOGIN",
            AuditLog.timestamp >= datetime.now() - timedelta(minutes=5)
        )
    )

    if failed_logins.scalar() > 20:  # Threshold
        alert_admin("Potential brute force attack")
```

### Dashboard Integration

```python
# API endpoint for audit dashboard
@router.get("/audit/dashboard")
async def get_audit_dashboard():
    # Recent activity
    recent_logs = await db.execute(
        select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50)
    )

    # Activity summary
    summary = await db.execute("""
        SELECT
            action,
            COUNT(*) as count,
            MAX(timestamp) as last_activity
        FROM audit_logs
        WHERE timestamp >= date('now', '-7 days')
        GROUP BY action
    """)

    return {
        "recent_activity": recent_logs.scalars().all(),
        "summary": summary.mappings().all()
    }
```

## Troubleshooting

### Missing Audit Logs

**Check middleware configuration:**
```python
# Ensure middleware is added to app
from modules.shared.middleware.audit_middleware import AuditLoggingMiddleware
app.add_middleware(AuditLoggingMiddleware)
```

**Verify database connectivity:**
```python
# Check if audit_logs table exists
result = await db.execute("SELECT COUNT(*) FROM audit_logs")
print(f"Audit logs count: {result.scalar()}")
```

### Performance Issues

**Audit logging overhead:**
- Middleware adds ~1-5ms per request
- Database writes are asynchronous
- Consider batching for high-traffic endpoints

**Optimization strategies:**
```python
# Batch audit logging for bulk operations
audit_entries = []
for item in bulk_items:
    audit_entries.append(AuditLog(...))

db.add_all(audit_entries)
await db.commit()
```

### Log Analysis Issues

**Large log tables:**
```sql
-- Create indexes for better query performance
CREATE INDEX idx_audit_logs_resource_type ON audit_logs(resource_type);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
```

**Slow queries:**
```sql
-- Use date ranges efficiently
SELECT * FROM audit_logs
WHERE timestamp >= '2026-01-01' AND timestamp < '2026-02-01'
AND resource_type = 'college_students';
```

## Integration Examples

### College Faculty Operations

```python
# modules/college/college_faculty/router.py
@router.post("/")
async def create_faculty(
    data: FacultyCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_college_async_db)
):
    # Create faculty
    service = CollegeFacultyService(db)
    result = await service.create_faculty(data)

    # Manual audit logging
    if result.get("faculty"):
        audit_logger = AuditLogger(db)
        await audit_logger.log_create(
            user_id=current_user.id,
            resource_type="college_faculty",
            resource_id=str(result["faculty"].id),
            new_values=data.model_dump(),
            ip_address=getattr(request.client, "host", None) if request.client else None,
            user_agent=request.headers.get("user-agent")
        )

    return result
```

### Enrollment Tracking

```python
# Automatic logging via middleware for:
# POST   /college/enrollments  → CREATE college_enrollment
# PUT    /college/enrollments/{id} → UPDATE college_enrollment
# DELETE /college/enrollments/{id} → DELETE college_enrollment
```

## Best Practices

### Logging Guidelines
1. **Log all state changes**: Every CREATE, UPDATE, DELETE
2. **Include context**: User, IP, timestamp, changed fields
3. **Avoid sensitive data**: Don't log passwords, tokens
4. **Use consistent resource types**: Follow naming conventions
5. **Monitor performance**: Ensure logging doesn't impact response times

### Maintenance
1. **Regular cleanup**: Implement retention policies
2. **Index optimization**: Maintain query performance
3. **Archive old logs**: Move to cheaper storage
4. **Monitor disk usage**: Plan for log growth

### Security
1. **Access control**: Restrict audit log access
2. **Data encryption**: Encrypt sensitive log data
3. **Integrity checks**: Ensure logs can't be tampered with
4. **Backup logs**: Include audit logs in backup strategy

## Compliance

### Regulatory Requirements
- **GDPR**: User data access logging
- **SOX**: Financial transaction auditing
- **HIPAA**: Health data access tracking (if applicable)
- **PCI DSS**: Payment data handling

### Audit Trail Requirements
- **Complete**: All actions tracked
- **Accurate**: Timestamps, user identification
- **Secure**: Tamper-evident logs
- **Accessible**: Easy querying and reporting

---

## Support

For audit logging issues:
1. Check middleware configuration in `app/main.py`
2. Verify `audit_logs` table exists and is accessible
3. Review application logs for audit-related errors
4. Test with a simple API call to confirm logging works
5. Contact development team with log excerpts and error details