## admin_feature_control_plan.md

# Implementation Plan (2026-03-12)

## Phase 1: Data Foundations
- [x] Add SystemSetting and BackupRecord persistence
- [x] Add media approval fields (notes/videos)
- [x] Wire attendance analytics to real data

## Phase 2: Replace Placeholders With Real Data
- [x] Admin settings stored in DB (general, academic, localization, SMTP, payment, notifications, features)
- [x] Security panel uses real login history and settings
- [x] Media management lists notes/videos with approvals and storage stats
- [x] Reports generate real data and export CSV/PDF
- [x] Backup system supports SQLite backup/list/restore and export/import data
- [x] Advanced features use heuristic analytics, alerts, automations, broadcasts, and multi-school list

## Phase 3: Academic Timetable
- [x] Timetable list and conflict checks backed by Schedule table

## Status Update
- Completed: All modules in this plan now have working implementations (no placeholders).
- Notes: Backup/restore is SQLite-first; external DBs may need pg_dump integration.

# Enterprise Admin Panel - Implementation Plan

## Project Overview
Full-featured admin dashboard for Nexus Elite School Management System with 14 comprehensive modules.

---

## Executive Summary

### ✅ What's Already Built
| Component | Status | Location |
|-----------|--------|----------|
| Feature Control Models | Complete | `app/models/admin_models.py` |
| Admin Dashboard API | Basic | `app/api/endpoints/admin_dashboard.py` |
| Feature Management | Complete | `app/api/endpoints/admin_features.py` |
| Feature Service | Complete | `app/services/feature_service.py` |
| Admin Dashboard UI | Basic | `app/templates/admin/dashboard.html` |
| Analytics Template | Template Only | `app/templates/authority/analytics_v2.html` |
| Audit Logs UI | Complete | `app/templates/admin/audit_logs.html` |
| Settings UI | Basic | `app/templates/admin/settings.html` |

### 🎯 What's Missing (Needs Implementation)
- Real-time dashboard data integration
- Chart.js analytics with actual data
- Complete user management CRUD
- All 14 modules fully implemented

---

## Detailed Implementation Plan

### Phase 1: Core Admin Dashboard Enhancement

```mermaid
flowchart TD
    A[Admin Dashboard] --> B[Overview Cards]
    A --> C[Analytics Charts]
    A --> D[Quick Actions]
    
    B --> B1[Total Students]
    B --> B2[Total Teachers]
    B --> B3[Total Parents]
    B --> B4[Total Courses]
    B --> B5[Revenue]
    B --> B6[Pending Fees]
    B --> B7[Upcoming Exams]
    B --> B8[Active Groups]
    
    C --> C1[Enrollment Growth Chart]
    C --> C2[Fee Collection Graph]
    C --> C3[Attendance %]
    C --> C4[Exam Performance]
```

**Tasks:**
1.1 Enhance [`admin_dashboard.py`](app/api/endpoints/admin_dashboard.py) with real data queries
1.2 Update [`dashboard.html`](app/templates/admin/dashboard.html) with overview cards
1.3 Integrate Chart.js into analytics section

---

### Phase 2: User & Role Management

```mermaid
flowchart LR
    subgraph Users
        U1[Students] --> U2[Teachers]
        U2 --> U3[Parents]
        U3 --> U4[HOD]
        U4 --> U5[Authority]
        U5 --> U6[Exam Section]
        U6 --> U7[Library]
        U7 --> U8[Accounts]
    end
    
    subgraph Actions
        A1[View/Edit]
        A2[Activate/Deactivate]
        A3[Reset Password]
        A4[Force Logout]
        A5[View Login History]
        A6[Lock Account]
    end
```

**API Endpoints to Create:**
- `GET /admin/users` - List all users
- `PATCH /admin/users/{id}/toggle-active` - Activate/deactivate
- `POST /admin/users/{id}/reset-password` - Reset password
- `POST /admin/users/{id}/force-logout` - Force logout
- `GET /admin/users/{id}/login-history` - Login history
- `POST /admin/users/{id}/lock` - Lock account

---

### Phase 3: Academic Management

```mermaid
flowchart TD
    A[Academic Management] --> B[Course Management]
    A --> C[Department Management]
    A --> D[Timetable Management]
    
    B --> B1[Create/Edit/Delete]
    B --> B2[Assign Teacher]
    B --> B3[Assign Students]
    B --> B4[Capacity Limit]
    B --> B5[Upload Syllabus]
    
    C --> C1[Create Department]
    C --> C2[Assign HOD]
    C --> C3[View Performance]
    
    D --> D1[Weekly Timetable]
    D --> D2[Conflict Detection]
    D --> D3[Export PDF]
```

---

### Phase 4: Exam & Result Control

```mermaid
flowchart TD
    E[Exam Control] --> E1[Exam Types]
    E --> E2[Grading Scale]
    E --> E3[Results]
    E --> E4[Report Cards]
    
    E1 --> E1A[Midterm]
    E1 --> E1B[Final]
    E1 --> E1C[Quiz]
    
    E3 --> E3A[Approve]
    E3 --> E3B[Lock Editing]
    E3 --> E3C[Publish]
```

---

### Phase 5: Finance & Fee Management

```mermaid
flowchart TD
    F[Finance] --> F1[Fee Structure]
    F --> F2[Invoices]
    F --> F3[Payments]
    F --> F4[Reports]
    
    F1 --> F1A[Create Structure]
    F1 --> F1B[Assign to Class]
    
    F2 --> F2A[Generate]
    F2 --> F2B[Send]
    
    F3 --> F3A[Payment History]
    F3 --> F3B[Refunds]
    F3 --> F3C[Late Fees]
    
    F4 --> F4A[Income vs Expense]
    F4 --> F4B[Export CSV/PDF]
```

---

### Phase 6-14: Additional Modules

| Phase | Module | Key Features |
|-------|--------|--------------|
| 6 | Notices | Global, role-based, scheduled, emergency |
| 7 | Communication | Message moderation, analytics |
| 8 | Media | File management, storage limits, approval |
| 9 | System Monitor | Active users, server status, DB health |
| 10 | Security | JWT config, 2FA, audit logs |
| 11 | Backup | Manual/auto backup, restore |
| 12 | Reports | Attendance, fees, performance (PDF/CSV) |
| 13 | Settings | School info, SMTP, payment gateway |
| 14 | Advanced | AI prediction, alerts, multi-school |

---

## Implementation Priority

1. **Phase 1-2** (Dashboard + Users) - Week 1
2. **Phase 3-5** (Academic + Finance) - Week 2
3. **Phase 6-8** (Notices + Communication + Media) - Week 3
4. **Phase 9-11** (Monitor + Security + Backup) - Week 4
5. **Phase 12-14** (Reports + Settings + Advanced) - Week 5

---

## Technical Notes

### Database Models Needed
- `LoginHistory` - Track user logins
- `FailedLoginAttempt` - Track failed attempts
- `BackupRecord` - Backup history
- `SystemSettings` - Global settings
- `ExamType` - Exam categories
- `GradingScale` - Grade definitions
- `TimetableEntry` - Schedule data
- `MediaFile` - Uploaded files
- `ReportedMessage` - Chat reports

### API Structure
```
/api/v1/admin/
├── dashboard/          # Stats & overview
├── users/              # User management
├── users/{id}/history  # Login history
├── academic/           # Courses, depts, timetable
├── exams/              # Exam management
├── finance/            # Fee management
├── notices/            # Announcements
├── messages/           # Chat moderation
├── media/              # File management
├── system/             # Monitoring
├── security/           # Security settings
├── backup/             # Backup operations
├── reports/            # Report generation
└── settings/           # Global settings
```

### Frontend Pages
```
/admin/
├── dashboard/           # Main dashboard
├── users/              # User list
├── users/{id}/         # User detail
├── academic/           # Academic management
├── courses/            # Course management
├── departments/        # Department management
├── timetable/          # Timetable view
├── exams/              # Exam management
├── finance/            # Finance dashboard
├── fees/               # Fee management
├── notices/            # Notice management
├── messages/           # Message moderation
├── media/              # Media management
├── system/             # System monitoring
├── security/           # Security settings
├── backup/             # Backup management
├── reports/            # Reports
└── settings/           # Global settings
```

---

## Dependencies Required
- Chart.js (already in use)
- PDFKit or similar (for PDF generation)
- OpenPyXL (for Excel export)
- APScheduler (for scheduled tasks)
- PostgreSQL backup tools

---

## Security Considerations
- All admin endpoints require ADMIN role
- Implement rate limiting on sensitive operations
- Add IP whitelist for admin access
- Enable detailed audit logging
- Add 2FA for admin accounts
