# Plan 9: Grades Page Enhancement

## Objective
Enhance student/teacher Grades pages to match backup/templates quality.

## Current State (React - Student)
- Basic table with columns (Course, Assessment, Marks, Total Marks, Grade, Date)
- No GPA display
- No filter options
- No color-coded grade badges

## Required Changes

### 9.1 Student Grades Page Enhancement

#### Stats Row (4 cards)
1. **Current GPA** - Large number with trend indicator (↑ from last term)
2. **Average Grade** - Percentage with improvement
3. **Highest Grade** - Best score
4. **Total Assessments** - Count

#### Filter Dropdown
- All Semesters
- All Courses

#### Enhanced Grades Table
Columns with color coding:
- Course (bold)
- Assignment name
- Marks (colored based on score)
- Total Marks
- Grade (colored badge: A=green, B=blue, C=yellow, F=red)
- Date

#### Grade Distribution Chart (optional)
- Visual bar chart showing grade distribution

### 9.2 Teacher Grades Page Enhancement

#### Stats Row
1. **Total Grades Entered** - Count
2. **Pending Reviews** - Count
3. **Courses** - Number

#### Course-wise Grade Entry
- Select course
- Select assignment
- Enter grades for students

#### Recent Grade Entries
- List of recently entered grades
- Quick edit option

## Priority
MEDIUM - Important for academic tracking

## Estimated Time
4-5 hours

## Files to Modify
- Modify: `frontend/src/modules/school/school_student/pages/Grades.jsx`
- Modify: `frontend/src/modules/school/school_teacher/pages/TeacherGrades.jsx`
- Enhance: `frontend/src/modules/school/school_student/pages/Grades.css`