#!/usr/bin/env python3
"""
Quick database check - Verify tables exist
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env
env_path = Path('.env')
if env_path.exists():
    load_dotenv(env_path)

# Get DB URL
db_url = os.getenv('COLLEGE_DATABASE_URL') or os.getenv('DATABASE_URL')
if not db_url:
    print("❌ No DATABASE_URL or COLLEGE_DATABASE_URL in .env")
    sys.exit(1)

# Parse for psql
if db_url.startswith('postgres://'):
    conn_str = db_url.replace('postgres://', 'postgresql://', 1)
elif db_url.startswith('postgresql://'):
    conn_str = db_url
else:
    print(f"❌ Unsupported database: {db_url[:30]}")
    print("   This script requires PostgreSQL.")
    sys.exit(1)

import subprocess

def run_query(sql):
    """Run query and return result"""
    cmd = ['psql', conn_str, '-t', '-c', sql]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None

print("="*60)
print("DATABASE VERIFICATION")
print("="*60)

# Check connection
print("\n1. Testing connection...")
res = run_query('SELECT version();')
if res:
    print(f"   ✓ Connected: {res[:50]}...")
else:
    print("   ❌ Connection failed")
    sys.exit(1)

# Count tables
print("\n2. Counting tables...")
counts = {}

prefixes = [
    'college_', 'school_', 'system_', 'audit_', 
    'notification_', 'attachment_', 'support_', 
    'survey_', 'backup_', 'webhook_'
]

for prefix in prefixes:
    sql = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE '{prefix}%';"
    res = run_query(sql)
    if res and res.isdigit():
        counts[prefix] = int(res)

total = sum(counts.values())
print(f"   Total tables: {total}")
for prefix, count in sorted(counts.items()):
    if count > 0:
        print(f"     {prefix:20s}: {count:4d}")

# List all tables
print("\n3. All tables in database:")
sql = """
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name NOT LIKE 'pg_%'
ORDER BY table_name;
"""
cmd = ['psql', conn_str, '-c', sql]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    for line in result.stdout.strip().split('\n'):
        if line.strip():
            print(f"   {line.strip()}")

# Check extensions
print("\n4. Checking extensions...")
for ext in ['pg_trgm', 'uuid-ossp']:
    sql = f"SELECT COUNT(*) FROM pg_extension WHERE extname='{ext}';"
    res = run_query(sql)
    if res and res == '1':
        print(f"   ✓ {ext} enabled")
    else:
        print(f"   ⚠️  {ext} not enabled (optional but recommended)")

# Sample data check
print("\n5. Sample records:")
samples = [
    ('college_students', 'Check core table'),
    ('college_teachers', 'Check core table'),
    ('college_subjects', 'Check core table'),
    ('college_departments', 'Check core table'),
    ('college_batches', 'Check core table'),
]
for table, desc in samples:
    sql = f"SELECT COUNT(*) FROM {table};"
    res = run_query(sql)
    if res:
        print(f"   {table}: {res} rows")
    else:
        print(f"   {table}: NOT FOUND")

print("\n" + "="*60)
print("✓ Verification complete!")
print("="*60)
