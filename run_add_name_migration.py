from database.database import engine
from sqlalchemy import text

def run_migration():
    """Add full_name columns to profile tables and populate from users table"""
    
    print("Running migration: add_name_columns")
    
    with engine.connect() as conn:
        # Add columns
        print("1. Adding full_name columns...")
        conn.execute(text("ALTER TABLE students ADD COLUMN IF NOT EXISTS full_name VARCHAR(255)"))
        conn.execute(text("ALTER TABLE teachers ADD COLUMN IF NOT EXISTS full_name VARCHAR(255)"))
        conn.execute(text("ALTER TABLE parents ADD COLUMN IF NOT EXISTS full_name VARCHAR(255)"))
        conn.execute(text("ALTER TABLE authorities ADD COLUMN IF NOT EXISTS full_name VARCHAR(255)"))
        conn.commit()
        print("   OK - Columns added")
        
        # Populate from users table
        print("2. Populating existing records...")
        conn.execute(text("UPDATE students SET full_name = (SELECT full_name FROM users WHERE users.id = students.user_id)"))
        result = conn.execute(text("SELECT COUNT(*) FROM students WHERE full_name IS NOT NULL"))
        student_count = result.scalar()
        
        conn.execute(text("UPDATE teachers SET full_name = (SELECT full_name FROM users WHERE users.id = teachers.user_id)"))
        result = conn.execute(text("SELECT COUNT(*) FROM teachers WHERE full_name IS NOT NULL"))
        teacher_count = result.scalar()
        
        conn.execute(text("UPDATE parents SET full_name = (SELECT full_name FROM users WHERE users.id = parents.user_id)"))
        result = conn.execute(text("SELECT COUNT(*) FROM parents WHERE full_name IS NOT NULL"))
        parent_count = result.scalar()
        
        conn.execute(text("UPDATE authorities SET full_name = (SELECT full_name FROM users WHERE users.id = authorities.user_id)"))
        result = conn.execute(text("SELECT COUNT(*) FROM authorities WHERE full_name IS NOT NULL"))
        authority_count = result.scalar()
        
        conn.commit()
        print(f"   OK - Populated {student_count} students, {teacher_count} teachers, {parent_count} parents, {authority_count} authorities")
        
    print("Migration completed successfully!")

if __name__ == "__main__":
    run_migration()
