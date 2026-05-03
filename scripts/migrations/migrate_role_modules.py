import os
import sys
# Ensure project root is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sqlalchemy import text
from backup.core.database import engine

def add_exam_results_columns():
    """Add new columns to exam_results table."""
    with engine.begin() as conn:
        columns_to_add = [
            ("max_marks", "FLOAT DEFAULT 100.0"),
            ("exam_type", "VARCHAR(20) DEFAULT 'final'"),
            ("is_published", "BOOLEAN DEFAULT TRUE"),
        ]
        
        for col_name, col_type in columns_to_add:
            result = conn.execute(
                text(f"""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name='exam_results' AND column_name='{col_name}';
                """)
            )
            if result.first():
                print(f"Column '{col_name}' already exists in exam_results.")
            else:
                conn.execute(
                    text(f"ALTER TABLE exam_results ADD COLUMN {col_name} {col_type};")
                )
                print(f"Added column '{col_name}' to exam_results.")

def add_book_loan_columns():
    """Add book_id column to book_loans table."""
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='book_loans' AND column_name='book_id';
            """)
        )
        if result.first():
            print("Column 'book_id' already exists in book_loans.")
        else:
            conn.execute(
                text("""
                    ALTER TABLE book_loans 
                    ADD COLUMN book_id INTEGER,
                    ADD CONSTRAINT fk_book_loans_book 
                        FOREIGN KEY (book_id) REFERENCES books(id) 
                        ON DELETE SET NULL;
                """)
            )
            print("Added column 'book_id' to book_loans.")

def create_books_table():
    """Create the books table if it doesn't exist."""
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name='books';
            """)
        )
        if result.first():
            print("Table 'books' already exists.")
            return
        
        conn.execute(
            text("""
                CREATE TABLE books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255),
                    isbn VARCHAR(20) UNIQUE,
                    category VARCHAR(100),
                    total_copies INTEGER DEFAULT 1,
                    available_copies INTEGER DEFAULT 1,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        )
        print("Created table 'books'.")

def create_exam_notices_table():
    """Create the exam_notices table if it doesn't exist."""
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name='exam_notices';
            """)
        )
        if result.first():
            print("Table 'exam_notices' already exists.")
            return
        
        conn.execute(
            text("""
                CREATE TABLE exam_notices (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT,
                    notice_type VARCHAR(20),
                    exam_date DATE,
                    created_by INTEGER REFERENCES users(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        )
        print("Created table 'exam_notices'.")

def run_all_migrations():
    """Run all migrations."""
    print("Starting database migrations...")
    print("-" * 50)
    
    # Create tables first (in correct order due to foreign keys)
    create_books_table()
    create_exam_notices_table()
    
    # Add columns
    add_exam_results_columns()
    add_book_loan_columns()
    
    print("-" * 50)
    print("Database migrations completed!")

if __name__ == "__main__":
    run_all_migrations()
