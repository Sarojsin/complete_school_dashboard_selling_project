import subprocess

# Get all school_* tables from PostgreSQL
cmd = [
    'psql', 
    'postgresql://user:tara@localhost:5432/school_sell_db',
    '-c',
    """SELECT table_name 
       FROM information_schema.tables 
       WHERE table_schema='public' 
         AND table_name LIKE 'school_%' 
       ORDER BY table_name;""",
    '-t'
]
result = subprocess.run(cmd, capture_output=True, text=True)
pg_tables = set(line.strip() for line in result.stdout.strip().split('\n') if line.strip())
print(f"PostgreSQL school_* tables: {len(pg_tables)}")
for t in sorted(pg_tables):
    print(f"  {t}")

# Expected 76 tables from school_dbplan
expected = {
    'users', 'teachers', 'school_students', 'school_parents', 'school_classes',
    'school_subjects', 'school_courses', 'school_course_enrollments', 'school_assignments',
    'school_assignment_submissions', 'school_assessments', 'school_exam_schedules',
    'school_exam_grades', 'school_grades', 'school_grade_reports', 'school_notes',
    'school_note_categories', 'school_note_views', 'notices', 'attendance_sessions',
    'attendance_records', 'periods', 'timetable_entries', 'school_authorities',
    'school_books', 'school_book_loans', 'school_book_reservations', 'school_videos',
    'school_video_progress', 'school_fees', 'school_payments', 'school_expenses',
    'groups', 'group_members', 'group_posts', 'chat_messages', 'tests', 'test_questions',
    'test_submissions', 'school_events', 'school_event_attendees', 'school_holidays',
    'school_academic_calendar', 'school_transport_routes', 'school_route_stops',
    'school_vehicles', 'school_vehicle_assignments', 'school_student_transport',
    'school_transport_fees', 'school_canteen_menu_items', 'school_canteen_orders',
    'school_canteen_order_items', 'school_meal_plans', 'school_student_meal_plans',
    'school_alumni_records', 'school_alumni_events', 'school_alumni_donations',
    'school_disciplinary_categories', 'school_disciplinary_actions',
    'school_counselling_sessions', 'school_student_health_records',
    'school_vaccination_records', 'school_medical_visits', 'school_health_announcements',
    'school_asset_categories', 'school_assets', 'school_asset_assignments',
    'school_asset_maintenance_logs', 'school_ptm_sessions', 'school_ptm_appointments',
    'school_ptm_feedback', 'school_surveys', 'school_survey_questions',
    'school_survey_responses', 'exam_notices', 'exam_results'
}

# Note: Some tables don't have school_ prefix: users, teachers, school_students already counted
# Actually all school tables start with school_ except: users, teachers, groups, notices, periods, tests, chat_messages, exam_notices, exam_results
# Let me recalc: Count of school_* prefixed tables = 61. Plus non-school-prefixed core tables = ?

non_school = {'users', 'teachers', 'groups', 'notices', 'periods', 'tests', 'chat_messages', 'exam_notices', 'exam_results'}
pg_non_school = pg_tables - {t for t in pg_tables if t.startswith('school_')}
print(f"\nNon-school-prefix tables in PG: {pg_non_school}")

missing = expected - pg_tables
print(f"\nMissing tables ({len(missing)}):")
for t in sorted(missing):
    print(f"  {t}")
