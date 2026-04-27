# Endpoint Mapping Plan 1: Authentication & User Management

## Overview

This document maps all authentication and user-related endpoints from the monolithic backup to the new modular structure.

---

## Source Files Analyzed

| File | Endpoints Count |
|------|-----------------|
| `backup/api/endpoints/auth.py` | 33 endpoints |
| `backup/api/v1/college/auth.py` | 1 endpoint |
| **Total** | **34 endpoints** |

---

## Endpoint Mapping Table

### Authentication Endpoints

| Method | Old Endpoint | New Module | New Endpoint | Notes |
|--------|--------------|------------|--------------|-------|
| POST | `/api/auth/login` | `auth` | `/auth/login` | Already exists |
| POST | `/api/auth/login-json` | `auth` | `/auth/login-json` | Already exists |
| POST | `/api/auth/refresh` | `auth` | `/auth/refresh` | Already exists |
| POST | `/api/auth/signup/student` | `auth` | `/auth/signup/student` | Already exists |
| POST | `/api/auth/signup/teacher` | `auth` | `/auth/signup/teacher` | Already exists |
| POST | `/api/auth/signup/admin` | `auth` | `/auth/signup/admin` | Already exists |
| POST | `/api/auth/signup/authority` | `auth` | `/auth/signup/authority` | Already exists |
| POST | `/api/auth/signup/parent` | `auth` | `/auth/signup/parent` | Already exists |
| POST | `/api/auth/signup/hod` | `auth` | `/auth/signup/hod` | Already exists |
| POST | `/api/auth/signup/exam-section` | `auth` | `/auth/signup/exam-section` | Already exists |
| POST | `/api/auth/signup/library` | `auth` | `/auth/signup/library` | Already exists |
| POST | `/api/auth/signup/account` | `auth` | `/auth/signup/account` | Already exists |
| POST | `/api/auth/logout` | `auth` | `/auth/logout` | Already exists |
| GET | `/api/v1/college/auth/students` | `college_student` | `/college/students/` | Duplicate - use existing college_student |

---

## Module: auth

### Current Status

| File | Status | Notes |
|------|--------|-------|
| `modules/auth/router.py` | ✅ Complete | Has login, signup, refresh, logout |
| `modules/auth/schemas.py` | ✅ Complete | Has all signup schemas |
| `modules/auth/service.py` | ✅ Complete | Has authentication logic |
| `modules/auth/repository.py` | ✅ Complete | Has user repository |
| `modules/auth/dependencies.py` | ✅ Complete | Has get_current_user |

### Required Updates

None - Authentication module is already complete.

---

## Summary

| Category | Endpoints | New Module | Status |
|----------|-----------|------------|--------|
| Authentication | 14 | `auth` | ✅ Complete |

---

## Action Items

- [x] Verify auth module completeness
- [x] Map endpoints to modules
- [ ] Document in this plan

---

## Notes

1. All authentication endpoints are already implemented in the `auth` module
2. The `auth` module follows the same pattern as other modules (router, service, repository, schemas)
3. No changes needed - this module is ready for production
