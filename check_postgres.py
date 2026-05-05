import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Get connection string
db_url = os.getenv('DATABASE_URL', 'postgresql://user:tara@localhost:5432/school_sell_db')
print(f"Connection string (password hidden): {db_url.split('@')[0]}@...")

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Check PostgreSQL version
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    print(f"\n✓ PostgreSQL connected successfully")
    print(f"  Version: {version.split()[0:2]}")
    
    # Count school_* tables
    cur.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'school_%'
    """)
    school_count = cur.fetchone()[0]
    print(f"\n✓ school_* tables found: {school_count}")
    
    # List all school_* tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'school_%'
        ORDER BY table_name
    """)
    tables = [row[0] for row in cur.fetchall()]
    print("\nSchool tables in PostgreSQL:")
    for t in tables:
        print(f"  {t}")
    
    # Count total tables
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'")
    total = cur.fetchone()[0]
    print(f"\n✓ Total tables in database: {total}")
    
    # Check if college_* tables also exist
    cur.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'college_%'
    """)
    college_count = cur.fetchone()[0]
    print(f"✓ college_* tables: {college_count}")
    
    conn.close()
    print("\n✓ pgAdmin should be able to connect to this database successfully")
    
except Exception as e:
    print(f"\n✗ Connection failed: {e}")
    print("\nTroubleshooting steps:")
    print("1. Check PostgreSQL is running:   pg_isready -h localhost -p 5432")
    print("2. Verify database exists:        psql -U user -l")
    print("3. Test credentials:              psql -U user -d school_sell_db")
    print("4. Check .env DATABASE_URL matches your actual credentials")
