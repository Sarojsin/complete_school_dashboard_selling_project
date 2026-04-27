# Plan 8: Courses Page Enhancement

## Objective
Enhance student/teacher Courses pages to match backup/templates quality.

## Current State (React - Student)
- Basic list of courses
- No stats summary
- No filters
- No progress indicators

## Required Changes

### 8.1 Student Courses Page Enhancement

#### Stats Row (4 cards)
1. **Current Courses** - Number with "This semester" label
2. **Total Credits** - Number with "Required: X" label
3. **Average Grade** - Number with improvement indicator
4. **Completed** - Number with progress

#### Filter Dropdown
- All Semesters / Semester 1 / Semester 2
- Active Courses / Completed

#### Course Cards Grid
Each card should show:
- Course code
- Course name
- Teacher name
- Grade/Year
- Progress indicator
- "View Details" button

### 8.2 Teacher Courses Page Enhancement

#### Stats Row
1. **Total Courses** - Number
2. **Total Students** - Across all courses
3. **Active Assignments** - Pending
4. **Avg. Class Size** - Average

#### Course List with Details
- Course name
- Student count
- Upcoming deadlines
- Quick actions (view students, add grade, take attendance)

## Priority
MEDIUM - Important learning page

## Estimated Time
4-5 hours

## Files to Modify
- Modify: `frontend/src/modules/school/school_student/pages/Courses.jsx`
- Modify: `frontend/src/modules/school/school_teacher/pages/Courses.jsx`
- Enhance: `frontend/src/modules/school/school_student/pages/Courses.css`