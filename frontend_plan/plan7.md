# Plan 7: Super Admin Dashboard Complete Fix & Enhancement

## Objective
Fix broken SuperAdminDashboard and enhance to match backup/templates/admin/dashboard.html quality.

## Current State (React)
- **BUG**: Shows "Student Dashboard" title instead of "Super Admin Dashboard"
- Only shows profile info
- No rich sidebar
- No command center UI

## Required Changes

### 7.1 Fix Component Name
```jsx
// WRONG
export default function StudentDashboard() {

// CORRECT
export default function SuperAdminDashboard() {
```

### 7.2 Enhanced Sidebar with 15+ Items
Create admin-style sidebar with:
- Command Center
- User Management
- Academic
- Finance
- Feature Matrix
- Audit Spectrum
- System Tuning
- System Monitor
- Security Control
- Backups
- Reports
- Notice Board
- Communications
- Media Vault
- Advanced Tasks

### 7.3 Stats Cards Row
- Total Users
- Active Sessions
- System Health
- Storage Used

### 7.4 Module Grid
Clickable cards for all management sections

### 7.5 System Integrity Indicator
- Visual progress bar showing system health
- Last backup time
- Active connections

### 7.6 Quick Actions
- View All Users
- System Settings
- Create Backup

## Priority
CRITICAL - Bug fix + feature completion

## Estimated Time
4-5 hours

## Files to Modify
- Modify: `frontend/src/modules/super_admin/pages/SuperAdminDashboard.jsx`
- Create: `frontend/src/modules/super_admin/pages/SuperAdminDashboard.css`