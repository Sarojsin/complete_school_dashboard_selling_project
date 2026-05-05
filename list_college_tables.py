import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='college_sell_db',
    user='user',
    password='tara',
    port=5432
)
cur = conn.cursor()

# Get all college_ tables
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' AND table_name LIKE 'college_%' ORDER BY table_name")
rows = cur.fetchall()
print(f"Total college_ tables: {len(rows)}")
for row in rows:
    print(f"  {row[0]}")

conn.close()
