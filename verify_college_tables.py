import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='college_sell_db',
    user='user',
    password='tara',
    port=5432
)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY table_name")
tables = [row[0] for row in cur.fetchall()]
print(f"College database tables ({len(tables)}):")
for t in tables:
    print(f"  - {t}")
conn.close()
