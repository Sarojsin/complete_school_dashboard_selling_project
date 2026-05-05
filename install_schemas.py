#!/usr/bin/env python3
"""
Execute PostgreSQL schemas in CORRECT dependency order
"""

import subprocess
import sys
import os
import re
from pathlib import Path

def get_connection_string():
    """Build connection string from environment"""
    college_url = os.getenv('COLLEGE_DATABASE_URL')
    if college_url:
        return college_url
    
    db_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    return db_url

def run_psql_file(conn_string, filepath):
    """Execute SQL file and return success/failure"""
    cmd = ['psql', conn_string, '-f', str(filepath), '-v', 'ON_ERROR_STOP=1']
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return True, ""
    else:
        # Extract first few error lines
        errors = []
        for line in result.stderr.split('\n')[:5]:
            if line.strip() and 'notices' not in line.lower():
                errors.append(line.strip())
        return False, '\n    '.join(errors)

def drop_all_tables(conn_string):
    """Drop all tables in the database"""
    print("\n[0/5] Clearing existing database...")
    
    # Get all user tables
    cmd = ['psql', conn_string, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        tables = [t.strip() for t in result.stdout.split('\n') if t.strip()]
        if tables:
            print(f"  Found {len(tables)} existing tables")
            
            # Drop with CASCADE to handle dependencies
            for table in tables:
                subprocess.run(['psql', conn_string, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'], 
                             capture_output=True)
            print(f"  [OK] Dropped all tables")
        else:
            print("  Database already empty")
    else:
        print("  [WARNING] Could not query existing tables")

def natural_sort_key(filename):
    """Extract number from filename for sorting: plan1 -> 1, plan10 -> 10"""
    match = re.search(r'plan(\d+)_', filename.name)
    if match:
        return int(match.group(1))
    return 999  # Unknown files go last

def execute_schemas(conn_string):
    """Execute all schema files in correct order"""
    # Get all plan files
    plan_files = sorted(Path('.').glob('plan*_postgres.sql'), key=natural_sort_key)
    
    if not plan_files:
        print("[ERROR] No plan*_postgres.sql files found!")
        return 0, 0
    
    print(f"\nExecution order:")
    for f in plan_files:
        print(f"  - {f.name}")
    
    success_count = 0
    error_count = 0
    
    for i, filepath in enumerate(plan_files, 1):
        print(f"\n[{i}/{len(plan_files)}] {filepath.name}")
        success, error_msg = run_psql_file(conn_string, filepath)
        
        if success:
            print("  [OK]")
            success_count += 1
        else:
            print(f"  [ERROR]")
            if error_msg:
                print(f"    Details: {error_msg}")
            error_count += 1
    
    return success_count, error_count

def verify(conn_string):
    """Verify tables were created"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    queries = [
        ("Total tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';"),
        ("college_* tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'college_%';"),
        ("school_* tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school_%';"),
        ("system_* tables", "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'system_%';"),
    ]
    
    for label, sql in queries:
        cmd = ['psql', conn_string, '-t', '-c', sql]
        result = subprocess.run(cmd, capture_output=True, text=True)
        count = result.stdout.strip() if result.returncode == 0 else "0"
        print(f"  {label:25s}: {count:>6s}")
    
    # List some tables
    cmd = ['psql', conn_string, '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%' ORDER BY table_name LIMIT 15;"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        print("\n  Tables created (first 15):")
        for line in result.stdout.split('\n')[:15]:
            if line.strip():
                print(f"    - {line.strip()}")

def main():
    print("="*60)
    print("POSTGRESQL SCHEMA INSTALLATION")
    print("="*60)
    
    # Load .env
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    
    conn_string = get_connection_string()
    # Mask password for display
    if '@' in conn_string:
        before_at = conn_string.split('@')[0]
        after_at = conn_string.split('@')[1]
        if ':' in before_at:
            user_pass = before_at.split('://')
            if len(user_pass) > 1:
                user, pwd = user_pass[1].split(':', 1) if ':' in user_pass[1] else (user_pass[1], '')
                display = f"{user_pass[0]}://{user}:***@{after_at}"
            else:
                display = conn_string
        else:
            display = conn_string
    else:
        display = conn_string
    
    print(f"\nDatabase: {display}")
    
    # Test connection
    print("\n[Pre-check] Testing connection...")
    test = subprocess.run(['psql', conn_string, '-c', 'SELECT 1;'], 
                         capture_output=True, text=True)
    if test.returncode != 0:
        print("[ERROR] Cannot connect to database:")
        print(test.stderr)
        return 1
    print("  [OK] Connected")
    
    # Enable extensions
    print("\n[Pre-check] Enabling extensions...")
    subprocess.run(['psql', conn_string, '-c', 
                   'CREATE EXTENSION IF NOT EXISTS pg_trgm; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'],
                   capture_output=True)
    print("  [OK] Extensions ready")
    
    # DROP existing tables for clean install
    drop_all_tables(conn_string)
    
    # Execute schemas
    print("\n" + "="*60)
    print("EXECUTING SCHEMAS")
    print("="*60)
    
    success, errors = execute_schemas(conn_string)
    
    # Verify
    verify(conn_string)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Files processed: {len(list(Path('.').glob('plan*_postgres.sql')))}")
    print(f"  Successful: {success}")
    print(f"  Errors: {errors}")
    
    if errors == 0:
        print("\n[SUCCESS] All schemas executed successfully!")
    else:
        print(f"\n[WARNING] {errors} file(s) had errors")
    
    return 0 if errors == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
