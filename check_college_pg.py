import subprocess

conn_str = 'postgresql://user:tara@localhost:5432/school_sell_db'

# Get all tables
result = subprocess.run(
    ['psql', conn_str, '-t', '-c',
     "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"],
    capture_output=True, text=True
)
tables = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]

college_tables = [t for t in tables if t.startswith('college_')]
print(f"Total tables: {len(tables)}")
print(f"college_* tables: {len(college_tables)}")
print("\nCollege tables:")
for t in college_tables:
    print(f"  {t}")

# Check against collagedb.txt expected
expected_existing = [
    'alembic_version', 'college_courses', 'college_departments', 'college_enrollments',
    'college_faculty', 'college_fee_records', 'college_fee_structures', 'college_programs',
    'college_semesters', 'college_students', 'hostel_allocations', 'hostel_complaints',
    'hostels', 'lab_equipment', 'lab_schedules', 'labs', 'placement_applications',
    'placement_companies', 'placement_jobs', 'research_patents', 'research_projects',
    'research_publications', 'rooms'
]
expected_new = [
    'college_attendance_sessions', 'college_attendance_records', 'college_assignments',
    'college_assignment_submissions', 'college_exams', 'college_exam_schedules',
    'college_exam_results', 'college_exam_grades', 'college_timetable_entries',
    'college_periods', 'college_notices', 'college_notice_views', 'college_notes',
    'college_note_categories', 'college_note_views', 'college_videos', 'college_video_progress',
    'college_books', 'college_book_copies', 'college_book_loans', 'college_book_reservations',
    'college_library_cards', 'college_tests', 'college_test_questions', 'college_test_submissions',
    'college_scholarships', 'college_scholarship_categories', 'college_scholarship_applications',
    'college_scholarship_awards', 'college_financial_aid_requests', 'college_internships',
    'college_internship_applications', 'college_internship_evaluations', 'college_industry_partners',
    'college_grievance_categories', 'college_grievances', 'college_grievance_replies',
    'college_leave_applications', 'college_student_warnings', 'college_alumni_records',
    'college_alumni_events', 'college_alumni_mentorship', 'college_research_collaborations',
    'college_research_grants', 'college_research_conferences', 'college_hostel_room_types',
    'college_hostel_fees', 'college_hostel_attendance', 'college_support_tickets',
    'college_ticket_replies'
]
expected_total = set(expected_existing + expected_new)
missing = expected_total - set(tables)
extra = set(tables) - expected_total
print(f"\nExpected total: {len(expected_total)}")
print(f"Missing: {len(missing)}")
if missing:
    print("  Missing tables:")
    for t in sorted(missing):
        print(f"    {t}")
print(f"Extra (not in expected): {len(extra)}")
if extra:
    print("  Extra tables:")
    for t in sorted(extra):
        print(f"    {t}")
