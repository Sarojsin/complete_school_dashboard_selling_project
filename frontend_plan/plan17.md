# Plan 17: Authority Feature Pages - Complete Set

## Objective
Create all authority pages to match backup/templates/authority/ functionality 1:1.

### 17.1 Students Page
File: `frontend/src/modules/school/school_authority/pages/Students.jsx`
- [ ] Enhance existing
- [ ] Search students
- [ ] Filter by grade/class
- [ ] List shows:
  - Roll number
  - Name
  - Grade
  - Section
  - Parent contact
- [ ] Add student button
- [ ] Export list

### 17.2 Add Student Page
File: `frontend/src/modules/school/school_authority/pages/authority/AddStudent.jsx`
- [ ] Full registration form:
  - Personal info (name, DOB, gender)
  - Aadhaar number
  - Address
  - Parent info
  - Previous school
- [ ] Photo upload
- [ ] Generate roll number

### 17.3 Edit Student Page
File: `frontend/src/modules/school/school_authority/pages/authority/EditStudent.jsx`
- [ ] Pre-populate form
- [ ] Update student

### 17.4 Student Detail Page
File: `frontend/src/modules/school/school_authority/pages/authority/StudentDetail.jsx`
- [ ] Full student profile
- [ ] Academic record
- [ ] Fees history
- [ ] Attendance summary

### 17.5 Teachers Page
File: `frontend/src/modules/school/school_authority/pages/Teachers.jsx`
- [ ] List all teachers
- [ ] Search/filter by department
- [ ] List shows:
  - Employee ID
  - Name
  - Department
  - Designation
- [ ] Add teacher button
- [ ] Export list

### 17.6 Add Teacher Page
File: `frontend/src/modules/school/school_authority/pages/authority/AddTeacher.jsx`
- [ ] Registration form:
  - Personal info
  - Qualification
  - Experience
  - Department
  - Specialization
- [ ] Photo upload

### 17.7 Edit Teacher Page
File: `frontend/src/modules/school/school_authority/pages/authority/EditTeacher.jsx`
- [ ] Edit teacher info

### 17.8 Teacher Detail Page
File: `frontend/src/modules/school/school_authority/pages/authority/TeacherDetail.jsx`
- [ ] Full profile
- [ ] Assigned courses
- [ ] Classes taught

### 17.9 Courses Page
File: `frontend/src/modules/school/school_authority/pages/Courses.jsx`
- [ ] List all courses
- [ ] Add course
- [ ] Assign teacher
- [ ] View enrolled students

### 17.10 Add Course Page
File: `frontend/src/modules/school/school_authority/pages/authority/AddCourse.jsx`
- [ ] Course code
- [ ] Name
- [ ] Description
- [ ] Credits
- [ ] Teacher assignment

### 17.11 Edit Course Page
File: `frontend/src/modules/school/school_authority/pages/authority/EditCourse.jsx`
- [ ] Edit course

### 17.12 Course Detail Page
File: `frontend/src/modules/school/school_authority/pages/authority/CourseDetail.jsx`
- [ ] Course info
- [ ] Enrolled students
- [ ] Assignments
- [ ] Grades

### 17.13 Fees Page
File: `frontend/src/modules/school/school_authority/pages/authority/Fees.jsx`
- [ ] Fee structure overview
- [ ] Payment status list
- [ ] Filter by grade
- [ ] Collect fee
- [ ] Generate receipt

### 17.14 Fee Structure Page
File: `frontend/src/modules/school/school_authority/pages/authority/FeeStructure.jsx`
- [ ] Define fee heads
- [ ] Set amounts per grade
- [ ] Set due dates
- [ ] Late fee rules

### 17.15 Notices Page
File: `frontend/src/modules/school/school_authority/pages/Notices.jsx`
- [ ] List all notices
- [ ] Create notice
- [ ] Set priority
- [ ] Target audience

### 17.16 Add Notice Page
File: `frontend/src/modules/school/school_authority/pages/authority/AddNotice.jsx`
- [ ] Title
- [ ] Content (rich text)
- [ ] Priority
- [ ] Publish date
- [ ] Expiry date

### 17.17 Edit Notice Page
File: `frontend/src/modules/school/school_authority/pages/authority/EditNotice.jsx`
- [ ] Edit existing

### 17.18 View Notice Page
File: `frontend/src/modules/school/school_authority/pages/authority/ViewNotice.jsx`
- [ ] Full notice display

### 17.19 Analytics Page
File: `frontend/src/modules/school/school_authority/pages/authority/Analytics.jsx`
- [ ] Enrollment stats
- [ ] Fee collection charts
- [ ] Academic performance
- [ ] Attendance trends

### 17.20 Groups Page
File: `frontend/src/modules/school/school_authority/pages/Groups.jsx`
- [ ] List class groups
- [ ] Create group (class)
- [ ] Assign students
- [ ] Assign teacher

### 17.21 Create Group Page
File: `frontend/src/modules/school/school_authority/pages/authority/CreateGroup.jsx`
- [ ] Class name
- [ ] Assign teacher
- [ ] Add students

### 17.22 Manage Group Page
File: `frontend/src/modules/school/school_authority/pages/authority/ManageGroup.jsx`
- [ ] View members
- [ ] Add/remove students

### 17.23 Departments Page
File: `frontend/src/modules/school/school_authority/pages/Departments.jsx`
- [ ] List departments
- [ ] Add department
- [ ] Assign HOD

### 17.24 Reports Page
File: `frontend/src/modules/school/school_authority/pages/authority/Reports.jsx`
- [ ] Student report cards
- [ ] Fee collection report
- [ ] Attendance report
- [ ] Export options

## Priority
HIGH - Authority manages entire school

## Files to Modify
- Enhance: All existing authority pages
- Add: All missing CRUD operations matching backup/templates