#!/usr/bin/env python3
"""
FIX DATABASE SEPARATION
Move school_* tables from college_sell_db to school_sell_db
Preserve existing data in both databases
"""

import subprocess
import sys
import os

def get_connections():
    """Get both database connection strings from .env"""
    db_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    college_url = os.getenv('COLLEGE_DATABASE_URL', 'postgresql://user:tara@localhost:5432/college_sell_db')
    
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    if college_url.startswith('postgres://'):
        college_url = college_url.replace('postgres://', 'postgresql://', 1)
    
    return {
        'school': db_url,
        'college': college_url,
        'school_db': db_url.split('/')[-1],
        'college_db': college_url.split('/')[-1],
    }

def get_tables(conn):
    """Get all table names in database"""
    cmd = ['psql', conn, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return [line.strip() for line in result.stdout.split('\n') if line.strip()]
    return []

def categorize_tables(tables):
    """Categorize tables by prefix"""
    school_tables = [t for t in tables if t.startswith('school_')]
    college_tables = [t for t in tables if t.startswith('college_')]
    shared_tables = [t for t in tables if not t.startswith('school_') and not t.startswith('college_')]
    return school_tables, college_tables, shared_tables

def transfer_table(conn_from, conn_to, table_name):
    """Transfer table structure and data using pg_dump/pg_restore"""
    try:
        # Dump table with data
        dump_cmd = ['pg_dump', '--data-only', '--inserts', '--table', table_name, conn_from, '-f', f'{table_name}.sql']
        result = subprocess.run(dump_cmd, capture_output=True)
        
        if result.returncode != 0 or not os.path.exists(f'{table_name}.sql'):
            return False
        
        # Restore to target
        restore_cmd = ['psql', conn_to, '-f', f'{table_name}.sql']
        result = subprocess.run(restore_cmd, capture_output=True)
        
        # Clean up
        os.remove(f'{table_name}.sql')
        
        return result.returncode == 0
    except Exception as e:
        print(f"    Error: {e}")
        return False

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
    
    print(f"\nSchool DB: {conns['school_db']}")
    print(f"College DB: {conns['college_db']}")
    
    # Check current state
    print("\n[1/4] Analyzing current state...")
    
    college_tables = get_tables(conns['college'])
    school_tables = get_tables(conns['school'])
    
    s_school, s_college, s_shared = categorize_tables(college_tables)
    sc_school, sc_college, sc_shared = categorize_tables(school_tables)
    
    print(f"\nIn college database:")
    print(f"  school_* tables: {len(s_school)}")
    print(f"  college_* tables: {len(s_college)}")
    print(f"  shared tables: {len(s_shared)}")
    
    print(f"\nIn school database:")
    print(f"  school_* tables: {len(sc_school)}")
    print(f"  college_* tables: {len(sc_college)}")
    print(f"  shared tables: {len(sc_shared)}")
    
    # Tables to move from college to school
    tables_to_move = [t for t in s_school if t not in sc_school]
    tables_already_in_school = [t for t in s_school if t in sc_school]
    
    print(f"\nNeed to move {len(tables_to_move)} school_* tables from college to school")
    print(f"Already in school: {len(tables_already_in_school)}")
    
    if not tables_to_move:
        print("\nNo tables need moving. Exiting.")
        return 0
    
    # Show what will be moved
    print("\nTables to transfer:")
    for table in tables_to_move[:10]:
        print(f"  - {table}")
    if len(tables_to_move) > 10:
        print(f"  ... and {len(tables_to_move)-10} more")
    
    confirm = input(f"\nProceed? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled.")
        return 0
    
    # Step 1: Transfer school_* tables from college to school
    print(f"\n[2/4] Transferring {len(tables_to_move)} tables...")
    success_count = 0
    
    for i, table in enumerate(tables_to_move, 1):
        print(f"  [{i}/{len(tables_to_move)}] {table}...", end="")
        if transfer_table(conns['college'], conns['school'], table):
            print(" OK")
            success_count += 1
        else:
            print(" FAILED")
    
    # Step 2: Remove school_* tables from college
    print(f"\n[3/4] Removing school_* tables from college database...")
    removed_count = 0
    for table in tables_to_move:
        if table in sc_school:  # Already in school, safe to remove from college
            subprocess.run(['psql', conns['college'], '-c', f'DROP TABLE IF EXISTS "{table}" CASCADE;'],
                          capture_output=True)
            removed_count += 1
    print(f"  Removed {removed_count} tables from college database")
    
    # Step 3: Ensure shared tables exist in both databases
    print(f"\n[4/4] Ensuring shared tables in both databases...")
    
    # Get final table lists
    final_school_tables, final_college_shared, _ = categorize_tables(get_tables(conns['school']))
    final_college_tables, _, _ = categorize_tables(get_tables(conns['college']))
    
    # Which shared tables should be in both?
    common_shared = set(s_shared) | set(sc_shared)
    
    print(f"\nFinal counts:")
    print(f"  School: {len(final_school_tables)} school_* tables + {len(common_shared)} shared")
    print(f"  College: {len(final_college_tables)} college_* tables + {len(common_shared)} shared")
    
    print("\n" + "="*60)
    print("SEPARATION COMPLETE")
    print("="*60)
    
    print(f"\nSchool DB ({conns['school_db']}):")
    for table in sorted(final_school_tables)[:5]:
        print(f"  - {table}")
    if len(final_school_tables) > 5:
        print(f"  ... and {len(final_school_tables)-5} more")
    
    print(f"\nCollege DB ({conns['college_db']}):")
    for table in sorted(final_college_tables)[:5]:
        print(f"  - {table}")
    if len(final_college_tables) > 5:
        print(f"  ... and {len(final_college_tables)-5} more")
    
    print(f"\nTotal: {len(final_school_tables) + len(common_shared)} tables in school")
    print(f"        {len(final_college_tables) + len(common_shared)} tables in college")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
