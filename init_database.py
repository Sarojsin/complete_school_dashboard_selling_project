#!/usr/bin/env python3
"""
Database Initialization Script - Execute all table plans
This script creates all tables in the PostgreSQL database using the SQL files.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

# Configuration from .env or environment
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'user',
    'password': 'tara',
    'database': 'college_sell_db',  # From COLLEGE_DATABASE_URL
}

# Alternative: Read from .env file
def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

def get_db_config():
    """Extract database config from environment"""
    # Try COLLEGE_DATABASE_URL first (separate mode)
    db_url = os.getenv('COLLEGE_DATABASE_URL')
    if not db_url:
        # Fall back to DATABASE_URL
        db_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
    
    # Parse postgresql://user:password@host:port/dbname
    if db_url.startswith('postgres://') or db_url.startswith('postgresql://'):
        # Remove protocol
        rest = db_url.split('://', 1)[1]
        if '@' in rest:
            user_pass, host_port_db = rest.split('@', 1)
            if ':' in user_pass:
                user, password = user_pass.split(':', 1)
            else:
                user = user_pass
                password = ''
            
            if '/' in host_port_db:
                host_port, database = host_port_db.split('/', 1)
                if ':' in host_port:
                    host, port = host_port.split(':', 1)
                    port = int(port)
                else:
                    host = host_port
                    port = 5432
            else:
                host = host_port_db
                database = ''
        else:
            raise ValueError(f"Invalid DATABASE_URL format: {db_url}")
    else:
        # SQLite fallback - not supported for this script
        raise ValueError("This script requires PostgreSQL. SQLite not supported.")
    
    return {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database,
    }

def connect_db(config=None):
    """Connect to PostgreSQL database"""
    if config is None:
        config = get_db_config()
    
    print(f"Connecting to PostgreSQL: {config['host']}:{config['port']}/{config['database']}")
    
    conn = psycopg2.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def execute_sql_file(conn, filepath):
    """Execute a SQL file"""
    print(f"\n{'='*60}")
    print(f"Executing: {Path(filepath).name}")
    print('='*60)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    cursor = conn.cursor()
    try:
        # Split by semicolon to execute multiple statements
        # But careful with function definitions, etc.
        statements = []
        current = []
        in_string = False
        string_char = None
        
        for line in sql.split('\n'):
            stripped = line.strip()
            
            # Handle strings (skip semicolons inside strings)
            for char in line:
                if char in ('"', "'") and (not in_string or string_char == char):
                    if not in_string:
                        in_string = True
                        string_char = char
                    else:
                        in_string = False
                        string_char = None
            
            # Add line to current statement
            current.append(line)
            
            # Check for statement end
            if not in_string and stripped.endswith(';'):
                statements.append('\n'.join(current))
                current = []
        
        # Add remaining
        if current:
            statements.append('\n'.join(current))
        
        # Execute each statement
        success_count = 0
        error_count = 0
        for i, stmt in enumerate(statements, 1):
            stmt = stmt.strip()
            if not stmt:
                continue
            
            # Skip comments
            if stmt.startswith('--') or stmt.startswith('/*') or stmt.startswith('* '):
                continue
            
            try:
                cursor.execute(stmt)
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"  ⚠️  Statement {i} error: {str(e)[:100]}")
                # Show statement context
                lines = stmt.split('\n')
                if len(lines) > 5:
                    print(f"    {lines[0][:80]}...")
                else:
                    for l in lines[:3]:
                        if l.strip():
                            print(f"    {l.strip()[:80]}")
        
        conn.commit()
        print(f"✓ Executed: {success_count} statements successful, {error_count} errors")
        return success_count, error_count
        
    except Exception as e:
        print(f"✗ Error executing file: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()

def main():
    """Main execution"""
    print("="*60)
    print("DATABASE INITIALIZATION SCRIPT")
    print("="*60)
    
    # Load environment
    load_env()
    
    # Get script directory
    script_dir = Path(__file__).parent
    sql_dir = script_dir
    
    # Find all plan SQL files
    plan_files = sorted(sql_dir.glob('plan*_postgres.sql'))
    
    if not plan_files:
        print("❌ No PostgreSQL plan files found!")
        print("   Looking for: plan*_postgres.sql")
        return 1
    
    print(f"Found {len(plan_files)} plan files to execute:")
    for f in plan_files:
        print(f"  - {f.name}")
    
    # Confirm with user
    response = input("\n⚠️  This will CREATE TABLES in your database. Continue? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Aborted.")
        return 0
    
    # Get database config
    try:
        db_config = get_db_config()
        print(f"\n📊 Target Database: {db_config['database']} on {db_config['host']}:{db_config['port']}")
    except Exception as e:
        print(f"❌ Database config error: {e}")
        return 1
    
    # Connect to database
    try:
        conn = connect_db(db_config)
        print("✓ Connected to PostgreSQL")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return 1
    
    # Execute each plan file in order
    total_success = 0
    total_errors = 0
    
    try:
        for i, sql_file in enumerate(plan_files, 1):
            print(f"\n[{i}/{len(plan_files)}] Processing: {sql_file.name}")
            try:
                success, errors = execute_sql_file(conn, sql_file)
                total_success += success
                total_errors += errors
            except Exception as e:
                print(f"✗ Failed to execute {sql_file.name}: {e}")
                total_errors += 1
                response = input("   Continue with next file? (yes/no): ").strip().lower()
                if response != 'yes':
                    break
        
        # Verify tables created
        print("\n" + "="*60)
        print("VERIFICATION")
        print("="*60)
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'college_%' OR table_name LIKE 'school_%'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        print(f"✓ Created {len(tables)} tables in database:")
        
        from collections import defaultdict
        prefix_count = defaultdict(int)
        for (table,) in tables:
            if table.startswith('college_'):
                prefix = 'college_'
            elif table.startswith('school_'):
                prefix = 'school_'
            else:
                prefix = 'other_'
            prefix_count[prefix] += 1
        
        for prefix, count in sorted(prefix_count.items()):
            print(f"  {prefix:20s} : {count:4d} tables")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    finally:
        conn.close()
        print("\n✓ Database connection closed")
    
    print(f"\n📊 Summary: {total_success} statements successful, {total_errors} errors")
    print("\n✓ Database initialization complete!")
    
    return 0 if total_errors == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
