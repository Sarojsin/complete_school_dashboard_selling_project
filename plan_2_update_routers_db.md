# Plan 2: Update College Routers Database Session

## Objective
Ensure all remaining college routers write to and read from `college_sell_db` instead of `school_sell_db`.

## Current State
`modules/college/college_student/router.py` has been updated to use `get_college_async_db`.
Other college routers/apis are still importing and using `get_db` from `modules.shared.database`.

## Implementation Steps

1. **Target Files**:
   - `modules/college/college_faculty/router.py` (and `api.py` if present)
   - `modules/college/college_placement/router.py` & `api.py`
   - `modules/college/college_research/router.py` & `api.py`
   - `modules/college/college_lab/router.py` & `api.py`
   - `modules/college/college_hostel/router.py` & `api.py`
   - `modules/college/college_courses/router.py` & `api.py`
   - `modules/college/college_hod/api.py`
   - `modules/college/college_dean/api.py`
   - `modules/college/college_registrar/api.py`
   - `modules/college/college_exam_section/api.py`
   - `modules/college/college_account_section/api.py`
   - `modules/college/college_semesters/api.py`
   - `modules/college/college_programs/api.py`
   - `modules/college/college_enrollments/api.py`
   - `modules/college/college_library/api.py`

2. **Refactoring Steps for Each File**:
   - Replace import:
     ```python
     # Remove
     from modules.shared.database import get_db
     # Add
     from modules.college.database import get_college_async_db
     ```
   - Replace `Depends(get_db)` with `Depends(get_college_async_db)` in all endpoint parameter lists.
   
3. **Validation**:
   - Perform a global search across `modules/college/` for `get_db` to ensure all instances have been replaced.
   - Start the FastAPI server and verify no startup errors occur due to missing imports.
