# Plan 4: Student Dashboard Complete Enhancement

## Objective
Enhance StudentDashboard to match backup/templates/student/dashboard.html quality.

## Current State (React)
- Only 3 basic stat cards (Courses, Assignments, Tests)
- No welcome banner with messages
- No upcoming assignments section
- No recent grades table
- No library section
- No notices
- No quick links
- No attendance overview

## Required Changes

### 4.1 Welcome Banner Section
Add personalized welcome with unread message count:
```jsx
<div className="welcome-banner mb-4">
  <div className="row align-items-center">
    <div className="col">
      <h4>👋 Welcome back, {user.full_name}!</h4>
      <p>Here's what's happening with your academics today.</p>
    </div>
    {unreadCount > 0 && (
      <div className="col-auto">
        <a href="/student/messages" className="btn btn-sm btn-light">
          <i className="bi bi-envelope me-1"></i>{unreadCount} new message(s)
        </a>
      </div>
    )}
  </div>
</div>
```

### 4.2 Stats Cards Row (6 cards)
Replace current 3 cards with:
1. **GPA Card** - gradient primary (#4361ee → #3a0ca3)
2. **Attendance Card** - gradient success (#10b981 → #059669)
3. **Pending Tasks Card** - gradient warning (#f59e0b → #d97706)
4. **Upcoming Tests Card** - gradient danger (#ef4444 → #dc2626)
5. **Library Books Card** - gradient purple (#8b5cf6 → #6d28d9) - with overdue badge
6. **Courses Card** - gradient info (#06b6d4 → #0891b2)

### 4.3 Upcoming Assignments Section
Card with list of assignments showing:
- Assignment title
- Course name
- Due date
- Status badge (pending/submitted/late)

### 4.4 Recent Grades Section
Table with columns:
- Course
- Assignment
- Grade (with color coding: green ≥90, blue ≥70, yellow ≥50, red <50)
- Date

### 4.5 Library Section
- Overdue alert if any books overdue
- List of currently borrowed books
- Total fines display
- Summary stats (total borrowed, returned, active)

### 4.6 Notices Section
- Most recent notice with priority badge
- Title and content preview (150 chars)
- "Read More" link

### 4.7 Quick Links Grid (8 buttons)
- Profile
- My Library
- Timetable
- Courses
- Notes
- Videos
- Fees
- Results

### 4.8 Attendance Overview
- Weekly attendance grid (Mon-Sun) per course
- Visual icons: ✓ (present), ✗ (absent), ⏰ (late)
- Performance summary table with progress bars

## Priority
HIGH - Main user-facing page

## Estimated Time
6-8 hours

## Files to Modify
- Modify: `frontend/src/modules/school/school_student/pages/StudentDashboard.jsx`
- Create: `frontend/src/modules/school/school_student/pages/StudentDashboard.css`

## API Endpoints Needed
- `/school/student/dashboard` - Full dashboard data
- `/school/student/assignments` - Upcoming assignments
- `/school/student/grades` - Recent grades
- `/school/student/library` - Library stats
- `/school/student/notices` - Recent notices
- `/school/student/attendance` - Attendance overview