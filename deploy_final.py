import subprocess
import sys

conn_str = 'postgresql://user:tara@localhost:5432/school_sell_db'

# Step 1: Drop all
print("[1] Dropping all tables...")
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
if result.returncode != 0:
    print(f"Drop failed: {result.stderr[:200]}")
    sys.exit(1)
print(" OK")

# Step 2: Execute schema
print("[2] Creating tables from school_schema_ordered.sql...")
result = subprocess.run(
    ['psql', conn_str, '-f', 'school_schema_ordered.sql'],
    capture_output=True, text=True
)

if result.returncode != 0:
    print(" WARNING - some errors may have occurred:")
    print(result.stderr[:1500])
    print("\n Retrying with each statement individually to identify issues...")
    # Parse file into separate statements by semicolon and try one by one
    with open('school_schema_ordered.sql', 'r') as f:
        content = f.read()
    stmts = [s.strip() for s in content.split(';') if s.strip() and not s.strip().startswith('--')]
    failed = []
    for i, stmt in enumerate(stmts, 1):
        r = subprocess.run(['psql', conn_str, '-c', stmt], capture_output=True, text=True)
        if r.returncode != 0:
            failed.append((i, stmt[:80], r.stderr[:200]))
    print(f" Failed: {len(failed)} statements")
    for idx, snippet, err in failed[:10]:
        print(f"  [{idx}] {snippet}... => {err}")
else:
    print(" OK")

# Step 3: Verify
print("[3] Verification...")
ver = subprocess.run(
    ['psql', conn_str, '-t', '-c',
     "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school_%';"],
    capture_output=True, text=True
)
count = ver.stdout.strip()
print(f" school_* tables: {count}")
total = subprocess.run(
    ['psql', conn_str, '-t', '-c',
     "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';"],
    capture_output=True, text=True
)
print(f" total tables: {total.stdout.strip()}")

if count == '76':
    print("\nSUCCESS: pgAdmin should now show 76 school tables!")
else:
    print(f"\nNOTE: Expected 76 school tables, found {count}")
