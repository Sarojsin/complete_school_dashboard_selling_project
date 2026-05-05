import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='college_sell_db',
    user='user',
    password='tara',
    port=5432
)
cur = conn.cursor()

# Check structure of existing college tables
existing = ['college_departments', 'college_courses', 'college_students']
for table in existing:
    print(f"\n{table} columns:")
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_schema='public' AND table_name=%s
        ORDER BY ordinal_position
    """, (table,))
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}, nullable={row[2]}, default={row[3]}")

conn.close()
