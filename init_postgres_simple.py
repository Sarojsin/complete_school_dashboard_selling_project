#!/usr/bin/env python3
"""
Simple PostgreSQL Schema Executor - No interactive prompts
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

def run_psql_file(conn_string, sql_file):
    """Execute SQL file using psql command"""
    cmd = ['psql', conn_string, '-f', str(sql_file), '-v', 'ON_ERROR_STOP=1']
    
    print(f"  Executing: {sql_file.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"  [ERROR] Failed:")
        if result.stderr:
            for line in result.stderr.split('\n')[:5]:
                if line.strip():
                    print(f"    {line}")
        return False
    else:
        # Count statements executed
        if 'CREATE TABLE' in result.stdout or 'CREATE INDEX' in result.stdout:
            print(f"  [OK]")
        else:
            print(f"  [OK] (no errors)")
        return True

def main():
    print("="*60)
    print("POSTGRESQL DATABASE INITIALIZATION")
    print("="*60)
    
    # Load environment from .env if exists
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    
    conn_string = get_connection_string()
    # Hide password for display
    display_conn = conn_string.replace('://', '://***:***@') if '@' in conn_string else conn_string
    print(f"Connection: {display_conn}")
    
    # Find SQL files
    sql_files = sorted(Path('.').glob('plan*_postgres.sql'))
    if not sql_files:
        print("[ERROR] No plan*_postgres.sql files found!")
        return 1
    
    print(f"\nFound {len(sql_files)} schema files:")
    for f in sql_files:
        print(f"  - {f.name}")
    
    # Auto-confirm for non-interactive execution
    print("\nProceeding with automatic execution...")
    
    # Test connection
    print("\n[1/4] Testing connection...")
    test_cmd = ['psql', conn_string, '-c', 'SELECT version();']
    result = subprocess.run(test_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("[ERROR] Connection failed:")
        print(result.stderr)
        print("\nPlease check:")
        print("1. PostgreSQL is running")
        print("2. Database exists")
        print("3. Credentials correct in .env")
        return 1
    print("  [OK] Connected")
    
    # Enable extensions
    print("\n[2/4] Enabling PostgreSQL extensions...")
    ext_cmd = ['psql', conn_string, '-c', 
               'CREATE EXTENSION IF NOT EXISTS pg_trgm; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";']
    result = subprocess.run(ext_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("  [OK] Extensions enabled (pg_trgm, uuid-ossp)")
    else:
        print("  [WARNING] Extension warning:")
        print(result.stderr)
    
    # Execute each file
    print("\n[3/4] Executing schema files...")
    success_count = 0
    error_count = 0
    
    for i, sql_file in enumerate(sql_files, 1):
        print(f"\n  [{i}/{len(sql_files)}] {sql_file.name}")
        if run_psql_file(conn_string, sql_file):
            success_count += 1
        else:
            error_count += 1
            # Continue anyway to try all files
    
    # Verification
    print("\n[4/4] Verification...")
    verify_sql = """
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND (table_name LIKE 'college_%' OR table_name LIKE 'school_%');
    """
    cmd = ['psql', conn_string, '-t', '-c', verify_sql]
    result = subprocess.run(cmd, capture_output=True, text=True)
    table_count = result.stdout.strip() if result.returncode == 0 else "0"
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files processed: {len(sql_files)}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Tables created: {table_count}")
    print(f"\n[{'OK' if error_count == 0 else 'WARNING'}] Database initialization {'complete' if error_count == 0 else 'completed with errors'}")
    
    # List some tables
    if table_count and int(table_count) > 0:
        list_cmd = ['psql', conn_string, '-c',
                   "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'college_%' ORDER BY table_name LIMIT 5;"]
        result = subprocess.run(list_cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("\nSample tables created:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"  - {line.strip()}")
    
    return 0 if error_count == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
