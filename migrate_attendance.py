from sqlalchemy import create_engine, text
import os

DATABASE_URL = "postgresql://postgres:tara@localhost:5432/school_db"

def run_migration():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Checking for arrival_time column...")
        conn.execute(text("ALTER TABLE attendance ADD COLUMN IF NOT EXISTS arrival_time TIME;"))
        conn.commit()
        print("Migration successful: arrival_time column added to attendance table.")

if __name__ == "__main__":
    run_migration()
