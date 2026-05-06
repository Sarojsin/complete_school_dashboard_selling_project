# Table Plan 1: Academic Core & Student Management

## Overview
Core academic functionality including attendance, assignments, exams, and timetabling.

## Tables (14)

### Attendance
- `college_attendance` - Daily student attendance records
- `college_attendance_records` - Detailed attendance logs (optional merge target)
- `college_timetable_entries` - Class schedule entries

### Assignments
- `college_assignments` - Assignment details and requirements
- `college_assignment_submissions` - Student submissions with grading

### Exams & Results
- `college_exams` - Exam definitions and schedules
- `college_exam_schedules` - Individual exam time slots
- `college_exam_results` - Student exam outcomes and marks

### Content & Resources
- `college_notices` - Official announcements and circulars
- `college_notice_views` - Tracking notice read status
- `college_notes` - Study materials and lecture notes
- `college_note_categories` - Note organization taxonomy
- `college_videos` - Educational video content
- `college_video_progress` - Student viewing progress tracking

## Dependencies
None - foundational tables for all other modules.

## Estimated Complexity
Medium - 14 tables with moderate relationships.