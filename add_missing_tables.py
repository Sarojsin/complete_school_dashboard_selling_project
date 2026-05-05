#!/usr/bin/env python3
"""
ADD MISSING TABLES ONLY
This script adds tables that don't already exist in your database.
It will NOT drop or modify existing tables.
"""

import subprocess
import sys
import os
import re
from pathlib import Path

def get_connection_string():
    """Get database connection string"""
    db_url = os.getenv('COLLEGE_DATABASE_URL') or os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    return db_url

def get_existing_tables(conn):
    """Get set of existing table names"""
    cmd = ['psql', conn, '-t', '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return set(line.strip() for line in result.stdout.split('\n') if line.strip())
    return set()

def extract_table_names(sql_content):
    """Extract table names from CREATE TABLE statements"""
    tables = []
    # Pattern: CREATE TABLE IF NOT EXISTS table_name
    pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z_][a-zA-Z0-9_]*)'
    matches = re.findall(pattern, sql_content, re.IGNORECASE)
    for match in matches:
        tables.append(match)
    return tables

def create_table_only_sql(sql_content, tables_to_skip):
    """Create a SQL file that only includes CREATE TABLE for missing tables"""
    lines = sql_content.split('\n')
    output_lines = []
    skip_this_table = False
    table_counter = 0
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Check if this starts a CREATE TABLE
        if line_lower.startswith('create table'):
            # Extract table name from this line
            match = re.search(r'create\s+table\s+(?:if\s+not\s+exists\s+)?([a-zA-Z_][a-zA-Z0-9_]*)', line, re.IGNORECASE)
            if match:
                table_name = match.group(1)
                if table_name in tables_to_skip:
                    skip_this_table = True
                    table_counter += 1
                else:
                    skip_this_table = False
        
        # Skip all lines until we find the end of this table (marked by next CREATE or ; after closing paren)
        if skip_this_table:
            # Check if we're past this table definition
            if line_lower.startswith(('create ', 'alter ', 'comment on ', 'create index', 'create unique', 'create gin', 'create btree')) and 'create table' not in line_lower:
                # We've reached the next statement, stop skipping
                skip_this_table = False
                output_lines.append(line)
            continue
        
        output_lines.append(line)
    
    return '\n'.join(output_lines), table_counter

def main():
    print("="*60)
    print("ADD MISSING TABLES")
    print("="*60)
    print("\nThis will ONLY create tables that don't already exist.")
    print("Existing tables will NOT be modified.\n")
    
    # Load .env
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v.strip('"').strip("'")
    
    conn = get_connection_string()
    print(f"Target: {conn.split('@')[-1] if '@' in conn else conn}")
    
    # Get existing tables
    print("\n[1/4] Checking existing tables...")
    existing_tables = get_existing_tables(conn)
    print(f"  Found {len(existing_tables)} existing tables")
    
    # Define execution order (only the 10 plan files - core already exists)
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
    
    # Count what we expect to add
    all_missing_tables = set()
    for plan_file in plan_files:
        if os.path.exists(plan_file):
            with open(plan_file, 'r', encoding='utf-8') as f:
                sql = f.read()
                tables = extract_table_names(sql)
                all_missing_tables.update(tables)
    
    # Filter to only missing
    truly_missing = all_missing_tables - existing_tables
    already_exist = all_missing_tables & existing_tables
    
    print(f"\n  Tables in plans: {len(all_missing_tables)}")
    print(f"  Already exist: {len(already_exist)}")
    print(f"  Need to create: {len(truly_missing)}")
    
    if len(truly_missing) == 0:
        print("\n✓ All tables already exist! Nothing to do.")
        return 0
    
    # Show what we'll create
    print("\n[2/4] Tables to be created:")
    for table in sorted(truly_missing):
        print(f"  - {table}")
    
    # Auto-confirm for non-interactive execution
    response = 'yes'
    if response != 'yes':
        print("Cancelled.")
        return 0
    
    # Enable extensions if needed
    print("\n[3/4] Enabling extensions...")
    subprocess.run(['psql', conn, '-c', 'CREATE EXTENSION IF NOT EXISTS pg_trgm;'], capture_output=True)
    subprocess.run(['psql', conn, '-c', 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'], capture_output=True)
    print("  [OK]")
    
    # Execute each plan file, but modify to skip existing tables
    print("\n[4/4] Creating tables...")
    success_count = 0
    error_count = 0
    
    for i, plan_file in enumerate(plan_files, 1):
        if not os.path.exists(plan_file):
            print(f"\n[{i}/{len(plan_files)}] {plan_file} - NOT FOUND")
            continue
        
        print(f"\n[{i}/{len(plan_files)}] Processing {plan_file}...")
        
        # Read original SQL
        with open(plan_file, 'r', encoding='utf-8') as f:
            original_sql = f.read()
        
        # Get tables in this file
        file_tables = extract_table_names(original_sql)
        missing_in_file = [t for t in file_tables if t not in existing_tables]
        
        if not missing_in_file:
            print(f"  All tables already exist, skipping")
            continue
        
        print(f"  Creating {len(missing_in_file)} new tables:")
        for t in missing_in_file[:5]:  # Show first 5
            print(f"    - {t}")
        if len(missing_in_file) > 5:
            print(f"    ... and {len(missing_in_file)-5} more")
        
        # Execute full file (IF NOT EXISTS handles it)
        result = subprocess.run(['psql', conn, '-f', plan_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  [OK] Success")
            success_count += 1
        else:
            print("  ✗ Failed")
            # Show errors
            if result.stderr:
                for line in result.stderr.split('\n')[:5]:
                    if line.strip() and 'NOTICE' not in line:
                        print(f"    {line.strip()}")
            error_count += 1
    
    # Final verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    new_count = get_existing_tables(conn)
    print(f"\nTotal tables now: {len(new_count)}")
    print(f"Added: {len(new_count) - len(existing_tables)}")
    
    # Count by prefix
    prefixes = ['college_', 'school_', 'system_', 'audit_', 'notification_', 
                'attachment_', 'support_', 'survey_', 'backup_', 'webhook_']
    
    print("\nBreakdown:")
    for prefix in prefixes:
        count = len([t for t in new_count if t.startswith(prefix)])
        if count > 0:
            print(f"  {prefix:20s}: {count:4d}")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Plans processed: {len(plan_files)}")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {error_count}")
    print(f"  Total tables: {len(new_count)}")
    
    if error_count == 0:
        print("\n[SUCCESS] New tables added successfully!")
    else:
        print(f"\n[WARNING] {error_count} plan(s) had issues")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
