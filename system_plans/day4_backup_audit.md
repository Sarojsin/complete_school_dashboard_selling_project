# Day 4 Production Implementation Plan
**Date**: 2026-05-09
**Focus**: Database Backup, Recovery & Audit Logging

## Objectives
- Implement automated backup system for both school (SQLite) and college (PostgreSQL) databases
- Create tested restore procedure with documented runbook
- Add audit logging for all state-changing operations (CREATE/UPDATE/DELETE)
- Ensure backups are compressed, rotated, and verifiable

## Tasks

### 1. Backup Script Development (Morning - 3 hours)
**Create `scripts/backup_databases.py`**:

**Features**:
- [ ] Detect database type from `.env` (`DATABASE_MODE=separate` or `unified`)
- [ ] For PostgreSQL (college):
  - `pg_dump` with `--format=custom` for compression
  - Include `--clean` flag for restorable dumps
  - Save to `backups/college/` with timestamp: `college_20260509_1600.dump`
- [ ] For SQLite (school):
  - Copy `.db` file to `backups/school/` with timestamp
  - Use `sqlite3` `.backup` command for consistency
- [ ] Compress backups with gzip (or use pg_dump's custom format)
- [ ] Log backup start/end times, file sizes to `backups/backup_log.csv`
- [ ] Return exit code 0 on success, non-zero on failure

**Configuration**:
- [ ] Add to `.env`:
  ```
  BACKUP_RETENTION_DAYS=30
  BACKUP_S3_BUCKET=  # optional for offsite
  ```
- [ ] Create `backups/` directory with subdirs: `college/`, `school/`, `logs/`

**Testing**:
- [ ] Run script manually: `python scripts/backup_databases.py`
- [ ] Verify backup files created
- [ ] Check logs written correctly

### 2. Restore Script Development (1.5 hours)
**Create `scripts/restore_databases.py`**:

**Features**:
- [ ] Accept command-line args: `--type college|school`, `--file <backup_file>`
- [ ] For college: `pg_restore --clean --no-owner --dbname $DATABASE_URL`
- [ ] For school: replace `.db` file (stop app first, copy, restart)
- [ ] Confirm with user before destructive restore (Y/N prompt)
- [ ] Log restore operation to `backups/restore_log.csv`
- [ ] Option: `--verify` to check backup integrity without restoring

**Testing** (use test databases):
- [ ] Create test backup, then restore to `college_sell_test` DB
- [ ] Verify tables exist and row counts match
- [ ] Document procedure in `BACKUP_RESTORE.md`

### 3. Automated Retention & Scheduling (1 hour)
**Retention cleanup script**:
- [ ] Add `--prune` flag to `backup_databases.py`:
  - Delete backups older than `BACKUP_RETENTION_DAYS` (default 30)
  - Keep at least 1 backup per week for 6 months (optional advanced)
- [ ] Run cleanup after each backup

**Cron job setup** (document in README):
- [ ] Create `scripts/schedule_backups.sh` (Linux/Mac) and `.bat` (Windows)
- [ ] Instructions: `crontab -e` → `0 2 * * * /path/to/backup_databases.py`
- [ ] For Windows: Task Scheduler instructions

### 4. Audit Logging Infrastructure (2 hours)
**Create `modules/shared/audit.py`**:
- [ ] Define `AuditLog` model (if not exists in backup):
  - id (UUID or int)
  - user_id (FK to users)
  - action (enum: CREATE, UPDATE, DELETE, LOGIN, LOGOUT)
  - resource_type (e.g., "college_faculty", "college_fee_record")
  - resource_id (string)
  - details (JSON, old/new values)
  - ip_address, user_agent
  - timestamp
- [ ] If model doesn't exist in backup, add to backup.models.shared or create migration
- [ ] Create `modules/shared/audit_logger.py`:
  ```python
  async def log_action(db: AsyncSession, user: User, action: str, resource_type: str, resource_id: str, details: dict = None):
      log = AuditLog(...)
      db.add(log)
      await db.commit()
  ```

**Middleware for Automatic Logging**:
- [ ] Create `modules/shared/middleware/audit_middleware.py`:
  - Intercept all PATCH, POST, DELETE requests
  - Extract `current_user` from request state
  - Log request path, method, body, response status
  - Exclude health check endpoints, static files
- [ ] Add middleware to `app/main.py`:
  ```python
  from modules.shared.middleware.audit_middleware import AuditLoggingMiddleware
  app.add_middleware(AuditLoggingMiddleware)
  ```

**Manual Logging in Endpoints**:
- [ ] Update college router endpoints (PATCH/DELETE/POST):
  ```python
  from modules.shared.audit_logger import log_action
  ...
  result = await service.update(...)
  await log_action(db, current_user, "UPDATE", "college_faculty", str(faculty_id), {"changed_fields": ...})
  ```

### 5. Test Backup & Restore (1 hour)
- [ ] Write backup verification test `tests/test_backup.py`:
  - `test_backup_creates_file()` – asserts file exists, size > 0
  - `test_backup_logs_entry()` – checks CSV log
- [ ] Write restore verification test (against test DB):
  - `test_restore_to_test_db()` – backup → drop → restore → verify data
- [ ] Run both tests; ensure pass

### 6. Test Audit Logging (1 hour)
- [ ] Write `tests/test_audit_logging.py`:
  - `test_audit_log_created_on_post()` – call exam_notice create, assert AuditLog entry
  - `test_audit_log_contains_user_id()` – user_id matches current_user
  - `test_audit_log_on_delete()` – resource marked DELETED, details has reason
- [ ] Run: `pytest tests/test_audit_logging.py -v`

### 7. Documentation (1 hour)
- [ ] Create `BACKUP_RESTORE.md`:
  - How to run manual backup
  - How to restore (step-by-step)
  - Retention policy (30 days daily, 6 months weekly)
  - Offsite upload instructions (S3/Azure Blob if applicable)
- [ ] Create `AUDIT_LOGGING.md`:
  - What is logged
  - How to query audit logs (SQL example)
  - Retention policy for audit logs (e.g., keep 2 years)
- [ ] Update `README.md` with backup schedule note

## Deliverables
- ✅ `scripts/backup_databases.py` – automated daily backup
- ✅ `scripts/restore_databases.py` – verified restore procedure
- ✅ `backups/` directory structure with sample backup
- ✅ `modules/shared/audit.py` + `audit_logger.py` + middleware
- ✅ Alembic migration (if needed) for audit_logs table
- ✅ Tests: `test_backup.py`, `test_audit_logging.py`
- ✅ Documentation: `BACKUP_RESTORE.md`, `AUDIT_LOGGING.md`

## Success Criteria
- Backup script runs successfully end-to-end
- Restore from backup recreates database exactly (data integrity verified)
- Audit log entry created for every POST/PATCH/DETETE request (excluding excluded paths)
- Backup retention cleanup removes files older than 30 days

## Notes
- Ensure backup files are NOT committed to git (`.gitignore` covers `backups/`)
- For PostgreSQL, ensure `pg_dump` and `pg_restore` are in PATH (install PostgreSQL client tools)
- Audit logging middleware should be async and not significantly impact response time
- Consider batching audit log writes (background task) if performance impact noted

## Next: Day 5
Monitoring & Observability setup: Prometheus metrics endpoint, structured logging with JSON, error tracking with Sentry, and health check enhancements.
