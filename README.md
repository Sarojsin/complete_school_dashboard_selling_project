# School & College Management System

A comprehensive dual-portal educational management system built with FastAPI (backend) and React (frontend). The system handles both school and college operations with strict data separation, portal-specific routing, and role-based access control.

## Architecture

### Dual-Database Separation

The system uses **two separate databases** to ensure complete isolation between school and college data:

- **School Database** (`school_sell_db`): Contains all school-related tables (teachers, students, classes, courses, assignments, etc.)
- **College Database** (`college_sell_db`): Contains all college-related tables (departments, programs, faculty, research, placements, etc.)

Configuration is controlled via the `DATABASE_MODE` environment variable:

| Value | Behavior |
|-------|----------|
| `separate` (production) | Uses `COLLEGE_DATABASE_URL` for college, `DATABASE_URL` for school |
| `school_only` | Single database with school schema only |
| `college_only` | Single database with college schema only |

### Portal Type & User Identity

Every user has a `portal_type` field (`'school'` or `'college'`) stored in the central `users` table (in school database by default, depending on config). This determines:

- Which dashboard the user is redirected to after login
- Which API routes they can access
- Which frontend routes they are allowed to visit

### Backend Route Protection

College routes are protected using the `require_college_portal` dependency in FastAPI. School routes use `require_school_portal`. These dependencies check the authenticated user's `portal_type` and return HTTP 403 if there's a mismatch.

Example:
```python
from modules.auth.dependencies import require_college_portal

router = APIRouter(dependencies=[Depends(require_college_portal)])
```

### Frontend Route Protection

The `PrivateRoute` component wraps protected routes and checks the user's `portal_type` from localStorage against the `allowedPortal` prop:

- College routes: `<PrivateRoute allowedPortal="college">`
- School routes: `<PrivateRoute allowedPortal="school">`

Mismatched access results in automatic redirection to the appropriate dashboard.

## Project Structure

```
├── app/main.py                 # FastAPI app & router registration
├── modules/
│   ├── auth/                   # Authentication (login, signup, JWT)
│   ├── shared/                 # Shared utilities, DB, models, exceptions
│   ├── school/                 # School-specific modules
│   │   ├── school_teacher/
│   │   ├── school_student/
│   │   ├── school_parent/
│   │   ├── school_authority/
│   │   ├── school_hod/
│   │   ├── school_exam_section/
│   │   ├── school_account_section/
│   │   ├── school_library/
│   │   └── ... (other school modules)
│   └── college/                # College-specific modules
│       ├── college_faculty/
│       ├── college_student/
│       ├── college_hod/
│       ├── college_dean/
│       ├── college_registrar/
│       ├── college_exam_section/
│       ├── college_account_section/
│       ├── college_library/
│       ├── college_lab/
│       ├── college_hostel/
│       ├── college_research/
│       ├── college_placement/
│       └── ... (other college modules)
├── backup/
│   └── models/
│       └── college/            # Single source of truth for college models
├── frontend/
│   └── src/
│       ├── App.jsx             # Route definitions
│       └── modules/
│           ├── auth/
│           ├── school/
│           └── college/
└── tests/
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# Core Settings
APP_NAME="EduManage"
SECRET_KEY="your-secret-key-here"
ENVIRONMENT="development"

# School Database (also stores central users table)
DATABASE_URL=postgresql://user:pass@localhost/school_sell_db

# College Database (separate)
COLLEGE_DATABASE_URL=postgresql://user:pass@localhost/college_sell_db

# Portal Mode (optional, defaults to separate)
DATABASE_MODE=separate
```

## Getting Started

### 1. Database Setup

Create two PostgreSQL databases:

```sql
CREATE DATABASE school_sell_db;
CREATE DATABASE college_sell_db;
```

Run migrations (Alembic) to create tables:

```bash
# For school
alembic -c alembic.ini upgrade head

# For college (if separate)
alembic_college -c alembic_college.ini upgrade head
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API will be available at http://localhost:8000

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:5173 (or 3000)

## Key Design Decisions

### Single Source of Truth for College Models

All shared college entity definitions (Department, Program, Semester, Faculty, CollegeStudent, Enrollment, etc.) live exclusively in `backup/models/college/`. The `modules/college/*/models.py` files only define **module-specific** tables (e.g., `college_courses` links to Department, Semester but doesn't redefine them). This avoids duplicate mapper registration and circular dependencies.

### Database Session Management

- School routes use `get_db` from `modules.shared.database`
- College routes use `get_college_async_db` from `modules.college.database`

### Portal Selection Flow

1. User visits landing page → clicks portal button (school/college)
2. Selection saved to `localStorage` as `selectedSystem`
3. Signup form respects this selection and sets `portal_type` accordingly
4. After login, `DashboardRedirector` reads `user.portal_type` and routes to correct dashboard
5. Frontend `PrivateRoute` enforces portal separation on client-side navigation

## Testing

### Backend Portal Guard Tests

```bash
pytest tests/test_portal_guard.py -v
```

This verifies:
- School users can access school endpoints (200)
- College users can access college endpoints (200)
- School users forbidden from college endpoints (403)
- College users forbidden from school endpoints (403)

### Frontend Manual Portal Guard Tests

See `tests/frontend_portal_guard_manual.md` for step-by-step manual testing of client-side redirection and localStorage persistence.

## Adding New College Modules

When creating a new college module:

1. **Define module-specific models** in `modules/college/<module>/models.py` that inherit from `CollegeBase`
2. **Import shared college models** from `backup.models.college` (Department, Program, Semester, Faculty, etc.)
3. **Use college database** in repository: `from modules.college.database import get_college_async_db`
4. **Protect routes** in API: `router = APIRouter(dependencies=[Depends(require_college_portal)])`
5. **Create frontend pages** under `frontend/src/modules/college/<module>/pages/`
6. **Register routes** in `App.jsx` with `<PrivateRoute allowedPortal="college">`

## Troubleshooting

### "Multiple classes found for table" Error

Cause: Duplicate model definitions for the same table (e.g., Department defined in both `backup.models.college` and a module's models.py).
Fix: Remove duplicate class definitions; import from backup only.

### Portal Mismatch (403 Forbidden)

Check:
- User's `portal_type` in database matches the route prefix (`school` vs `college`)
- Frontend `PrivateRoute` has correct `allowedPortal` prop
- Backend router has correct `require_school_portal` or `require_college_portal` dependency

### Database Connection Issues

Verify `DATABASE_URL` and `COLLEGE_DATABASE_URL` are correctly set and point to separate databases. Use `scripts/verify_schema.py` to check table counts.
