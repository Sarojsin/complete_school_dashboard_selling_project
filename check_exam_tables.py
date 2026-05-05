import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='college_sell_db',
    user='user',
    password='tara',
    port=5432
)
cur = conn.cursor()

# Check if college_exam_results exists and describe it
print(" college_exam_results table:")
cur.execute("""
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_schema='public' AND table_name='college_exam_results'
    ORDER BY ordinal_position
""")
rows = cur.fetchall()
if rows:
    for row in rows:
        print(f"  {row[0]}: {row[1]}, nullable={row[2]}")
else:
    print("  NOT FOUND")

# Check if college_exam_notices exists
print("\n college_exam_notices table:")
cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='college_exam_notices')")
print(f"  exists: {cur.fetchone()[0]}")

# Check if college_faculty_payments exists
print("\n college_faculty_payments table:")
cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='college_faculty_payments')")
print(f"  exists: {cur.fetchone()[0]}")

conn.close()
