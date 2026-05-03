import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='school_sell_db',
    user='user',
    password='tara',
    port=5432
)
conn.set_isolation_level(0)  # AUTOCOMMIT
cur = conn.cursor()

print("Dropping all tables with CASCADE...")
cur.execute('DROP SCHEMA public CASCADE')
cur.execute('CREATE SCHEMA public')
cur.execute('GRANT ALL ON SCHEMA public TO "user"')
cur.execute('GRANT ALL ON SCHEMA public TO public')

cur.close()
conn.close()
print("Schema dropped and recreated successfully!")
