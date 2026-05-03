# Plan 7: Final Review & Cleanup

## Objective
Perform a final audit of the codebase to ensure all separations are clean, no temporary code remains, and the system is ready for production scaling.

## Implementation Steps

1. **Code Cleanup**:
   - Remove unused imports (e.g., leftover `from modules.shared.database import get_db` in college models).
   - Remove any temporary print statements or debug logs added during debugging of the dual-database setup.
   - Uncomment and properly configure the relationships in `Faculty` and other college models that were temporarily disabled to prevent circular dependencies.

2. **Database Verification**:
   - Check the schema of `college_sell_db` using a tool like DBeaver or pgAdmin.
   - Confirm exactly 23 tables exist and no school tables (like `school_assignments`) accidentally leaked into the college database.
   - Confirm `school_sell_db` holds the central `users` table and correctly points to profiles in both databases logically.

3. **Documentation**:
   - Update `README.md` to document the `DATABASE_MODE=separate` flag and the dual-database architecture.
   - Document the use of `portal_type` and the routing guards for future developers.

4. **Final End-to-End Walkthrough**:
   - Register a School User -> Login -> View Dashboard -> Verify DB insertion.
   - Register a College User -> Login -> View Dashboard -> Verify DB insertion.
   - Execute an overarching sanity check of the application UI to ensure no visual breakages.
