## merging two endpoints/ api
@app.post("/student/profile") : occuring 1+1

## main issues 
## ENDPOINT DUPLICATES (Multiple Definitions):
Highest Duplicates:
GET /student/assignments - 3 times (lines 693, 763, 1091)
GET /teacher/assignments - 2 times (lines 349, 456)
GET /authority/courses/add - 2 times (lines 1377, 1386) + POST /authority/courses/add - 2 times (lines 1392, 1393)
GET /teacher/grades - 2 times (lines 359, 620)
GET /teacher/attendance - 2 times (lines 361, 575)
GET /teacher/tests - 2 times (lines 363, 588)
GET /teacher/timetable - 2 times (lines 365, 613)
GET /health - 2 times (lines 157, 176)
POST /teacher/students/{student_id}/contact - 2 times (lines 330, 733)
GET /teacher/assignments/{id}/edit - 2 times (lines 548, 662)

## AUTHENTICATION ENDPOINTS (14 endpoints):
GET / - 1
GET /health - 2 ❌ DUPLICATE
GET /logout - 1
GET /login - 1
GET /signup - 1
GET /signup/student - 1
GET /signup/teacher - 1
GET /signup/authority - 1
GET /signup/parent - 1
GET /register - 1
GET /register/student - 1
GET /register/teacher - 1
GET /register/parent - 1
GET /favicon.ico - 1

## STUDENT ENDPOINTS (28 endpoints):
GET /student/dashboard - 1
GET /student/profile - 1
POST /student/profile - 1
GET /student/courses - 1
GET /student/assignments - 3 ❌ TRIPLICATE (lines 693, 763, 1091)
GET /student/assignments/{assignment_id} - 2 ❌ DUPLICATE (lines 219, 1097)
POST /student/assignments/{assignment_id}/submit - 2 ❌ DUPLICATE (lines 233, 1103)
GET /student/grades - 1
GET /student/attendance - 1
GET /student/fees - 1
GET /student/tests - 1
GET /student/tests/{test_id}/start - 1
GET /student/tests/{test_id}/result - 1
GET /student/notices - 1
GET /student/timetable - 1
GET /student/notes - 1
GET /student/videos - 1
GET /student/forum - 1
GET /student/messages - 1
POST /student/messages/{message_id}/read - 1
GET /student/teachers - 1
POST /student/teachers/{teacher_id}/contact - 1
GET /student/groups - 1

## TEACHER ENDPOINTS (44 endpoints):
GET /teacher/dashboard - 1
GET /teacher/profile - 1
POST /teacher/profile - 1
GET /teacher/students - 1
GET /teacher/students/{student_id} - 1
GET /teacher/students/{student_id}/grades - 1
POST /teacher/students/{student_id}/contact - 2 ❌ DUPLICATE (lines 330, 733)
GET /teacher/messages - 1
POST /teacher/messages/{message_id}/read - 1
GET /teacher/assignments - 2 ❌ DUPLICATE (lines 349, 456)
GET /teacher/assignments/create - 1
POST /teacher/assignments/create - 1
GET /teacher/grades - 2 ❌ DUPLICATE (lines 359, 620)
GET /teacher/attendance - 2 ❌ DUPLICATE (lines 361, 575)
GET /teacher/tests - 2 ❌ DUPLICATE (lines 363, 588)
GET /teacher/timetable - 2 ❌ DUPLICATE (lines 365, 613)
GET /teacher/chat - 1
GET /teacher/courses - 1
GET /teacher/create-assignment - 1
GET /teacher/assignments/{assignment_id}/edit - 3 ❌ TRIPLICATE (lines 548, 662, 750)
GET /teacher/attendance/take - 1
GET /teacher/grades/add - 1
GET /teacher/tests/create - 1
GET /teacher/tests/{id}/edit - 1
GET /teacher/notices/create - 1
GET /teacher/courses/{id} - 1
GET /teacher/courses/{id}/students - 1
GET /teacher/assignments/{id}/submissions - 1
POST /teacher/assignments/submissions/{submission_id}/grade - 1
GET /teacher/attendance/{id} - 1
GET /teacher/attendance/{id}/edit - 1
GET /teacher/tests/{id}/results - 1
DELETE /teacher/tests/delete/{id} - 1
DELETE /teacher/assignments/delete/{id} - 1
GET /teacher/notes/upload - 1
POST /teacher/notes/upload - 1
GET /teacher/videos/upload - 1
POST /teacher/videos/upload - 1
GET /teacher/attendance/delete/{id} - 1
GET /teacher/videos/{id} - 1
GET /teacher/videos/{id}/edit - 1
DELETE /teacher/videos/{id} - 1
GET /teacher/groups - 1
GET /teacher/assignments/{id}/edit - 1 (line 750 - 4th occurrence total but listed above)

## AUTHORITY ENDPOINTS (36 endpoints):
GET /authority/dashboard - 1
GET /authority/students - 1
GET /authority/students/add - 1
GET /authority/students/{student_id}/edit - 1
GET /authority/students/{student_id} - 1
POST /authority/students/{id}/delete - 1
GET /authority/teachers - 1
GET /authority/teachers/add - 1
GET /authority/teachers/{teacher_id}/edit - 1
GET /authority/teachers/{teacher_id} - 1
POST /authority/teachers/{id}/delete - 1
GET /authority/courses - 1
GET /authority/courses/add - 2 ❌ DUPLICATE (lines 1377, 1386)
GET /authority/add-course - 1 (alias, same as above)
POST /authority/courses/add - 2 ❌ DUPLICATE (lines 1392, 1393)
POST /authority/add-course - 1 (alias, same as above)
GET /authority/courses/{course_id} - 1
GET /authority/courses/{course_id}/edit - 1
POST /authority/courses/{course_id}/edit - 1
POST /authority/courses/{id}/delete - 1
GET /authority/fees - 1
GET /authority/fees/structure - 1
POST /authority/fees/structure - 1
GET /authority/fees/add - 1
POST /authority/fees/add - 1
GET /authority/notices - 1
GET /authority/notices/add - 1
POST /authority/notices/add - 1
GET /authority/notices/{id}/edit - 1
POST /authority/notices/{id}/edit - 1
DELETE /authority/notices/delete/{id} - 1
GET /authority/notices/view/{id} - 1
GET /authority/analytics - 1
GET /authority/groups - 1

# authority_routes_complete
@app.get("/authority/students")
@app.post("/authority/students/add")
@app.get("/authority/teachers")
@app.get("/authority/courses")


# AUTHENTICATION ENDPOINTS
@router.post("/login")
@router.post("/login-json", response_model=Token)
@router.post("/refresh")
@router.post("/signup/student")
@router.post("/signup/teacher")
@router.post("/signup/authority")
@router.post("/signup/parent")
@router.post("/logout")

# STUDENT ENDPOINTS (students.py)
@router.get("/me", response_model=StudentResponse)
@router.put("/me", response_model=StudentResponse)
@router.get("/dashboard")
@router.get("/courses", response_model=List[CourseResponse])
@router.get("/courses/{course_id}")
@router.get("/assignments")
@router.get("/grades")
@router.get("/attendance")
@router.get("/fees")
@router.get("/tests", response_model=List[TestForStudent])
@router.get("/notices")
@router.get("/timetable")
@router.get("/notes")
@router.get("/videos")

# TEACHER ENDPOINTS (teachers.py)
@router.get("/me", response_model=TeacherResponse)
@router.put("/me", response_model=TeacherResponse)
@router.get("/dashboard")
@router.get("/courses")
@router.get("/students")
@router.get("/students/{student_id}")
@router.get("/assignments")
@router.get("/attendance")
@router.get("/grades")
@router.get("/tests")
@router.get("/timetable")

# AUTHORITY ENDPOINTS (authority.py)
@router.get("/dashboard")
@router.get("/students", response_model=List[StudentResponse])
@router.post("/students", response_model=StudentResponse)
@router.put("/students/{student_id}", response_model=StudentResponse)
@router.delete("/students/{student_id}")
@router.get("/teachers", response_model=List[TeacherResponse])
@router.post("/teachers", response_model=TeacherResponse)
@router.put("/teachers/{teacher_id}", response_model=TeacherResponse)
@router.delete("/teachers/{teacher_id}")
@router.get("/analytics/students")
@router.get("/analytics/attendance")
@router.get("/analytics/performance")
@router.get("/courses")
@router.get("/fees")
@router.get("/notices")
@router.get("/analytics")
@router.get("/reports")

# PARENT ENDPOINTS (parents.py)
@router.get("/dashboard", response_class=HTMLResponse)
@router.get("/profile", response_class=HTMLResponse)
@router.get("/child/{student_id}/attendance", response_class=HTMLResponse)
@router.get("/child/{student_id}/grades", response_class=HTMLResponse)
@router.get("/child/{student_id}/homework", response_class=HTMLResponse)
@router.get("/notices", response_class=HTMLResponse)
@router.get("/chat", response_class=HTMLResponse)

# ASSIGNMENT ENDPOINTS (assignments.py)
@router.post("/", response_model=AssignmentResponse)
@router.post("/{assignment_id}/upload")
@router.get("/teacher/my-assignments", response_model=List[AssignmentResponse])
@router.get("/{assignment_id}/submissions")
@router.put("/submissions/{submission_id}/grade")
@router.put("/{assignment_id}", response_model=AssignmentResponse)
@router.delete("/{assignment_id}")
@router.get("/{assignment_id}", response_model=AssignmentResponse)
@router.post("/{assignment_id}/submit")
@router.get("/{assignment_id}/my-submission")

# ATTENDANCE ENDPOINTS (attendance.py)
@router.post("/", response_model=AttendanceResponse)
@router.post("/bulk")
@router.get("/course/{course_id}")
@router.get("/course/{course_id}/stats")
@router.get("/my-attendance")
@router.get("/my-attendance/course/{course_id}")

# COURSES ENDPOINTS (courses.py)
@router.get("/", response_model=List[CourseResponse])
@router.get("/{course_id}", response_model=CourseResponse)
@router.post("/", response_model=CourseResponse)
@router.put("/{course_id}", response_model=CourseResponse)
@router.delete("/{course_id}")
@router.get("/{course_id}/students")
@router.get("/search/{query}")

# FEES ENDPOINTS (fees.py)
@router.post("/", response_model=FeeRecordResponse)
@router.post("/bulk")
@router.put("/{fee_id}", response_model=FeeRecordResponse)
@router.post("/{fee_id}/payment")
@router.delete("/{fee_id}")
@router.get("/summary")
@router.get("/overdue")
@router.get("/student/{student_id}")
@router.get("/type/{fee_type}")
@router.get("/my-fees")
@router.get("/my-fees/pending")
@router.get("/my-fees/overdue")
@router.get("/my-fees/payment-history")

# GRADES ENDPOINTS (grades.py)
@router.post("/", response_model=GradeResponse)
@router.post("/bulk")
@router.put("/{grade_id}", response_model=GradeResponse)
@router.delete("/{grade_id}")
@router.get("/course/{course_id}")
@router.get("/course/{course_id}/top-performers")
@router.get("/my-grades")


# CHAT ENDPOINTS (chat.py)
@router.get("/conversations")
@router.get("/messages/{other_user_id}")
@router.post("/messages/{receiver_id}")
@router.post("/mark-read/{sender_id}")
@router.get("/unread-count")
@router.get("/online-users")
@router.get("/search/{query}")
@router.get("/contacts/parent")
@router.get("/contacts/teacher")
@router.get("/search-messages/{query}")

# GROUP ENDPOINTS (groups.py)
@router.get("/", response_class=HTMLResponse)
@router.get("/create", response_class=HTMLResponse)
@router.post("/create", response_class=RedirectResponse)
@router.get("/{group_id}", response_class=HTMLResponse)
@router.get("/{group_id}/edit", response_class=HTMLResponse)
@router.post("/{group_id}/edit", response_class=RedirectResponse)
@router.get("/{group_id}/manage", response_class=HTMLResponse)
@router.post("/{group_id}/members/add", response_class=RedirectResponse)
@router.post("/{group_id}/members/{user_id}/remove", response_class=RedirectResponse)
@router.get("/api/{group_id}/members")

# GROUP POSTS ENDPOINTS (group_posts.py)
@router.get("/", response_class=HTMLResponse)
@router.get("/create", response_class=HTMLResponse)
@router.post("/create", response_class=RedirectResponse)
@router.get("/{post_id}", response_class=HTMLResponse)
@router.post("/{post_id}/delete", response_class=RedirectResponse)
@router.get("/api/posts")

# NOTES ENDPOINTS (notes.py)
@router.post("/upload", response_model=NoteResponse)
@router.get("/teacher/my-notes")
@router.delete("/{note_id}")
@router.get("/course/{course_id}")
@router.get("/{note_id}", response_model=NoteResponse)
@router.get("/{note_id}/download")
@router.get("/search/{query}")
@router.get("/recent/all")

# NOTICES ENDPOINTS (notices.py)
@router.post("/", response_model=NoticeResponse)
@router.post("/{notice_id}/upload")
@router.put("/{notice_id}", response_model=NoticeResponse)
@router.delete("/{notice_id}")
@router.get("/all")
@router.get("/", response_model=List[NoticeResponse])
@router.get("/urgent", response_model=List[NoticeResponse])
@router.get("/recent", response_model=List[NoticeResponse])
@router.get("/{notice_id}", response_model=NoticeResponse)
@router.get("/search/{query}")

# TESTS ENDPOINTS (tests.py)
@router.post("/", response_model=TestResponse)
@router.get("/teacher/my-tests", response_model=List[TestResponse])
@router.get("/teacher/{test_id}", response_model=TestResponse)
@router.put("/{test_id}", response_model=TestResponse)
@router.delete("/{test_id}")
@router.get("/{test_id}/results")
@router.get("/student/available", response_model=List[TestForStudent])
@router.get("/student/{test_id}", response_model=TestForStudent)
@router.post("/{test_id}/start")
@router.post("/{test_id}/submit", response_model=TestSubmissionResponse)
@router.get("/student/{test_id}/result", response_model=TestResult)
@router.get("/student/my-results")

# VIDEOS ENDPOINTS (videos.py)
@router.post("/upload", response_model=VideoResponse)
@router.get("/teacher/my-videos")
@router.delete("/{video_id}")
@router.get("/course/{course_id}")
@router.get("/{video_id}", response_model=VideoResponse)
@router.get("/{video_id}/stream")
@router.get("/search/{query}")
@router.get("/recent/all")

# WEBSOCKET ENDPOINT (websocket_chat.py)
@router.websocket("/ws/chat")