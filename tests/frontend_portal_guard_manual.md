# Frontend Portal Guard Testing (Manual)

## Overview
These are manual tests to verify that the frontend `PrivateRoute` component correctly enforces portal separation.

## Prerequisites
- Frontend development server running: `cd frontend && npm run dev`
- Backend server running: `uvicorn app.main:app --reload`
- A browser (Chrome/Firefox)

## Test Scenarios

### Scenario C: School User Accessing College Dashboard

1. Log in as a school user (e.g., student, teacher) via the normal login flow.
2. After login, you should be redirected to the school dashboard (e.g., `/student/dashboard` or `/teacher/dashboard`).
3. In the browser address bar, manually change the URL to: `http://localhost:5173/college/student/dashboard`
4. **Expected Outcome**: The `PrivateRoute` component detects that your `user.portal_type` is `"school"` and immediately redirects you away. You should be sent to your school dashboard or the login page.
5. Verify that the URL changes to a school route or `/login`.

### Scenario D: College User Accessing School Dashboard

1. Log in as a college user (e.g., college student) via the college portal selection.
2. After login, you should be at `/college/student/dashboard`.
3. Manually change the URL to: `http://localhost:5173/school/student/dashboard`
4. **Expected Outcome**: The `PrivateRoute` with `allowedPortal="college"` will block access and redirect you back to your college dashboard or login.
5. Confirm the path no longer starts with `/school`.

### Verification via Network Tab
- Open DevTools → Network.
- After attempting to navigate to the mismatched portal URL, observe if a navigation occurs and where you land.
- The PrivateRoute component does not make an API call; it just reads from `localStorage` and `user` object, then renders `<Navigate to=... />`.

## Portal Selection Persistence

The landing page (`LandingPage.jsx`) and signup flow use `localStorage` to remember the selected portal (`selectedSystem`). This determines which portal the user intends to sign up for and which dashboard they'll be redirected to after login.

### Test Steps:

1. Open the application in a fresh browser (or clear localStorage: `localStorage.clear()`).
2. On the landing page, click **"College Portal"** button.
   - This should call `localStorage.setItem('selectedSystem', 'college')`.
3. Open the browser console and verify:
   ```javascript
   console.log(localStorage.getItem('selectedSystem')); // should output "college"
   ```
4. Refresh the page. The `selectedSystem` should persist.
5. Now click **"School Portal"** and verify it changes to `"school"`.
6. Proceed to the signup page (`/register`). The signup form should indicate the college portal (e.g., the title says "College Student Sign Up" or similar).
7. Complete a test signup (with unique email). Ensure the API receives `portal_type: "college"` in the request payload.
8. After signup, login and verify you are redirected to `/college/student/dashboard`.
9. Repeat for school portal and verify school redirection.

### Automated Console Checks

Open the console on the landing page and run:

```javascript
// Test persistence
localStorage.removeItem('selectedSystem');
location.reload();
setTimeout(() => {
    const sel = localStorage.getItem('selectedSystem');
    console.log('After reload with no selection:', sel); // null or 'school' default?
}, 500);

// Set to college and check after reload
localStorage.setItem('selectedSystem', 'college');
location.reload();
setTimeout(() => {
    const sel = localStorage.getItem('selectedSystem');
    console.log('After reload set to college:', sel);
    // Also check if the College portal button is highlighted:
    const collegeBtn = document.querySelector('button[value="college"]');
    if (collegeBtn) console.log('College button active?', collegeBtn.classList.contains('active'));
}, 500);
```

**Expected**: The selectedSystem value remains after reload, and the UI correctly reflects the selection.

## Notes
- The frontend PrivateRoute component is located at `frontend/src/modules/shared/components/PrivateRoute.jsx`.
- Currently, college routes use `<PrivateRoute allowedPortal="college">` but school routes use `<PrivateRoute>` without `allowedPortal`. This means school routes are not strictly guarded on the frontend; a college user could theoretically access them if they know the URL. Backend guards still protect them. For full frontend separation, add `allowedPortal="school"` to all school routes.
- Backend route protection is enforced via `require_school_portal` and `require_college_portal` dependencies in `modules/auth/dependencies.py`. These are applied at the router level (or endpoint level) and return 403 Forbidden on mismatch.
