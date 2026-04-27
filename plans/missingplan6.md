# Missing Endpoints Migration Plan - Priority 6: Admin Exams & Finance

**Plan 6: Admin Exam & Financial Management**

This plan covers Admin Exams and Finance modules.

## Module Overview

| Module | Missing Endpoints | Priority |
|--------|------------------|----------|
| Admin Exams | 9 endpoints | LOW |
| Admin Finance | 11 endpoints | LOW |

---

## 1. Admin Exams Module

**Target Location:** `modules/super_admin/exams/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/exam/types` | Get exam types | backup/api/endpoints/admin_exams.py |
| GET | `/api/exam/grading-scale` | Get grading scale | backup/api/endpoints/admin_exams.py |
| GET | `/api/exam/results` | Get exam results | backup/api/endpoints/admin_exams.py |
| POST | `/api/exam/results/publish` | Publish results | backup/api/endpoints/admin_exams.py |
| POST | `/api/exam/results/unpublish` | Unpublish results | backup/api/endpoints/admin_exams.py |
| GET | `/api/exam/notices` | Get exam notices | backup/api/endpoints/admin_exams.py |
| POST | `/api/exam/notices` | Create exam notice | backup/api/endpoints/admin_exams.py |
| GET | `/api/exam/stats` | Get exam stats | backup/api/endpoints/admin_exams.py |
| GET | `/api/exam/report-card/{student_id}` | Generate report card | backup/api/endpoints/admin_exams.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/exams/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/exam_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## 2. Admin Finance Module

**Target Location:** `modules/super_admin/finance/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/finance/structures` | Get fee structures | backup/api/endpoints/admin_finance.py |
| POST | `/api/finance/structures` | Create fee structure | backup/api/endpoints/admin_finance.py |
| PATCH | `/api/finance/structures/{structure_id}` | Update fee structure | backup/api/endpoints/admin_finance.py |
| GET | `/api/finance/records` | Get fee records | backup/api/endpoints/admin_finance.py |
| POST | `/api/finance/records/pay` | Record payment | backup/api/endpoints/admin_finance.py |
| POST | `/api/finance/records/refund` | Refund payment | backup/api/endpoints/admin_finance.py |
| POST | `/api/finance/penalty/apply` | Apply late penalty | backup/api/endpoints/admin_finance.py |
| GET | `/api/finance/reports/summary` | Get financial summary | backup/api/endpoints/admin_finance.py |
| GET | `/api/finance/reports/export` | Export financial report | backup/api/endpoints/admin_finance.py |
| GET | `/api/finance/invoice/{record_id}` | Generate invoice | backup/api/endpoints/admin_finance.py |
| GET | `/api/finance/stats` | Get finance stats | backup/api/endpoints/admin_finance.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/super_admin/finance/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/admin_finance_repository.py`
   - Source: `backup/repositories/fee_repository.py`
   - Source: `backup/repositories/fee_structure_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## Migration Strategy

### Step 1: Analyze Existing Code
- Review `backup/api/endpoints/admin_exams.py`
- Review `backup/api/endpoints/admin_finance.py`

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
- Test exam management operations
- Test financial operations
- Test report generation

---

## Time Estimate

| Module | Development Time | Testing Time |
|--------|-----------------|--------------|
| Admin Exams | 2-3 days | 1 day |
| Admin Finance | 2-3 days | 1 day |
| **Total** | **4-6 days** | **2 days** |

---

## Files to Reference

### Source Files (from backup/)
- `backup/api/endpoints/admin_exams.py`
- `backup/api/endpoints/admin_finance.py`
- `backup/repositories/exam_repository.py`
- `backup/repositories/admin_exam_repository.py`
- `backup/repositories/admin_finance_repository.py`
- `backup/repositories/fee_repository.py`
- `backup/repositories/fee_structure_repository.py`

### Reference Templates
- `modules/super_admin/` (for structure reference)

---

## Dependencies

- Admin Exams requires exam management system
- Admin Finance requires financial tracking system
- Both require admin role authentication

---

## Integration Notes

1. **Admin Exams Module:**
   - Should integrate with existing exam-section module
   - Need to handle grading scale configuration
   - Must manage result publication workflow

2. **Admin Finance Module:**
   - Should integrate with existing fees modules
   - Need to handle payment processing
   - Must generate proper invoices

---

*Plan created: 2026-03-26*