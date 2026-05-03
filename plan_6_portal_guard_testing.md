# Plan 6: Portal Guard Testing

## Objective
Verify that the `require_school_portal` and `require_college_portal` dependencies enforce strict separation on both the frontend and backend.

## Implementation Steps

1. **Backend Route Protection Testing**:
   - **Scenario A**: Authenticate as a `school` user (get JWT token).
     - Attempt to access `GET /api/v1/college/student/me`.
     - **Expected Outcome**: HTTP 403 Forbidden ("Access restricted to college portal users").
   - **Scenario B**: Authenticate as a `college` user.
     - Attempt to access `GET /api/v1/school/student/me` (or any school route).
     - **Expected Outcome**: HTTP 403 Forbidden ("Access restricted to school portal users").

2. **Frontend Route Protection Testing**:
   - **Scenario C**: Log in as a `school` user.
     - Manually change the browser URL to `/college/student/dashboard`.
     - **Expected Outcome**: The `PrivateRoute` component should detect the mismatch and redirect the user back to their designated dashboard or to the unauthorized page.
   - **Scenario D**: Log in as a `college` user.
     - Manually change the browser URL to `/school/student/dashboard`.
     - **Expected Outcome**: Redirection away from the school dashboard.

3. **Portal Selection Persistence**:
   - Verify that when a user selects "College Portal" on the landing page, the `selectedSystem` (or equivalent) in `localStorage` persists correctly across page refreshes and determines API call behavior in `SignupPage`.
