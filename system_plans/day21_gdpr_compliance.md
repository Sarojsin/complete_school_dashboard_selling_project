# Day 21 Production Implementation Plan
**Date**: 2026-05-26
**Focus**: GDPR/Privacy Compliance – Data Export & Deletion

## Objectives
- Implement user data export endpoint (right to data portability)
- Implement account deletion with proper anonymization (right to be forgotten)
- Add consent management for marketing communications
- Create Privacy Policy and Terms of Service pages (frontend routes + backend content)
- Document data retention policies

## Background: GDPR/DPDP Requirements
General Data Protection Regulation (EU) and Digital Personal Data Protection Act (India) require:
- **Right to Access**: Users can request their data in portable format
- **Right to Erasure**: Users can request account deletion + personal data removal
- **Consent Management**: Explicit opt-in for marketing communications; easy opt-out
- **Privacy Policy**: Clear explanation of data collection, usage, retention
- **Terms of Service**: Legal agreement governing use

We already have: Audit logging, security measures, structured data. Need these last compliance pieces.

## Tasks

### 1. Data Export Endpoint (Morning - 2 hours)
**Endpoint**: `GET /api/v1/user/data-export`

**Implementation** (`modules/auth/router.py` or new `modules/compliance/router.py`):

```python
from fastapi import APIRouter, Depends
from modules.auth.dependencies import get_current_user
from sqlalchemy import select
import json
from datetime import datetime

router = APIRouter(prefix="/api/v1/user", tags=["compliance"])

@router.get("/data-export")
async def export_user_data(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Export all personal data for logged-in user in JSON format.
    Includes: profile, enrollment history, fee records, exam results (if student)
    or teaching assignments (if faculty).
    """
    export_data = {
        "user": {
            "id": str(current_user.public_id) if hasattr(current_user, 'public_id') else current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role.value,
            "locale": current_user.locale,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        },
        "profile": None,
        "enrollments": [],
        "fee_records": [],
        "exam_results": [],
        "consent_log": [],
    }
    
    # Student profile data
    if current_user.role == UserRole.COLLEGE_STUDENT:
        from modules.college.college_student.repository import CollegeStudentRepository
        student_repo = CollegeStudentRepository()
        student = await student_repo.get_by_user_id(db, current_user.id)
        if student:
            export_data["profile"] = {
                "roll_number": student.roll_number,
                "department": student.department.name if student.department else None,
                "program": student.program.name if student.program else None,
                "admission_date": student.admission_date.isoformat() if student.admission_date else None,
                # other student fields...
            }
            # Enrollments
            from modules.college.college_enrollments.repository import EnrollmentRepository
            enroll_repo = EnrollmentRepository()
            enrollments = await enroll_repo.get_by_student(db, student.id)
            export_data["enrollments"] = [
                {
                    "semester": e.semester.name,
                    "program": e.program.name,
                    "enrollment_date": e.enrollment_date.isoformat(),
                    "status": e.status.value,
                } for e in enrollments
            ]
            # Fee records
            from modules.college.college_fee_records.repository import FeeRecordRepository
            fee_repo = FeeRecordRepository()
            fee_records = await fee_repo.get_by_student(db, student.id)
            export_data["fee_records"] = [
                {
                    "amount": r.amount,
                    "due_date": r.due_date.isoformat(),
                    "status": r.status.value,
                    "payments": [
                        {"amount": p.amount, "date": p.payment_date.isoformat(), "method": p.payment_method}
                        for p in r.payments
                    ]
                } for r in fee_records
            ]
    
    # Faculty profile data
    elif current_user.role == UserRole.COLLEGE_FACULTY:
        from modules.college.college_faculty.repository import CollegeFacultyRepository
        faculty_repo = CollegeFacultyRepository()
        faculty = await faculty_repo.get_by_user_id(db, current_user.id)
        if faculty:
            export_data["profile"] = {
                "employee_id": faculty.employee_id,
                "department": faculty.department.name if faculty.department else None,
                "designation": faculty.designation,
                "joining_date": faculty.joining_date.isoformat() if faculty.joining_date else None,
            }
    
    # Audit log (last 90 days)
    from modules.shared.audit.models import AuditLog
    from datetime import timedelta
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    audit_logs = await db.execute(
        select(AuditLog).where(
            AuditLog.user_id == current_user.id,
            AuditLog.timestamp >= ninety_days_ago
        ).order_by(AuditLog.timestamp.desc()).limit(100)
    )
    export_data["audit_logs"] = [
        {
            "action": log.action.value,
            "resource": log.resource_type,
            "resource_id": log.resource_id,
            "timestamp": log.timestamp.isoformat(),
            "details": log.details,
        } for log in audit_logs.scalars().all()
    ]
    
    # Create downloadable file
    filename = f"user_data_export_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d')}.json"
    filepath = f"/tmp/exports/{filename}"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(export_data, f, indent=2, default=str)
    
    # Queue email with download link (or return FileResponse)
    # Option A: Immediate response (small data)
    # return JSONResponse(content=export_data)
    # Option B: Background + email link (large data) – better for faculty with many records
    from modules.shared.tasks.email_tasks import send_email
    download_url = f"https://example.com/downloads/{filename}"  # signed URL generator needed
    # TODO: implement secure file serving
    
    return {
        "message": "Data export prepared",
        "filename": filename,
        "record_count": len(export_data["enrollments"]) + len(export_data["fee_records"])
    }
```

### 2. Account Deletion with Anonymization (2 hours)
**Endpoint**: `POST /api/v1/user/request-deletion`

**Process**:
1. User confirms password
2. Soft delete user (set `is_deleted=True, deleted_at=...`)
3. Anonymize personal identifiers: replace email with `anon_{id}@deleted.invalid`, remove name
4. Delete or anonymize related data based on legal retention requirements:
   - Financial records (fee payments) – keep for 7 years (tax) – **DO NOT DELETE**
   - Academic records (enrollments, exam results) – keep permanently – **KEEP**
   - Personal messages (chat) – delete after 30 days if no legal hold – **ANONYMIZE**
   - Audit logs – keep for security investigation – **KEEP** (but pseudonymize user info)
5. Send confirmation email
6. Schedule hard purge after 30-day grace period (allow undo)

**Implementation** (`modules/compliance/service.py`):
```python
class DataRetentionService:
    async def request_account_deletion(self, db: AsyncSession, user: User, password: str):
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise ValidationError("Incorrect password")
        
        # Anonymize personal data
        user.email = f"anon_{user.id}@deleted.invalid"
        user.full_name = "Deleted User"
        user.is_active = False
        user.is_deleted = True
        user.deleted_at = datetime.utcnow()
        user.locale = None
        user.tfa_secret = None
        user.tfa_backup_codes = None
        
        await db.commit()
        
        # Queue hard purge after 30 days
        from modules.shared.tasks.cleanup_tasks import schedule_hard_delete
        schedule_hard_delete.apply_async(args=[user.id], countdown=30*24*3600)
        
        # Send confirmation email
        from modules.shared.tasks.email_tasks import send_email
        await send_email.delay(
            to=user.email,  # actually deleted email won't receive; send before anonymize?
            subject="Account Deletion Confirmation",
            body="Your account has been scheduled for deletion in 30 days. Contact support to restore."
        )
        
        return {"status": "scheduled", "purge_date": (datetime.utcnow() + timedelta(days=30)).isoformat()}
```

**Hard purge task** (Celery):
```python
@shared_task(name="compliance.hard_delete_user")
async def hard_delete_user(user_id: int):
    """After 30-day grace period, permanently delete user record"""
    async with get_db() as db:
        user = await db.get(User, user_id)
        if not user or not user.is_deleted:
            return {"skipped": True, "reason": "Not marked for deletion"}
        
        # Remove all PII: email already anon; remove name again; delete sensitive profiles
        from modules.college.college_student.repository import CollegeStudentRepository
        student_repo = CollegeStudentRepository()
        await student_repo.anonymize_by_user_id(db, user_id)  # set roll_num=anon, remove photos
        
        # For faculty: anonymize similarly
        
        # Finally, hard delete user record? Keep audit requirement: mark as purged instead
        user.is_purged = True
        await db.commit()
        
        logger.info("User purged after retention period", user_id=user_id)
```

### 3. Consent Management (1.5 hours)
**Track marketing consent**:
- [ ] Table `consent_logs` (new):
  ```sql
  CREATE TABLE consent_logs (
      id SERIAL PRIMARY KEY,
      user_id INT REFERENCES users(id),
      purpose VARCHAR(50),  -- 'marketing', 'newsletter', 'sms_alerts'
      granted BOOLEAN,
      ip_address INET,
      user_agent TEXT,
      timestamp TIMESTAMP
  );
  ```
- Migration: `alembic/versions/20260526_add_consent.py`

**Endpoint**: `POST /api/v1/user/consent`:
```python
@router.post("/consent")
async def record_consent(
    purpose: str = Body(...),
    granted: bool = Body(...),
    current_user=Depends(get_current_user),
    db: AsyncSession=Depends(get_db)
):
    consent = ConsentLog(
        user_id=current_user.id,
        purpose=purpose,
        granted=granted,
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent"),
        timestamp=datetime.utcnow()
    )
    db.add(consent)
    await db.commit()
    return {"recorded": True}
```

**Frontend**: On signup, ask for marketing consent (checkbox); call consent endpoint

### 4. Privacy Policy & TOS Pages (1 hour)
**Static page endpoints**:
```python
@router.get("/privacy-policy")
async def privacy_policy():
    """Serve Privacy Policy text or markdown file"""
    # Read from file or database
    return {"content": "...", "last_updated": "2026-05-26"}

@router.get("/terms-of-service")
async def terms_of_service():
    return {"content": "...", "last_updated": "2026-05-26"}
```

**Store documents** in `docs/legal/` as Markdown; serve parsed HTML

### 5. Data Retention Policy Documentation (30 min)
**Create `DATA_RETENTION.md`**:
| Data Category | Retention Period | Justification |
|---------------|----------------|---------------|
| User accounts (deleted) | 30 days grace + purge | Allow undo |
| Audit logs | 2 years | Security investigations |
| Financial records (fee payments) | 7 years | Tax/legal requirement |
| Exam results | Permanent | Academic record |
| Chat messages | 90 days | Operational, not critical |
| Backup data | 30 days daily + 1 year monthly | DR requirement |

### 6. Testing & Documentation (1 hour)
- [ ] `tests/test_gdpr.py`:
  - `test_data_export_returns_all_user_data()`
  - `test_deletion_soft_deletes_user()`
  - `test_hard_delete_after_grace_period()`
  - `test_consent_logging_works()`
- [ ] `tests/test_retention_policy.py`: verify delete vs anonymize
- [ ] `COMPLIANCE.md` documenting all compliance features
- [ ] Update `README.md` with privacy policy link

**Commit**: "feat(compliance): Add GDPR data export, deletion with anonymization, consent management, privacy policy endpoints"

## Deliverables
- ✅ `GET /api/v1/user/data-export` (JSON download of all personal data)
- ✅ `POST /api/v1/user/request-deletion` (soft delete + 30-day grace)
- ✅ Celery task `hard_delete_user` after 30 days
- ✅ `POST /api/v1/user/consent` endpoint + `consent_logs` table
- ✅ Privacy Policy & Terms endpoints
- ✅ `DATA_RETENTION.md` policy document
- ✅ Compliance tests

## Success Criteria
- Student can download all their data (enrollments, fees, profile) as JSON
- Deletion request anonymizes email/name immediately; account deactivated
- After 30 days, user record purged (hard delete or full anonymize)
- Consent logged with IP, timestamp; can be audited
- Privacy policy accessible at public route `/privacy-policy`

## Notes
- Financial records must be retained even after deletion request (legal hold)
- Provide way to contact DPO (Data Protection Officer) for manual requests
- Consider email notification before deletion (confirmation step)
- Secure file downloads: expiring signed URLs (S3 pre-signed) rather than `/tmp` direct access

## Next: Day 22
Complete audit logging coverage: verify all CRUD operations log, add admin endpoint to query audit logs, implement retention policy (auto-purge after 2 years), move SQLAlchemy events to background if slow.
