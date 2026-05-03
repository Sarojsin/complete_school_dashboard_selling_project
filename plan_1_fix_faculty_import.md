# Plan 1: Fix Faculty Model Import

## Objective
Resolve the `Faculty` model import error preventing college teacher signup and other faculty-related endpoints from functioning correctly.

## Root Cause Analysis
The wrapper module `modules/college/college_faculty/models.py` imports `Faculty` from `backup/models/college/faculty.py` and aliases it as `CollegeFaculty` (`from backup.models.college.faculty import Faculty as CollegeFaculty`). Consequently, it does not expose `Faculty`, causing an `ImportError` when services (like `auth/service.py`) try to import `Faculty` from `modules.college.college_faculty.models`.

## Implementation Steps

1. **Update `modules/college/college_faculty/models.py`**:
   - Change the aliased export so `Faculty` is exported directly.
   - Or, just remove the alias and export `Faculty`.

   ```python
   # File: modules/college/college_faculty/models.py
   
   from backup.models.college.faculty import Faculty
   from modules.school.school_teacher.models import Teacher

   __all__ = ["Faculty", "Teacher"]
   ```

2. **Update `modules/auth/service.py` (if necessary)**:
   - Ensure the import statement matches the exported model name:
     `from modules.college.college_faculty.models import Faculty`
   - Alternatively, directly import from the backup model:
     `from backup.models.college.faculty import Faculty`

3. **Verify Faculty Relationships**:
   - In `backup/models/college/faculty.py`, check that commented-out relationships (`user`, `department`, etc.) do not break serialization or creation in the signup flow. 
   - Re-enable relationships cautiously by using string references (e.g., `"User"`, `"Department"`) to avoid circular imports during mapper initialization.

4. **Validation**:
   - Run `python -c "from modules.college.college_faculty.models import Faculty"` from the root directory to confirm the `ImportError` is resolved.
