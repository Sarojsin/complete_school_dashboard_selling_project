import sqlite3

conn = sqlite3.connect('school_sell.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
all_tables = [row[0] for row in cur.fetchall()]
print(f'Total tables in school_sell.db: {len(all_tables)}')
print('\nAll tables:')
for t in all_tables:
    print(f'  {t}')

# Expected list from user
expected = [
    'attendance_records','attendance_sessions','chat_messages','exam_notices','exam_results',
    'group_members','group_posts','groups','notices','periods','school_academic_calendar',
    'school_alumni_donations','school_alumni_events','school_alumni_records','school_assessments',
    'school_asset_assignments','school_asset_categories','school_asset_maintenance_logs','school_assets',
    'school_assignment_submissions','school_assignments','school_authorities','school_book_loans',
    'school_book_reservations','school_books','school_canteen_menu_items','school_canteen_order_items',
    'school_canteen_orders','school_classes','school_counselling_sessions','school_course_enrollments',
    'school_courses','school_disciplinary_actions','school_disciplinary_categories','school_event_attendees',
    'school_events','school_exam_grades','school_exam_schedules','school_expenses','school_fees',
    'school_grade_reports','school_grades','school_health_announcements','school_holidays','school_meal_plans',
    'school_medical_visits','school_note_categories','school_note_views','school_notes','school_parents',
    'school_payments','school_ptm_appointments','school_ptm_feedback','school_ptm_sessions','school_route_stops',
    'school_student_health_records','school_student_meal_plans','school_student_transport','school_students',
    'school_subjects','school_survey_questions','school_survey_responses','school_surveys','school_transport_fees',
    'school_transport_routes','school_vaccination_records','school_vehicle_assignments','school_vehicles',
    'school_video_progress','school_videos','teachers','test_questions','test_submissions','tests',
    'timetable_entries','users'
]
print(f'\nExpected: {len(expected)} tables')
missing = set(expected) - set(all_tables)
extra = set(all_tables) - set(expected)
print(f'\nMissing from DB: {missing if missing else "None"}')
print(f'\nExtra in DB (not in expected list):')
for t in sorted(extra):
    print(f'  {t}')
conn.close()
