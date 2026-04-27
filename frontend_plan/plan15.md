# Plan 15: Student Feature Pages - Complete Set

## Objective
Create all missing student pages to match backup/templates/student/ functionality 1:1.

## Current State
React has: Dashboard, Courses, Grades, Attendance, Assignments, Notices, ExamResults, Fees, Forum, Profile, StudentTeachers
React MISSING: messages, notes, videos, test list, test result, take test, timetable, library in dashboard

### 15.1 Assignments Page Enhancement
File: `frontend/src/modules/school/school_student/pages/Assignments.jsx`

Match backup/templates/student/assignments.html:
- [ ] Filter by status (All/Pending/Submitted)
- [ ] Filter by course
- [ ] List of assignments with:
  - Title (link to detail)
  - Course name
  - Due date
  - Status badge
  - Points/Weight
- [ ] Assignment detail page (AssignmentDetail.jsx exists)
- [ ] Submit assignment functionality

### 15.2 Messages Page
File: `frontend/src/modules/school/school_student/pages/Messages.jsx`

Match backup/templates/student/messages.html:
- [ ] Chat list sidebar
- [ ] Message conversation view
- [ ] Search contacts
- [ ] Unread badge indicators
- [ ] Message input with send button
- [ ] Timestamp display
- [ ] "No messages" empty state

### 15.3 Notes Page
File: `frontend/src/modules/school/school_student/pages/NotesPage.jsx`

Match backup/templates/student/notes.html:
- [ ] Subject/course filter
- [ ] Notes grid/list view toggle
- [ ] Each note shows:
  - Title
  - Subject
  - Teacher name
  - Upload date
  - Download button
- [ ] Search notes
- [ ] Download functionality

### 15.4 Videos Page
File: `frontend/src/modules/school/school_student/pages/Videos.jsx`

Match backup/templates/student/videos.html:
- [ ] Video grid
- [ ] Each video shows:
  - Thumbnail
  - Title
  - Course name
  - Duration
  - Views count
- [ ] Video player (embedded)
- [ ] Course filter

### 15.5 Timetable Page
File: `frontend/src/modules/school/school_student/pages/Timetable.jsx`

Match backup/templates/student/timetable.html:
- [ ] Weekly view table
- [ ] Rows: periods/time slots
- [ ] Columns: days (Mon-Fri)
- [ ] Each cell shows:
  - Subject name
  - Teacher name
  - Room number
- [ ] Download as PDF option

### 15.6 Test List Page
File: `frontend/src/modules/school/school_student/pages/TestList.jsx`

Match backup/templates/student/test_list.html:
- [ ] Filter by status (All/Upcoming/Completed)
- [ ] List shows:
  - Test title
  - Course
  - Date/Time
  - Duration
  - Status
- [ ] "Take Test" link

### 15.7 Take Test Page
File: `frontend/src/modules/school/school_student/pages/TakeTest.jsx`

Match backup/templates/student/take_test.html:
- [ ] Question display
- [ ] Options (multiple choice)
- [ ] Navigation (prev/next)
- [ ] Timer countdown
- [ ] Submit button
- [ ] Progress indicator

### 15.8 Test Result Page
File: `frontend/src/modules/school/school_student/pages/TestResult.jsx`

Match backup/templates/student/test_result.html:
- [ ] Score display
- [ ] Time taken
- [ ] Correct/incorrect breakdown
- [ ] Review answers

### 15.9 Profile Page Enhancement
File: `frontend/src/modules/school/school_student/pages/StudentProfile.jsx`

Already exists but enhance:
- [ ] Full profile display
- [ ] Edit profile form
- [ ] Profile photo upload
- [ ] Change password

## Priority
MEDIUM-HIGH

## Files to Create/Modify
- Create: `frontend/src/modules/school/school_student/pages/Messages.jsx`
- Create: `frontend/src/modules/school/school_student/pages/NotesPage.jsx`
- Create: `frontend/src/modules/school/school_student/pages/Videos.jsx`
- Create: `frontend/src/modules/school/school_student/pages/Timetable.jsx`
- Create: `frontend/src/modules/school/school_student/pages/TestList.jsx`
- Create: `frontend/src/modules/school/school_student/pages/TakeTest.jsx`
- Create: `frontend/src/modules/school/school_student/pages/TestResult.jsx`
- Enhance existing: `Attendance.jsx`, `Fees.jsx`, `Forum.jsx`, `StudentTeachers.jsx`