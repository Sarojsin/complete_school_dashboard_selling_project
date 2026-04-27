# Plan 10: Attendance Page Enhancement

## Objective
Enhance attendance pages to match backup/templates quality with visual grid and stats.

## Current State (React - Student)
- Basic list of attendance records
- No weekly grid view
- No summary stats
- No visual indicators

## Required Changes

### 10.1 Student Attendance Page Enhancement

#### Stats Row
1. **Overall Attendance** - Percentage with color (green ≥85%, yellow ≥75%, red <75%)
2. **Present Days** - Count
3. **Absent Days** - Count
4. **Late Days** - Count

#### Weekly Attendance Grid
- Rows: Courses
- Columns: Days of week (Mon-Sun)
- Cells: Icon (✓ green, ✗ red, ⏰ yellow, - gray)
- Highlight today column

#### Course-wise Summary Table
- Course name
- Present / Absent / Late counts
- Total classes
- Attendance rate with progress bar

#### Date Filter
- Select date range
- Select month

### 10.2 Teacher Attendance Page Enhancement

#### Stats Row
1. **Total Sessions** - Count
2. **Students Present** - Average percentage
3. **Pending Sessions** - Count to take

#### Take Attendance Feature
- Select course
- Select date
- Student list with Present/Absent/Late buttons
- Submit attendance

#### View Past Sessions
- List of taken attendance
- Edit option
- Download as CSV

## Priority
MEDIUM - Important for tracking

## Estimated Time
5-6 hours

## Files to Modify
- Modify: `frontend/src/modules/school/school_student/pages/Attendance.jsx`
- Modify: `frontend/src/modules/school/school_teacher/pages/TeacherAttendance.jsx`
- Create: `frontend/src/modules/school/school_attendance/styles/attendance.css`