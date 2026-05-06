# Day 18 Production Implementation Plan
**Date**: 2026-05-23
**Focus**: Analytics Dashboards & Real-time Metrics

## Objectives
- Implement analytics endpoints for college leadership roles (Dean, HOD, Registrar)
- Create aggregated metrics: enrollment trends, fee collection, faculty workload, student performance
- Provide chart-ready data (time-series, categorical breakdowns)
- Cache analytics results for performance (Redis 5-15 min TTL)
- Build simple response format for frontend consumption (JSON)

## Tasks

### 1. Morning: Requirements Gathering (1 hour)
**Define analytics metrics per role**:

**College Dean** (highest oversight):
- Total students, faculty, staff across all departments
- Enrollment trends by semester (last 12 months)
- Fee collection summary (collected vs pending, by program)
- Faculty workload distribution (courses taught per faculty)
- Department-wise student-to-faculty ratio
- Top-performing programs (GPA averages, pass rates if available)
- Monthly admission count
- Active research projects/publications count

**College HOD** (department-specific):
- Department student count (by program, by semester)
- Department faculty list (with workload)
- Course offerings current semester
- Student performance (exam results average) by course
- Department fee collection status
- Department research output (publications, patents)
- Lab equipment utilization (if applicable)

**College Registrar** (administrative):
- Enrollment numbers by program/semester
- Fee collection totals and outstanding
- Exam result publication status
- Student demographics (gender, region)
- Graduation rate estimates
- New admissions per intake

**Common**:
- Time-series: 12-month trend lines
- Filters: date range, department, program, semester

### 2. Service Layer Implementation (2.5 hours)
**Create `modules/college/college_analytics/service.py`** (new module):

```python
from datetime import datetime, date, timedelta
from sqlalchemy import func, extract, case
from modules.shared.database import get_db
from modules.college.college_student.models import CollegeStudent
from modules.college.college_faculty.models import CollegeFaculty
from modules.college.college_enrollments.models import Enrollment
from modules.college.college_programs.models import CollegeProgram
from modules.college.college_departments.models import CollegeDepartment
from modules.college.college_fee_records.models import CollegeFeeRecord
from modules.college.college_fee_collections.models import CollegeFeeCollection

class CollegeAnalyticsService:
    def __init__(self):
        self.cache_ttl = 900  # 15 minutes for analytics
    
    async def get_dean_overview(self, db: AsyncSession) -> dict:
        """High-level metrics for Dean dashboard"""
        cache_key = "analytics:dean:overview"
        cached = await cache_manager.get(cache_key)
        if cached:
            return cached
        
        # Student count
        student_count = await db.scalar(select(func.count(CollegeStudent.id)))
        
        # Faculty count
        faculty_count = await db.scalar(select(func.count(CollegeFaculty.id)))
        
        # Enrollment last 12 months
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)
        enrollment_trend = await db.execute(
            select(
                extract('month', Enrollment.enrollment_date).label('month'),
                extract('year', Enrollment.enrollment_date).label('year'),
                func.count(Enrollment.id).label('count')
            ).where(Enrollment.enrollment_date >= twelve_months_ago)
            .group_by('year', 'month')
            .order_by('year', 'month')
        )
        enrollment_trend_data = [{"month": r.month, "year": r.year, "count": r.count} for r in enrollment_trend]
        
        # Fee collection summary
        total_fees = await db.scalar(select(func.sum(CollegeFeeRecord.amount)))
        total_paid = await db.scalar(select(func.sum(CollegeFeeCollection.amount)))
        
        # Faculty workload (courses per faculty)
        from modules.college.college_courses.models import CollegeCourse
        workload = await db.execute(
            select(CollegeFaculty.id, func.count(CollegeCourse.id).label('course_count'))
            .outerjoin(CollegeCourse, CollegeCourse.instructor_id == CollegeFaculty.id)
            .group_by(CollegeFaculty.id)
        )
        workload_data = [{"faculty_id": r.id, "courses": r.course_count} for r in workload]
        
        # Department student ratio
        dept_stats = await db.execute(
            select(
                CollegeDepartment.name,
                func.count(CollegeStudent.id).label('student_count'),
                func.count(CollegeFaculty.id).label('faculty_count')
            )
            .outerjoin(CollegeStudent, CollegeStudent.department_id == CollegeDepartment.id)
            .outerjoin(CollegeFaculty, CollegeFaculty.department_id == CollegeDepartment.id)
            .group_by(CollegeDepartment.id, CollegeDepartment.name)
        )
        dept_ratios = [
            {
                "department": r.name,
                "students": r.student_count,
                "faculty": r.faculty_count,
                "ratio": round(r.student_count / r.faculty_count, 2) if r.faculty_count > 0 else None
            }
            for r in dept_stats
        ]
        
        result = {
            "total_students": student_count,
            "total_faculty": faculty_count,
            "enrollment_trend_12m": enrollment_trend_data,
            "fee_summary": {"total": total_fees, "collected": total_paid, "pending": total_fees - (total_paid or 0)},
            "faculty_workload": workload_data,
            "department_ratios": dept_ratios,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        await cache_manager.set(cache_key, result, ttl=self.cache_ttl)
        return result
    
    async def get_hod_dashboard(self, db: AsyncSession, department_id: int) -> dict:
        """Department-specific metrics for HOD"""
        cache_key =f"analytics:hod:dept{department_id}"
        cached = await cache_manager.get(cache_key)
        if cached:
            return cached
        
        # Students in department
        student_count = await db.scalar(
            select(func.count(CollegeStudent.id)).where(CollegeStudent.department_id == department_id)
        )
        
        # Faculty in department
        faculty_count = await db.scalar(
            select(func.count(CollegeFaculty.id)).where(CollegeFaculty.department_id == department_id)
        )
        
        # Courses offered this semester
        current_semester = await self._get_current_semester(db)
        course_count = await db.scalar(
            select(func.count(CollegeCourse.id)).where(
                CollegeCourse.department_id == department_id,
                CollegeCourse.semester_id == current_semester.id if current_semester else None
            )
        )
        
        # Student performance (avg marks from exam results if available)
        # If exam_section module has results, join with enrollments
        # Simplified for now
        performance_data = {"average_gpa": None, "pass_rate": None}  # TODO
        
        result = {
            "department_id": department_id,
            "students": student_count,
            "faculty": faculty_count,
            "courses_this_semester": course_count,
            "performance": performance_data,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        await cache_manager.set(cache_key, result, ttl=self.cache_ttl)
        return result
    
    async def get_registrar_report(self, db: AsyncSession, semester_id: int = None) -> dict:
        """Operational metrics for Registrar"""
        cache_key = f"analytics:registrar:semester{semester_id}" if semester_id else "analytics:registrar:all"
        cached = await cache_manager.get(cache_key)
        if cached:
            return cached
        
        if semester_id:
            # Enrollment count for specific semester
            enrollment_count = await db.scalar(
                select(func.count(Enrollment.id)).where(Enrollment.semester_id == semester_id)
            )
            # Fee collection by program
            fee_summary = await db.execute(
                select(
                    CollegeProgram.name,
                    func.count(CollegeFeeRecord.id).label('records'),
                    func.sum(CollegeFeeRecord.amount).label('total_amount'),
                    func.sum(case((CollegeFeeRecord.status == 'paid', 1), else_=0)).label('paid_count')
                )
                .join(CollegeFeeRecord, CollegeFeeRecord.program_id == CollegeProgram.id)
                .group_by(CollegeProgram.id, CollegeProgram.name)
            )
        else:
            enrollment_count = await db.scalar(select(func.count(Enrollment.id)))
            fee_summary = []  # all programs
        
        result = {
            "semester_id": semester_id,
            "total_enrollments": enrollment_count,
            "fee_summary_by_program": [dict(r) for r in fee_summary],
            "generated_at": datetime.utcnow().isoformat()
        }
        
        await cache_manager.set(cache_key, result, ttl=self.cache_ttl)
        return result
```

### 3. Router Layer (1 hour)
**Create `modules/college/college_analytics/router.py`**:

```python
from fastapi import APIRouter, Depends, Query
from modules.auth.dependencies import require_dean, require_hod, require_registrar
from modules.college.college_analytics.service import CollegeAnalyticsService

router = APIRouter(prefix="/api/v1/college/analytics", tags=["analytics"])

@router.get("/dean/overview")
async def dean_overview(current_user=Depends(require_dean), db: AsyncSession = Depends(get_college_async_db)):
    service = CollegeAnalyticsService()
    return await service.get_dean_overview(db)

@router.get("/hod/dashboard")
async def hod_dashboard(
    department_id: int,
    current_user=Depends(require_hod),
    db: AsyncSession = Depends(get_college_async_db)
):
    # Verify HOD is requesting own department
    if current_user.college_faculty.department_id != department_id:
        raise HTTPException(403, "Can only view own department")
    
    service = CollegeAnalyticsService()
    return await service.get_hod_dashboard(db, department_id)

@router.get("/registrar/summary")
async def registrar_summary(
    semester_id: int = None,
    current_user=Depends(require_registrar),
    db: AsyncSession = Depends(get_college_async_db)
):
    service = CollegeAnalyticsService()
    return await service.get_registrar_report(db, semester_id)

@router.get("/trends/enrollment")
async def enrollment_trends(
    months: int = Query(12, ge=1, le=36),
    current_user=Depends(require_dean),  # or any analytics role
    db: AsyncSession = Depends(get_college_async_db)
):
    """Time-series enrollment data for charting"""
    # Reuse dean service logic or extract common
    service = CollegeAnalyticsService()
    # ... return trends
```

### 4. Caching Integration (already done Day 12, but apply here) (30 min)
- [ ] Use `@cacheable` decorator on service methods (already in service)
- [ ] Cache key: per-metric + parameters (e.g., `analytics:dean:overview`)
- [ ] Invalidate on data change: when new enrollment created, delete `analytics:*` keys
- [ ] In service methods on write: `await cache_manager.invalidate_pattern("analytics:*")`

### 5. Chart Data Formatting (30 min)
Ensure JSON response is chart-ready:
```json
{
  "enrollment_trend_12m": [
    {"month": 1, "year": 2025, "count": 45},
    {"month": 2, "year": 2025, "count": 52}
  ]
}
```
Frontend can directly use for line/bar charts

### 6. Testing (1 hour)
**Tests** (`tests/college/test_analytics.py`):
- [ ] `test_dean_overview_contains_expected_keys()`
- [ ] `test_hod_dashboard_filters_by_department()`
- [ ] `test_registrar_summary_with_semester_filter()`
- [ ] `test_analytics_cached_returns_same_data()`
- [ ] `test_analytics_invalidated_on_enrollment_create()`

### 7. Documentation (30 min)
- [ ] `docs/analytics.md`: Metrics definitions, data sources, refresh frequency
- [ ] API docs: examples for each endpoint
- [ ] Update `README.md` with analytics availability

**Commit**:
- [ ] "feat(analytics): Add dean/HOD/registrar dashboards with aggregated metrics and Redis caching"

## Deliverables
- ✅ `modules/college/college_analytics/` (models if needed, schemas, service, router)
- ✅ 3 endpoints: `/analytics/dean/overview`, `/analytics/hod/dashboard`, `/analytics/registrar/summary`
- ✅ Time-series endpoint: `/analytics/trends/enrollment`
- ✅ Caching with 15 min TTL; invalidated on writes
- ✅ Unit + integration tests
- ✅ API documentation with examples

## Success Criteria
- Dean can see all aggregated data in one API call
- HOD sees only own department data (access control enforced)
- Data response includes `generated_at` timestamp and `cache_age` maybe
- Second call within 15 min is instant (Redis cache hit)
- Cache cleared when new enrollment added (next call regenerates)

## Notes
- Analytics queries can be heavy; use SQLAlchemy aggregate functions (func.count, func.sum, extract)
- Consider materialized views for complex aggregates if performance lags (future)
- Use pagination only if datasets large (dean overview is single-doc response)
- Add `@cacheable` with short TTL; analytics don't need real-time (15 min acceptable)

## Next: Day 19
Internationalization (i18n) implementation: add translation support for error messages, email templates, UI strings. Support at least English + one regional language (e.g., Hindi for India). Frontend React already has i18n; coordinate message keys.
