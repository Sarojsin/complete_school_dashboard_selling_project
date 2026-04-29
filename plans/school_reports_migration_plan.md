# Plan: Migrate school_reports Module from Backup

## Current State Analysis

### Existing Module (modules/school/school_reports/)
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
| `backup/web/routers/authority.py` | /authority/reports endpoint |
| `backup/web/routers/exam_section.py` | Grade sheet, results endpoints |
| `backup/api/v1/school/authorities.py` | /reports endpoint |

---

## Detailed Migration Plan

### Step 1: Create `models.py`
**Target:** `modules/school/school_reports/models.py`

```python
# Expected structure:
class ReportTemplate(Base):
    __tablename__ = "school_report_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    template_type = Column(String(50), nullable=False)  # report_card, progress, certificate, transcript, custom
    description = Column(Text, nullable=True)
    content_schema = Column(JSON, nullable=True)  # Template structure
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GeneratedReport(Base):
    __tablename__ = "school_generated_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("school_report_templates.id", ondelete="SET NULL"), nullable=True)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete="SET NULL"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    term = Column(String(20), nullable=True)
    report_data = Column(JSON, nullable=True)
    pdf_url = Column(String(500), nullable=True)
    status = Column(String(20), default="draft")  # draft, generated, published
    generated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)


class ReportComment(Base):
    __tablename__ = "school_report_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    generated_report_id = Column(Integer, ForeignKey("school_generated_reports.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comment = Column(Text, nullable=False)
    comment_type = Column(String(20), default="teacher")  # teacher, principal, custom
    created_at = Column(DateTime, default=datetime.utcnow)


class AttendanceReport(Base):
    __tablename__ = "school_attendance_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("school_students.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("school_classes.id", ondelete="SET NULL"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    total_days = Column(Integer, default=0)
    present_days = Column(Integer, default=0)
    absent_days = Column(Integer, default=0)
    leave_days = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)
    generated_at = Column(DateTime, default=datetime.utcnow)
```

### Step 2: Create `schemas.py`
**Target:** `modules/school/school_reports/schemas.py`

```python
# Expected schemas:
class ReportTemplateBase(BaseModel):
    name: str
    template_type: str
    description: Optional[str] = None
    content_schema: Optional[dict] = None

class ReportTemplateCreate(ReportTemplateBase):
    pass

class ReportTemplateResponse(ReportTemplateBase):
    id: int
    is_active: bool
    created_by: Optional[int] = None
    created_at: datetime
    class Config:
        from_attributes = True


class GeneratedReportBase(BaseModel):
    template_id: Optional[int] = None
    student_id: int
    class_id: Optional[int] = None
    academic_year: str
    term: Optional[str] = None
    report_data: Optional[dict] = None

class GeneratedReportCreate(GeneratedReportBase):
    pass

class GeneratedReportResponse(GeneratedReportBase):
    id: int
    pdf_url: Optional[str] = None
    status: str
    generated_by: Optional[int] = None
    generated_at: datetime
    class Config:
        from_attributes = True


class ReportCommentBase(BaseModel):
    comment: str
    comment_type: str = "teacher"

class ReportCommentCreate(ReportCommentBase):
    generated_report_id: int
```

### Step 3: Create `repository.py`
**Target:** `modules/school/school_reports/repository.py`

Methods needed:
- `create_template(template_data)` - Create new template
- `get_template(template_id)` - Get template by ID
- `get_templates()` - Get all templates
- `update_template(template_id, data)` - Update template
- `delete_template(template_id)` - Delete template
- `create_report(report_data)` - Generate new report
- `get_report(report_id)` - Get report by ID
- `get_reports(filters)` - Get all reports
- `update_report(report_id, data)` - Update report
- `delete_report(report_id)` - Delete report
- `publish_report(report_id)` - Publish report
- `add_comment(comment_data)` - Add comment to report
- `get_comments(report_id)` - Get report comments
- `delete_comment(comment_id)` - Delete comment

### Step 4: Create `api.py`
**Source:** `backup/web/routers/exam_section.py`, `backup/api/v1/school/authorities.py`
**Target:** `modules/school/school_reports/api.py`

Endpoints needed:
- `GET /templates` - List report templates
- `POST /templates` - Create template
- `GET /templates/{id}` - Get template
- `PUT /templates/{id}` - Update template
- `DELETE /templates/{id}` - Delete template
- `POST /generate` - Generate report
- `GET /reports` - List generated reports
- `GET /reports/{id}` - Get report
- `PUT /reports/{id}` - Update report
- `DELETE /reports/{id}` - Delete report
- `POST /reports/{id}/publish` - Publish report
- `GET /reports/{id}/download` - Download report
- `POST /reports/{id}/comments` - Add comment
- `GET /reports/{id}/comments` - Get comments

### Step 5: Create `router.py`
**Target:** `modules/school/school_reports/router.py`

```python
from .api import router

__all__ = ["router"]
```

---

## File-by-File Changes Summary

### 1. models.py
| Component | Action |
|-----------|--------|
| ReportTemplate class | Create with table name "school_report_templates" |
| GeneratedReport class | Create with table name "school_generated_reports" |
| ReportComment class | Create with table name "school_report_comments" |
| AttendanceReport class | Create with table name "school_attendance_reports" |
| Use Base | Import from modules.shared.base |

### 2. schemas.py
| Schema | Fields |
|--------|--------|
| ReportTemplateBase | name, template_type, description, content_schema |
| GeneratedReportBase | template_id, student_id, class_id, academic_year, term, report_data |
| ReportCommentBase | comment, comment_type |

### 3. repository.py
| Method | Purpose |
|--------|---------|
| create_template | Create report template |
| get_template | Fetch template by ID |
| get_templates | List templates |
| create_report | Generate new report |
| get_report | Fetch report by ID |
| get_reports | List reports |
| publish_report | Change status to published |
| add_comment | Add comment to report |
| get_comments | Get report comments |

### 4. api.py
| Endpoint | Description |
|----------|-------------|
| GET /templates | List templates |
| POST /templates | Create template |
| GET /reports | List reports |
| POST /generate | Generate report |
| POST /reports/{id}/publish | Publish report |
| GET /reports/{id}/download | Download PDF |
| POST /reports/{id}/comments | Add comment |

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