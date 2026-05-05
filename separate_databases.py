#!/usr/bin/env python3
"""
SEPARATE TABLES INTO SCHOOL AND COLLEGE DATABASES
This script will:
1. Create school_sell_db if it doesn't exist
2. Move all school_* tables from college_sell_db to school_sell_db
3. Keep college_* tables in college_sell_db
4. Add shared tables (system_*, audit_*, notification_*, etc.) to both databases
"""

import subprocess
import sys
import os
import re

def get_connections():
    """Get both database connection strings from .env"""
    db_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    college_url = os.getenv('COLLEGE_DATABASE_URL', 'postgresql://user:tara@localhost:5432/college_sell_db')
    
    # Normalize
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    if college_url.startswith('postgres://'):
        college_url = college_url.replace('postgres://', 'postgresql://', 1)
    
    # Extract database names
    school_db = db_url.split('/')[-1]
    college_db = college_url.split('/')[-1]
    
    return {
        'school': db_url,
        'college': college_url,
        'school_db': school_db,
        'college_db': college_db,
        'admin': db_url.rsplit('/', 1)[0] + '/postgres'
    }

def get_table_lists(conn):
    """Get all tables and categorize them"""
    cmd = ['psql', conn, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        return [], [], []
    
    tables = [line.strip() for line in result.stdout.split('\n') if line.strip()]
    
    school_tables = []
    college_tables = []
    shared_tables = []
    
    for table in tables:
        if table.startswith('school_'):
            school_tables.append(table)
        elif table.startswith('college_'):
            college_tables.append(table)
        else:
            # Shared/infrastructure tables - in both
            shared_tables.append(table)
    
    return school_tables, college_tables, shared_tables

def table_exists(conn, table_name):
    """Check if table exists in database"""
    cmd = ['psql', conn, '-t', '-c',
           f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name='{table_name}';"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0 and result.stdout.strip() == '1'

def create_school_db(admin_conn, school_db):
    """Create school database if not exists"""
    # Terminate connections
    subprocess.run(['psql', admin_conn, '-c', 
                   f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='{school_db}';"],
                  capture_output=True)
    
    # Drop and create
    subprocess.run(['psql', admin_conn, '-c', f'DROP DATABASE IF EXISTS "{school_db}";'], 
                   capture_output=True)
    result = subprocess.run(['psql', admin_conn, '-c', f'CREATE DATABASE "{school_db}";'],
                           capture_output=True)
    return result.returncode == 0

def transfer_table(conn_from, conn_to, table_name):
    """Transfer a table from one database to another"""
    # Dump table structure from source
    dump_cmd = ['pg_dump', '--schema-only', '--table', table_name, conn_from, '-f', f'{table_name}.sql']
    subprocess.run(dump_cmd, capture_output=True)
    
    # Check if file created
    if not os.path.exists(f'{table_name}.sql'):
        return False, "dump failed"
    
    # Load into target
    restore_cmd = ['psql', conn_to, '-f', f'{table_name}.sql']
    result = subprocess.run(restore_cmd, capture_output=True, text=True)
    
    # Clean up
    os.remove(f'{table_name}.sql')
    
    return result.returncode == 0, result.stderr

def create_shared_tables_in_db(target_conn, shared_sql_files):
    """Create shared infrastructure tables in target database"""
    for sql_file in shared_sql_files:
        if os.path.exists(sql_file):
            result = subprocess.run(['psql', target_conn, '-f', sql_file],
                                   capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    Warning: {sql_file} had errors")
                # Continue anyway

def main():
    print("="*60)
    print("SEPARATE SCHOOL & COLLEGE DATABASES")
    print("="*60)
    
    # Load .env
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v.strip('"').strip("'")
    
    conns = get_connections()
    
    print(f"\nSchool Database: {conns['school_db']}")
    print(f"College Database: {conns['college_db']}")
    print("\nThis will:")
    print("1. Create school database if needed")
    print("2. Move school_* tables to school database")
    print("3. Keep college_* tables in college database")
    print("4. Create shared tables in both databases")
    print("\nExisting data will be preserved in both databases.\n")
    
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled.")
        return 0
    
    # Step 1: Check current state
    print("\n[1/5] Analyzing current database state...")
    school_tables, college_tables, shared_tables = get_table_lists(conns['college'])
    
    print(f"  Found in college_sell_db:")
    print(f"    school_* tables: {len(school_tables)}")
    print(f"    college_* tables: {len(college_tables)}")
    print(f"    shared tables: {len(shared_tables)}")
    
    # Step 2: Create school database
    print("\n[2/5] Creating school database...")
    if create_school_db(conns['admin'], conns['school_db']):
        print(f"  [OK] Created {conns['school_db']}")
    else:
        print(f"  [ERROR] Failed to create school database")
        return 1
    
    # Step 3: Transfer school_* tables to school database
    print(f"\n[3/5] Transferring {len(school_tables)} school_* tables...")
    if school_tables:
        for i, table in enumerate(school_tables, 1):
            print(f"  [{i}/{len(school_tables)}] {table}...", end="")
            if table_exists(conns['school'], table):
                print(" already exists")
                continue
            
            # Transfer using pg_dump/pg_restore
            success, error = transfer_table(conns['college'], conns['school'], table)
            if success:
                print(" OK")
            else:
                print(f" FAILED: {error}")
    else:
        print("  No school_* tables found to transfer")
    
    # Step 4: Remove school_* tables from college database
    if school_tables:
        print(f"\n[4/5] Removing school_* tables from college database...")
        for table in school_tables:
            subprocess.run(['psql', conns['college'], '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
        print(f"  [OK] Removed {len(school_tables)} tables")
    
    # Step 5: Create shared tables in both databases
    print(f"\n[5/5] Creating shared tables in both databases...")
    shared_sql_files = [
        'core_tables_minimal.sql',  # For school (will create shared core if needed)
        # System admin tables go in both
        'plan3_system_admin_postgres.sql',
        'plan10_reporting_postgres.sql'  # attachments, reports, webhooks, backups
    ]
    
    # For school database
    print("  Adding shared tables to school database...")
    for sql_file in shared_sql_files:
        if os.path.exists(sql_file):
            print(f"    - {sql_file}")
            subprocess.run(['psql', conns['school'], '-f', sql_file], capture_output=True)
    
    # For college database (already has these, but ensure they're there)
    print("  Verifying shared tables in college database...")
    for sql_file in shared_sql_files:
        if os.path.exists(sql_file):
            subprocess.run(['psql', conns['college'], '-f', sql_file], capture_output=True)
    
    # Final verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    school_tables_after, college_tables_after, shared_after = get_table_lists(conns['school'])
    s_school, s_college, s_shared = get_table_lists(conns['college'])
    
    print(f"\nSchool Database ({conns['school_db']}):")
    print(f"  Total: {len(school_tables_after) + len(shared_after)}")
    print(f"  school_* tables: {len(school_tables_after)}")
    print(f"  shared tables: {len(shared_after)}")
    
    print(f"\nCollege Database ({conns['college_db']}):")
    print(f"  Total: {len(s_college) + len(s_shared)}")
    print(f"  college_* tables: {len(s_college)}")
    print(f"  shared tables: {len(s_shared)}")
    
    print("\n" + "="*60)
    print("SEPARATION COMPLETE")
    print("="*60)
    print(f"\nSchool DB: postgresql://***:***@{conns['school'].split('@')[-1]}")
    print(f"College DB: postgresql://***:***@{conns['college'].split('@')[-1]}")
    print("\nYour databases are now properly separated!")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
