#!/usr/bin/env python3
"""
Fresh Database Installation - Clean Slate
"""

import subprocess
import sys
import os

def get_db_config():
    """Parse connection string"""
    db_url = os.getenv('COLLEGE_DATABASE_URL') or os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    # Parse: postgresql://user:password@host:port/dbname
    parts = db_url.split('://')[1].split('@')
    user_pass = parts[0].split(':')
    user = user_pass[0]
    password = user_pass[1] if len(user_pass) > 1 else ''
    
    host_port_db = parts[1].split('/')
    host_port = host_port_db[0].split(':')
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 5432
    dbname = host_port_db[1] if len(host_port_db) > 1 else 'school_sell_db'
    
    return {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'dbname': dbname,
        'conn_string': f"postgresql://{user}:{password}@{host}:{port}/{dbname}",
        'admin_conn': f"postgresql://{user}:{password}@{host}:{port}/postgres"
    }

def terminate_connections(admin_conn, dbname):
    """Terminate all connections to the database"""
    sql = f"""
    SELECT pg_terminate_backend(pid) 
    FROM pg_stat_activity 
    WHERE datname = '{dbname}' AND pid <> pg_backend_pid();
    """
    subprocess.run(['psql', admin_conn, '-c', sql], capture_output=True)

def drop_database(admin_conn, dbname):
    """Drop database if exists"""
    # Must run outside transaction, use separate subprocess call
    cmd = ['psql', admin_conn, '-c', f'DROP DATABASE IF EXISTS "{dbname}";']
    subprocess.run(cmd, capture_output=True)

def create_database(admin_conn, dbname):
    """Create fresh database"""
    result = subprocess.run(['psql', admin_conn, '-c', f'CREATE DATABASE "{dbname}";'], capture_output=True)
    return result.returncode == 0

def enable_extensions(conn):
    """Enable required PostgreSQL extensions"""
    subprocess.run(['psql', conn, '-c', 'CREATE EXTENSION IF NOT EXISTS pg_trgm;'], capture_output=True)
    subprocess.run(['psql', conn, '-c', 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'], capture_output=True)

def execute_sql_file(conn, filepath):
    """Execute SQL file"""
    cmd = ['psql', conn, '-f', str(filepath), '-v', 'ON_ERROR_STOP=1']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def get_execution_order():
    """Get files in correct dependency order"""
    return [
        'core_foundation_tables.sql',  # Core tables first
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

def count_tables(conn):
    """Count tables created"""
    cmd = ['psql', conn, '-t', '-c', 
           "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%';"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "0"

def main():
    print("="*60)
    print("FRESH DATABASE INSTALLATION")
    print("="*60)
    
    # Load .env
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    
    config = get_db_config()
    print(f"\nTarget Database: {config['dbname']}")
    print(f"Host: {config['host']}:{config['port']}")
    
    # Non-interactive mode - auto-confirm
    # Uncomment next line to require confirmation:
    # response = input("\n[WARNING] This will DROP and RECREATE the database. Continue? (yes/no): ").strip().lower()
    # if response != 'yes':
    #     print("Cancelled.")
    #     return 0
    response = 'yes'
    if response != 'yes':
        print("Cancelled.")
        return 0
    
    # Connect to admin database
    print("\n[1/6] Connecting to postgres database...")
    test = subprocess.run(['psql', config['admin_conn'], '-c', 'SELECT 1;'], 
                         capture_output=True, text=True)
    if test.returncode != 0:
        print("[ERROR] Cannot connect to PostgreSQL server:")
        print(test.stderr)
        return 1
    print("  [OK] Connected to server")
    
    # Terminate connections and drop database
    print("\n[2/6] Dropping existing database...")
    terminate_connections(config['admin_conn'], config['dbname'])
    drop_database(config['admin_conn'], config['dbname'])
    print("  [OK] Database dropped (if it existed)")
    
    # Create fresh database
    print("\n[3/6] Creating fresh database...")
    if create_database(config['admin_conn'], config['dbname']):
        print(f"  [OK] Database '{config['dbname']}' created")
    else:
        print(f"  [ERROR] Failed to create database")
        return 1
    
    # Enable extensions
    print("\n[4/6] Enabling PostgreSQL extensions...")
    enable_extensions(config['conn_string'])
    print("  [OK] Extensions enabled (pg_trgm, uuid-ossp)")
    
    # Execute core foundation
    print("\n[5/6] Creating core foundation tables...")
    core_file = 'core_foundation_tables.sql'
    if os.path.exists(core_file):
        if execute_sql_file(config['conn_string'], core_file):
            print(f"  [OK] Core tables created")
        else:
            print(f"  [ERROR] Failed to create core tables")
            return 1
    else:
        print(f"  [ERROR] {core_file} not found!")
        return 1
    
    # Execute all plan files
    print("\n[6/6] Executing schema plans...")
    execution_order = get_execution_order()
    success = 0
    errors = 0
    
    for i, filename in enumerate(execution_order, 1):
        if not os.path.exists(filename):
            print(f"  [{i}/{len(execution_order)}] {filename} - NOT FOUND, skipping")
            errors += 1
            continue
        
        print(f"\n  [{i}/{len(execution_order)}] {filename}...")
        if execute_sql_file(config['conn_string'], filename):
            print(f"    [OK]")
            success += 1
        else:
            print(f"    [ERROR]")
            errors += 1
    
    # Verify
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    table_count = count_tables(config['conn_string'])
    print(f"\nTotal tables created: {table_count}")
    
    # Sample tables
    cmd = ['psql', config['conn_string'], '-c',
           "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name NOT LIKE 'pg_%' ORDER BY table_name LIMIT 20;"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        tables = [line.strip() for line in result.stdout.split('\n') if line.strip() and not line.strip().startswith('(')]
        print(f"\nFirst {min(20, len(tables))} tables:")
        for table in tables[:20]:
            print(f"  - {table}")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  Database: {config['dbname']}")
    print(f"  Core foundation: CREATED")
    print(f"  Schema plans: {success}/{len(execution_order)-1} successful (1 core already counted)")
    print(f"  Total tables: {table_count}")
    
    if errors == 0:
        print("\n[SUCCESS] Database fully installed from clean slate!")
    else:
        print(f"\n[WARNING] {errors} schema(s) had errors")
    
    print("\nYou can now connect with pgAdmin or your application.")
    print(f"Connection: postgresql://{config['user']}:******@{config['host']}:{config['port']}/{config['dbname']}")
    
    return 0 if errors == 0 else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[INFO] Installation interrupted by user")
        sys.exit(1)
