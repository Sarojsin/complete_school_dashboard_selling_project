Implementation Plan - Phase 4: Modern Authority & Admin Portal
This plan outlines the modernization of the Authority & Admin Portal, transforming it into a high-fidelity "Nerve Center" for school management with global analytics, streamlined user administration, and premium glassmorphic interfaces.

User Review Required
IMPORTANT

Global Analytics: The new dashboard will aggregate data from all modules (Revenue, Attendance, Staffing). Some data points might be simulated if real-time aggregation isn't available in the current backend repositories.

WARNING

User Management: Redesigning student/teacher management involves complex forms. We will prioritize a "Quick-Action" drawer for rapid edits while maintaining full-page views for detailed profiles.

Proposed Changes
1. API Service Layer
[MODIFY] 
authority.js
Update all endpoints to match the modular /api/v1/authorities/ structure.
Add analytics-specific fetchers for students, attendance, and finance.
2. Authority Dashboard (The Command Center)
[MODIFY] 
AuthorityDashboard.jsx
Design: Premium "Control Room" aesthetic with glassmorphic cards and 3D-effect stat visualizations.
Analytics: Integrated charts for enrollment trends and revenue performance (using simulated or real data).
Navigation: A tile-based grid for all administrative modules (Students, Staff, Finance, Library, etc.).
3. Staff & Student Administration
[MODIFY] 
Students.jsx
Redesign: High-fidelity student search & filter interface with bulk action support.
Profiles: Premium detailed view for individual student history and behavioral logs.
[NEW] 
Teachers.jsx
Design: Staff directory with department-based filtering and workload visualization.
4. Operational Control
[NEW] 
AdminFees.jsx
Features: Global fee collection monitoring and overdue alerts management.
[NEW] 
AdminAnalytics.jsx
Visuals: Comprehensive data visualizations for school-wide performance metrics.
Verification Plan
Automated Verification
Build Integrity: Run npm run build to verify Tailwind 4 and Lucide integration.
API Mapping: Verify all /api/v1/authorities/ endpoints return data using development tokens.
Manual Verification
Complex Forms: Test the student/teacher creation modals for validation and responsiveness.
Global Search: Verify the cross-module search functionality in the Admin dashboard.