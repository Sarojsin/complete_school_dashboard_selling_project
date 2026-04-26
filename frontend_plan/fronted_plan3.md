# Frontend Plan 3: School Management & Admin

Focuses on the core institutional functions for Authority, Exams, and Finance.

## 1. School Authority Dashboard
- **Goal**: Institutional oversight.
- **Features**: KPIs (Enrollment Trends, Financial Health, Overall Academic Stats), System-wide Announcements.
- **Backend**: `/api/authorities/dashboard`.

## 2. Exam Hub (Results & Schedules)
- **Goal**: Exam cycle management.
- **Features**: Result post board, Grade sheet generators, Timetable creation forms.
- **Backend**: `/api/exams/*`, `/api/exam-section/*`.

## 3. Financial/Account Section
- **Goal**: Revenue and expense tracking.
- **Features**: Fee payment portal for students/parents, Expense tracking for school admin.
- **Backend**: `/api/account/summary`, `/api/account/fees`.

## 4. Timetable Management (Global)
- **Goal**: Master schedule control.
- **Features**: Drag-and-drop timetable builder.
- **Backend**: `/api/timetable/*`.

## 5. Academic Analytics Report
- **Goal**: Data-driven decisions.
- **Features**: Charts for Year-on-year performance, Subject performance heatmaps.
- **Backend**: `/api/authorities/analytics/*`.

---
*Implementation Order: 1 -> 5*
