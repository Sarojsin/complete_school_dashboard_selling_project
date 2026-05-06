# Day 14 Production Implementation Plan
**Date**: 2026-05-19
**Focus**: Database Tuning, Offsite Backups & Consistency Checks

## Objectives
- Review and optimize database indexes based on actual query patterns
- Configure SQLAlchemy connection pool for production load
- Implement offsite backup upload (S3/cloud storage)
- Create database consistency/integrity check scripts
- Run performance benchmarks and log improvements
- Finalize Week 2 deliverables

## Tasks

### 1. Index Optimization Review (Morning - 2 hours)
**Analyze actual queries** from repository methods:
- [ ] Review all `select()` statements in college and school repositories
- [ ] Identify columns used in: WHERE, JOIN ON, ORDER BY, GROUP BY
- [ ] Cross-check with existing indexes (use `\d table_name` in psql)

**Verify current indexes** (`alembic/versions/20260508_add_indexes.py` already applied):
- [ ] Confirm indexes exist:
  ```sql
  \d college_enrollments  -- check ix_college_enrollments_student_id, etc.
  \d college_fee_records
  \d college_exam_notices
  ```
- [ ] If any missing, create new migration to add

**Add missing indexes** (if identified):
- [ ] Composite index: `college_enrollments (semester_id, program_id)` – common filter combo
- [ ] Composite index: `college_fee_records (student_id, status)` – outstanding fees query
- [ ] Index: `college_courses (code)` – search by course code
- [ ] Index: `college_faculty (department_id, designation)` – filtering by dept+designation
- [ ] Index: `school_attendance (date, class_section_id)` – daily attendance roll

**Create migration if needed**:
```bash
alembic -c alembic_college.ini revision --autogame -m "Add composite indexes for enrollments and fee_records"
```
Edit migration to add `op.create_index()` calls, then `alembic upgrade head`

### 2. Connection Pool Configuration (1 hour)
**SQLAlchemy engine settings** in `modules/college/database.py` and `modules/shared/database.py`:

**Current setup** likely uses defaults:
```python
engine = create_engine(DATABASE_URL, echo=False)
AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
```

**Production config**:
```python
from sqlalchemy.pool import QueuePool, NullPool

# College PostgreSQL
college_engine = create_async_engine(
    COLLEGE_DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,           # Number of connections kept open
    max_overflow=10,        # Additional connections beyond pool_size
    pool_pre_ping=True,     # Validate connection before using
    pool_recycle=3600,      # Recycle connections after 1 hour
    future=True,
)

# School SQLite (use NullPool as SQLite doesn't pool well)
school_engine = create_async_engine(
    SCHOOL_DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool,
    future=True,
)
```

**Add pool metrics monitoring**:
- [ ] Instrument pool stats in health check:
  ```python
  from sqlalchemy import inspect
  def get_pool_status():
      insp = inspect(college_engine)
      return {
          "pool_size": insp.pool.size(),
          "checked_in": insp.pool.checkedin(),
          "checked_out": insp.pool.checkedout(),
          "overflow": insp.pool.overflow(),
      }
  ```
- [ ] Expose via `/health/ready` or `/metrics`

**Test**:
- [ ] Simulate 50 concurrent requests; ensure no connection exhaustion
- [ ] Monitor logs for `QueuePool limit overflow` warnings

### 3. Offsite Backup Implementation (1.5 hours)
**Enhance backup script** (`scripts/backup_databases.py` from Day 4):

**Add S3 upload**:
- [ ] Install: `pip install boto3` (AWS S3) or `azure-storage-blob` (Azure)
- [ ] Add to `.env`:
  ```
  AWS_ACCESS_KEY_ID=...
  AWS_SECRET_ACCESS_KEY=...
  AWS_REGION=us-east-1
  S3_BUCKET=school-college-backups
  ```
- [ ] Modify backup script:
  ```python
  import boto3
  from botocore.exceptions import ClientError
  
  def upload_to_s3(local_path: str, bucket: str, key: str):
      s3 = boto3.client('s3')
      try:
          s3.upload_file(local_path, bucket, key)
          logger.info("Backup uploaded to S3", bucket=bucket, key=key)
      except ClientError as e:
          logger.error("S3 upload failed", error=str(e))
  ```

**After local backup**:
- [ ] Compress (gzip) backup file
- [ ] Upload to S3: `s3://bucket/backups/college/YYYY-MM-DD.dump.gz`
- [ ] Verify S3 object exists (head_object)

**Offsite retention**:
- [ ] Keep local: 7 days
- [ ] Keep S3: 30 days + weekly archive to Glacier (optional)
- [ ] Week 1+ monthly backups retained for 1 year

**Alternative: Azure Blob Storage**:
- [ ] Use `azure-storage-blob` if AWS not preferred
- [ ] Container: `backups`

### 4. Database Consistency Check Script (1 hour)
**Create `scripts/check_db_consistency.py`**:

**Integrity checks**:
- [ ] Foreign key orphans:
  ```sql
  -- Find enrollments with invalid student_id
  SELECT e.id FROM college_enrollments e
  LEFT JOIN college_students s ON e.student_id = s.id
  WHERE s.id IS NULL;
  
  -- Same for program_id, semester_id
  ```
- [ ] Duplicate emails:
  ```sql
  SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;
  ```
- [ ] Students without enrollments (stale):
  ```sql
  SELECT s.id FROM college_students s
  LEFT JOIN college_enrollments e ON s.id = e.student_id
  WHERE e.id IS NULL AND s.created_at < NOW() - INTERVAL '1 year';
  ```
- [ ] Soft-deleted records with active dependencies (shouldn't happen but check)

**Script**:
```python
#!/usr/bin/env python3
import asyncpg
import asyncio
from modules.shared.config import get_settings

async def check_consistency():
    settings = get_settings()
    # Connect to college DB
    conn = await asyncpg.connect(settings.COLLEGE_DATABASE_URL)
    
    checks = {
        "orphan_enrollments_student": "SELECT COUNT(*) FROM college_enrollments WHERE student_id NOT IN (SELECT id FROM college_students)",
        "orphan_enrollments_program": "SELECT COUNT(*) FROM college_enrollments WHERE program_id NOT IN (SELECT id FROM college_programs)",
        "duplicate_emails": "SELECT COUNT(*) FROM (SELECT email FROM users GROUP BY email HAVING COUNT(*) > 1) t",
        "students_without_enrollments": "SELECT COUNT(*) FROM college_students WHERE id NOT IN (SELECT DISTINCT student_id FROM college_enrollments) AND created_at < NOW() - INTERVAL '6 months'",
    }
    
    for name, query in checks.items():
        count = await conn.fetchval(query)
        if count > 0:
            logger.warning(f"Consistency check failed: {name}", count=count)
        else:
            logger.info(f"Consistency check passed: {name}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_consistency())
```

**Schedule**:
- [ ] Add to cron: `0 4 * * * /path/to/scripts/check_db_consistency.py`
- [ ] Email alert on failures (integrate with Celery email task)

### 5. Offsite Backup Upload & Retention (30 min)
**S3 lifecycle policy** (via AWS Console or script):
- [ ] Rule: Delete backups older than 30 days from S3 standard
- [ ] Rule: Transition backups > 7 days old to S3 Glacier (cheaper)
- [ ] Enable versioning for backup bucket (optional, prevents accidental deletion)

**Verify offsite backup**:
- [ ] Run backup script; check S3 console shows object
- [ ] `aws s3 ls s3://school-college-backups/college/ --recursive`
- [ ] Download a random backup; confirm file size matches

### 6. Documentation & Commit (1 hour)
- [ ] Update `BACKUP_RESTORE.md`:
  - Offsite backup locations (S3 bucket name)
  - Restore procedure from S3: download → decrypt → restore
  - Retention schedule table:
    | Location | Retention | Frequency |
    |----------|-----------|-----------|
    | Local   | 7 days   | Daily    |
    | S3 Standard | 30 days | Daily |
    | S3 Glacier | 1 year  | Monthly |
- [ ] Create `DATABASE_CONSISTENCY.md`:
  - What checks run
  - How to manually run
  - Alert thresholds
- [ ] Create `DATABASE_TUNING.md`:
  - Indexes added and rationale
  - Connection pool settings explanation
  - How to monitor pool usage
- [ ] Commit: "perf(db): Add composite indexes, configure connection pool, implement offsite S3 backups with lifecycle, add consistency checker"

## Deliverables
- ✅ Missing composite indexes added (if needed)
- ✅ Connection pool configured (pool_size 20, max_overflow 10, pool_pre_ping)
- ✅ Offsite backup upload to S3/Blob storage implemented
- ✅ S3 lifecycle policy configured (30 day deletion, Glacier archive)
- ✅ `scripts/check_db_consistency.py` and scheduled run
- ✅ Documentation: `DATABASE_TUNING.md`, `BACKUP_RESTORE.md` updated, `DATABASE_CONSISTENCY.md`

## Success Criteria
- `\d enrollment` shows index on (student_id, program_id) or similar composite
- Connection pool stats visible in health check JSON
- Backup file appears in S3 bucket after script runs
- Consistency check returns 0 warnings when run manually
- Offsite backups older than 30 days auto-deleted by S3 lifecycle

## Notes
- Monitor DB performance with `pg_stat_statements` extension (enable in PostgreSQL)
- Connection pool size depends on max concurrent requests; adjust based on load testing results
- Offsite backups critical for disaster recovery; test restore from S3 monthly
- Use `pgBadger` or `pg_stat_monitor` for slow query analysis if needed

## Next: Day 15
Week 2 review: audit progress against checklist, update production readiness score, create Week 3 plan (Advanced features: 2FA, UUID, Analytics, i18n, GDPR compliance, doc finalization).
