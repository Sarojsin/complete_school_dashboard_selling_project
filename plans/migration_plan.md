# Migration Plan: Current Project → School & College Structure

**Current Project:** Mixed structure (flat modules)  
**Target:** school_collage_structure.md  
**Goal:** Restructure into modular School & College systems

---

## Current Project Structure (What You Have)

```
app/
├── api/endpoints/         # All endpoints mixed (students, teachers, admin...)
├── core/                 # Config, database
├── dependencies/         # Auth dependencies
├── middleware/           # Feature check, security
├── models/               # All models flat (models.py, admin_models.py, etc.)
├── repositories/         # All repositories flat
├── schemas/             # All schemas flat
├── services/            # All services flat
├── templates/           # Flat template folders
├── web/routes/         # Web routes mixed
└── websocket/          # WebSocket handlers
```

---

## Target Structure (What You Want)

```
app/
├── core/                 # Shared (config, database, auth)
├── shared/              # Shared modules
│   ├── auth/
│   ├── middleware/
│   └── utils/
├── models/              # Base + school/college folders
│   ├── school/
│   └── college/
├── modules/             # Feature modules
│   ├── school/
│   │   ├── authority/
│   │   ├── teacher/
│   │   ├── student/
│   │   ├── parent/
│   │   ├── exam_section/
│   │   ├── account_section/
│   │   └── library/
│   └── college/
│       ├── dean/
│       ├── hod/
│       ├── faculty/
│       ├── student/
│       ├── registrar/
│       ├── exam_section/
│       ├── account_section/
│       ├── library/
│       ├── placement/
│       ├── research/
│       ├── hostel/
│       └── lab/
└── web/
    ├── routes/
    │   ├── school/
    │   └── college/
    └── templates/
        ├── school/
        └── college/
```

---

## Migration Phases

### Phase 1: Setup Shared Infrastructure
**Duration:** 1-2 days

#### Tasks:
1. Create `app/shared/` directory structure
2. Move authentication to `app/shared/auth/`
3. Move middleware to `app/shared/middleware/`
4. Move utils to `app/shared/utils/`
5. Update imports across project

#### Files to Create:
- `app/shared/__init__.py`
- `app/shared/auth/__init__.py`
- `app/shared/auth/dependencies.py` (copy from dependencies/auth.py)
- `app/shared/auth/jwt.py` (extract from existing)
- `app/shared/middleware/__init__.py`

#### Files to Modify:
- `app/main.py` - Update imports

---

### Phase 2: Restructure Models
**Duration:** 2-3 days

#### Tasks:
1. Create `app/models/school/` folder
2. Create `app/models/college/` folder
3. Move existing models appropriately:
   - **To school:** models.py (Student, Teacher), parent.py → `app/models/school/`
   - **To college:** department_models.py, new college models → `app/models/college/`
4. Create base model in `app/models/base.py`
5. Update all imports

#### Mapping:

| Current File | New Location | Contains |
|-------------|--------------|----------|
| models.py | models/school/student.py | Student, User |
| models.py | models/school/teacher.py | Teacher |
| models.py | models/school/parent.py | Parent |
| parent.py | models/school/parent.py | Parent |
| department_models.py | models/college/department.py | Department |
| exam_models.py | models/school/exam.py | Exam |
| library_models.py | shared/library.py | Library (same for both) |
| account_models.py | shared/account.py | Account (same for both) |

---

### Phase 3: Create Module Structure
**Duration:** 3-5 days

#### Tasks:
1. Create `app/modules/school/` directory with all role modules
2. Create `app/modules/college/` directory with all role modules
3. Each module gets: models.py, repository.py, service.py, api.py

#### School Modules to Create:
```
app/modules/school/
├── authority/
│   ├── models.py
│   ├── repository.py
│   ├── service.py
│   └── api.py
├── teacher/
├── student/
├── parent/
├── exam_section/
├── account_section/
└── library/
```

#### College Modules to Create:
```
app/modules/college/
├── dean/
├── hod/
├── faculty/
├── registrar/
├── student/
├── exam_section/
├── account_section/
├── library/
├── placement/
├── research/
├── hostel/
└── lab/
```

---

### Phase 4: Restructure API Endpoints
**Duration:** 2-3 days

#### Tasks:
1. Create `app/api/v1/school/` folder
2. Create `app/api/v1/college/` folder
3. Move endpoints to appropriate folders:
   - Current `students.py` → `api/v1/school/students.py`
   - Current `teachers.py` → `api/v1/school/teachers.py`
   - Current `authority.py` → `api/v1/school/authorities.py`
   - Current `hod.py` → `api/v1/college/hod.py`
   - etc.

#### Update in main.py:
```python
# Old way
from app.api.endpoints import students, teachers

# New way
from app.api.v1.school import students, teachers
from app.api.v1.college import faculty, hod
```

---

### Phase 5: Restructure Templates
**Duration:** 2-3 days

#### Tasks:
1. Create `app/templates/school/` folder
2. Create `app/templates/college/` folder
3. Move templates:
   - `templates/student/` → `templates/school/student/`
   - `templates/teacher/` → `templates/school/teacher/`
   - `templates/authority/` → `templates/school/authority/`
   - `templates/hod/` → `templates/college/hod/`
   - `templates/exam_section/` → `templates/college/exam_section/` (for college)
   - Keep `templates/student/` as `templates/school/student/` equivalent

---

### Phase 6: Create College-Specific Features
**Duration:** 5-7 days

#### New College Modules to Build:
1. **Placement Cell**
   - Companies CRUD
   - Job postings
   - Applications
   - Placement drives

2. **Research**
   - Research projects
   - Publications
   - Grants management

3. **Hostel**
   - Room allocation
   - Mess management
   - Complaints

4. **Lab**
   - Equipment management
   - Lab bookings

5. **Registrar**
   - Enrollment management
   - Transcripts
   - Certificates

---

### Phase 7: Database Separation (Optional)
**Duration:** 3-5 days

#### Tasks:
1. Set up PostgreSQL databases:
   - `school_db` (migrate existing data)
   - `college_db` (new database)
   - `auth_db` (shared authentication)
2. Update database connections
3. Create migration scripts

#### If keeping single database:
- Add `institution_type` column to key tables
- Update queries to filter by institution

---

### Phase 8: Testing & Deployment
**Duration:** 2-3 days

#### Tasks:
1. Test all school features
2. Test all college features
3. Test authentication
4. Update documentation

---

## Summary of Phases

| Phase | Duration | Focus |
|-------|----------|-------|
| Phase 1 | 1-2 days | Shared Infrastructure |
| Phase 2 | 2-3 days | Restructure Models |
| Phase 3 | 3-5 days | Create Module Structure |
| Phase 4 | 2-3 days | Restructure API Endpoints |
| Phase 5 | 2-3 days | Restructure Templates |
| Phase 6 | 5-7 days | Create College Features |
| Phase 7 | 3-5 days | Database Separation |
| Phase 8 | 2-3 days | Testing & Deployment |

**Total Estimated Time:** 18-31 days

---

## Priority Order (What to Do First)

1. **Week 1-2:** Phase 1 + Phase 2 (Foundation)
2. **Week 3:** Phase 3 (Module structure)
3. **Week 4:** Phase 4 (API restructuring)
4. **Week 5:** Phase 5 (Templates)
5. **Week 6-7:** Phase 6 (College features)
6. **Week 8:** Phase 7 (Database)
7. **Week 9:** Phase 8 (Testing)

---

## Files That Will Be Created

### New Directories:
```
app/shared/
app/models/school/
app/models/college/
app/modules/school/
app/modules/college/
app/api/v1/school/
app/api/v1/college/
app/web/routes/school/
app/web/routes/college/
app/templates/school/
app/templates/college/
```

### New Files:
- 7 school modules (authority, teacher, student, parent, exam_section, account_section, library)
- 12 college modules (dean, hod, faculty, registrar, student, exam_section, account_section, library, placement, research, hostel, lab)

---

## Backward Compatibility

During migration:
1. Keep old endpoints working alongside new ones
2. Use redirects from old URLs to new
3. Deprecate old endpoints gradually
4. Update clients slowly

---

*End of Migration Plan*
