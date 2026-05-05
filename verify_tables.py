import sqlite3

conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cursor.fetchall()]
print(f"Current tables: {len(tables)}")
print("\nExpected 76 tables from schooldb.txt:")
expected = {
    # Existing (41)
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
    'school_academic_calendar',
    # New (35)
    'school_transport_routes', 'school_route_stops', 'school_vehicles',
    'school_vehicle_assignments', 'school_student_transport', 'school_transport_fees',
    'school_canteen_menu_items', 'school_canteen_orders', 'school_canteen_order_items',
    'school_meal_plans', 'school_student_meal_plans', 'school_alumni_records',
    'school_alumni_events', 'school_alumni_donations', 'school_disciplinary_categories',
    'school_disciplinary_actions', 'school_counselling_sessions',
    'school_student_health_records', 'school_vaccination_records', 'school_medical_visits',
    'school_health_announcements', 'school_asset_categories', 'school_assets',
    'school_asset_assignments', 'school_asset_maintenance_logs', 'school_ptm_sessions',
    'school_ptm_appointments', 'school_ptm_feedback', 'school_surveys',
    'school_survey_questions', 'school_survey_responses', 'school_support_tickets',
    'school_ticket_replies', 'school_attachments', 'exam_notices', 'exam_results'
}

# Note: The plan says 35 new tables but lists 37 items including exam_notices, exam_results, school_attachments, school_support_tickets, school_ticket_replies
# The schooldb.txt shows: 41 existing + 35 new = 76 total
# Let's count what's in the expected set
print(f"Total expected: {len(expected)}")
missing = expected - set(tables)
extra = set(tables) - expected
print(f"\nMissing tables ({len(missing)}):")
for t in sorted(missing):
    print(f"  - {t}")
print(f"\nExtra tables ({len(extra)}):")
for t in sorted(extra):
    print(f"  - {t}")

conn.close()
