# Missing Endpoints Migration Plan - Priority 1: Core Academic Modules

**Plan 1: High Priority Academic Modules**

This plan covers the most critical modules that need to be implemented in the new structure.

## Module Overview

| Module | Missing Endpoints | Priority |
|--------|------------------|----------|
| Assignments | 10 endpoints | HIGH |
| Grades | 7 endpoints | HIGH |
| Fees | 13 endpoints | HIGH |
| Tests | 12 endpoints | HIGH |

---

## 1. Assignments Module

**Target Location:** `modules/school/assignments/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| POST | `/api/assignments/` | Create assignment | backup/api/endpoints/assignments.py |
| POST | `/api/assignments/{assignment_id}/upload` | Upload assignment file | backup/api/endpoints/assignments.py |
| GET | `/api/assignments/teacher/my-assignments` | Get my assignments | backup/api/endpoints/assignments.py |
| GET | `/api/assignments/{assignment_id}/submissions` | Get assignment submissions | backup/api/endpoints/assignments.py |
| PUT | `/api/assignments/submissions/{submission_id}/grade` | Grade submission | backup/api/endpoints/assignments.py |
| PUT | `/api/assignments/{assignment_id}` | Update assignment | backup/api/endpoints/assignments.py |
| DELETE | `/api/assignments/{assignment_id}` | Delete assignment | backup/api/endpoints/assignments.py |
| GET | `/api/assignments/{assignment_id}` | Get assignment | backup/api/endpoints/assignments.py |
| POST | `/api/assignments/{assignment_id}/submit` | Submit assignment | backup/api/endpoints/assignments.py |
| GET | `/api/assignments/{assignment_id}/my-submission` | Get my submission | backup/api/endpoints/assignments.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/school/assignments/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/assignment_repository.py`
   - Need to create: Assignment, AssignmentSubmission models

3. **Implement API endpoints:**
   - Follow patterns from existing modules (e.g., modules/school/student/)

4. **Test endpoints:**
   - Verify CRUD operations
   - Test file upload functionality
   - Test submission workflow

---

## 2. Grades Module

**Target Location:** `modules/school/grades/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| POST | `/api/grades/` | Add grade | backup/api/endpoints/grades.py |
| POST | `/api/grades/bulk` | Add bulk grades | backup/api/endpoints/grades.py |
| PUT | `/api/grades/{grade_id}` | Update grade | backup/api/endpoints/grades.py |
| DELETE | `/api/grades/{grade_id}` | Delete grade | backup/api/endpoints/grades.py |
| GET | `/api/grades/course/{course_id}` | Get course grades | backup/api/endpoints/grades.py |
| GET | `/api/grades/course/{course_id}/top-performers` | Get top performers | backup/api/endpoints/grades.py |
| GET | `/api/grades/my-grades` | Get my grades | backup/api/endpoints/grades.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/school/grades/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/grade_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## 3. Fees Module

**Target Location:** `modules/school/fees/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| POST | `/api/fees/` | Create fee record | backup/api/endpoints/fees.py |
| POST | `/api/fees/bulk` | Create bulk fees | backup/api/endpoints/fees.py |
| PUT | `/api/fees/{fee_id}` | Update fee record | backup/api/endpoints/fees.py |
| POST | `/api/fees/{fee_id}/payment` | Record payment | backup/api/endpoints/fees.py |
| DELETE | `/api/fees/{fee_id}` | Delete fee record | backup/api/endpoints/fees.py |
| GET | `/api/fees/summary` | Get all fees summary | backup/api/endpoints/fees.py |
| GET | `/api/fees/overdue` | Get all overdue fees | backup/api/endpoints/fees.py |
| GET | `/api/fees/student/{student_id}` | Get student fees | backup/api/endpoints/fees.py |
| GET | `/api/fees/type/{fee_type}` | Get fees by type | backup/api/endpoints/fees.py |
| GET | `/api/fees/my-fees` | Get my fees | backup/api/endpoints/fees.py |
| GET | `/api/fees/my-fees/pending` | Get my pending fees | backup/api/endpoints/fees.py |
| GET | `/api/fees/my-fees/overdue` | Get my overdue fees | backup/api/endpoints/fees.py |
| GET | `/api/fees/my-fees/payment-history` | Get my payment history | backup/api/endpoints/fees.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/school/fees/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/fee_repository.py`, `backup/repositories/fee_structure_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## 4. Tests Module

**Target Location:** `modules/school/tests/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| POST | `/api/tests/` | Create test | backup/api/endpoints/tests.py |
| GET | `/api/tests/teacher/my-tests` | Get my tests | backup/api/endpoints/tests.py |
| GET | `/api/tests/teacher/{test_id}` | Get test for teacher | backup/api/endpoints/tests.py |
| PUT | `/api/tests/{test_id}` | Update test | backup/api/endpoints/tests.py |
| DELETE | `/api/tests/{test_id}` | Delete test | backup/api/endpoints/tests.py |
| GET | `/api/tests/{test_id}/results` | Get test results | backup/api/endpoints/tests.py |
| GET | `/api/tests/student/available` | Get available tests | backup/api/endpoints/tests.py |
| GET | `/api/tests/student/{test_id}` | Get test for student | backup/api/endpoints/tests.py |
| POST | `/api/tests/{test_id}/start` | Start test | backup/api/endpoints/tests.py |
| POST | `/api/tests/{test_id}/submit` | Submit test | backup/api/endpoints/tests.py |
| GET | `/api/tests/student/{test_id}/result` | Get test result | backup/api/endpoints/tests.py |
| GET | `/api/tests/student/my-results` | Get my results | backup/api/endpoints/tests.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/school/tests/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/test_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## Migration Strategy

### Step 1: Analyze Existing Code
- Review `backup/api/endpoints/assignments.py`
- Review `backup/api/endpoints/grades.py`
- Review `backup/api/endpoints/fees.py`
- Review `backup/api/endpoints/tests.py`

### Step 2: Extract Logic
- Copy repository logic from backup/repositories/
- Adapt service layer for new structure
- Update schemas for new API format

### Step 3: Create New Modules
- Follow existing module pattern in modules/school/
- Use consistent naming conventions
- Implement proper error handling

### Step 4: Integration
- Register routes in main.py
- Add dependencies
- Update __init__.py exports

### Step 5: Testing
- Test each endpoint individually
- Verify authentication/authorization
- Check database integration

---

## Time Estimate

| Module | Development Time | Testing Time |
|--------|-----------------|--------------|
| Assignments | 2-3 days | 1 day |
| Grades | 1-2 days | 0.5 day |
| Fees | 2-3 days | 1 day |
| Tests | 3-4 days | 1-2 days |
| **Total** | **8-12 days** | **3.5-5.5 days** |

---

## Files to Reference

### Source Files (from backup/)
- `backup/api/endpoints/assignments.py`
- `backup/api/endpoints/grades.py`
- `backup/api/endpoints/fees.py`
- `backup/api/endpoints/tests.py`
- `backup/repositories/assignment_repository.py`
- `backup/repositories/grade_repository.py`
- `backup/repositories/fee_repository.py`
- `backup/repositories/fee_structure_repository.py`
- `backup/repositories/test_repository.py`

### Reference Templates (from modules/school/)
- `modules/school/student/`
- `modules/school/teacher/`

---

*Plan created: 2026-03-26*