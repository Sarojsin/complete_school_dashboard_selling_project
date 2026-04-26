Implementation Plan - Frontend Plan 2: Modern Teacher Experience
This plan details the modernization of the Teacher Portal, focusing on a high-productivity, glassmorphic UI that integrates seamlessly with the new modular FastAPI backend.

User Review Required
IMPORTANT

Aesthetic Consistency: All teacher pages will follow the same glassmorphic design language established in Plan 1 (Student Portal) to ensure a unified product feel. Logic Verification: I will migrate the existing logic for attendance taking and grading to the new UI containers. Please confirm if there are any specific "New" features (like bulk grading) you want to see.

Proposed Changes
1. API Integration Layer
Update the teacher API service to map to the new modular backend structure.

[MODIFY] 
teachers.js
Update base URL mapping to /api/v1/teachers/*.
Ensure all methods (getTeacherDashboard, getTeacherCourses, etc.) are async/await compliant.
2. Teacher Dashboard (Command Center)
Redesign the primary entry point for teachers.

[MODIFY] 
TeacherDashboard.jsx
Implement ModernStatCard for key metrics (Students, Classes, Grading).
Create a "Quick Action" grid with glassmorphic buttons.
Design a high-fidelity "Today's Schedule" timeline.
3. Class & Student Management
Redesign the course list and student rosters.

[MODIFY] 
Courses.jsx
[MODIFY] 
Students.jsx
use GlassCard for course cards.
Implement a searchable, paginated student table with premium styling.
4. Assignment & Grading Portal
Streamline the workflow for creating and evaluating assignments.

[MODIFY] 
Assignments.jsx
[MODIFY] 
TeacherViewSubmissions.jsx
Redesign the assignment list with status badges (Draft, Published, Grading).
Create a split-screen grading view (Submission vs. Grade Input).
5. Attendance & Resource Hub
Modernize the attendance-taking experience and resource uploads.

[MODIFY] 
TeacherTakeAttendance.jsx
[MODIFY] 
TeacherUploadNotes.jsx
Implement a "Quick Attendance" toggle list for classes.
Design a drag-and-drop file upload interface for notes and videos.
Verification Plan
Automated Tests
Run npm run build after each phase to ensure zero syntax errors.
Verify API response mapping with console logging during development.
Manual Verification
Test navigation between all redesigned teacher pages.
Verify "Take Attendance" form submission logic.
Ensure responsive design on mobile and tablet views (using browser tool if possible).