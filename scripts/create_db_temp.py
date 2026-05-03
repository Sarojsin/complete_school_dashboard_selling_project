import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            host='127.0.0.1',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Create user 'user' with password 'tara'
        print("Checking user 'user'...")
        cur.execute("SELECT 1 FROM pg_roles WHERE rolname='user'")
        if not cur.fetchone():
            print("Creating role 'user'...")
            cur.execute("CREATE ROLE \"user\" WITH LOGIN PASSWORD 'tara' SUPERUSER")
        else:
            print("Role 'user' already exists.")

        # Create databases
        for db_name in ['school_sell_db', 'college_sell_db']:
            print(f"Checking database '{db_name}'...")
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
            if not cur.fetchone():
                print(f"Creating database '{db_name}'...")
                cur.execute(f"CREATE DATABASE {db_name} OWNER \"user\"")
            else:
                print(f"Database '{db_name}' already exists.")

        cur.close()
        conn.close()
        print("Database setup completed successfully!")

    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    create_database()
