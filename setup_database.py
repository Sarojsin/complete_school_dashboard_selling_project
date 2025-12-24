"""
Database setup script for Render deployment
Ensures tables exist and runs custom migrations
"""
import os
import sys
import logging
from sqlalchemy import text

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import engine, Base
# Import all models to ensure they are registered with Base.metadata
from models.models import (
    User, Student, Teacher, Parent, Authority, 
    Course, CourseEnrollment, Assignment, AssignmentSubmission, 
    Grade, Attendance, FeeRecord, Notice, Note, Video, Message, Schedule
)
from models import group_models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_columns_exist():
    """Manually check and add missing columns for critical tables"""
    logger.info("Checking for missing columns...")
    
    # 1. Check 'assignments' table for 'target_classes'
    with engine.connect() as conn:
        try:
            # PostgreSQL check
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='assignments' AND column_name='target_classes';"
            ))
            if not result.first():
                logger.info("Adding 'target_classes' column to 'assignments' table...")
                conn.execute(text("ALTER TABLE assignments ADD COLUMN target_classes VARCHAR(255);"))
                conn.commit()
                logger.info("Added 'target_classes' column successfully.")
            else:
                logger.info("'target_classes' column already exists in 'assignments'.")
        except Exception as e:
            logger.warning(f"Failed to check/add 'target_classes' column: {e}")

def setup_database():
    """Ensure tables exist and run migrations"""
    try:
        logger.info("Starting database setup...")
        
        # 1. Create all tables if they don't exist
        logger.info("Creating tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully (or already exist).")
        
        # 2. Sync schema (add missing columns to existing tables)
        ensure_columns_exist()
        
        # 3. Run custom migrations if they exist
        migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
        if os.path.exists(migrations_dir):
            import subprocess
            
            # Example: Run add_parent_id_to_students.py
            migration_script = os.path.join(migrations_dir, "add_parent_id_to_students.py")
            if os.path.exists(migration_script):
                logger.info(f"Running migration: {migration_script}")
                subprocess.run([sys.executable, migration_script], check=False)
            
            # Check for SQL migrations
            for file in os.listdir(migrations_dir):
                if file.endswith(".sql"):
                    sql_path = os.path.join(migrations_dir, file)
                    logger.info(f"Running SQL migration: {sql_path}")
                    with open(sql_path, "r") as f:
                        sql_content = f.read()
                        with engine.begin() as conn:
                            # Split by semicolon for multiple statements
                            for statement in sql_content.split(";"):
                                if statement.strip():
                                    conn.execute(text(statement))
        
        logger.info("Database setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        # Continue anyway, as the app might still work
        logger.warning("Continuing despite setup errors...")

if __name__ == "__main__":
    setup_database()
