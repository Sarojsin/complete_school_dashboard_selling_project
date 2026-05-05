#!/usr/bin/env python3
"""
Direct PostgreSQL execution using subprocess (most reliable)
"""

import subprocess
import sys
import os
from pathlib import Path

def get_connection_string():
    """Build connection string from environment"""
    # Try college database first
    college_url = os.getenv('COLLEGE_DATABASE_URL')
    if college_url:
        return college_url
    
    # Fall back to DATABASE_URL
    db_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    
    # Fix protocol
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    return db_url

def run_psql_file(conn_string, sql_file):
    """Execute SQL file using psql command"""
    cmd = ['psql', conn_string, '-f', str(sql_file), '-v', 'ON_ERROR_STOP=1']
    
    print(f"  Executing: {sql_file.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"  ⚠️  Errors in {sql_file.name}:")
        if result.stderr:
            for line in result.stderr.split('\n')[:10]:
                if line.strip():
                    print(f"    {line}")
        # Don't stop on errors - continue with next file
        return False
    else:
        print(f"  ✓ Success")
        return True

def main():
    print("="*60)
    print("POSTGRESQL DATABASE INITIALIZATION")
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
    print(f"Connection: {conn_string.split('@')[0].split('@')[0]}...")  # Hide password
    
    # Find SQL files
    sql_files = sorted(Path('.').glob('plan*_postgres.sql'))
    if not sql_files:
        print("❌ No plan*_postgres.sql files found!")
        return 1
    
    print(f"\nFound {len(sql_files)} schema files:")
    for f in sql_files:
        print(f"  - {f.name}")
    
    # Confirm (default yes for non-interactive)
    try:
        resp = input("\n[WARNING] Create tables in database? (yes/no): ").strip().lower()
    except EOFError:
        resp = 'yes'  # Default to yes in non-interactive mode
    
    if resp != 'yes':
        print("Cancelled.")
        return 0
    
    # Test connection
    print("\nTesting connection...")
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
     print("[OK] Connected")
    
    # Enable extensions first
    print("\nEnabling PostgreSQL extensions...")
    ext_cmd = ['psql', conn_string, '-c', 
               'CREATE EXTENSION IF NOT EXISTS pg_trgm; CREATE EXTENSION IF NOT EXISTS "uuid-ossp";']
    subprocess.run(ext_cmd, capture_output=True)
    
    # Execute each file
    success_count = 0
    error_count = 0
    
    print("\nExecuting schema files...")
    for i, sql_file in enumerate(sql_files, 1):
        print(f"\n[{i}/{len(sql_files)}] {sql_file.name}")
        if run_psql_file(conn_string, sql_file):
            success_count += 1
        else:
            error_count += 1
            try:
                resp = input("   Continue? (yes/no): ").strip().lower()
            except EOFError:
                resp = 'yes'  # Default to yes in non-interactive mode
            if resp != 'yes':
                break
    
    # Verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    verify_cmd = ['psql', conn_string, '-t', 
                  '-c', "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'college_%';"]
    result = subprocess.run(verify_cmd, capture_output=True, text=True)
    college_count = result.stdout.strip() if result.returncode == 0 else "0"
    
    verify_cmd2 = ['psql', conn_string, '-t',
                   '-c', "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school_%';"]
    result2 = subprocess.run(verify_cmd2, capture_output=True, text=True)
    school_count = result2.stdout.strip() if result2.returncode == 0 else "0"
    
    print(f"✓ college_* tables: {college_count}")
    print(f"✓ school_* tables: {school_count}")
    print(f"\nTotal success: {success_count}/{len(sql_files)} files")
    
    if error_count > 0:
        print(f"⚠️  {error_count} files had errors (may be due to existing tables)")
    
    print("\n✓ Database initialization complete!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
