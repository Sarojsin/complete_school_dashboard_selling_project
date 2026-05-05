import subprocess

# Test connection
cmd = [
    'psql', 
    'postgresql://user:tara@localhost:5432/school_sell_db',
    '-c',
    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school_%';",
    '-t'
]
result = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", result.returncode)
print("Output:", result.stdout)
print("Error:", result.stderr)

if result.returncode == 0:
    count = result.stdout.strip()
    print(f"\n✓ PostgreSQL is running and accessible")
    print(f"✓ school_* tables count: {count}")

    # List all tables
    cmd2 = [
        'psql', 
        'postgresql://user:tara@localhost:5432/school_sell_db',
        '-c',
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE 'school_%' ORDER BY table_name;",
        '-t'
    ]
    result2 = subprocess.run(cmd2, capture_output=True, text=True)
    print("\nTables in PostgreSQL:")
    for line in result2.stdout.strip().split('\n'):
        print(f"  {line}")
else:
    print("\n✗ Could not connect to PostgreSQL")
    print("\nPlease verify:")
    print("1. PostgreSQL service is running")
    print("   Command: pg_isready -h localhost -p 5432")
    print("2. Database exists:")
    print("   Command: psql -U user -c '\\l'")
    print("3. Credentials correct in .env:")
    print("   DATABASE_URL=postgresql://user:tara@localhost:5432/school_sell_db")
