import asyncio
import sys
import os

# Add the parent directory to sys.path to resolve app imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from backup.core.database import async_engine

async def create_new_tables():
    async with async_engine.begin() as conn:
        # Create new tables
        print("Creating departments table...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                code VARCHAR(10) NOT NULL UNIQUE,
                hod_teacher_id INTEGER REFERENCES teachers(id)
            );
        """))
        
        print("Creating exam_results table...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS exam_results (
                id SERIAL PRIMARY KEY,
                student_id INTEGER NOT NULL REFERENCES students(id),
                course_id INTEGER NOT NULL REFERENCES courses(id),
                marks FLOAT NOT NULL,
                grade VARCHAR(2) NOT NULL,
                published_by INTEGER NOT NULL REFERENCES users(id),
                published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                semester VARCHAR(10) NOT NULL
            );
        """))
        
        print("Creating book_loans table...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS book_loans (
                id SERIAL PRIMARY KEY,
                student_id INTEGER NOT NULL REFERENCES students(id),
                book_title VARCHAR NOT NULL,
                book_author VARCHAR NOT NULL,
                book_isbn VARCHAR,
                taken_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE,
                status VARCHAR DEFAULT 'borrowed',
                fine_amount INTEGER DEFAULT 0
            );
        """))
        
        print("Creating teacher_payments table...")
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS teacher_payments (
                id SERIAL PRIMARY KEY,
                teacher_id INTEGER NOT NULL REFERENCES teachers(id),
                amount FLOAT NOT NULL,
                month VARCHAR(7) NOT NULL,
                payment_type VARCHAR DEFAULT 'salary',
                paid_by INTEGER NOT NULL REFERENCES users(id),
                paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            );
        """))
        
        # Add department_id columns to existing tables
        print("Adding department_id columns...")
        try:
            await conn.execute(text("""
                ALTER TABLE teachers ADD COLUMN IF NOT EXISTS department_id INTEGER REFERENCES departments(id);
            """))
            print("Added department_id to teachers.")
        except Exception as e:
            print(f"⚠️ Error adding department_id to teachers (might exist): {e}")
            
        try:
            await conn.execute(text("""
                ALTER TABLE students ADD COLUMN IF NOT EXISTS department_id INTEGER REFERENCES departments(id);
            """))
            print("Added department_id to students.")
        except Exception as e:
            print(f"⚠️ Error adding department_id to students (might exist): {e}")
            
        print("✅ New tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_new_tables())
