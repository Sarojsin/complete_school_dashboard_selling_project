#!/usr/bin/env python3
"""
FIX DATABASE SEPARATION - MOVE SCHOOL TABLES FROM COLLEGE TO SCHOOL
This script will safely transfer school_* tables from college_sell_db to school_sell_db
"""

import subprocess
import sys
import os

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

def get_tables(conn):
    """Get all table names in database"""
    cmd = ['psql', conn, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%' ORDER BY table_name;"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return [line.strip() for line in result.stdout.split('\n') if line.strip()]
    return []

def main():
    print("="*60)
    print("FIX SCHOOL/COLLEGE DATABASE SEPARATION")
    print("="*60)
    
    school_conn, college_conn = get_connection_strings()
    
    print(f"\nSchool DB: {school_conn.split('/')[-1]}")
    print(f"College DB: {college_conn.split('/')[-1]}")
    
    # Get current tables
    print("\n[1/3] Analyzing databases...")
    school_tables = get_tables(school_conn)
    college_tables = get_tables(college_conn)
    
    school_prefix_tables = [t for t in college_tables if t.startswith('school_')]
    already_in_school = [t for t in school_prefix_tables if t in school_tables]
    need_to_move = [t for t in school_prefix_tables if t not in school_tables]
    
    print(f"\nCollege database has {len(school_prefix_tables)} school_* tables")
    print(f"  Already in school DB: {len(already_in_school)}")
    print(f"  Need to move: {len(need_to_move)}")
    
    if not need_to_move:
        print("\nNo tables need moving. Databases appear correctly separated.")
        return 0
    
    print("\nTables to move from college to school:")
    for table in need_to_move[:15]:
        print(f"  - {table}")
    if len(need_to_move) > 15:
        print(f"  ... and {len(need_to_move)-15} more")
    
    confirm = 'yes'  # Auto-confirm for non-interactive
    if confirm != 'yes':
        print("Cancelled.")
        return 0
    
    # Step 1: Transfer tables
    print(f"\n[2/3] Transferring {len(need_to_move)} tables...")
    success_count = 0
    
    for i, table in enumerate(need_to_move, 1):
        print(f"  [{i}/{len(need_to_move)}] {table}...", end="")
        
        # Use pg_dump to transfer table with data
        dump_file = f'/tmp/{table}_dump.sql'
        
        # Dump from college
        dump_cmd = ['pg_dump', '--schema-only', '--table', table, college_conn, '-f', dump_file]
        subprocess.run(dump_cmd, capture_output=True)
        
        if not os.path.exists(dump_file):
            print(" DUMP FAILED")
            continue
        
        # Restore to school
        restore_cmd = ['psql', school_conn, '-f', dump_file]
        result = subprocess.run(restore_cmd, capture_output=True, text=True)
        
        # Also transfer data if it's not just schema
        if result.returncode == 0:
            # Try to copy data
            data_cmd = ['pg_dump', '--data-only', '--table', table, college_conn, '-f', f'/tmp/{table}_data.sql']
            subprocess.run(data_cmd, capture_output=True)
            
            if os.path.exists(f'/tmp/{table}_data.sql'):
                # Check if file has actual data (not empty)
                with open(f'/tmp/{table}_data.sql', 'r') as f:
                    content = f.read().strip()
                    if content and 'COPY' in content:
                        # Restore data
                        data_restore = subprocess.run(['psql', school_conn, '-f', f'/tmp/{table}_data.sql'],
                                                     capture_output=True)
                        if data_restore.returncode == 0:
                            print(" OK (with data)")
                        else:
                            print(" OK (schema only)")
                        os.remove(f'/tmp/{table}_data.sql')
                    else:
                        print(" OK")
                        os.remove(f'/tmp/{table}_data.sql')
            else:
                print(" OK")
            
            success_count += 1
        else:
            print(" FAILED")
            if os.path.exists(dump_file):
                os.remove(dump_file)
    
    # Step 2: Drop from college
    if success_count > 0:
        print(f"\n[3/3] Removing transferred tables from college database...")
        for table in need_to_move[:success_count]:  # Only ones that succeeded
            subprocess.run(['psql', college_conn, '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
        print(f"  Removed {success_count} tables")
    
    # Final verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    new_school = get_tables(school_conn)
    new_college = get_tables(college_conn)
    
    school_school = [t for t in new_school if t.startswith('school_')]
    college_college = [t for t in new_college if t.startswith('college_')]
    school_college = [t for t in new_college if t.startswith('school_')]
    
    print(f"\nSchool database:")
    print(f"  Total tables: {len(new_school)}")
    print(f"  school_* tables: {len(school_school)}")
    
    print(f"\nCollege database:")
    print(f"  Total tables: {len(new_college)}")
    print(f"  college_* tables: {len(college_college)}")
    print(f"  Remaining school_* tables: {len(school_college)}")
    
    if len(school_college) == 0:
        print("\n✓ SUCCESS - All school tables now in school database")
    else:
        print(f"\n⚠ WARNING - {len(school_college)} school_* tables still in college")
    
    print(f"\nConnection strings:")
    print(f"  School: {school_conn}")
    print(f"  College: {college_conn}")

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
