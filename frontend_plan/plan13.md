# Plan 13: Parent & HOD Dashboard Enhancement

## Objective
Enhance Parent and HOD (Head of Department) dashboards to match backup/templates quality.

## Current State (React)
- ParentDashboard exists with basic data
- HOD pages exist but limited
- Missing stats, quick actions, child overview

## Required Changes

### 13.1 Parent Dashboard Enhancement

#### Child Overview Section
- List of children (if multiple)
- Each child: Name, Grade, Section
- Quick links to each child's details

#### Stats Row (per child or combined)
1. **Attendance** - Percentage
2. **Average Grades** - Score
3. **Pending Fees** - Amount
4. **Upcoming Events** - Count

#### Quick Actions
- View Attendance
- View Grades
- View Homework
- Pay Fees
- Contact Teacher

#### Recent Notices
- School notices relevant to parent
- Child-specific notices

#### Messages/Chat
- Quick chat with teachers

### 13.2 HOD Dashboard Enhancement

#### Department Overview
- Department name
- Total teachers
- Total students
- Total courses

#### Stats Row
1. **Teachers** - Count
2. **Students** - Count
3. **Courses** - Count
4. **Performance** - Average scores

#### Teachers List
- Name, designation, subjects
- Quick view profile

#### Students Performance
- Aggregate performance metrics
- Top performers
- At-risk students

#### Reports
- Department reports
- Export options

## Priority
MEDIUM - Supporting roles

## Estimated Time
4-5 hours

## Files to Modify
- Modify: `frontend/src/modules/school/school_parent/pages/ParentDashboard.jsx`
- Modify: `frontend/src/modules/school/school_hod/pages/HODDashboard.jsx`
- Modify: `frontend/src/modules/school/school_hod/pages/HODProfile.jsx`