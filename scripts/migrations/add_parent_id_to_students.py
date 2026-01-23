import os
import sys
# Ensure project root is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy import text
from database.database import engine

def add_parent_id_column():
    """Add nullable parent_id column with foreign key to parents.id if it does not exist."""
    with engine.begin() as conn:
        # Check if column already exists
        result = conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='students' AND column_name='parent_id';
                """
            )
        )
        if result.first():
            print("parent_id column already exists – nothing to do.")
            return
        # Add column and foreign key constraint
        conn.execute(
            text(
                """
                ALTER TABLE students
                ADD COLUMN parent_id INTEGER,
                ADD CONSTRAINT fk_students_parent
                    FOREIGN KEY (parent_id) REFERENCES parents(id)
                    ON DELETE SET NULL;
                """
            )
        )
        print("parent_id column added successfully.")

if __name__ == "__main__":
    add_parent_id_column()
