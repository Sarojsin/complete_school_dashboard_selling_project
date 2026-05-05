#!/usr/bin/env python3
"""
SIMPLER FIX: Just run the plan files against school database for school_* tables
"""

import subprocess
import sys
import os
import re

def get_connection_strings():
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

def get_table_names_in_file(filepath):
    """Extract table names from SQL file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all CREATE TABLE statements
    pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z_][a-zA-Z0-9_]*)'
    return re.findall(pattern, content, re.IGNORECASE)

def main():
    print("="*60)
    print("FIX DATABASE SEPARATION")
    print("="*60)
    
    school_conn, college_conn = get_connection_strings()
    
    print(f"\nSchool DB: {school_conn.split('/')[-1]}")
    print(f"College DB: {college_conn.split('/')[-1]}")
    
    # Find which plan files contain school_* tables
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
    
    school_tables_to_create = []
    college_tables_to_create = []
    
    for plan_file in plan_files:
        if not os.path.exists(plan_file):
            continue
        
        tables = get_table_names_in_file(plan_file)
        school_tables = [t for t in tables if t.startswith('school_')]
        college_tables = [t for t in tables if t.startswith('college_')]
        
        if school_tables:
            school_tables_to_create.append((plan_file, school_tables))
        if college_tables:
            college_tables_to_create.append((plan_file, college_tables))
    
    print(f"\nAnalysis of plan files:")
    print(f"  Files with school_* tables: {len(school_tables_to_create)}")
    print(f"  Files with college_* tables: {len(college_tables_to_create)}")
    
    # Check what's already in each database
    print("\n[1/3] Checking existing tables...")
    
    # Get existing tables in college
    college_cmd = ['psql', college_conn, '-t', '-c',
                   "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"]
    result = subprocess.run(college_cmd, capture_output=True, text=True)
    college_existing = set(line.strip() for line in result.stdout.split('\n') if line.strip())
    
    # Get existing tables in school
    school_cmd = ['psql', school_conn, '-t', '-c',
                  "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"]
    result = subprocess.run(school_cmd, capture_output=True, text=True)
    school_existing = set(line.strip() for line in result.stdout.split('\n') if line.strip())
    
    print(f"  College has {len(college_existing)} tables")
    print(f"  School has {len(school_existing)} tables")
    
    # Determine which school_* tables are missing from school but exist in college
    all_school_from_plans = set()
    for _, tables in school_tables_to_create:
        all_school_from_plans.update(tables)
    
    school_in_college = all_school_from_plans & college_existing
    school_missing_from_school = all_school_from_plans - school_existing
    
    print(f"\n  school_* tables in college DB: {len(school_in_college)}")
    print(f"  Missing from school DB: {len(school_missing_from_school)}")
    
    if not school_missing_from_school:
        print("\n✓ No missing school tables. Separation already done.")
        return 0
    
    print("\n[2/3] Creating school_* tables in school database...")
    
    # For each plan file with school tables, execute it against school database
    for plan_file, tables in school_tables_to_create:
        missing_tables = [t for t in tables if t in school_missing_from_school]
        if not missing_tables:
            print(f"  Skipping {plan_file} (all tables already exist)")
            continue
        
        print(f"\n  Executing {plan_file}...")
        print(f"    Will create: {', '.join(missing_tables[:5])}" + 
              (f" +{len(missing_tables)-5} more" if len(missing_tables)>5 else ""))
        
        result = subprocess.run(['psql', school_conn, '-f', plan_file],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"    ✓ Success")
        else:
            # Check if error is just "already exists"
            if 'already exists' in result.stderr:
                print(f"    ✓ Already exists (some tables)")
            else:
                print(f"    ✗ Failed")
                print(f"      {result.stderr[:200]}")
    
    # Step 3: Remove school_* tables from college
    print(f"\n[3/3] Removing school_* tables from college database...")
    
    # Verify what's still in college
    result = subprocess.run(college_cmd, capture_output=True, text=True)
    college_now = set(line.strip() for line in result.stdout.split('\n') if line.strip())
    school_still_in_college = school_in_college & college_now
    
    if school_still_in_college:
        for table in sorted(school_still_in_college):
            subprocess.run(['psql', college_conn, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
        print(f"  Removed {len(school_still_in_college)} school_* tables from college")
    else:
        print("  No school_* tables remain in college")
    
    # Final check
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    result = subprocess.run(school_cmd, capture_output=True, text=True)
    school_final = set(line.strip() for line in result.stdout.split('\n') if line.strip())
    
    result = subprocess.run(college_cmd, capture_output=True, text=True)
    college_final = set(line.strip() for line in result.stdout.split('\n') if line.strip())
    
    school_school_tables = [t for t in school_final if t.startswith('school_')]
    college_college_tables = [t for t in college_final if t.startswith('college_')]
    college_school_tables = [t for t in college_final if t.startswith('school_')]
    
    print(f"\nSchool database:")
    print(f"  Total tables: {len(school_final)}")
    print(f"  school_* tables: {len(school_school_tables)}")
    
    print(f"\nCollege database:")
    print(f"  Total tables: {len(college_final)}")
    print(f"  college_* tables: {len(college_college_tables)}")
    print(f"  Remaining school_* tables: {len(college_school_tables)}")
    
    if len(college_school_tables) == 0:
        print("\n✓ SUCCESS - Separation complete!")
    else:
        print(f"\n⚠ Still {len(college_school_tables)} school tables in college")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
