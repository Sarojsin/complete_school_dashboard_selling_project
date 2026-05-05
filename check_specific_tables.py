import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='college_sell_db',
    user='user',
    password='tara',
    port=5432
)
cur = conn.cursor()

# Check for specific missing tables
missing = ['college_semesters', 'college_programs', 'college_enrollments', 'college_exam_notices', 'college_faculty_payments']
print("Checking for specific tables:")
for table in missing:
    cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name=%s)", (table,))
    exists = cur.fetchone()[0]
    print(f"  {table}: {'EXISTS' if exists else 'MISSING'}")

# Also check what exam-related tables exist
print("\nAll tables containing 'exam':")
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' AND table_name LIKE '%exam%'")
for row in cur.fetchall():
    print(f"  {row[0]}")

# Check what notice tables exist
print("\nAll tables containing 'notice':")
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' AND table_name LIKE '%notice%'")
for row in cur.fetchall():
    print(f"  {row[0]}")

# Check what faculty-related tables exist
print("\nAll tables containing 'faculty':")
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' AND table_name LIKE '%faculty%'")
for row in cur.fetchall():
    print(f"  {row[0]}")

# Check what payment-related tables exist
print("\nAll tables containing 'payment':")
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' AND table_name LIKE '%payment%'")
for row in cur.fetchall():
    print(f"  {row[0]}")

# Check for semester/program/enrollment with college_ prefix
print("\nAll tables with 'college_' prefix containing semester/program/enrollment:")
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' AND table_name LIKE 'college_%' AND (table_name LIKE '%semester%' OR table_name LIKE '%program%' OR table_name LIKE '%enrollment%')")
for row in cur.fetchall():
    print(f"  {row[0]}")

conn.close()
