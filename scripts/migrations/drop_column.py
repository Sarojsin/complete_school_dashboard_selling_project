
from sqlalchemy import text
from app.core.database import engine

def drop_course_id():
    print("Dropping 'course_id' column from 'tests' table...")
    with engine.connect() as conn:
        try:
            # Check if column exists first (PostgreSQL)
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='tests' AND column_name='course_id';"
            ))
            if result.first():
                # Drop constraint first if it exists
                conn.execute(text("ALTER TABLE tests DROP CONSTRAINT IF EXISTS tests_course_id_fkey CASCADE;"))
                # Drop column
                conn.execute(text("ALTER TABLE tests DROP COLUMN course_id;"))
                conn.commit()
                print("Successfully dropped 'course_id'.")
            else:
                print("'course_id' column does not exist.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    drop_course_id()
