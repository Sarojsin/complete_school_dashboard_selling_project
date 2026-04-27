# Plan 16: Teacher Feature Pages - Complete Set

## Objective
Create all teacher pages to match backup/templates/teacher/ functionality 1:1.

### 16.1 Assignments Page
File: `frontend/src/modules/school/school_teacher/pages/Assignments.jsx`
- [ ] Enhance existing page
- [ ] List all assignments across courses
- [ ] Filter by course
- [ ] Filter by status (All/Active/Draft)
- [ ] Each shows:
  - Title
  - Course
  - Due date
  - Submissions count
  - Edit/Delete actions

### 16.2 Create Assignment Page
File: `frontend/src/modules/school/school_teacher/pages/CreateAssignment.jsx`
- [ ] Enhance existing page
- [ ] Form fields:
  - Title *
  - Course *
  - Description
  - Due date/time
  - Points
  - Attach file
- [ ] Preview before submit
- [ ] Save as draft

### 16.3 Edit Assignment Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherEditAssignment.jsx`
- [ ] Pre-populate form
- [ ] Update existing
- [ ] Re-open submissions

### 16.4 View Submissions Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherViewSubmissions.jsx`
- [ ] List of submitted students
- [ ] Each shows:
  - Student name
  - Submitted date
  - File attachment
  - Grade input
  - Feedback textarea
- [ ] Bulk grade option
- [ ] Download all files

### 16.5 Grades Page Enhancement
File: `frontend/src/modules/school/school_teacher/pages/TeacherGrades.jsx`
- [ ] Add/Edit grades
- [ ] Select course
- [ ] Select assignment/test
- [ ] Enter student grades
- [ ] Bulk import grades

### 16.6 Add Grade Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherAddGrade.jsx`
- [ ] Select course
- [ ] Select assessment
- [ ] Enter grades for all students
- [ ] Auto-calculate totals
- [ ] Submit all

### 16.7 Students Page
File: `frontend/src/modules/school/school_teacher/pages/Students.jsx`
- [ ] List enrolled students per course
- [ ] Search/filter
- [ ] View student detail
- [ ] View student's grades
- [ ] Contact parent

### 16.8 Student Detail Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherStudentDetail.jsx`
- [ ] Student profile
- [ ] Grades in each course
- [ ] Attendance record
- [ ] Notes/comments

### 16.9 Attendance Page Enhancement
File: `frontend/src/modules/school/school_teacher/pages/TeacherAttendance.jsx`
- [ ] Select course
- [ ] Select date
- [ ] Student list with P/A/L buttons
- [ ] Submit attendance

### 16.10 Take Attendance Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherTakeAttendance.jsx`
- [ ] Full attendance taking interface
- [ ] Student list with status buttons
- [ ] Date picker
- [ ] Remark field

### 16.11 View Attendance Session
File: `frontend/src/modules/school/school_teacher/pages/ViewAttendanceSession.jsx`
- [ ] Past session details
- [ ] Edit option

### 16.12 Courses Page Enhancement
File: `frontend/src/modules/school/school_teacher/pages/Courses.jsx`
- [ ] List of my courses
- [ ] Each shows:
  - Course details
  - Student count
  - Next class time
  - Actions

### 16.13 Course Detail Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherCourseDetail.jsx`
- [ ] Course info
- [ ] Enrolled students
- [ ] Assignments
- [ ] Tests
- [ ] Attendance sessions

### 16.14 Create Test Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherCreateTest.jsx`
- [ ] Test title
- [ ] Course
- [ ] Date/Time
- [ ] Duration
- [ ] Questions (MCQ/Essay)
- [ ] Add questions

### 16.15 Edit Test Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherEditTest.jsx`
- [ ] Edit test details
- [ ] Add/remove questions

### 16.16 View Tests Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherViewTests.jsx`
- [ ] List all tests
- [ ] View results
- [ ] Export grades

### 16.17 Timetable Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherTimetable.jsx`
- [ ] Weekly schedule
- [ ] Period-wise

### 16.18 Upload Notes Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherUploadNotes.jsx`
- [ ] Upload file
- [ ] Set subject
- [ ] Description

### 16.19 Upload Videos Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherUploadVideos.jsx`
- [ ] Upload video
- [ ] Set title, description
- [ ] Thumbnail

### 16.20 Chat Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherChat.jsx`
- [ ] Message students/parents
- [ ] Group chats

### 16.21 Profile Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherProfile.jsx`
- [ ] View profile
- [ ] Edit profile
- [ ] Change password

### 16.22 Create Notice Page
File: `frontend/src/modules/school/school_teacher/pages/TeacherNotices.jsx`
- [ ] Create new notice
- [ ] Select priority

## Priority
HIGH - Teacher portal is critical

## Files to Modify
- Enhance: All existing teacher pages
- Add: Missing pages with full backup/templates functionality