# Plan 5: Create Missing College Frontend Pages

## Objective
Develop the missing frontend dashboard pages for college-specific roles.

## Current State
`CollegeTeacherDashboard` and `StudentDashboard` (under `college_placement`) exist, but others are missing.

## Implementation Steps

1. **Scaffold Layouts**:
   - Duplicate the base layout structure used for School dashboards.
   - Ensure the sidebar navigation is tailored for College modules.

2. **Create Role-Specific Dashboards**:
   Create the following pages under `frontend/src/modules/college/`:
   - `college_hod/pages/HODDashboard.jsx`
   - `college_dean/pages/DeanDashboard.jsx`
   - `college_registrar/pages/RegistrarDashboard.jsx`
   - `college_exam_section/pages/ExamDashboard.jsx`
   - `college_account_section/pages/AccountDashboard.jsx`
   - `college_library/pages/LibraryDashboard.jsx`
   - `college_lab/pages/LabDashboard.jsx`
   - `college_hostel/pages/HostelDashboard.jsx`
   - `college_research/pages/ResearchDashboard.jsx`

3. **Update Router Configuration**:
   - In `frontend/src/App.jsx` (or the respective router file), register these new routes.
   - Wrap all of these routes in the `PrivateRoute` component with `allowedPortal="college"`.

4. **Integrate APIs (Mock or Real)**:
   - Initially, map these dashboards to placeholder data.
   - Gradually integrate with the newly updated `college_sell_db`-backed routers.
