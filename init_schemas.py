#!/usr/bin/env python3
"""
Execute PostgreSQL schemas in correct dependency order
"""

import subprocess
import sys
import os
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

def run_psql_command(conn_string, sql, description):
    """Run a single SQL command"""
    cmd = ['psql', conn_string, '-c', sql]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"  [ERROR] {description}:")
        if result.stderr:
            for line in result.stderr.split('\n')[:3]:
                if line.strip():
                    print(f"    {line}")
        return False
    return True

def drop_existing_tables(conn_string):
    """Drop all existing tables to start fresh"""
    print("\n[0/5] Dropping existing tables...")
    
    # Get all tables
    cmd = ['psql', conn_string, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and result.stdout.strip():
        tables = [t.strip() for t in result.stdout.split('\n') if t.strip()]
        if tables:
            print(f"  Found {len(tables)} existing tables")
            # Disable constraints temporarily
            run_psql_command(conn_string, "SET session_replication_role = 'replica';", "Disable constraints")
            
            for table in tables:
                run_psql_command(conn_string, f"DROP TABLE IF EXISTS {table} CASCADE;", f"Drop {table}")
            
            run_psql_command(conn_string, "SET session_replication_role = 'origin';", "Enable constraints")
            print(f"  [OK] Dropped {len(tables)} tables")
        else:
            print("  No existing tables found")
    else:
        print("  No existing tables found")

def execute_schema_files(conn_string):
    """Execute schema files in correct order"""
    # Correct order: Plan 1 through 10
    plan_files = [
        'plan1_academic_core_postgres.sql',
        'plan2_library_postgres.sql',
        'plan3_system_admin_postgres.sql',
        'plan4_transport_postgres.sql',
        'plan5_canteen_postgres.sql',
        'plan6_alumni_placement_postgres.sql',
        'plan7_welfare_discipline_postgres.sql',
        'plan8_assets_postgres.sql',
        'plan9_events_communication_postgres.sql',
        'plan10_reporting_postgres.sql'
    ]
    
    success_count = 0
    error_count = 0
    
    for i, filename in enumerate(plan_files, 1):
        filepath = Path(filename)
        if not filepath.exists():
            print(f"\n[{i}/10] {filename} - NOT FOUND")
            error_count += 1
            continue
        
        print(f"\n[{i}/10] Executing {filename}...")
        
        # Use psql to execute file
        cmd = ['psql', conn_string, '-f', str(filepath), '-v', 'ON_ERROR_STOP=1']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Count tables created (rough estimate)
            if 'CREATE TABLE' in result.stdout:
                tables_created = result.stdout.count('CREATE TABLE')
                print(f"  [OK] Created approximately {tables_created} tables/objects")
            else:
                print(f"  [OK]")
            success_count += 1
        else:
            print(f"  [ERROR] Execution failed:")
            if result.stderr:
                for line in result.stderr.split('\n')[:10]:
                    if line.strip():
                        print(f"    {line}")
            error_count += 1
    
    return success_count, error_count

def verify_tables(conn_string):
    """Verify tables were created"""
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    queries = [
        ("Total tables", """
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name NOT LIKE 'pg_%'
        """),
        ("college_* tables", """
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name LIKE 'college_%'
        """),
        ("school_* tables", """
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name LIKE 'school_%'
        """),
        ("system_* tables", """
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name LIKE 'system_%'
        """),
    ]
    
    for label, sql in queries:
        cmd = ['psql', conn_string, '-t', '-c', sql]
        result = subprocess.run(cmd, capture_output=True, text=True)
        count = result.stdout.strip() if result.returncode == 0 else "0"
        print(f"  {label:25s}: {count:6s}")
    
    # List sample tables
    print("\n  Sample tables (first 10):")
    cmd = ['psql', conn_string, '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'college_%' ORDER BY table_name LIMIT 10;"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        for line in result.stdout.split('\n'):
            if line.strip():
                print(f"    - {line.strip()}")

def main():
    print("="*60)
    print("POSTGRESQL SCHEMA EXECUTION")
    print("="*60)
    
    # Load environment
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    
    conn_string = get_connection_string()
    print(f"\nTarget Database: {conn_string.split('@')[-1] if '@' in conn_string else conn_string}")
    
    # Test connection
    print("\n[Pre-check] Testing connection...")
    test_cmd = ['psql', conn_string, '-c', 'SELECT 1;']
    result = subprocess.run(test_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("[ERROR] Cannot connect to database:")
        print(result.stderr)
        return 1
    print("  [OK] Connected")
    
    # Enable extensions
    print("\n[Pre-check] Enabling extensions...")
    run_psql_command(conn_string, 
                     'CREATE EXTENSION IF NOT EXISTS pg_trgm; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',
                     "Enable extensions")
    
    # Drop existing tables (for clean install)
    drop_existing = True  # Change to False to keep existing data
    if drop_existing:
        drop_existing_tables(conn_string)
    else:
        print("\n[Skipping] Table drop - preserving existing data (errors may occur)")
    
    # Execute schemas
    print("\n" + "="*60)
    print("EXECUTING SCHEMAS")
    print("="*60)
    
    success, errors = execute_schema_files(conn_string)
    
    # Verify
    verify_tables(conn_string)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Files processed: 10")
    print(f"  Successful: {success}")
    print(f"  Errors: {errors}")
    
    if errors == 0:
        print("\n[SUCCESS] All schemas executed successfully!")
    else:
        print(f"\n[WARNING] Completed with {errors} error(s)")
        print("  Some tables may not have been created.")
        print("  Check the error messages above.")
    
    return 0 if errors == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
