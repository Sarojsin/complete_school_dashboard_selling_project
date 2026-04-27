# Missing Endpoints Migration Plan - Priority 5: Admin Users & Academic

**Plan 5: Admin User Management & Academic Control**

This plan covers Admin Users and Academic modules.

## Module Overview

| Module | Missing Endpoints | Priority |
|--------|------------------|----------|
| Admin Users | 13 endpoints | LOW |
| Admin Academic | 11 endpoints | LOW |

---

## 1. Admin Users Module

**Target Location:** `modules/super_admin/users/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/users` | Get all users | backup/api/endpoints/admin_users.py |
| GET | `/api/users/{user_id}` | Get user | backup/api/endpoints/admin_users.py |
| PATCH | `/api/users/{user_id}/toggle-active` | Toggle user active | backup/api/endpoints/admin_users.py |
| POST | `/api/users/{user_id}/reset-password` | Reset user password | backup/api/endpoints/admin_users.py |
| POST | `/api/users/{user_id}/lock` | Lock user account | backup/api/endpoints/admin_users.py |
| POST | `/api/users/{user_id}/force-logout` | Force logout user | backup/api/endpoints/admin_users.py |
| GET | `/api/users/{user_id}/login-history` | Get user login history | backup/api/endpoints/admin_users.py |
| POST | `/api/users/{user_id}/change-role` | Change user role | backup/api/endpoints/admin_users.py |
| GET | `/api/users/stats/by-role` | Get user stats by role | backup/api/endpoints/admin_users.py |
| GET | `/api/users/students/list` | Get students list | backup/api/endpoints/admin_users.py |
| GET | `/api/users/teachers/list` | Get teachers list | backup/api/endpoints/admin_users.py |
| GET | `/api/users/parents/list` | Get parents list | backup/api/endpoints/admin_users.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/users/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/admin_user_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## 2. Admin Academic Module

**Target Location:** `modules/super_admin/academic/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/courses` | Get all courses (admin) | backup/api/endpoints/admin_academic.py |
| POST | `/api/courses` | Create course (admin) | backup/api/endpoints/admin_academic.py |
| PATCH | `/api/courses/{course_id}` | Update course (admin) | backup/api/endpoints/admin_academic.py |
| DELETE | `/api/courses/{course_id}` | Delete course (admin) | backup/api/endpoints/admin_academic.py |
| GET | `/api/departments` | Get all departments (admin) | backup/api/endpoints/admin_academic.py |
| POST | `/api/departments` | Create department (admin) | backup/api/endpoints/admin_academic.py |
| PATCH | `/api/departments/{dept_id}` | Update department (admin) | backup/api/endpoints/admin_academic.py |
| DELETE | `/api/departments/{dept_id}` | Delete department (admin) | backup/api/endpoints/admin_academic.py |
| GET | `/api/timetable` | Get timetable (admin) | backup/api/endpoints/admin_academic.py |
| GET | `/api/timetable/conflicts` | Check timetable conflicts | backup/api/endpoints/admin_academic.py |
| GET | `/api/stats` | Get academic stats | backup/api/endpoints/admin_academic.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/academic/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/admin_academic_repository.py`
   - Source: `backup/repositories/course_repository.py`
   - Source: `backup/repositories/department_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## Migration Strategy

### Step 1: Analyze Existing Code
- Review `backup/api/endpoints/admin_users.py`
- Review `backup/api/endpoints/admin_academic.py`

### Step 2: Extract Logic
- Copy repository logic from backup/repositories/
- Adapt service layer for new structure

### Step 3: Create New Modules
- Create in modules/super_admin/
- Follow existing module pattern

### Step 4: Integration
- Register routes in main.py
- Add to module exports
- Ensure proper admin authentication

### Step 5: Testing
- Test user management operations
- Test academic CRUD operations
- Test timetable conflict detection

---

## Time Estimate

| Module | Development Time | Testing Time |
|--------|-----------------|--------------|
| Admin Users | 2-3 days | 1 day |
| Admin Academic | 2-3 days | 1 day |
| **Total** | **4-6 days** | **2 days** |

---

## Files to Reference

### Source Files (from backup/)
- `backup/api/endpoints/admin_users.py`
- `backup/api/endpoints/admin_academic.py`
- `backup/repositories/admin_user_repository.py`
- `backup/repositories/admin_academic_repository.py`
- `backup/repositories/course_repository.py`
- `backup/repositories/department_repository.py`

### Reference Templates
- `modules/super_admin/` (for structure reference)

---

## Dependencies

- Admin Users requires user management system
- Admin Academic requires course and department management
- Both require admin role authentication

---

## Integration Notes

1. **Admin Users Module:**
   - Should integrate with authentication system
   - Need to handle password reset securely
   - Must track login history

2. **Admin Academic Module:**
   - Should integrate with existing course modules
   - Need conflict detection algorithm for timetable
   - Must maintain data integrity

---

*Plan created: 2026-03-26*
