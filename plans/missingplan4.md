# Missing Endpoints Migration Plan - Priority 4: Admin Features & Dashboard

**Plan 4: Admin Core Features**

This plan covers Admin Features and Dashboard modules.

## Module Overview

| Module | Missing Endpoints | Priority |
|--------|------------------|----------|
| Admin Features | 14 endpoints | LOW |
| Admin Dashboard | 13 endpoints | LOW |

---

## 1. Admin Features Module

**Target Location:** `modules/super_admin/features/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/admin` | Get all features | backup/api/endpoints/admin_features.py |
| GET | `/api/admin/categories` | Get feature categories | backup/api/endpoints/admin_features.py |
| GET | `/api/admin/category/{category}` | Get features by category | backup/api/endpoints/admin_features.py |
| POST | `/api/admin` | Create feature | backup/api/endpoints/admin_features.py |
| GET | `/api/admin/{feature_code}` | Get feature | backup/api/endpoints/admin_features.py |
| PUT | `/api/admin/{feature_code}` | Update feature | backup/api/endpoints/admin_features.py |
| DELETE | `/api/admin/{feature_code}` | Delete feature | backup/api/endpoints/admin_features.py |
| POST | `/api/admin/{feature_code}/toggle` | Toggle feature | backup/api/endpoints/admin_features.py |
| GET | `/api/admin/{feature_code}/permissions` | Get feature permissions | backup/api/endpoints/admin_features.py |
| PUT | `/api/admin/{feature_code}/permissions` | Update role permissions | backup/api/endpoints/admin_features.py |
| POST | `/api/admin/{feature_code}/permissions` | Batch update permissions | backup/api/endpoints/admin_features.py |
| GET | `/api/admin/audit-logs` | Get audit logs | backup/api/endpoints/admin_features.py |
| GET | `/api/admin/audit-logs/feature/{feature_code}` | Get feature audit logs | backup/api/endpoints/admin_features.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/features/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/feature_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## 2. Admin Dashboard Module

**Target Location:** `modules/super_admin/dashboard/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/dashboard` | Get dashboard | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/stats` | Get system stats | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/users/count` | Get users by role | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/overview` | Get dashboard overview | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/features/summary` | Get features summary | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/features/enabled` | Get enabled features | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/features/disabled` | Get disabled features | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/analytics/enrollment` | Get enrollment analytics | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/analytics/fees` | Get fee analytics | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/analytics/attendance` | Get attendance analytics | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/analytics/exams` | Get exam analytics | backup/api/endpoints/admin_dashboard.py |
| GET | `/api/analytics/summary` | Get analytics summary | backup/api/endpoints/admin_dashboard.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/dashboard/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/dashboard_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## Migration Strategy

### Step 1: Analyze Existing Code
- Review `backup/api/endpoints/admin_features.py`
- Review `backup/api/endpoints/admin_dashboard.py`

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
- Test feature CRUD operations
- Test dashboard analytics
- Test permission management

---

## Time Estimate

| Module | Development Time | Testing Time |
|--------|-----------------|--------------|
| Admin Features | 2-3 days | 1 day |
| Admin Dashboard | 2-3 days | 1 day |
| **Total** | **4-6 days** | **2 days** |

---

## Files to Reference

### Source Files (from backup/)
- `backup/api/endpoints/admin_features.py`
- `backup/api/endpoints/admin_dashboard.py`
- `backup/repositories/feature_repository.py`
- `backup/repositories/dashboard_repository.py`

### Reference Templates
- `modules/super_admin/` (for structure reference)

---

## Dependencies

- Admin Features requires feature management system
- Admin Dashboard requires analytics aggregation
- Both require admin role authentication

---

## Integration Notes

1. **Admin Features Module:**
   - Should integrate with existing role-based access control
   - Need to track feature usage for audit logs

2. **Admin Dashboard Module:**
   - Should aggregate data from multiple sources
   - May require caching for performance

---

*Plan created: 2026-03-26*
