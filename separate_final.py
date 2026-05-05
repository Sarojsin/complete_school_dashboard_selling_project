#!/usr/bin/env python3
"""
FIX DATABASE SEPARATION
Execute school_* table creation on school database
"""

import subprocess
import sys
import os
import re

def get_connections():
    """Get both database connection strings from .env"""
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v.strip('"').strip("'")
    
    school_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    college_url = os.getenv('COLLEGE_DATABASE_URL', 'postgresql://user:tara@localhost:5432/college_sell_db')
    
    if school_url.startswith('postgres://'):
        school_url = school_url.replace('postgres://', 'postgresql://', 1)
    if college_url.startswith('postgres://'):
        college_url = college_url.replace('postgres://', 'postgresql://', 1)
    
    return school_url, college_url

def get_tables(conn):
    """Get all table names in database"""
    cmd = ['psql', conn, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return set(line.strip() for line in result.stdout.split('\n') if line.strip())
    return set()

def extract_create_table_for_tables(sql_content, table_names):
    """Extract CREATE TABLE statements for specific tables"""
    output_lines = []
    table_set = set(table_names)
    skip_until_next_create = False
    
    for line in sql_content.split('\n'):
        line_lower = line.lower().strip()
        
        # Check if this is a CREATE TABLE line
        if line_lower.startswith('create table'):
            # Extract table name
            match = re.search(r'create\s+table\s+(?:if\s+not\s+exists\s+)?([a-zA-Z_][a-zA-Z0-9_]*)', line, re.IGNORECASE)
            if match:
                current_table = match.group(1)
                if current_table in table_set:
                    skip_until_next_create = False
                    output_lines.append(line)
                else:
                    skip_until_next_create = True
        elif not skip_until_next_create:
            output_lines.append(line)
        
        # End of table definition (next CREATE or other DDL)
        if skip_until_next_create and line_lower.startswith(('create ', 'alter ', 'comment on ', 'create index', 'create unique', 'create gin', 'create btree')) and 'create table' not in line_lower:
            skip_until_next_create = False
    
    return '\n'.join(output_lines)

def main():
    print("="*60)
    print("FIX DATABASE SEPARATION")
    print("="*60)
    
    school_conn, college_conn = get_connections()
    
    print(f"\nSchool DB: {school_conn.split('/')[-1]}")
    print(f"College DB: {college_conn.split('/')[-1]}")
    
    # Check existing tables
    print("\n[1/3] Checking existing tables...")
    school_existing = get_tables(school_conn)
    college_existing = get_tables(college_conn)
    
    school_school_in_college = {t for t in college_existing if t.startswith('school_')}
    school_school_in_school = {t for t in school_existing if t.startswith('school_')}
    
    missing_school_tables = school_school_in_college - school_school_in_school
    
    print(f"  college_* tables in college DB: {len([t for t in college_existing if t.startswith('college_')])}")
    print(f"  school_* tables in college DB: {len(school_school_in_college)}")
    print(f"  school_* tables in school DB: {len(school_school_in_school)}")
    print(f"  Missing from school DB: {len(missing_school_tables)}")
    
    if len(missing_school_tables) == 0:
        print("\n[OK] All school tables already in school database")
        return 0
    
    print(f"\n  Missing school tables (first 10):")
    for t in sorted(missing_school_tables)[:10]:
        print(f"    - {t}")
    if len(missing_school_tables) > 10:
        print(f"    ... and {len(missing_school_tables)-10} more")
    
    # Enable extensions in school DB
    print("\n[2/4] Enabling extensions in school DB...")
    subprocess.run(['psql', school_conn, '-c', 'CREATE EXTENSION IF NOT EXISTS pg_trgm;'], capture_output=True)
    subprocess.run(['psql', school_conn, '-c', 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'], capture_output=True)
    print("  OK")
    
    # Create shared infrastructure in school DB
    print("\n[3/4] Creating shared infrastructure in school DB...")
    shared_files = [
        'core_tables_minimal.sql',  # Core: departments, courses, students, teachers
        'plan3_system_admin_postgres.sql',  # System tables
        'plan10_reporting_postgres.sql'  # Attachments, reports, webhooks
    ]
    
    for sql_file in shared_files:
        if os.path.exists(sql_file):
            print(f"  Executing {sql_file}...")
            subprocess.run(['psql', school_conn, '-f', sql_file], capture_output=True)
    
    # Now execute only school_* portions from each plan against school DB
    print("\n[4/4] Creating school_* tables in school DB...")
    
    plan_files = [
        'plan1_academic_core_postgres.sql',
        'plan2_library_postgres.sql',
        'plan4_transport_postgres.sql',
        'plan5_canteen_postgres.sql',
        'plan6_alumni_placement_postgres.sql',
        'plan7_welfare_discipline_postgres.sql',
        'plan8_assets_postgres.sql',
        'plan9_events_communication_postgres.sql'
    ]
    
    success = 0
    errors = 0
    
    for plan_file in plan_files:
        if not os.path.exists(plan_file):
            print(f"  Skipping {plan_file} (not found)")
            continue
        
        # Extract table names from this file
        with open(plan_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Find all table names in this file
        all_tables = re.findall(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z_][a-zA-Z0-9_]*)', sql_content, re.IGNORECASE)
        school_tables_in_file = [t for t in all_tables if t.startswith('school_')]
        
        # Check which of these are still missing
        needed = [t for t in school_tables_in_file if t in missing_school_tables]
        
        if not needed:
            print(f"  Skipping {plan_file} (all school tables already exist)")
            continue
        
        print(f"\n  {plan_file}:")
        print(f"    Creating {len(needed)} school_* tables")
        
        # Create a filtered SQL with only needed school tables
        filtered_sql = extract_create_table_for_tables(sql_content, needed)
        
        # Execute
        result = subprocess.run(['psql', school_conn, '-c', filtered_sql],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"    [OK] OK")
            success += 1
        else:
            print(f"    [ERROR] FAILED")
            if 'already exists' in result.stderr.lower():
                print("      (likely already exists)")
            errors += 1
    
    # Step 5: Remove school_* tables from college
    print(f"\n[5/5] Removing school_* tables from college DB...")
    school_in_college_now = {t for t in get_tables(college_conn) if t.startswith('school_')}
    
    if school_in_college_now:
        for table in sorted(school_in_college_now):
            subprocess.run(['psql', college_conn, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
        print(f"  Removed {len(school_in_college_now)} tables from college")
    else:
        print("  No school_* tables remain in college")
    
    # Final verification
    print("\n" + "="*60)
    print("FINAL STATE")
    print("="*60)
    
    school_final = get_tables(school_conn)
    college_final = get_tables(college_conn)
    
    school_school = [t for t in school_final if t.startswith('school_')]
    college_college = [t for t in college_final if t.startswith('college_')]
    college_school_remaining = [t for t in college_final if t.startswith('school_')]
    
    print(f"\nSchool DB ({school_conn.split('/')[-1]}):")
    print(f"  Total tables: {len(school_final)}")
    print(f"  school_* tables: {len(school_school)}")
    print(f"  college_* tables: {len([t for t in school_final if t.startswith('college_')])}")
    
    print(f"\nCollege DB ({college_conn.split('/')[-1]}):")
    print(f"  Total tables: {len(college_final)}")
    print(f"  college_* tables: {len(college_college)}")
    print(f"  Remaining school_*: {len(college_school_remaining)}")
    
    if len(college_school_remaining) == 0:
        print("\n✓ SUCCESS - All school tables are in school database only!")
    else:
        print(f"\n⚠ {len(college_school_remaining)} school tables still in college DB")
    
    return 0 if errors == 0 else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
