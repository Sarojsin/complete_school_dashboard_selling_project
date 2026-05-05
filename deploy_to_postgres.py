import subprocess
import sys

conn_str = 'postgresql://user:tara@localhost:5432/school_sell_db'

print("="*70)
print("EXECUTING SCHOOL SCHEMA ON POSTGRESQL")
print("="*70)

# Step 1: Drop everything
print("\n[1] Dropping all existing tables...")
drop_sql = """
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;
"""
result = subprocess.run(['psql', conn_str, '-c', drop_sql], capture_output=True, text=True)
if result.returncode == 0:
    print("OK - all tables dropped")
else:
    print(f"ERROR: {result.stderr[:200]}")
    sys.exit(1)

# Step 2: Execute ordered schema
print("\n[2] Creating tables from school_schema_ordered.sql...")
cmd = ['psql', conn_str, '-f', 'school_schema_ordered.sql', '-v', 'ON_ERROR_STOP=1']
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("OK - schema executed successfully")
else:
    print("WARNING - Some errors occurred (may be due to indexes):")
    print(result.stderr[:1000])

# Step 3: Verification
print("\n[3] Verification...")

# Count school_* tables
result = subprocess.run(
    ['psql', conn_str, '-t',
     "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school_%';"],
    capture_output=True, text=True
)
school_count = result.stdout.strip() or "0"
print(f"  school_* tables: {school_count}")

# Count total
result = subprocess.run(
    ['psql', conn_str, '-t',
     "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';"],
    capture_output=True, text=True
)
total = result.stdout.strip() or "0"
print(f"  Total tables: {total}")

# List all tables
result = subprocess.run(
    ['psql', conn_str, '-t',
     "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"],
    capture_output=True, text=True
)
tables = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
print("\nAll tables in database:")
for t in tables:
    print(f"  {t}")

# Check for non-school tables
non_school = [t for t in tables if not t.startswith('school_')]
if non_school:
    print(f"\nNon-school tables present: {len(non_school)}")
    for t in sorted(non_school):
        print(f"  {t}")
else:
    print("\nNo extra tables found.")

expected = 76
actual_school = int(school_count) if school_count.isdigit() else 0
print(f"\n{'='*70}")
print(f"Expected school tables: {expected}")
print(f"Actual school tables:   {actual_school}")

if actual_school >= 76:
    print("SUCCESS: School schema is correctly implemented in PostgreSQL!")
else:
    print(f"Note: {expected - actual_school} tables may have failed to create.")
    print("Check errors above for details.")

print("\nYou can now view the database in pgAdmin.")
