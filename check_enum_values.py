from sqlalchemy import create_engine, text
from database.database import engine

def check_enum_values():
    print("Checking 'userrole' enum values in database...")
    try:
        with engine.connect() as conn:
            # Check if using PostgreSQL
            if 'postgres' in str(engine.url):
                result = conn.execute(text("""
                    SELECT e.enumlabel
                    FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = 'userrole';
                """))
                print("PostgreSQL Enum values:")
                for row in result:
                    print(f" - {row[0]}")
            else:
                print("Not using PostgreSQL, checking distinct values in users table:")
                result = conn.execute(text("SELECT DISTINCT role FROM users"))
                for row in result:
                    print(f" - {row[0]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_enum_values()
