# Plan 4: Test College Student & Teacher Signup Flow

## Objective
Verify the end-to-end functionality of college student and teacher signups, ensuring data lands in the correct databases and routing works perfectly.

## Implementation Steps

1. **Test College Student Signup**:
   - Send `POST /api/v1/auth/signup/college/student` with payload including `portal_type: "college"`.
   - **Database Check**: 
     - Query `school_sell_db.users` to confirm the user was created with `portal_type='college'`.
     - Query `college_sell_db.college_students` to confirm the student profile was created.
   - **Login Test**: 
     - Authenticate via `POST /api/v1/auth/login`.
     - Verify the JWT token contains `portal_type: "college"`.
     - Ensure the frontend automatically routes to `/college/student/dashboard`.
   - **Data Fetch Test**: 
     - From the dashboard, verify that `GET /api/v1/college/student/me` successfully retrieves the student profile from `college_sell_db`.

2. **Test College Teacher Signup**:
   - (Requires Plan 1 completion)
   - Send `POST /api/v1/auth/signup/college/teacher` with payload including `portal_type: "college"`.
   - **Database Check**:
     - Query `school_sell_db.users` and `college_sell_db.college_faculty`.
   - **Login Test**:
     - Authenticate via `/api/v1/auth/login`.
     - Ensure routing directs the user to `/college/teacher/dashboard`.

3. **Debugging Flow**:
   - If 500 errors occur, inspect the server logs for missing parameters or uninitialized relationships.
   - If database connection errors occur, verify `college_sell_db` URL and ensure `college_faculty` tables exist.
