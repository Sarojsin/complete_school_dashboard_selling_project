# Plan: Migrate school_analytics Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_analytics/)
Check if this module exists in modules/school/ - likely doesn't exist yet.

| File | Current State | Issues |
|------|---------------|--------|
| `models.py` | ❌ Missing | Need to create from backup |
| `schemas.py` | ❌ Missing | Need to create from backup |
| `repository.py` | ❌ Missing | Need to create from backup |
| `api.py` | ❌ Missing | Need to create from backup |
| `router.py` | ❌ Missing | Need to create from backup |

### Source from Backup
| File | Contents |
|------|----------|
| `backup/api/v1/school/authorities.py` | /analytics/students, /analytics/attendance, /analytics/performance endpoints |
| `backup/api/v1/school/students.py` | Student analytics |
| `backup/repositories/admin_message_repository.py` | Has get_analytics method |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Target:** `modules/school/school_analytics/models.py`

```python
# Expected structure:
class AnalyticsReport(Base):
    __tablename__ = "school_analytics_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(50), nullable=False)  # attendance, performance, engagement, overview
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete="SET NULL"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    data = Column(JSON, nullable=True)  # Report data stored as JSON
    generated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)


class StudentActivityLog(Base):
    __tablename__ = "school_student_activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # login, resource_access, assignment, exam, chat, video
    activity_data = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Step 2: Create `schemas.py`
**Target:** `modules/school/school_analytics/schemas.py`

```python
# Expected schemas:
class AnalyticsReportBase(BaseModel):
    report_type: str
    title: str
    description: Optional[str] = None
    class_id: Optional[int] = None
    academic_year: str
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    data: Optional[dict] = None

class AnalyticsReportCreate(AnalyticsReportBase):
    pass

class AnalyticsReportResponse(AnalyticsReportBase):
    id: int
    generated_by: Optional[int] = None
    generated_at: datetime
    class Config:
        from_attributes = True


class StudentActivityLogBase(BaseModel):
    activity_type: str
    activity_data: Optional[dict] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class DashboardResponse(BaseModel):
    total_students: int
    total_teachers: int
    total_courses: int
    attendance_rate: float
    average_grade: float
    recent_activity: list
```

### Step 3: Create `repository.py`
**Target:** `modules/school/school_analytics/repository.py`

Methods needed:
- `generate_report(report_type, filters)` - Generate new report
- `get_report(report_id)` - Get report by ID
- `get_reports(filters)` - Get all reports
- `delete_report(report_id)` - Delete report
- `log_activity(activity_data)` - Log student activity
- `get_activity_logs(filters)` - Get activity logs
- `get_student_analytics(student_id)` - Get student analytics
- `get_class_analytics(class_id)` - Get class analytics
- `get_attendance_stats(days)` - Get attendance stats
- `get_performance_stats()` - Get performance stats

### Step 4: Create `api.py`
**Source:** `backup/api/v1/school/authorities.py` (analytics endpoints)
**Target:** `modules/school/school_analytics/api.py`

Endpoints needed:
- `GET /dashboard` - Get overall dashboard
- `GET /students` - Student analytics
- `GET /attendance` - Attendance analytics
- `GET /performance` - Performance analytics
- `GET /reports` - List generated reports
- `POST /reports` - Generate report
- `GET /reports/{id}` - Get report
- `DELETE /reports/{id}` - Delete report
- `GET /activity` - Get activity logs
- `GET /activity/student/{student_id}` - Get student activity
- `GET /metrics/trends` - Get trend data

### Step 5: Create `router.py`
**Target:** `modules/school/school_analytics/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| AnalyticsReport class | Create with table name "school_analytics_reports" |
| StudentActivityLog class | Create with table name "school_student_activity_logs" |
| Fields (Report) | report_type, title, description, class_id, academic_year, period_start, period_end, data |
| Fields (Log) | user_id, activity_type, activity_data, ip_address, user_agent |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| AnalyticsReportBase | report_type, title, description, class_id, academic_year, period, data |
| AnalyticsReportResponse | All fields with generated_by, generated_at |
| DashboardResponse | total_students, total_teachers, attendance_rate, average_grade |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| generate_report | Create analytics report |
| get_report | Fetch report by ID |
| get_reports | List reports |
| log_activity | Log student activity |
| get_activity_logs | Get activity logs |
| get_student_analytics | Get student-specific analytics |
| get_class_analytics | Get class-level analytics |
| get_attendance_stats | Get attendance statistics |
| get_performance_stats | Get performance statistics |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| GET /dashboard | Overall dashboard |
| GET /students | Student analytics |
| GET /attendance | Attendance analytics |
| GET /performance | Performance analytics |
| GET /reports | List reports |
| POST /reports | Generate report |
| GET /activity | Get activity logs |

### 5. router.py
| Export | Purpose |
|--------|---------|
| router | FastAPI router from api.py |

---

## Import Fixes Required

| Old (backup) | New (modules) |
|--------------|---------------|
| `from backup.models.base import Base` | `from modules.shared.base import Base` |
| `from modules.shared.database import get_async_db` | `from modules.shared.database import get_db` |
| `from modules.shared.auth import get_current_user` | `from modules.auth.dependencies import get_current_user` |

---

## Next Steps

1. **Approve this plan** → Proceed to code implementation in Code mode
2. **Request changes** → Specify which parts to skip/modify
3. **Expand scope** → Include other modules