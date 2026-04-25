# Migration Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - Modular Architecture (2026)

### ⚠️ Major Architecture Change
This release introduces a complete modular architecture. The application has been
refactored from a monolithic structure to 32 self-contained modules.

### Architecture Changes
- Migrated from monolithic `app/` structure to 32 self-contained modules under `modules/`
- Each module owns: models, schemas, repository, service, api
- Shared utilities centralized in `modules/shared/`
- New `alembic/` directory for database migrations

### New API Structure
| Old Path | New Path | Module |
|----------|----------|--------|
| `/api/school/teachers/` | `/api/v1/school/teachers/` | `school_teacher` |
| `/api/students/` | `/api/v1/school/students/` | `school_student` |
| `/api/admin/` | `/api/v1/admin/` | `super_admin` |
| `/api/auth/login` | `/api/v1/auth/login` | `auth` |
| `/ws/chat/` | `/ws/chat/{room_id}` | `chat` |

### New Modules Added
- `modules/auth/` — Dedicated auth module with role system
- `modules/super_admin/` — System-wide admin control
- `modules/school_authority/` — School principal management
- `modules/school_teacher/` — Teacher management
- `modules/school_student/` — Student management
- `modules/school_parent/` — Parent portal
- `modules/school_exam_section/` — Exam management
- `modules/school_account_section/` — Fees and finance
- `modules/school_library/` — Library management
- `modules/school_attendance/` — Attendance tracking
- `modules/college_faculty/` — College faculty
- `modules/college_student/` — College student management
- `modules/college_hod/` — Head of Department
- `modules/college_dean/` — Dean office
- `modules/college_registrar/` — Programs, semesters, courses
- `modules/college_exam_section/` — College exams
- `modules/college_account_section/` — College fees
- `modules/college_library/` — College library
- `modules/college_placement/` — Placement cell
- `modules/college_research/` — Research projects
- `modules/college_hostel/` — Hostel management
- `modules/college_lab/` — Lab management
- `modules/chat/` — Real-time WebSocket chat
- `modules/groups/` — Study groups
- `modules/notices/` — Announcements
- `modules/notifications/` — Push notifications

### Database Changes
- New tables added: `audit_logs`, `system_settings`, `features`, `system_backups`
- All existing tables preserved with unchanged schema
- Alembic migrations now used for all schema changes

### Breaking Changes
**None** — All old routes preserved during migration. Old code moved to `archive/`.

### New Features
- **Feature Flags** — Module-level enable/disable via `features` table
- **Alembic Migrations** — Version-controlled database schema changes
- **Rollback Scripts** — One-command emergency rollback capability
- **Health Endpoints** — `/health`, `/health/db`, `/health/modules`
- **Structured Logging** — JSON-formatted logs for production
- **Performance Benchmarking** — Built-in benchmarking tools

### Deprecation Notices
The following endpoints are deprecated and will be removed in future versions:
- `/api/` (old v1 endpoints) → use `/api/v1/` instead
- Legacy direct database access → use repository layer only

---

## [1.x.x] - Legacy Monolith (Previous Versions)

### Previous Structure
- Single `app/` directory with all endpoints
- Flat API routes under `/api/`
- Manual database management
- No formal migration system

### Known Issues (Fixed in 2.0.0)
- N+1 query problems in list endpoints
- No structured logging
- No health monitoring
- Difficult to add new modules
- No rollback capability

---

## Upgrade Guide from 1.x to 2.0.0

1. **Backup your database** before upgrading
2. **Run Alembic migrations**: `alembic upgrade head`
3. **Update client code** to use `/api/v1/` endpoints
4. **Test thoroughly** using benchmark scripts
5. **Monitor health** using new monitoring endpoints

### Configuration Changes
New environment variables:
- `DATABASE_URL` (existing, now required)
- `COLLEGE_DATABASE_URL` (optional, for separate college DB)
- `DATABASE_MODE` (single/separate)
- `SENTRY_DSN` (optional, for error tracking)
- `ENVIRONMENT` (production/development)

---

*For detailed migration plans, see `plans/elite_plan*.md`*
