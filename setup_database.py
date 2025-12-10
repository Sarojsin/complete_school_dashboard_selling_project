"""
Database setup script for Render deployment
Runs database migrations before starting the application
"""
import os
import logging
from alembic.config import Config
from alembic import command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Run database migrations"""
    try:
        logger.info("Starting database setup...")
        
        # Run Alembic migrations
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        
        logger.info("Database migrations completed successfully!")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        # Don't fail the deployment if migrations fail
        # The app might still work if tables already exist
        logger.warning("Continuing despite migration errors...")

if __name__ == "__main__":
    setup_database()
