import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='college_sell_db',
    user='user',
    password='tara',
    port=5432
)
cur = conn.cursor()

# Check college_teachers structure
print("college_teachers columns:")
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns 
    WHERE table_schema='public' AND table_name='college_teachers'
    ORDER BY ordinal_position
""")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}, nullable={row[2]}")

# Check college_batches structure
print("\ncollege_batches columns:")
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns 
    WHERE table_schema='public' AND table_name='college_batches'
    ORDER BY ordinal_position
""")
rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"  {row[0]}: {row[1]}, nullable={row[2]}")
else:
    print("  NOT FOUND")

# Check college_notices structure
print("\ncollege_notices columns:")
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns 
    WHERE table_schema='public' AND table_name='college_notices'
    ORDER BY ordinal_position
""")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}, nullable={row[2]}")

conn.close()
