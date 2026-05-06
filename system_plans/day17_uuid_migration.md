# Day 17 Production Implementation Plan
**Date**: 2026-05-22
**Focus**: UUID Migration for Public Resource Identifiers

## Objectives
- Replace integer primary keys with UUIDs for all public-facing resources to prevent ID enumeration attacks
- Implement zero-downtime migration strategy using dual-key approach
- Update all API endpoints to accept/return UUIDs instead of integers
- Update foreign key relationships across college modules
- Ensure backward compatibility where needed (internal references)

## Background: Why UUIDs?
- Auto-increment integer IDs allow attackers to guess sequential IDs (e.g., `/students/1`, `/students/2`)
- Exposes user count, allows scraping, unauthorized data access if auth flaws exist
- UUIDs (v4 random) are unguessable and non-sequential
- Trade-off: Slightly larger index size, harder to debug manually

## Scope
**Affected tables** (public-facing resources):
- college_students
- college_faculty
- college_courses
- college_enrollments
- college_programs
- college_semesters
- college_departments
- college_exam_notices
- college_fee_records
- college_fee_structures
- college_library_books, college_library_book_loans
- college_hostels, college_rooms, college_hostel_allocations
- college_research_projects, research_publications, research_patents
- placement_companies, placement_jobs, placement_applications

**Internal tables** (can keep integer PK):
- users (auth internal; but consider if user_id exposed)
- college_faculty_payments
- college_lab_equipment
- college_lab_schedules
- audit_logs, sessions, tokens

## Tasks

### 1. Morning: Shared UUID Mixin (1 hour)
**Create `modules/shared/models.py` mixin**:
```python
import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class UUIDMixin:
    """Mixin for models using UUID primary keys (PostgreSQL only)"""
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
```

**Note**: For SQLite (school DB), UUID stored as TEXT (String). Create conditional:
```python
def UUIDColumn():
    """Return appropriate UUID column type based on dialect"""
    if settings.DATABASE_MODE == "separate" and settings.COLLEGE_DATABASE_URL.startswith("postgresql"):
        return PG_UUID(as_uuid=True)
    else:
        return String(36)  # UUID as hex string
```

### 2. Alembic Batched Migration (Zero-Downtime) (3 hours)
**Strategy**: Use Alembic batch mode for PostgreSQL; handles both schema and data migration safely

**Create migration**: `alembic_college/versions/20260522_migrate_to_uuid.py`

```python
"""Migrate integer PKs to UUID for college tables (zero-downtime)"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# Helper: generate UUID from integer via hash (deterministic mapping)
def generate_uuid_from_id(old_id: int) -> str:
    import hashlib
    # Create UUID v5 (namespace + name) using fixed namespace
    namespace = uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')  # classic DNS namespace
    return str(uuid.uuid5(namespace, str(old_id)))

def upgrade():
    # Step 1: For each table, add new UUID column
    # Step 2: Populate UUID from existing ID
    # Step 3: Add new temporary UUID PK constraint (or swap)
    # Step 4: Drop old integer PK, rename UUID to id
    # Step 5: Update FKs in dependent tables
    
    bind = op.get_bind()
    
    tables_order = [
        ("college_departments", None),
        ("college_programs", "college_departments", "department_id"),
        ("college_semesters", None),
        ("college_courses", ["college_departments", "college_semesters"], ["department_id", "semester_id"]),
        ("college_faculty", ["college_departments"], ["department_id"]),
        ("college_students", ["college_departments", "college_programs"], ["department_id", "program_id"]),
        ("college_enrollments", ["college_students", "college_programs", "college_semesters"], ["student_id", "program_id", "semester_id"]),
        # ... continue for all 23 tables
    ]
    
    for table_name, parent_tables, fk_cols in tables_order:
        # 1. Add uuid column
        op.add_column(table_name, sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True))
        
        # 2. Populate uuid from id
        # UPDATE table SET uuid = gen_random_uuid() WHERE id IS NOT NULL;
        # For deterministic mapping across environments, use uuid5 hash:
        op.execute(f"UPDATE {table_name} SET uuid = gen_random_uuid()")  # random UUIDs; simpler
        
        # 3. Set NOT NULL
        op.alter_column(table_name, 'uuid', nullable=False)
        
        # 4. Drop PK constraint (need to find constraint name)
        # Get constraint name from pg_constraint
        # op.drop_constraint(table_name + '_pkey', table_name, type_='primary')
        
        # 5. Add new PK on uuid
        # op.create_primary_key(table_name + '_pkey', table_name, ['uuid'])
        
        # 6. Rename column id -> old_id, uuid -> id
        # op.alter_column(table_name, 'id', new_column_name='old_id')
        # op.alter_column(table_name, 'uuid', new_column_name='id')
        
        # 7. Recreate FK constraints pointing to new UUID PKs
        if parent_tables:
            for parent_table in parent_tables:
                # Find FK constraint from this table to parent
                # Drop old FK, create new one on uuid → parent.uuid
                pass  # detailed per-table FK update required

def downgrade():
    # Reverse: swap back to integer PKs
    # Complex; ensure backup before running upgrade
    pass
```

**IMPORTANT**: This is a complex multi-step migration. Simplify approach:

**Simplified approach** (safer for Day 17 limited time):
1. Keep existing `id` integer PK as-is (primary key, auto-increment)
2. Add new column `public_id` (UUID) with `UNIQUE` constraint and `NOT NULL`
3. Backfill `public_id` with `gen_random_uuid()` for all existing rows
4. Update all API endpoints to use `public_id` in URLs (e.g., `/students/{public_id}`)
5. Create index on `public_id` (unique)
6. Future: optionally drop old `id` PK in later sprint after verification

**Adopt simplified approach**:
- [ ] Migration: `alembic/versions/20260522_add_public_id_uuid.py`
  ```python
  op.add_column('college_students', sa.Column('public_id', postgresql.UUID(as_uuid=True), unique=True))
  op.execute("UPDATE college_students SET public_id = gen_random_uuid() WHERE public_id IS NULL")
  op.alter_column('college_students', 'public_id', nullable=False)
  op.create_index('ix_college_students_public_id', 'college_students', ['public_id'], unique=True)
  ```
- [ ] Apply to all 23 college tables in one migration (loop through table list)

### 3. Update Models (1 hour)
**Backup models**: Already in `backup/models/college/*.py`

**New models**: `modules/college/*/models.py` inherit from backup models directly

Thus: automatically get `public_id` column if added to backup models

**Update backup models**:
- [ ] Edit `backup/models/college/base.py` or each model file:
  ```python
  from sqlalchemy.dialects.postgresql import UUID
  import uuid
  
  class CollegeStudent(Base):
      __tablename__ = "college_students"
      id = Column(Integer, primary_key=True, autoincrement=True)  # keep internal
      public_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
      # ... other fields
  ```
- [ ] Apply same to faculty, programs, semesters, departments, courses, enrollments, etc.

**Important**: Keep `id` as PK for internal FK relationships; `public_id` used in APIs only

### 4. Update API Endpoints (2 hours)
**All college routers** need URL path changes:

**Before**:
```python
@router.get("/{student_id}")
async def get_student(student_id: int, ...): ...
```

**After**:
```python
@router.get("/{public_id}")
async def get_student(public_id: uuid.UUID, ...): ...
```

**Implementation**:
- [ ] Search all `router.get("/{something_id}")` and change param type to `UUID`
- [ ] In service/repository, query by `public_id` instead of `id`:
  ```python
  student = await db.execute(select(CollegeStudent).where(CollegeStudent.public_id == public_id))
  ```
- [ ] Update response schemas to include `public_id` field (already present)
- [ ] Update all foreign key accepts: when referencing a resource, expect UUID of parent

**Filtering**: If endpoints accept `?student_id=...`, change to `?student_public_id=...` or keep integer? 
- **Decision**: Keep integer `id` for internal filters (joins) but change external APIs to UUID
- Update repository queries to join on `id` internally; endpoints convert UUID→id lookup

**Helper function**:
```python
async def get_student_by_public_id(db: AsyncSession, public_id: uuid.UUID) -> CollegeStudent:
    result = await db.execute(select(CollegeStudent).where(CollegeStudent.public_id == public_id))
    student = result.scalar_one_or_none()
    if not student:
        raise NotFoundError("Student not found")
    return student
```

### 5. Update Tests (1 hour)
- [ ] All test data factories: use `uuid.uuid4()` when creating records (or let DB generate)
- [ ] Update test client calls: replace integer IDs with `str(public_id)` in URLs
- [ ] Ensure tests still pass

### 6. Documentation (30 min)
- [ ] `PUBLIC_IDS.md`: Explain public_id vs internal id, rationale
- [ ] Update API docs: all IDs are now UUID strings in responses
- [ ] Update frontend migration guide (must switch to UUID)

### 7. Deployment Considerations (30 min)
**Zero-downtime** strategy:
- **Phase 1** (today): Add `public_id` column, backfill, add unique index. Old APIs still use `id`. No breaking change.
- **Phase 2** (next week): Switch API endpoints to use `public_id` in URLs; keep `id` support internally. Old frontend may still use integer? Both work if we accept both params, but we choose to fully switch.
- **Phase 3** (future): Drop `id` column entirely (optional, long-term)

**For today**: We'll implement Phase 1 + Phase 2 simultaneously (controlled deploy):
- Deploy code that adds `public_id` column (migration run first)
- Update API endpoints to require UUID in routes
- Deploy frontend change simultaneously (both expect UUID)
- If rollback: keep old code accepting `id` (temporarily) – implement dual-mode for 1 week

### 8. Commit (30 min)
- [ ] `feat(security): Add UUID public_id to college tables; migrate API routes to use UUID for resource identification`
- [ ] Include migration, model changes, router updates, tests

## Deliverables
- ✅ Alembic migration: adds `public_id` UUID column (unique, not null) to 23 college tables
- ✅ Backup models updated with `public_id` column
- ✅ All college API endpoints changed: `/resource/{public_id}` with UUID type
- ✅ Repositories query by `public_id`
- ✅ Tests updated to use UUIDs
- ✅ ✅ Documentation: `PUBLIC_IDS.md`

## Success Criteria
- Migration applied cleanly to college DB (existing rows get UUID)
- `SELECT public_id FROM college_students LIMIT 1;` returns valid UUID v4
- API GET `/api/v1/college/students/{public_id}` works (where public_id is UUID string)
- Old integer ID no longer works in URLs (returns 404)
- All tests pass with UUIDs

## Notes
- PostgreSQL `gen_random_uuid()` from `pgcrypto` extension; ensure enabled: `CREATE EXTENSION IF NOT EXISTS "pgcrypto";` in migration
- SQLite fallback: use `str(uuid.uuid4())` stored as TEXT (auto-handled by SQLAlchemy)
- Use `uuid.UUID(hex=public_id_str)` conversion for Pydantic schema Field
- In schemas, define `public_id: uuid.UUID` – Pydantic handles string conversion
- Large data sets: backfilling 23 tables may take minutes; schedule downtime window

## Next: Day 18
Build analytics dashboards for dean, HOD, and registrar with aggregated metrics, charts data, and real-time stats using SQLAlchemy aggregate queries and Redis caching.
