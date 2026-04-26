# Frontend Plan 2: The Teacher & Classroom Experience

Focuses on educators' tools, student management, and daily teaching tasks with a premium touch.

## 1. Teacher Dashboard (Command Center)
- **Goal**: Centralized view of teaching daily tasks.
- **Features**: Statistics cards (Total Students, Attendance %, Submissions Pending), Quick Actions (Mark Attendance, Upload Notes).
- **Backend**: `/api/teachers/dashboard`.

## 2. Grade Management & Performance Tracker
- **Goal**: Easy grade input and tracking.
- **Features**: Grade input grid with real-time validation, automatic calculation of averages.
- **Backend**: `/api/teachers/my-courses`, `/api/teachers/add-grade`.

## 3. Digital Attendance Taking
- **Goal**: Fast and modern attendance marking.
- **Features**: Grid layout with student photos and Simple P/A/L choice.
- **Backend**: `/api/teachers/take-attendance`.

## 4. Assignment & Test Creation Hub
- **Goal**: Modern assessment management.
- **Features**: Template-driven assignment creation, file uploading for attachments.
- **Backend**: `/api/teachers/create-assignment`, `/api/teachers/create-test`.

## 5. Course & Student Detail Pages
- **Goal**: Deep dive into specifics.
- **Features**: Individual student performance charts, course material structure view.
- **Backend**: `/api/teachers/my-students`, `/api/teachers/student/{id}`.

---
*Implementation Order: 1 -> 5*
