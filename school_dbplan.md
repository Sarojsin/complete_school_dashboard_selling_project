# School Database Implementation Plan

## Overview
Complete plan to implement the school_sell.db database with all 76 tables as specified in `schooldb.txt`.

## Current State Analysis
- Database file: `school_sell.db`
- Existing tables: **0** (initially empty)
- Target: **76 tables** (41 core + 35 extended)

## Implementation Steps

### Step 1: Preparation
- Review `schooldb.txt` to understand table requirements
- Identify dependencies between tables
- Determine creation order to satisfy foreign key constraints

### Step 2: Schema Source
- Reference implementation available in `script.txt` (PostgreSQL DDL)
- Contains complete CREATE TABLE statements for all 76 tables
- Includes indexes, constraints, and relationships

### Step 3: Database Creation
- Create/connect to `school_sell.db` (SQLite)
- Enable foreign key support: `PRAGMA foreign_keys = ON`
- Convert PostgreSQL syntax to SQLite (data types, defaults, constraints)
- Execute CREATE TABLE statements in dependency order

### Step 4: Table Categories & Creation Order

#### Phase 1: Foundation (No dependencies)
1. `users`
2. `school_subjects`
3. `school_classes`
4. `school_courses`
5. `school_holidays`
6. `school_academic_calendar`
7. `school_asset_categories`
8. `school_disciplinary_categories`
9. `school_surveys`
10. `school_note_categories`

#### Phase 2: Dependent on Users
11. `teachers` (→users)
12. `school_students` (→users)
13. `school_parents` (→users)
14. `school_authorities` (no FK but user-related)
15. `groups` (→users)
16. `school_events` (→users)
17. `school_assets` (→users)

#### Phase 3: Academic Structure
18. `school_course_enrollments` (→school_students, school_courses)
19. `school_assignments` (→school_classes, school_subjects, school_courses, teachers)
20. `school_assignment_submissions` (→school_assignments, school_students)
21. `school_assessments` (→school_classes, school_subjects, teachers)
22. `school_exam_schedules` (→school_classes, school_subjects, teachers)
23. `school_exam_grades` (→school_exam_schedules, school_students, school_subjects)
24. `school_grades` (→school_students, school_subjects, school_classes, teachers)
25. `school_grade_reports` (→school_students, school_classes)
26. `attendance_sessions` (→school_classes, school_subjects, teachers)
27. `attendance_records` (→school_students, attendance_sessions, teachers)
28. `timetable_entries` (→school_classes, school_subjects, teachers)
29. `periods` (no FKs but related to timetable)
30. `tests` (→school_subjects, school_classes, teachers)
31. `test_questions` (→tests)
32. `test_submissions` (→tests, school_students)

#### Phase 4: Communications
33. `notices` (→users)
34. `school_notes` (→school_subjects, teachers, school_note_categories)
35. `school_note_views` (→school_notes, users)
36. `chat_messages` (→users)
37. `group_members` (→groups, users)
38. `group_posts` (→groups, users)
39. `school_videos` (→school_subjects, teachers)
40. `school_video_progress` (→school_videos, school_students)
41. `exam_notices` (→school_subjects, school_classes, users)
42. `exam_results` (→school_exam_schedules, school_students, users)

#### Phase 5: Library & Resources
43. `school_books` (→school_subjects)
44. `school_book_loans` (→school_books, school_students, teachers, users)
45. `school_book_reservations` (→school_books, school_students, teachers)

#### Phase 6: Finance
46. `school_fees` (→school_students)
47. `school_payments` (→school_students, school_fees, users)
48. `school_expenses` (→users)

#### Phase 7: Transport
49. `school_transport_routes`
50. `school_route_stops` (→school_transport_routes)
51. `school_vehicles` (→users)
52. `school_vehicle_assignments` (→school_vehicles, school_transport_routes, users)
53. `school_student_transport` (→school_students, school_transport_routes, school_route_stops)
54. `school_transport_fees` (→school_students, school_transport_routes)

#### Phase 8: Canteen
55. `school_canteen_menu_items`
56. `school_canteen_orders` (→school_students)
57. `school_canteen_order_items` (→school_canteen_orders, school_canteen_menu_items)
58. `school_meal_plans` (→users)
59. `school_student_meal_plans` (→school_students, school_meal_plans)

#### Phase 9: Alumni
60. `school_alumni_records` (→school_students)
61. `school_alumni_events` (→users)
62. `school_alumni_donations` (→school_alumni_records)

#### Phase 10: Discipline & Counseling
63. `school_disciplinary_actions` (→school_students, school_disciplinary_categories, users)
64. `school_counselling_sessions` (→school_students, users)

#### Phase 11: Health
65. `school_student_health_records` (→school_students)
66. `school_vaccination_records` (→school_students)
67. `school_medical_visits` (→school_students, users)
68. `school_health_announcements` (→users)

#### Phase 12: Assets
69. `school_asset_assignments` (→school_assets, users)
70. `school_asset_maintenance_logs` (→school_assets)

#### Phase 13: PTM
71. `school_ptm_sessions` (→users)
72. `school_ptm_appointments` (→school_ptm_sessions, school_students, teachers, school_parents)
73. `school_ptm_feedback` (→school_ptm_appointments)

#### Phase 14: Surveys
74. `school_survey_questions` (→school_surveys)
75. `school_survey_responses` (→school_surveys, school_survey_questions, users)

### Step 5: Post-Creation Validation
- Verify table count: `SELECT COUNT(*) FROM sqlite_master WHERE type='table'` → 76
- Check foreign key integrity: `PRAGMA foreign_key_check`
- Verify indexes created successfully
- Test basic INSERT/SELECT operations on sample data

## Dependencies Map

```
users
├── teachers
├── school_students ─┐
├── school_parents   │
├── groups           │
├── school_events    │
├── school_assets    │
│                   ├── all other tables (via FK chains)
school_classes───────┘
school_subjects──────┘
school_courses───────┘
```

## Migration Strategy
- Fresh database: Execute all CREATE statements
- Existing database with partial tables:
  1. Check for existing tables
  2. Drop tables in reverse dependency order if needed
  3. Recreate from scratch
  4. Preserve data if possible (use ALTER TABLE for schema changes)

## Implementation Status (Current)
- ✅ Schema defined in `script.txt`
- ✅ Converted PostgreSQL → SQLite
- ✅ All 76 tables created successfully in `school_sell.db`
- ✅ Foreign keys enabled
- ⚠️ Minor: Some GIN indexes and duplicate unique indexes not created (non-critical)

## Files
- `school_dbplan.md` - This plan
- `schooldb.txt` - Table listing from existing system
- `script.txt` - Original PostgreSQL schema
- `build_final_v2.py` - Conversion & execution script
- `final_schema.sql` - Generated SQLite schema
- `school_sell.db` - Output database

## Quick Start
```bash
# Rebuild database from scratch
python build_final_v2.py

# Verify
python -c "import sqlite3; c=sqlite3.connect('school_sell.db').cursor(); c.execute('SELECT COUNT(*) FROM sqlite_master WHERE type=\"table\"'); print('Tables:', c.fetchone()[0])"
```

## Notes
- SQLite limitations: No partial indexes, no GIN indexes, no ENUM types (handled via CHECK)
- Data types simplified: VARCHAR→TEXT, DECIMAL→REAL, TIMESTAMP→DATETIME
- All foreign key constraints preserved and enforced
- Auto-increment handled via `INTEGER PRIMARY KEY AUTOINCREMENT` for all `id` columns
