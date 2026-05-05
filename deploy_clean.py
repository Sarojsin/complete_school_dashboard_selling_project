import subprocess
import sys

conn_str = 'postgresql://user:tara@localhost:5432/school_sell_db'

# Drop everything
print("Dropping all tables...")
drop_sql = """
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;
"""
subprocess.run(['psql', conn_str, '-c', drop_sql], capture_output=True)

# Now use original script.txt but only CREATE TABLE parts (skip ALTER, add later)
# Better: use the ordered schema we generated but ensure no duplicates
print("Executing ordered schema...")
result = subprocess.run(
    ['psql', conn_str, '-f', 'school_schema_ordered.sql'],
    capture_output=True, text=True
)

if result.returncode == 0:
    print("Success!")
else:
    print("Error during execution:")
    print(result.stderr[:1000])

# Verification
ver = subprocess.run(
    ['psql', conn_str, '-t', '-c',
     "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school_%';"],
    capture_output=True, text=True
)
print(f"school_* tables: {ver.stdout.strip()}")
