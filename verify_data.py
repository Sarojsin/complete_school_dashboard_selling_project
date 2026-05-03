import psycopg2

def check_db(name, dbname):
    print(f"\n--- Checking {name} ({dbname}) ---")
    try:
        conn = psycopg2.connect(
            host='localhost',
            database=dbname,
            user='user',
            password='tara',
            port=5432
        )
        cur = conn.cursor()
        
        # Check users if it's school db
        if "school" in dbname:
            cur.execute("SELECT count(*) FROM users")
            user_count = cur.fetchone()[0]
            print(f"Total Users: {user_count}")
            
            cur.execute("SELECT id, username, email, role FROM users LIMIT 5")
            users = cur.fetchall()
            for u in users:
                print(f"  User: {u}")
                
            # Check if college_students table exists here too
            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'college_students')")
            if cur.fetchone()[0]:
                cur.execute("SELECT count(*) FROM college_students")
                print(f"Total College Students (in school db!): {cur.fetchone()[0]}")
        
        # Check college students if it's college db
        if "college" in dbname:
            cur.execute("SELECT count(*) FROM college_students")
            student_count = cur.fetchone()[0]
            print(f"Total College Students: {student_count}")
            
            # Check other tables to see if they have data
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
            tables = [row[0] for row in cur.fetchall()]
            for t in tables:
                cur.execute(f"SELECT count(*) FROM {t}")
                count = cur.fetchone()[0]
                if count > 0:
                    print(f"  Table {t}: {count} rows")
        
        conn.close()
    except Exception as e:
        print(f"Error connecting to {dbname}: {e}")

check_db("School Database", "school_sell_db")
check_db("College Database", "college_sell_db")
