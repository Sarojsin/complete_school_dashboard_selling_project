"""
Database setup script for Render deployment
Ensures tables exist and runs custom migrations
"""
import os
import sys
import logging
from sqlalchemy import text

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backup.core.database import engine, Base
# Import all models to ensure they are registered with Base.metadata
from backup.models.models import (
    User, Student, Teacher, Parent, Authority, 
    Course, CourseEnrollment, Assignment, AssignmentSubmission, 
    Grade, Attendance, FeeRecord, Notice, Note, Video, Message, Schedule
)
from backup.models.test_models import Test, TestQuestion, TestSubmission
from backup.models import group_models, admin_models

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

    # 2. Check 'tests' table for 'target_section'
    with engine.connect() as conn:
        try:
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='tests' AND column_name='target_section';"
            ))
            if not result.first():
                logger.info("Adding 'target_section' column to 'tests' table...")
                conn.execute(text("ALTER TABLE tests ADD COLUMN target_section VARCHAR(50);"))
                conn.commit()
                logger.info("Added 'target_section' column successfully.")
            else:
                logger.info("'target_section' column already exists in 'tests'.")
        except Exception as e:
            logger.warning(f"Failed to check/add 'target_section' column: {e}")

    # 3. Check 'tests' table for 'subject_name' and 'grade_level'
    with engine.connect() as conn:
        try:
            # Check subject_name
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='tests' AND column_name='subject_name';"
            ))
            if not result.first():
                logger.info("Adding 'subject_name' column to 'tests' table...")
                conn.execute(text("ALTER TABLE tests ADD COLUMN subject_name VARCHAR(255);"))
                conn.commit()
            
            # Check grade_level
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='tests' AND column_name='grade_level';"
            ))
            if not result.first():
                logger.info("Adding 'grade_level' column to 'tests' table...")
                conn.execute(text("ALTER TABLE tests ADD COLUMN grade_level VARCHAR(50);"))
                conn.commit()
        except Exception as e:
            logger.warning(f"Failed to check/add subject/grade columns: {e}")

    # 3. Check 'test_questions' table for 'explanation'
    with engine.connect() as conn:
        try:
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='test_questions' AND column_name='explanation';"
            ))
            if not result.first():
                logger.info("Adding 'explanation' column to 'test_questions' table...")
                conn.execute(text("ALTER TABLE test_questions ADD COLUMN explanation TEXT;"))
                conn.commit()
                logger.info("Added 'explanation' column successfully.")
            else:
                logger.info("'explanation' column already exists in 'test_questions'.")
        except Exception as e:
            logger.warning(f"Failed to check/add 'explanation' column: {e}")

    # 4. Check 'notes' table for 'is_approved'
    with engine.connect() as conn:
        try:
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='notes' AND column_name='is_approved';"
            ))
            if not result.first():
                logger.info("Adding 'is_approved' column to 'notes' table...")
                conn.execute(text("ALTER TABLE notes ADD COLUMN is_approved BOOLEAN DEFAULT TRUE;"))
                conn.commit()
                logger.info("Added 'is_approved' column successfully.")
            else:
                logger.info("'is_approved' column already exists in 'notes'.")
        except Exception as e:
            logger.warning(f"Failed to check/add 'is_approved' column on notes: {e}")

    # 5. Check 'videos' table for 'is_approved'
    with engine.connect() as conn:
        try:
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='videos' AND column_name='is_approved';"
            ))
            if not result.first():
                logger.info("Adding 'is_approved' column to 'videos' table...")
                conn.execute(text("ALTER TABLE videos ADD COLUMN is_approved BOOLEAN DEFAULT TRUE;"))
                conn.commit()
                logger.info("Added 'is_approved' column successfully.")
            else:
                logger.info("'is_approved' column already exists in 'videos'.")
        except Exception as e:
            logger.warning(f"Failed to check/add 'is_approved' column on videos: {e}")

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

            security_tables_migration = os.path.join(migrations_dir, "add_admin_security_tables.py")
            if os.path.exists(security_tables_migration):
                logger.info(f"Running migration: {security_tables_migration}")
                subprocess.run([sys.executable, security_tables_migration], check=False)
            
            # Check for SQL migrations
            for file in os.listdir(migrations_dir):
                if file.endswith(".sql"):
                    sql_path = os.path.join(migrations_dir, file)
                    logger.info(f"Running SQL migration: {sql_path}")
                    with open(sql_path, "r") as f:
                        sql_content = f.read()
                        with engine.begin() as conn:
                            # Split by semicolon and filter out empty/comment-only statements
                            for statement in sql_content.split(";"):
                                clean_statement = statement.strip()
                                if clean_statement and not clean_statement.startswith("--"):
                                    conn.execute(text(clean_statement))
        
        logger.info("Database setup completed successfully!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        # Continue anyway, as the app might still work
        logger.warning("Continuing despite setup errors...")

if __name__ == "__main__":
    setup_database()
'''STEP 1 — Initialize Alembic

From project root:

alembic init migrations

This creates:

migrations/
migrations/env.py
migrations/script.py.mako
alembic.ini
⚙ STEP 2 — Configure Database URL

Open:

alembic.ini

Replace:

sqlalchemy.url = driver://user:pass@localhost/dbname

With your real database.

For PostgreSQL (recommended):

sqlalchemy.url = postgresql+psycopg2://user:password@localhost/school_db

⚠ In production (Render/AWS), you’ll override this using environment variables.

Better version:

In alembic.ini:

sqlalchemy.url = ${DATABASE_URL}
🧠 STEP 3 — Connect Alembic to Your Models

Open:

migrations/env.py

Find:

target_metadata = None

Replace with:

from app.models import Base
target_metadata = Base.metadata

Now Alembic can detect model changes.

🔄 STEP 4 — Handle Existing Database (IMPORTANT)

Since you already have tables:

We DO NOT want Alembic to recreate them.

Run:

alembic revision --autogenerate -m "initial"

Then:

alembic stamp head

What this does:

Creates migration history

Marks DB as already up-to-date

Prevents table recreation

This is the safe transition step.

🧱 STEP 5 — Test a Real Migration

Now let’s test it properly.

Add a new field to one model:

is_active = Column(Boolean, default=True)

Now generate migration:

alembic revision --autogenerate -m "add is_active to students"

Review the generated file.

Then apply:

alembic upgrade head

Done.

Your DB is now versioned.

🔁 STEP 6 — Remove setup_database.py

Once Alembic is working:

Delete:

setup_database.py
manual ALTER TABLE logic
column existence checks

Never mutate DB manually again.

🌍 STEP 7 — Configure Production Deployment

On:

Render

Amazon Web Services

Change your start command to:

alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 10000

This ensures:

DB migrates

Then app starts

Safe production behavior.

🏗 Final Production Structure

Your project should now look like:

app/
migrations/
alembic.ini
requirements.txt
Dockerfile

No manual DB scripts.

🧠 Proper Workflow From Now On

Whenever you:

Add a column

Remove a column

Change a field type

Add a table

You do:

alembic revision --autogenerate -m "describe change"
alembic upgrade head

Commit the migration file.

Push.

Deploy.

That’s it.

⚠ Common Mistakes to Avoid

❌ Editing migration files randomly

❌ Deleting migration history

❌ Running Base.metadata.create_all() in production

❌ Mixing manual SQL + Alembic

Once you switch — commit fully. '''
