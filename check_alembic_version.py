import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='college_sell_db',
    user='user',
    password='tara',
    port=5432
)
cur = conn.cursor()

# Check alembic version
print("Alembic version table (college):")
cur.execute("SELECT version_num FROM alembic_version")
rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"  {row[0]}")
else:
    print("  No alembic version found - migrations not applied")

# Also check if alembic_version table exists at all
print("\nChecking if alembic_version table exists:")
cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='alembic_version')")
print(f"  alembic_version exists: {cur.fetchone()[0]}")

conn.close()
