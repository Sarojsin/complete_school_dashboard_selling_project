# Day 13 Production Implementation Plan
**Date**: 2026-05-18
**Focus**: Background Task Processing with Celery

## Objectives
- Implement asynchronous task queue for long-running operations
- Setup Celery with Redis as message broker
- Configure periodic tasks (beat schedule) for maintenance jobs
- Implement specific use cases: bulk email, report generation, data export, cleanup jobs
- Monitor task status and failures

## Tasks

### 1. Install & Configure Celery (Morning - 2 hours)
**Install dependencies**:
- [ ] `pip install celery[redis]`
- [ ] Already have Redis from Day 12

**Create Celery app** (`modules/shared/celery_app.py`):
```python
from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "school_college_backend",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "modules.shared.tasks.cleanup_tasks",
        "modules.shared.tasks.email_tasks",
        "modules.shared.tasks.report_tasks",
        "modules.shared.tasks.backup_tasks",
    ]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes max
    task_soft_time_limit=29 * 60,  # soft limit 29 min
    worker_prefetch_multiplier=1,  # one task at a time per worker
    task_acks_late=True,  # acknowledge after completion
    worker_max_tasks_per_child=1000,  # prevent memory leaks
)

# Auto-discover tasks
celery_app.autodiscover_tasks(["modules.shared.tasks"])
```

**Create `modules/shared/tasks/__init__.py`**:
```python
from . import cleanup_tasks, email_tasks, report_tasks, backup_tasks
```

### 2. Define Cleanup Tasks (1 hour)
**File**: `modules/shared/tasks/cleanup_tasks.py`

```python
from celery import shared_task
from modules.shared.database import get_db
from modules.college.college_exam_sections.repository import CollegeExamNoticeRepository
from modules.school.school_chat.repository import ChatMessageRepository
import datetime

@shared_task(name="cleanup.expired_exam_notices")
async def cleanup_expired_exam_notices():
    """Soft delete or remove exam notices older than 1 year"""
    async with get_db() as db:
        repo = CollegeExamNoticeRepository()
        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=365)
        # Soft delete old notices
        await repo.soft_delete_older_than(db, cutoff_date)
    logger.info("Expired exam notices cleanup completed", cutoff=cutoff_date.isoformat())

@shared_task(name="cleanup.old_chat_messages")
async def cleanup_old_chat_messages(days_to_keep: int = 30):
    """Purge chat messages older than retention period"""
    async with get_db() as db:
        repo = ChatMessageRepository()
        cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days_to_keep)
        count = await repo.delete_older_than(db, cutoff)
    logger.info("Chat message cleanup completed", deleted_count=count, days=days_to_keep)

@shared_task(name="cleanup.temp_files")
def cleanup_temp_files():
    """Remove files from /tmp older than 1 day"""
    import os
    import glob
    from datetime import datetime, timedelta
    
    temp_dirs = ["/tmp/uploads", "/tmp/exports"]
    cutoff = datetime.now() - timedelta(days=1)
    
    deleted = 0
    for dir_path in temp_dirs:
        for file_path in glob.glob(os.path.join(dir_path, "*")):
            if os.path.isfile(file_path):
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff:
                    os.remove(file_path)
                    deleted += 1
    
    logger.info("Temp file cleanup completed", files_deleted=deleted)
```

### 3. Define Email Tasks (1 hour)
**File**: `modules/shared/tasks/email_tasks.py`

```python
from celery import shared_task
from modules.shared.email import send_email  # existing email utility
from modules.college.college_faculty.repository import CollegeFacultyRepository

@shared_task(name="email.send_welcome_email")
async def send_welcome_email(user_email: str, user_name: str, password: str = None):
    """Send welcome email to new user"""
    subject = "Welcome to School/College Management System"
    body = f"""
    Dear {user_name},
    
    Your account has been created successfully.
    {f'Your temporary password is: {password}' if password else ''}
    
    Please login at: http://localhost:3000/login
    
    Regards,
    Administration
    """
    await send_email(to=user_email, subject=subject, body=body)
    logger.info("Welcome email sent", email=user_email)

@shared_task(name="email.send_fee_receipt")
async def send_fee_receipt_email(student_email: str, receipt_data: dict):
    """Send fee payment receipt"""
    subject = "Fee Payment Receipt"
    body = f"Payment of ₹{receipt_data['amount']} received. Receipt No: {receipt_data['receipt_no']}"
    await send_email(to=student_email, subject=subject, body=body)
    logger.info("Fee receipt email sent", receipt_no=receipt_data.get("receipt_no"))

@shared_task(name="email.send_bulk_announcement")
async def send_bulk_announcement(recipient_emails: list, subject: str, body: str):
    """Send announcement to multiple recipients (rate-limited)"""
    for email in recipient_emails:
        await send_email(to=email, subject=subject, body=body)
        # Small delay to avoid rate limits
        await asyncio.sleep(0.1)
    logger.info("Bulk email sent", recipient_count=len(recipient_emails))
```

### 4. Define Report Generation Tasks (1.5 hours)
**File**: `modules/shared/tasks/report_tasks.py`

```python
import csv
import io
import pandas as pd
from celery import shared_task
from modules.college.college_dean.service import CollegeDeanService
from modules.college.college_registrar.service import CollegeRegistrarService

@shared_task(name="report.generate_enrollment_report")
async def generate_enrollment_report(semester_id: int, format: str = "csv"):
    """Generate enrollment report for a semester (CSV or Excel)"""
    dean_service = CollegeDeanService()
    async with get_db() as db:
        data = await dean_service.get_enrollment_report_data(db, semester_id)
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["student_id", "name", "program", "enrollment_date"])
        writer.writeheader()
        writer.writerows(data)
        csv_data = output.getvalue()
        # Save to /tmp/exports or S3
        filename = f"enrollment_report_sem_{semester_id}_{datetime.utcnow().isoformat()}.csv"
        filepath = f"/tmp/exports/{filename}"
        with open(filepath, "w") as f:
            f.write(csv_data)
        return {"status": "completed", "filepath": filepath, "format": "csv"}
    
    elif format == "excel":
        df = pd.DataFrame(data)
        filename = f"enrollment_report_sem_{semester_id}_{datetime.utcnow().isoformat()}.xlsx"
        filepath = f"/tmp/exports/{filename}"
        df.to_excel(filepath, index=False)
        return {"status": "completed", "filepath": filepath, "format": "excel"}

@shared_task(name="report.generate_fee_collection_summary")
async def generate_fee_summary_report(program_id: int = None, start_date: str = None, end_date: str = None):
    """Generate fee collection summary report"""
    registrar_service = CollegeRegistrarService()
    async with get_db() as db:
        summary = await registrar_service.get_fee_collection_summary(
            db, program_id=program_id, start_date=start_date, end_date=end_date
        )
    # Convert to CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Program", "Total Students", "Paid", "Pending", "Total Amount"])
    for row in summary:
        writer.writerow([row.program_name, row.total_students, row.paid_count, row.pending_count, row.total_amount])
    
    filename = f"fee_summary_{datetime.utcnow().isoformat()}.csv"
    filepath = f"/tmp/exports/{filename}"
    with open(filepath, "w") as f:
        f.write(output.getvalue())
    
    return {"status": "completed", "filepath": filepath, "rows": len(summary)}

@shared_task(name="report.export_student_data")
async def export_student_data(format: str = "json"):
    """Export all student data (admin only, large dataset)"""
    from modules.college.college_student.repository import CollegeStudentRepository
    repo = CollegeStudentRepository()
    async with get_db() as db:
        students = await repo.get_all_exportable(db)  # serializable dicts
    
    if format == "json":
        import json
        filename = f"students_export_{datetime.utcnow().isoformat()}.json"
        filepath = f"/tmp/exports/{filename}"
        with open(filepath, "w") as f:
            json.dump(students, f, default=str, indent=2)
    
    return {"status": "completed", "filepath": filepath, "records": len(students)}
```

### 5. Celery Worker & Beat Setup (1 hour)
**Create `scripts/start_celery.sh`** (or `.bat` for Windows):
```bash
#!/bin/bash
# Start Celery worker
celery -A modules.shared.celery_app worker --loglevel=info --concurrency=4

# In separate terminal, start beat scheduler
celery -A modules.shared.celery_app beat --loglevel=info
```

**Docker-compose integration**:
In `docker-compose.prod.yml` or `docker-compose.dev.yml`:
```yaml
  celery-worker:
    build: .
    command: celery -A modules.shared.celery_app worker --loglevel=info
    depends_on:
      - redis
      - backend
    env_file: .env
  
  celery-beat:
    build: .
    command: celery -A modules.shared.celery_app beat --loglevel=info
    depends_on:
      - redis
      - backend
    env_file: .env
```

**Configure Celery Beat Schedule** (`modules/shared/celery_app.py`):
```python
celery_app.conf.beat_schedule = {
    "cleanup-expired-exam-notices-daily": {
        "task": "cleanup.expired_exam_notices",
        "schedule": crontab(hour=2, minute=0),  # 2 AM daily
    },
    "cleanup-old-chat-messages-weekly": {
        "task": "cleanup.old_chat_messages",
        "schedule": crontab(hour=3, day_of_week=0),  # Sunday 3 AM
        "args": (30,),  # keep 30 days
    },
    "backup-database-daily": {
        "task": "backup.create_daily_backup",
        "schedule": crontab(hour=1, minute=30),  # 1:30 AM daily
    },
}
```

### 6. Integrate Tasks into Endpoints (1 hour)
**Example 1: Bulk student enrollment** (`college_enrollments/router.py`):
```python
from modules.shared.tasks.email_tasks import send_welcome_email

@router.post("/bulk")
async def bulk_enroll_students(enrollments: list[EnrollmentSchema], background_tasks: BackgroundTasks):
    # Process enrollment in DB
    for enrollment in enrollments:
        await service.create(enrollment)
        # Send welcome email asynchronously (not Celery for simple case)
        background_tasks.add_task(send_welcome_email.delay, enrollment.student.email, enrollment.student.name)
    return {"message": "Enrollments created, emails queued"}
```

**Example 2: Report generation endpoint** (`college_dean/router.py`):
```python
@router.post("/reports/enrollment")
async def generate_enrollment_report(semester_id: int, background_tasks: BackgroundTasks):
    task = generate_enrollment_report.delay(semester_id, "csv")
    return {"task_id": task.id, "status": "queued", "check": f"/api/v1/tasks/{task.id}"}
```

**Example 3: Fee receipt email after payment** (`college_account_section/service.py`):
```python
from modules.shared.tasks.email_tasks import send_fee_receipt_email

async def create_payment(self, fee_record_id: int, amount: float):
    payment = await self.repository.create_payment(fee_record_id, amount)
    # Queue email
    send_fee_receipt_email.delay(
        payment.fee_record.student.email,
        {"amount": amount, "receipt_no": payment.receipt_no}
    )
    return payment
```

### 7. Task Status Endpoint (30 min)
**Create `modules/shared/tasks/status.py`**:

```python
from fastapi import APIRouter, Depends, HTTPException
from celery.result import AsyncResult
from modules.shared.celery_app import celery_app
from modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

@router.get("/{task_id}")
async def get_task_status(task_id: str, current_user=Depends(get_current_user)):
    """Check status of asynchronous task"""
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
        "meta": result.meta,
    }
```

### 8. Testing & Documentation (1 hour)
**Write Celery tests** (`tests/test_celery_tasks.py`):
```python
from_modules.shared.tasks.cleanup_tasks import cleanup_expired_exam_notices

@pytest.mark.asyncio
async def test_cleanup_expired_notices():
    # Create old exam notice in DB
    # Call task
    result = cleanup_expired_exam_notices.delay()
    result.wait(timeout=10)
    assert result.successful()
    # Verify notice marked deleted
```

**Document**:
- [ ] `BACKGROUND_TASKS.md`:
  - List of all periodic tasks + schedule
  - How to monitor tasks (`celery -A modules.shared.celery_app inspect active`)
  - How to retry failed tasks (`celery -A ... revoke <task_id>` + `retry`)
  - Task result backend (Redis) used for status queries

**Commit**:
- [ ] `feat(background): Add Celery task queue with Redis, implement cleanup, email, report tasks`

## Deliverables
- ✅ `modules/shared/celery_app.py` + `modules/shared/tasks/` package
- ✅ Celery worker runs (dev): `celery -A modules.shared.celery_app worker --loglevel=info`
- ✅ Celery beat scheduler running for periodic jobs
- ✅ Background tasks: cleanup (expired notices, chat), emails (welcome, fee receipt), reports (enrollment, fee summary)
- ✅ Task status endpoint `/api/v1/tasks/{task_id}`
- ✅ Docker-compose services for celery-worker + celery-beat
- ✅ Tests for each task type (verify execution)
- ✅ `BACKGROUND_TASKS.md`

## Success Criteria
- `celery -A modules.shared.celery_app status` shows worker online
- Periodic tasks execute on schedule (check logs)
- Long-running report generation doesn't block HTTP response
- Task status endpoint returns PENDING → SUCCESS/FAILURE
- All tasks pass in test environment

## Notes
- Use Redis as both broker and result backend for simplicity
- Configure proper task routes if needing different queues (high-priority vs low)
- Monitor Celery Flower in production (optional): `pip install flower`, `celery -A ... flower`
- Ensure tasks handle DB sessions correctly (async with get_db())

## Next: Day 14
Database tuning: add missing indexes, optimize connection pool, implement offsite backup (S3/Blob storage), create consistency check scripts, and deadline for Week 2 deliverables.
