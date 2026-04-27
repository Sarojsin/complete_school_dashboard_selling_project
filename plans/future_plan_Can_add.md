# Potential Remaining Work: Web Routes & Other Features

**Status: 2026-03-29**

This document identifies areas that may require additional work beyond the core API endpoints.

---

## Summary

| Category | Status | Notes |
|----------|--------|-------|
| Web Routes (HTML) | ⚠️ Needs Evaluation | Template-based routes might need migration |
| Multi-school Features | ⚠️ Needs Evaluation | May not be fully implemented |
| Advanced AI/Analytics | ⚠️ Needs Evaluation | May need separate service |
| SMS/Email Broadcast | ⚠️ Needs Evaluation | May use external services |
| Notification Automations | ⚠️ Needs Evaluation | May need separate module |

---

## 1. Web Routes (HTML Template Pages)

The `modules_missing_endpoints.md` mentions "Web Routes (HTML Pages)" as missing. These are HTML template-based routes from `backup/web/routers/`.

### Potential Missing Routes

| Category | Files in backup/web |
|----------|-------------------|
| Student web routes | `student.py` |
| Teacher web routes | `teacher.py` |
| Authority web routes | `authority.py` |
| Parent web routes | `parent.py` |
| Admin web routes | `admin.py` |
| Common routes | `common.py` |

### Recommendation

- If React frontend is being used, these HTML routes may be **obsolete**
- Check `frontend/` directory for React-based counterparts
- If needed, could create a separate `modules/web/` module

---

## 2. Multi-School Features

The `modules_missing_endpoints.md` mentions:

| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/api/multi-school/schools` | May Need Work |
| POST | `/api/multi-school/schools` | May Need Work |

### Current Status

- Current architecture appears to use a single database per school
- Multi-school might require separate database architecture
- Check `plans/separate_database_architecture*.md` for design docs

---

## 3. Advanced AI/Analytics Features

The document mentions these advanced endpoints:

| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/api/ai/performance-prediction` | May Need Work |
| GET | `/api/ai/at-risk-students` | May Need Work |
| GET | `/api/analytics/dashboard` | Check school_dashboard |

### Current Implementation

- See `modules/school/school_dashboard/` for analytics
- AI features would require ML/AI service integration
- These are advanced features that can be added later

---

## 4. Broadcast Features

The document mentions:

| Method | Endpoint | Status |
|--------|----------|--------|
| POST | `/api/broadcast/sms` | May Need External Service |
| POST | `/api/broadcast/email` | May Need External Service |
| GET | `/api/broadcast/history` | May Need Work |

### Current Status

- SMS/Email would require external service integration
- Could integrate with services like Twilio, SendGrid
- Currently, notifications use in-app system

---

## 5. Media Management (Extended)

The document mentions:

| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/api/media/files` | Check super_admin |
| GET | `/api/media/storage/usage` | May Need Work |
| GET | `/api/media/storage/by-user` | May Need Work |

### Current Status

- Static files handled by `app/static/`
- Media uploads handled by individual modules
- May need centralized media management

---

## 6. System Status Endpoints

The document mentions:

| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/api/system/status` | Check main.py |
| GET | `/api/system/database/health` | May Need Work |
| GET | `/api/system/users/online` | May Need Work |
| GET | `/api/system/performance` | May Need Work |
| GET | `/api/system/backup/status` | Check super_admin |
| GET | `/api/system/security/status` | Check super_admin |
| GET | `/api/system/dashboard` | May Need Work |

### Current Status

- Server status available via `/health` in main.py
- Database health can be checked via Alembic
- Some features can be added to super_admin

---

## 7. Notices Extended

The document mentions general notices endpoints (beyond school_notices):

| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/api/notices` | Implemented in school_notices |
| POST | `/api/notices/{notice_id}/toggle` | May Need Work |
| POST | `/api/notices/{notice_id}/mark-emergency` | May Need Work |
| GET | `/api/notices/stats` | May Need Work |
| GET | `/api/notices/scheduled` | May Need Work |

### Current Status

- Implemented in `modules/school/school_notices/`
- Admin notices are in super_admin
- Extended features may need addition

---

## 8. Messages Extended (Admin)

The document mentions admin-level messages:

| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/api/messages/all` | Implemented in school_chat |
| DELETE | `/api/messages/{message_id}` | Implemented in school_chat |
| GET | `/api/messages/analytics` | May Need Work |

### Current Status

- Chat/d_messages handled in school_chat module
- Admin analytics may need work in super_admin

---

## Recommended Next Steps

1. **Evaluate Web Routes need:**
   - Check if React frontend is complete
   - If complete, HTML routes are obsolete

2. **Prioritize remaining work:**
   - System health endpoints
   - Media management extension
   - Notification automations

3. **Defer for later:**
   - Multi-school features (requires architecture change)
   - AI features (requires ML service)
   - SMS/Email broadcast (requires external services)

---

## Files Reference

- `frontend/` - Frontend React application
- `backup/web/routers/` - Old HTML routes
- `modules/school/school_dashboard/` - Analytics
- `modules/school/school_notices/` - Notices
- `modules/school/school_chat/` - Chat/Messages
- `modules/super_admin/` - Admin features

---

*Last Updated: 2026-03-29*