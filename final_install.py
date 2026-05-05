#!/usr/bin/env python3
"""
FINAL DATABASE INSTALLATION
- Clean start (drops database)
- Creates minimal core foundation
- Executes all 10 schema plans in order
"""

import subprocess
import sys
import os

def get_conn():
    """Get connection string from environment"""
    db_url = os.getenv('COLLEGE_DATABASE_URL') or os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    return db_url

def get_admin_conn():
    """Get admin connection (to postgres db)"""
    conn = get_conn()
    # Replace database name with 'postgres' for admin operations
    if '/' in conn:
        parts = conn.split('/')
        parts[-1] = 'postgres'
        return '/'.join(parts)
    return conn

def run_cmd(cmd, check=True):
    """Run shell command"""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if check and result.returncode != 0:
        print(f"ERROR: {' '.join(cmd)}")
        print(result.stderr)
        return False
    return result.returncode == 0

def main():
    print("="*60)
    print("COMPLETE DATABASE INSTALLATION")
    print("="*60)
    
    # Load .env
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v.strip('"').strip("'")
    
    conn = get_conn()
    admin_conn = get_admin_conn()
    
    # Extract database name for display
    dbname = conn.split('/')[-1] if '/' in conn else 'unknown'
    print(f"\nTarget: {dbname}")
    
    # Auto-confirm for script mode
    print("\nThis will DROP and RECREATE the database.")
    print("Make sure you have a backup if needed!\n")
    
    # Step 1: Drop and recreate database
    print("[1/4] Dropping existing database...")
    run_cmd(['psql', admin_conn, '-c', f'DROP DATABASE IF EXISTS "{dbname}";'], check=False)
    
    print("[2/4] Creating fresh database...")
    if not run_cmd(['psql', admin_conn, '-c', f'CREATE DATABASE "{dbname}";']):
        print("[ERROR] Cannot create database")
        return 1
    print("  [OK] Database created")
    
    # Step 2: Enable extensions
    print("[3/4] Enabling extensions...")
    run_cmd(['psql', conn, '-c', 'CREATE EXTENSION IF NOT EXISTS pg_trgm;'])
    run_cmd(['psql', conn, '-c', 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'])
    print("  [OK]")
    
    # Step 3: Create core foundation
    print("[4/4] Creating core tables...")
    if not os.path.exists('core_tables_minimal.sql'):
        print("[ERROR] core_tables_minimal.sql not found!")
        return 1
    
    if not run_cmd(['psql', conn, '-f', 'core_tables_minimal.sql']):
        print("[ERROR] Failed to create core tables")
        return 1
    print("  [OK] Core tables (departments, courses, students, teachers, ...)")
    
    # Step 4: Execute plans
    print("\n" + "="*60)
    print("EXECUTING SCHEMA PLANS")
    print("="*60)
    
    plans = [
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
    
    success = 0
    errors = 0
    
    for i, plan in enumerate(plans, 1):
        if not os.path.exists(plan):
            print(f"[{i}/{len(plans)}] {plan} - NOT FOUND")
            errors += 1
            continue
        
        print(f"\n[{i}/{len(plans)}] {plan}")
        if run_cmd(['psql', conn, '-f', plan], check=False):
            print("  ✓")
            success += 1
        else:
            print("  ✗")
            errors += 1
    
    # Verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    result = subprocess.run(['psql', conn, '-t', '-c',
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';"],
        capture_output=True, text=True)
    count = result.stdout.strip() if result.returncode == 0 else "0"
    
    print(f"\nTotal tables: {count}")
    
    if errors == 0:
        print("\n✓ SUCCESS - Database fully installed!")
    else:
        print(f"\n⚠ WARNING - {errors} plan(s) had errors")
    
    print(f"\nConnection string: postgresql://user:***@{conn.split('@')[-1] if '@' in conn else conn}")
    print("Open pgAdmin and connect to see all tables.")
    
    return 0 if errors == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
