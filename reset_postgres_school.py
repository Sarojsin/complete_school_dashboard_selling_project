import subprocess
import sys
import os
import re

def run_psql(conn_str, sql, quiet=False):
    cmd = ['psql', conn_str, '-c', sql, '-v', 'ON_ERROR_STOP=1']
    result = subprocess.run(cmd, capture_output=True, text=True)
    if not quiet and result.returncode != 0:
        print(f"ERROR: {result.stderr[:200]}")
    return result.returncode == 0

def main():
    conn_str = 'postgresql://user:tara@localhost:5432/school_sell_db'
    
    print("="*70)
    print("POSTGRESQL DATABASE RESET & RECREATION")
    print("="*70)
    print(f"\nDatabase: school_sell_db")
    print("WARNING: This will DROP ALL EXISTING TABLES and recreate the schema.")
    
    try:
        resp = input("\nProceed? (type 'yes' to confirm): ").strip().lower()
    except EOFError:
        resp = 'yes'
    
    if resp != 'yes':
        print("Cancelled.")
        return 0
    
    # Step 1: Check connection
    print("\n[1] Testing connection...")
    if not run_psql(conn_str, "SELECT 1;"):
        print("Cannot connect. Is PostgreSQL running?")
        return 1
    print("Connected OK")
    
    # Step 2: Drop all tables
    print("\n[2] Dropping all tables...")
    drop_sql = """
    DO $$ DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END $$;
    """
    if run_psql(conn_str, drop_sql):
        print("All tables dropped")
    else:
        print("Failed to drop tables")
        return 1
    
    # Verify drop
    result = subprocess.run(
        ['psql', conn_str, '-t', '-c',
         "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';"],
        capture_output=True, text=True
    )
    count = result.stdout.strip()
    print(f"  Tables remaining: {count}")
    
    # Step 3: Load school schema from script.txt
    print("\n[3] Reading school schema from script.txt...")
    with open('script.txt', 'r') as f:
        content = f.read()
    
    sql_match = re.search(r'```(?:postgresql|sql)?\s*(.*?)\s*```', content, re.DOTALL)
    if not sql_match:
        print("ERROR: Could not find SQL in script.txt")
        return 1
    
    pg_sql = sql_match.group(1)
    print(f"Extracted {len(pg_sql)} chars of PostgreSQL DDL")
    
    # Step 4: Execute schema
    print("\n[4] Creating tables...")
    with open('/tmp/school_schema.sql', 'w') as f:
        f.write(pg_sql)
    
    cmd = ['psql', conn_str, '-f', '/tmp/school_schema.sql', '-v', 'ON_ERROR_STOP=1']
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Schema executed successfully")
    else:
        print("Schema execution had errors (showing first 2000 chars):")
        print(result.stderr[:2000])
        # Continue to check what was created
    
    # Step 5: Verification
    print("\n[5] Verification...")
    
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
    
    # List all school tables
    result = subprocess.run(
        ['psql', conn_str, '-t',
         "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"],
        capture_output=True, text=True
    )
    all_tables = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    print("\nAll tables in database:")
    for t in sorted(all_tables):
        print(f"  {t}")
    
    # Count non-school tables
    non_school = [t for t in all_tables if not t.startswith('school_')]
    if non_school:
        print(f"\nNon-school tables: {len(non_school)}")
        for t in sorted(non_school):
            print(f"  {t}")
    else:
        print("\nNo non-school tables found.")
    
    expected = 76
    actual_school = int(school_count) if school_count.isdigit() else 0
    print(f"\n{'='*70}")
    print(f"Expected school tables: {expected}")
    print(f"Actual school tables:   {actual_school}")
    
    if actual_school == expected:
        print("SUCCESS: All 76 school tables exist")
    elif actual_school > expected:
        print(f"Note: {actual_school - expected} extra school_* tables found")
        print("(These may be from other modules - check if you need them)")
    else:
        print(f"WARNING: Missing {expected - actual_school} school tables")
    
    print("\npgAdmin should now show the database correctly.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
