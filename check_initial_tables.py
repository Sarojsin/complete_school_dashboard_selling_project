import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='college_sell_db',
    user='user',
    password='tara',
    port=5432
)
cur = conn.cursor()

# Check for the core initial migration tables that should exist
expected_initial = ['college_departments', 'college_faculty', 'college_programs', 'college_semesters', 'college_courses', 'college_students', 'college_enrollments']
print("Checking expected initial migration tables:")
for table in expected_initial:
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name=%s)", (table,))
    exists = cur.fetchone()[0]
    print(f"  {table}: {'EXISTS' if exists else 'MISSING'}")

# Also check some other expected tables from initial migration
other = ['hostels', 'labs', 'research_patents', 'research_projects', 'research_publications', 'placement_companies', 'placement_jobs', 'placement_applications']
print("\nOther expected tables from initial migration:")
for table in other:
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name=%s)", (table,))
    exists = cur.fetchone()[0]
    print(f"  {table}: {'EXISTS' if exists else 'MISSING'}")

conn.close()
